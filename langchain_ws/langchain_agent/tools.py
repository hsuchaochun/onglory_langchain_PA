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
from metadata import onglory_overview_metadata, onglory_portfolio_metadata, onglory_quant_status_metadata, onglory_crypto_quant_indicator_status_metadata, onglory_trading_history_metadata, onglory_value_history_metadata, whale_trace_metadata, bitcoinETF_history_metadata, bitcoinETF_netflow_metadata, news_metadata

class SqlSearchInput(BaseModel):
    query: str = Field(description="The question that was asked by the user.")

class SqlSearchTool(BaseTool):
    name = "sql_search_tool"
    description = "This is a tool to search the SQL database."
    arg_schema: Type[BaseModel] = SqlSearchInput
    
    database_metadata = {
        "onglory_overview": onglory_overview_metadata,
        "onglory_portfolio": onglory_portfolio_metadata,
        "onglory_quant_status": onglory_quant_status_metadata,
        "onglory_crypto_quant_indicator_status": onglory_crypto_quant_indicator_status_metadata,
        "onglory_trading_history": onglory_trading_history_metadata,
        "onglory_value_history": onglory_value_history_metadata,
        "onglory_whale_trace": whale_trace_metadata,
        "bitcoinETF_history": bitcoinETF_history_metadata,
        "bitcoinETF_netflow": bitcoinETF_netflow_metadata,
        "news": news_metadata,
    }
    
    def _run(
        self, input: str, run_manager: Optional[CallbackManagerForToolRun] = None
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
            Given the following user question and table metadata, generate an SQL query.

            Question: {input}
            Table Metadata: {database_metadata}
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
            "input": input,
            "database_metadata": self.database_metadata,  # Include database metadata
        })
        
        return result
            
    async def _arun(
        self, input: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool to search the SQL database asynchronously."""
        # Initialize environment variables, LLM, and database connection
        set_env_vars()
        llm = get_llm_model(model_name="gpt-3.5-turbo")
        db = get_onglory_db()
        
        print('input:', input)

        # Create SQL chain and prompt template
        write_query = create_sql_query_chain(llm, db)
        execute_query = QuerySQLDataBaseTool(db=db)
    
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

        # Chain execution in an async manner
        chain = (
            RunnablePassthrough.assign(query=write_query).assign(
                result=itemgetter("query") | execute_query
            )
            | answer_prompt
            | llm
            | StrOutputParser()
        )
        
        result = await chain.ainvoke({
            "input": input,
            "question": input,
            "database_metadata": self.database_metadata,
        })
        
        return result
    
# search = SqlSearchTool()
# print(search.name)
# print(search.description)
# print(search.args)
# print(search.invoke(input="SELECT * FROM users"))