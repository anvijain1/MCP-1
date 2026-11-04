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
    limit: int = 5) -> list[dict]:

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



@mcp.tool()
def sort_products(
    sort_by: str,
    order: str,
    limit: int = 5
) -> list[dict]:
    """
    Sort products by price, rating, review count, or stock quantity.
    Supports ascending and descending order.
    """
    
    sort_by = sort_by.strip().lower()
    order = order.strip().lower()

    allowed_columns = [
        "price_inr",
        "rating",
        "review_count",
        "stock_quantity"
    ]

    if sort_by not in allowed_columns:
        raise ValueError(
            f"Invalid sorting column. Choose from: {allowed_columns}"
        )

    if order == "ascending":
        ascending = True

    elif order == "descending":
        ascending = False

    else:
        raise ValueError(
            "Invalid order. Use 'ascending' or 'descending'."
        )

    if limit < 1:
        raise ValueError("Limit must be at least 1.")

    sorted_products = products.sort_values(
        by=sort_by,
        ascending=ascending
    )

    return sorted_products.head(limit).to_dict(orient="records")



if __name__ == "__main__":
    mcp.run() 

