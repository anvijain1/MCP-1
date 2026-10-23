from mcp.server.fastmcp import FastMCP
from data_loader import load_products

mcp = FastMCP("my-first-server")

products = load_products()

@mcp.tool()
def search_products(query: str) -> list[dict]:

    """Search products by product name, category, brand, or description."""

    #Convert the query to lowercase
    query = query.lower()
    # Search the relevant columns for matches

    search_columns = [
    "product_name",
    "category",
    "brand",
    "description"
]

    mask = False

    for column in search_columns:
        mask = mask | products[column].str.contains(
            query, case=False, na=False
    )

    matches = products[mask]
    
    # Return the matching products as a list of dictionaries
    return matches.to_dict(orient="records")

print(products.shape)

