from langchain.agents import initialize_agent, tool
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType
from self_defined_tool import Gojo_satoru, SQLTool
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
        verbose=True
    )

if __name__ == "__main__":
    llm = get_llm_model()
    agent = get_agent_tool(llm)

    print(agent.invoke("Onglory investment current value"))

    # print(agent.invoke("請幫我找到告五人的資訊"))
    # print(agent.invoke("請問一百的四分之三是多少"))
    # print(agent.invoke("請解析下文，幫我產生五條體：丹帝對戰小智，皮卡丘會鎖血"))