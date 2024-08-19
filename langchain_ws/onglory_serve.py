import os
import getpass
import uvicorn
import config
from operator import itemgetter
from fastapi import FastAPI, Request
from langserve import add_routes
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.messages import trim_messages

# Export environment variables
os.environ["LANGCHAIN_API_KEY"] = config.LANGCHAIN_API_KEY
os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY
os.environ["TAVILY_API_KEY"] = config.TAVILY_API_KEY

# Prompt for API keys if they are not set
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass()

if not os.environ.get("LANGCHAIN_API_KEY"):
    os.environ["LANGCHAIN_API_KEY"] = getpass.getpass()
    os.environ["LANGCHAIN_TRACING_V2"] = "true"

# Initialize components
sql_llm = ChatOpenAI(model="gpt-3.5-turbo")
llm = ChatOpenAI(model="gpt-4o")
db = SQLDatabase.from_uri(config.SQL_CONNECT_URL)
store = {}

# Function to get or create session history
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Define the SQL query execution and writing
execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(sql_llm, db)

# Define the answer prompt template
answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result.\
Answer the user question in Chinese(traditional), make the output be structured, might contain some tables or listed data.\
If the output data contains table, add sufficient tab to make the table look good.\
Also, please make sure the answer is accurate and easy to understand.\

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

# Define message trimming strategy
trimmer = trim_messages(
    max_tokens=65,
    strategy="last",
    token_counter=llm,
    include_system=True,
    allow_partial=False,
    start_on="human",
)

# Define the chain with memory integration
chain = (
    RunnablePassthrough()
    .assign(query=write_query)
    .assign(result=itemgetter("query") | execute_query)
    | answer_prompt
    | llm
    | StrOutputParser()
)

# Define the FastAPI app
app = FastAPI(
    title="Onglory LangChain Server",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces",
)

# Endpoint to handle the chain requests with memory
@app.post("/onglory")
async def run_chain(request: Request):
    data = await request.json()
    print('data:', data)
    input_data = data.get("input")
    question = input_data.get("question")
    if "session_id" not in input_data:
        session_id = "test"
    else:
        session_id = input_data.get("session_id")
    
    # Retrieve the session history
    history = get_session_history(session_id)
    history.add_user_message(question)
    
    # Prepare the messages list with the history
    messages = history.messages  # Get the message history
    
    # print('question:', question)
    # print('session_id:', session_id)
    # print('history:', history.messages)
    
    # Run the chain, including messages in the context
    result = chain.invoke({
        "messages": messages,
        "question": question,
    })

    # Save the AI's response to the history
    history.add_ai_message(result)
    
    # print('result:', result)

    return {"result": result}

add_routes(
    app,
    chain,
    path="/onglory",
)

# Run the FastAPI server
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)