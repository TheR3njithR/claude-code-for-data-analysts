"""A tiny, read-only MCP server over data/orders.db (synthetic data).
Register with Claude Code (project scope), from the project folder:
  claude mcp add --transport stdio --scope project orders -- python src/mcp_orders.py
Tools: describe_orders, run_select (SELECT only, opened read-only, max 200 rows)."""
import re, sqlite3, pathlib
from mcp.server.mcpserver import MCPServer   # mcp 2.x (was FastMCP in 1.x)
DB = pathlib.Path(__file__).resolve().parents[1] / "data" / "orders.db"
mcp = MCPServer("orders")

def _con():
    return sqlite3.connect(f"file:{DB}?mode=ro", uri=True)   # read-only at the database level

@mcp.tool()
def describe_orders() -> str:
    """Columns and types of the orders table, plus the revenue definition."""
    with _con() as c:
        cols = c.execute("pragma table_info(orders)").fetchall()
    return "\n".join(f"{n} {t}" for _, n, t, *_ in cols) + "\nRevenue = sum(revenue) where status = 'delivered'."

@mcp.tool()
def run_select(sql: str) -> str:
    """Run ONE read-only SELECT on the orders table. Returns up to 200 rows as tab-separated text."""
    if not re.fullmatch(r"\s*select\b[^;]*;?\s*", sql, flags=re.I | re.S):
        return "Refused: only a single SELECT statement is allowed."
    with _con() as c:
        cur = c.execute(sql); rows = cur.fetchmany(200)
        head = [d[0] for d in cur.description]
    return "\t".join(head) + "\n" + "\n".join("\t".join(str(v) for v in r) for r in rows)

if __name__ == "__main__":
    mcp.run()   # stdio transport
