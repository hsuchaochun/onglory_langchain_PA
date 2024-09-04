from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.runnables import Runnable
from langserve import add_routes
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from typing import List, Dict, Any
from tools import SqlSearchTool, gmail_toolkit
from functions import get_llm_model

# Setup templates
templates = Jinja2Templates(directory="templates")

# FastAPI app definition
app = FastAPI(
    title="LangChain Playground",
    version="1.0",
    description="A custom playground for LangChain",
)

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize tools
sql_tool = SqlSearchTool().as_tool()
gmail_tools = gmail_toolkit.get_tools()
tools = [sql_tool] + gmail_tools

# Create prompt template
system_message = ("You are an assistant whose only job is to forward user input "
                  "directly to the tool without processing or interpreting the input. "
                  "Do not attempt to answer or modify the input. Always pass the "
                  "user's input directly to the tool.")

prompt = ChatPromptTemplate.from_messages([
    ("system", system_message),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("assistant", "Forwarding the input to the tool."),
    ("placeholder", "{agent_scratchpad}"),
])

# Create model and agent
model = get_llm_model()
agent = create_tool_calling_agent(model, tools, prompt)

# Create agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=10,
    max_execution_time=300
)

# Pydantic model for input validation
class InputSchema(BaseModel):
    input: str
    chat_history: List[str] = []
    agent_scratchpad: List[str] = []

# Create a Runnable
class MyChainRunnable(Runnable):
    def input_schema(self):
        return InputSchema

    def invoke(self, input_data: InputSchema) -> Any:
        chain_input = {
            "input": input_data.input,
            "chat_history": input_data.chat_history,
            "agent_scratchpad": input_data.agent_scratchpad
        }
        return agent_executor.invoke(chain_input)

my_chain_runnable = MyChainRunnable()

# Serve the HTML template
@app.get("/", response_class=HTMLResponse)
async def get_playground(request: Request):
    return templates.TemplateResponse("playground.html", {"request": request})

# Endpoint for executing the chain
@app.post("/execute_chain/")
async def execute_chain(input_data: InputSchema):
    result = my_chain_runnable.invoke(input_data)
    return {"result": result}

# Add chain route
add_routes(app, my_chain_runnable, path="/chain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)