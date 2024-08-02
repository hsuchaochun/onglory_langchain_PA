import os
import config
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite import SqliteSaver

# export
os.environ["LANGCHAIN_API_KEY"] = config.LANGCHAIN_API_KEY
os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY
os.environ["TAVILY_API_KEY"] = config.TAVILY_API_KEY

model = ChatOpenAI(model="gpt-4o")

search = TavilySearchResults(max_results=2)
search_results = search.invoke("what is the weather in SF")
# print(search_results)

# If we want, we can create other tools.
# Once we have all the tools we want, we can put them in a list that we will reference later.
tools = [search]

# model_with_tools = model.bind_tools(tools)

# response = model_with_tools.invoke([HumanMessage(content="What's the weather in SF?")])

# print(f"ContentString: {response.content}")
# print(f"ToolCalls: {response.tool_calls}")

# agent_executor = create_react_agent(model, tools)

# response = agent_executor.invoke({"messages": [HumanMessage(content="whats the weather in sf?")]})
# print(response["messages"])

# for chunk in agent_executor.stream(
#     {"messages": [HumanMessage(content="whats the weather in sf?")]}
# ):
#     print(chunk)
#     print("----")

memory = SqliteSaver.from_conn_string(":memory:")
agent_executor = create_react_agent(model, tools, checkpointer=memory)
config = {"configurable": {"thread_id": "abc123"}}

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im bob!")]}, config
):
    print(chunk)
    print("----")

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="whats my name?")]}, config
):
    print(chunk)
    print("----")

# async def test():
#     async for event in agent_executor.astream_events(
#         {"messages": [HumanMessage(content="whats the weather in sf?")]}, version="v1"
#     ):
#         kind = event["event"]
#         if kind == "on_chain_start":
#             if (
#                 event["name"] == "Agent"
#             ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
#                 print(
#                     f"Starting agent: {event['name']} with input: {event['data'].get('input')}"
#                 )
#         elif kind == "on_chain_end":
#             if (
#                 event["name"] == "Agent"
#             ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
#                 print()
#                 print("--")
#                 print(
#                     f"Done agent: {event['name']} with output: {event['data'].get('output')['output']}"
#                 )
#         if kind == "on_chat_model_stream":
#             content = event["data"]["chunk"].content
#             if content:
#                 # Empty content in the context of OpenAI means
#                 # that the model is asking for a tool to be invoked.
#                 # So we only print non-empty content
#                 print(content, end="")
#         elif kind == "on_tool_start":
#             print("--")
#             print(
#                 f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}"
#             )
#         elif kind == "on_tool_end":
#             print(f"Done tool: {event['name']}")
#             print(f"Tool output was: {event['data'].get('output')}")
#             print("--")
            
# async def main():
#     await test()

# import asyncio
# # Run the main function
# if __name__ == "__main__":
#     asyncio.run(main())