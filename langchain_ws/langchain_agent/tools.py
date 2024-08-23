from typing import Type, Optional
from pydantic import BaseModel, Field
from operator import itemgetter
from langchain.tools import BaseTool
from langchain.callbacks.manager import (
    CallbackManagerForToolRun, 
    AsyncCallbackManagerForToolRun, 
)
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from functions import set_env_vars, get_llm_model, get_onglory_db

class SqlSearchInput(BaseModel):
    query: str = Field(description="The question that was asked by the user.")

class SqlSearchTool(BaseTool):
    name = "sql_search_tool"
    description = "This is a tool to search the SQL database."
    arg_schema: Type[BaseModel] = SqlSearchInput
    
    def _run(
        self, question: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool to search the SQL database."""
        
        # Initialize environment variables, LLM, and database connection
        set_env_vars()  # Assuming this is a method that sets your environment variables
        llm = get_llm_model(model_name="gpt-3.5-turbo")  # Initialize the LLM model
        db = get_onglory_db()  # Connect to the Onglory database
        
        # Create SQL chain and prompt template
        write_query = create_sql_query_chain(llm, db)
        execute_query = QuerySQLDataBaseTool(db=db)
    
        answer_prompt = PromptTemplate.from_template(
            """
            Given the following user question, corresponding SQL query, and SQL result, answer the user question.

            Question: {question}
            SQL Query: {query}
            SQL Result: {result}
            Answer: 
            """
        )

        chain = (
            RunnablePassthrough.assign(query=write_query).assign(
                result=itemgetter("query") | execute_query
            )
            | answer_prompt
            | llm
            | StrOutputParser()
        )
        
        result = chain.invoke({
            "question": question,
        })
        
        return result
            
    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool to search the SQL database."""
        raise NotImplementedError("This tool does not support async run.")
    
# search = SqlSearchTool()
# print(search.name)
# print(search.description)
# print(search.args)
# print(search.invoke(input="SELECT * FROM users"))