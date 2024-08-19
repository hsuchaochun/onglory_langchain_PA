import os
import getpass
import config
from operator import itemgetter
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

# export
os.environ["LANGCHAIN_API_KEY"] = config.LANGCHAIN_API_KEY
os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY
os.environ["TAVILY_API_KEY"] = config.TAVILY_API_KEY

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass()

# Comment out the below to opt-out of using LangSmith in this notebook. Not required.
if not os.environ.get("LANGCHAIN_API_KEY"):
    os.environ["LANGCHAIN_API_KEY"] = getpass.getpass()
    os.environ["LANGCHAIN_TRACING_V2"] = "true"

llm = ChatOpenAI(model="gpt-3.5-turbo")
db = SQLDatabase.from_uri(config.SQL_CONNECT_URL)
# print(db.dialect)
# print(db.get_usable_table_names())
# print(db.run("SELECT * FROM `onglory_overview`;"))

# chain = create_sql_query_chain(llm, db)
# response = chain.invoke({"question": "What's the onglory investment overview?"})
# print(response)

# db.run(response)
# chain.get_prompts()[0].pretty_print()

execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)
# chain = write_query | execute_query
# result = chain.invoke({"question": "What's the bitcoin ETF netflow today?"})
# print(result)

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result.\
        Answer the user question in Chinese(traditional), make the output be structured, might contain some tables or listed data.\
        If the output data contains table, add sufficient tab to make the table looks good.\
        Also, please make sure the answer is accurate, easy to understand, and answer the question properly without losing any data.\
        The number should be rounded to 2 decimal places.\

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer_prompt
    | llm
    | StrOutputParser()
)

result = chain.invoke({"question": "Onglory investment overview"})
print(result)