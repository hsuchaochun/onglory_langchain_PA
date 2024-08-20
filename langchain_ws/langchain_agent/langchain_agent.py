from langchain.agents import initialize_agent, tool
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType
from self_defined_tool import Gojo_satoru, SQLTool
from functions import generate_pdf_from_markdown
import sys
sys.path.append("../")
import config

OPENAI_API_KEY = config.OPENAI_API_KEY

def get_llm_model():
    return ChatOpenAI(
        openai_api_key=config.OPENAI_API_KEY,
        model_name="gpt-4o",
        temperature=0
    )

def get_agent_tool(llm):
    # Load built-in tools
    built_in_tools = load_tools(["llm-math", "wikipedia"], llm=llm)

    # Create instances of the custom tools
    gojo_tool = Gojo_satoru()
    sql_tool = SQLTool()

    # Merge built-in and custom tools
    # all_tools = built_in_tools + [gojo_tool, sql_tool.as_tool()]
    all_tools = [sql_tool.as_tool()]
    
    # Initialize the agent with the combined tools
    return initialize_agent(
        all_tools,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        verbose=True, 
        max_iterations=50,  # Set a higher iteration limit
        max_execution_time=600  # Set a higher time limit (in seconds)
    )

if __name__ == "__main__":
    # Initialize LLM and Agent
    llm = get_llm_model()
    agent = get_agent_tool(llm)

    # Invoke the agent with a task
    result = agent.invoke('''
        Onglory Holding coins' symbol, amount and current value, other info is unnecessary.\
        If the symbol is the same, please sum the amount and value and create a table.\
        Ensure that all data is included, and none of the rows or columns are skipped. If any data is missing, try to add a placeholder like `N/A`. 
        The table must use proper HTML tags like `<table>`, `<tr>`, `<th>`, and `<td>`. Please ensure that the columns are spaced for readability and the table fits well within an A4 horizontal PDF format. 
        Ensure that all rows of data are included in the table, and no rows are skipped or truncated.
    ''')
    
    # Retrieve the markdown output from the agent
    output_content = result.get('output', '')

    # Generate PDF from the markdown output
    output_pdf_file = 'output.pdf'
    generate_pdf_from_markdown(output_content, output_pdf_file)

    # print(agent.invoke("請幫我找到告五人的資訊"))
    # print(agent.invoke("請問一百的四分之三是多少"))
    # print(agent.invoke("請解析下文，幫我產生五條體：丹帝對戰小智，皮卡丘會鎖血"))