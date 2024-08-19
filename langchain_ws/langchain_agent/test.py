import sys
from self_defined_tool import SQLQueryTool
sys.path.append("../") 
import config

# Example usage
if __name__ == "__main__":
    # Instantiate the tool with appropriate database URI and API key
    sql_tool = SQLQueryTool(
        db_uri=config.SQL_CONNECT_URL,
        api_key=config.OPENAI_API_KEY
    )
    
    # Run the tool with a sample query
    result = sql_tool._run("Onglory investment overview")
    print(result)