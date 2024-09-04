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

llm = ChatOpenAI(model="gpt-4o")
db = SQLDatabase.from_uri("sqlite:///Chinook.db", sample_rows_in_table_info=3)
# print(db.dialect)
# print(db.get_usable_table_names())
# print(db.run("SELECT * FROM Artist LIMIT 10;"))

chain = create_sql_query_chain(llm, db)
response = chain.invoke({"question": "How many employees are there"})
print(response)

# # db.run(response)
# # chain.get_prompts()[0].pretty_print()

# execute_query = QuerySQLDataBaseTool(db=db)
# write_query = create_sql_query_chain(llm, db)
# # chain = write_query | execute_query
# # result = chain.invoke({"question": "What's the bitcoin ETF netflow today?"})
# # print(result)

# answer_prompt = PromptTemplate.from_template(
#     """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

# Question: {question}
# SQL Query: {query}
# SQL Result: {result}
# Answer: """
# )

# chain = (
#     RunnablePassthrough.assign(query=write_query).assign(
#         result=itemgetter("query") | execute_query
#     )
#     | answer_prompt
#     | llm
#     | StrOutputParser()
# )

# result = chain.invoke({"question": "What's the onglory investment net value?"})
# print(result)