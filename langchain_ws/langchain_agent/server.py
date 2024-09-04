from fastapi import FastAPI, HTTPException, Request
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from tools import SqlSearchTool, gmail_toolkit
from functions import get_llm_model

# Initialize the FastAPI app
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain",
)

# Initialize tools
sql_tool = SqlSearchTool().as_tool()
gmail_tools = gmail_toolkit.get_tools()
tools = [sql_tool] + gmail_tools

# Initialize LLM
llm = get_llm_model()

# Define chat prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an assistant whose only job is to forward user input directly to the tool without processing or interpreting the input. Do not attempt to answer or modify the input. Always pass the user's input directly to the tool."),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("assistant", "Forwarding the input to the tool."),
    ("placeholder", "{agent_scratchpad}"),
])

# Create agent and executor
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=10,
    max_execution_time=300
)

@app.post("/execute_chain/")
async def execute_chain(request: Request):
    try:
        input_data = await request.json()
        
        if "input" not in input_data:
            raise HTTPException(status_code=400, detail="Missing 'input' in request body")
        
        user_input = input_data["input"]
        chain_input = {
            "input": user_input,
            "chat_history": [],
            "agent_scratchpad": []
        }
        
        result = await agent_executor.ainvoke(chain_input)
        return {"result": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)