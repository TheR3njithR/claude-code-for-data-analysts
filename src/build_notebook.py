"""Chapter: Claude Code + Jupyter. Builds notebooks/explore_orders.ipynb from code cells, then executes it
headlessly so every output in the notebook is real. Run: python src/build_notebook.py"""
import nbformat as nbf
from nbclient import NotebookClient
nb = nbf.v4.new_notebook()
nb.cells = [
    nbf.v4.new_markdown_cell("# Chai & Chips: exploration notebook\nBuilt and executed by `src/build_notebook.py`. Synthetic data."),
    nbf.v4.new_code_cell("import sys; sys.path.insert(0, 'src')\nimport pandas as pd\nfrom analysis import load, net_sales\ndf = load(); s = net_sales(df)\nlen(df), len(s)"),
    nbf.v4.new_markdown_cell("## Which weekday sells most?"),
    nbf.v4.new_code_cell("wd = s.groupby(s['order_date'].dt.day_name())['revenue'].sum()\n(wd / wd.sum() * 100).round(1).sort_values(ascending=False)"),
    nbf.v4.new_markdown_cell("## Basket size by category"),
    nbf.v4.new_code_cell("s.groupby('category')['qty'].mean().round(2).sort_values(ascending=False)"),
    nbf.v4.new_markdown_cell("## Price bands\nGift boxes dominate the top band."),
    nbf.v4.new_code_cell("bands = pd.cut(s['unit_price'], [0, 200, 500, 1000, 5000], labels=['<200', '200-500', '500-1000', '1000+'])\npd.crosstab(bands, s['category'])"),
]
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
NotebookClient(nb, timeout=120, kernel_name="python3", resources={"metadata": {"path": "."}}).execute()
nbf.write(nb, "notebooks/explore_orders.ipynb")
for c in nb.cells:
    if c.cell_type == "code":
        for o in c.outputs:
            txt = o.get("data", {}).get("text/plain") or o.get("text", "")
            print("---\n" + txt)
print("\nwrote notebooks/explore_orders.ipynb (executed)")
