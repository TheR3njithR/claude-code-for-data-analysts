"""Start the MCP server over stdio exactly as Claude Code would, list its tools, and call them."""
import asyncio, sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
async def main():
    params = StdioServerParameters(command=sys.executable, args=["src/mcp_orders.py"])
    async with stdio_client(params) as (r, w), ClientSession(r, w) as s:
        await s.initialize()
        print("tools:", [t.name for t in (await s.list_tools()).tools])
        q = ("select city, round(sum(revenue)) as net_revenue from orders "
             "where status = 'delivered' group by city order by net_revenue desc limit 3")
        print((await s.call_tool("run_select", {"sql": q})).content[0].text)
        print((await s.call_tool("run_select", {"sql": "delete from orders"})).content[0].text)
asyncio.run(main())
