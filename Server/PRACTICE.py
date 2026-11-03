from mcp.server.fastmcp import FastMCP
from data_loader import load_products

mcp = FastMCP("my-first-server")

products = load_products()

@mcp.tool()
def search_products(query: str, limit: int = 10) -> list[dict]:

    """Search products by product name, category, brand, or description."""

    query = query.strip()

    if not query:
        return []


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

@mcp.tool()
def filter_products(
    category: str,
    operator: str,
    price: float,
    limit: int = 50) -> list[dict]:

    """filter products by category and price comparison ."""

    #filter by category 
    filtered_product = products[
        products["category"].str.lower() == category.lower()
    ]

    #filter by price 
    if operator == "less_than":
        filtered_product = filtered_product[
            filtered_product["price_inr"] < price
        ]
    
    elif operator == "greater_than":
        filtered_product = filtered_product[
            filtered_product["price_inr"] > price
        ]

    elif operator == "equal":
        filtered_product = filtered_product[filtered_product["price_inr"] == price]

    else:
        raise ValueError("invalid operator")


    return filtered_product.head(limit).to_dict(orient="records")



if __name__ == "__main__":
    mcp.run() 

