
from pathlib import Path
import pandas as pd

# Find the project root based on this file's location
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Build the path to the CSV file
DATA_FILE = PROJECT_ROOT / "data" / "ecommerce_products.csv"

# TODO 1: Load the CSV into a pandas DataFrame
df = pd.read_csv(DATA_FILE)

if df.empty:
    raise ValueError("The product dataset is empty.")

required_columns = [
    "product_id",
    "product_name",
    "category",
    "brand",
    "price_inr",
    "rating",
    "review_count",
    "stock_quantity",
    "description"
]

missing_columns = set(required_columns) - set(df.columns)

if missing_columns:
    raise ValueError(f"Missing required columns: {missing_columns}")

numeric_columns = [
    "price_inr",
    "rating",
    "review_count",
    "stock_quantity"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="raise")

def load_products():
    return df

# TODO 2: Print the number of rows and columns
print(df.shape)

# TODO 3: Print the column names
print(df.columns)
# TODO 4: Print the first five products
print(df.head())
