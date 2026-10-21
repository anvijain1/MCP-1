from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my first srerver")

@mcp.tool()

def add_number(a: int , b: int ) -> int :
    "add two numbers and return the reuslt"
    return a+b 

if __name__ == "__main__":
    mcp.run()

