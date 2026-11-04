# E-commerce Product MCP Server

A simple **Model Context Protocol (MCP) server** built using Python and FastMCP that enables AI applications to interact with an e-commerce product dataset through structured tools.

The server provides functionalities to search, filter, and sort products based on different attributes such as product name, category, price, rating, and stock quantity.

## Features

The server currently provides three MCP tools:

### 1. Search Products
- Search products using keywords.
- Supports searching across product name, category, brand, and description.
- Performs case-insensitive searching.
- Returns matching products as structured dictionaries.

### 2. Filter Products
- Filter products based on their category.
- Apply price comparison operators:
  - `less_than`
  - `greater_than`
  - `equal`
- Specify the maximum number of results.

### 3. Sort Products
- Sort products using different attributes:
  - Price
  - Rating
  - Review count
  - Stock quantity
- Supports ascending and descending order.
- Specify the number of results to return.

## Tech Stack

- **Python** – Core programming language.
- **FastMCP** – Building the MCP server and exposing tools.
- **Pandas** – Loading, filtering, searching, and sorting product data.
- **CSV** – Storing the sample e-commerce product dataset.

## Dataset

The project uses a sample e-commerce dataset containing 100 products and 9 attributes.

| Column | Description |
|---|---|
| product_id | Unique product identifier |
| product_name | Name of the product |
| category | Product category |
| brand | Product brand |
| price_inr | Product price in INR |
| rating | Customer rating |
| review_count | Number of customer reviews |
| stock_quantity | Available stock |
| description | Product description |

## Project Structure

```text
ecommerce-mcp-server/
│
├── PRACTICE.py
├── data_loader.py
├── ecommerce_products.csv
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd ecommerce-mcp-server
```

### 2. Install dependencies

```bash
pip install "mcp[cli]" pandas
```

### 3. Run the MCP server

```bash
python PRACTICE.py
```

The server starts using FastMCP and exposes the registered product management tools to an MCP-compatible client.

## Learning Objectives

This project was developed to understand the fundamentals of the Model Context Protocol and how Python functions can be exposed as tools for AI applications.

Key concepts explored:

- Understanding MCP servers and tools.
- Creating tools using FastMCP decorators.
- Defining function parameters and return types.
- Processing structured datasets using Pandas.
- Implementing search, filtering, and sorting logic.
- Returning structured data from MCP tools.

## Future Improvements

- Add product recommendations.
- Implement advanced filtering with multiple conditions.
- Add pagination and result limits consistently across all tools.
- Connect the server to a database instead of a CSV file.
- Integrate the server with an AI-powered MCP client.

---

**Project Type:** Learning / Practice Project  
**Language:** Python  
**Protocol:** Model Context Protocol (MCP)