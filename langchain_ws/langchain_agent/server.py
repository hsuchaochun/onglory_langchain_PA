from fastapi import FastAPI, HTTPException, Request
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from tools import SqlSearchTool
from tools import gmail_toolkit
from functions import get_llm_model

# Initialize the FastAPI app
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain",
)

# Initialize the SQL tool
sql_tool = SqlSearchTool().as_tool()
# Initialize the Gmail toolkit
gmail_tools = gmail_toolkit.get_tools()
# Combine the tools
tools = [sql_tool] + gmail_tools

llm = get_llm_model()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an assistant whose only job is to forward user input directly to the tool without processing or interpreting the input. Do not attempt to answer or modify the input. Always pass the user's input directly to the tool."),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("assistant", "Forwarding the input to the tool."),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# Create the agent
agent = create_tool_calling_agent(llm, tools, prompt)

# Create the agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=10,  # Increase this to allow more iterations
    max_execution_time=300  # Increase the time limit if necessary
)

# Define the chain execution route
@app.post("/execute_chain/")
async def execute_chain(request: Request):
    try:
        # Get input from the request body (assumed to be JSON)
        input_data = await request.json()

        # Ensure input contains the 'input' field
        if "input" not in input_data:
            raise HTTPException(status_code=400, detail="Missing 'input' in request body")

        user_input = input_data["input"]

        # Construct the chain input
        chain_input = {
            "input": user_input,
            "chat_history": [],  # Placeholder for chat history if needed
            "agent_scratchpad": []  # Placeholder for agent's internal thoughts
        }

        # Run the agent executor
        result = await agent_executor.ainvoke(chain_input)

        return {"result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)