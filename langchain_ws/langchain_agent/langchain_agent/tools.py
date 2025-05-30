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
from langchain_google_community import GmailToolkit
from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
from functions import set_env_vars, get_llm_model, get_onglory_db
from metadata import (
    onglory_overview_metadata,
    onglory_portfolio_metadata,
    onglory_quant_status_metadata,
    onglory_crypto_quant_indicator_status_metadata,
    onglory_trading_history_metadata,
    onglory_value_history_metadata,
    whale_trace_metadata,
    bitcoinETF_history_metadata,
    bitcoinETF_netflow_metadata,
    news_metadata,
)

# Gmail toolkit setup
credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
)
api_resource = build_resource_service(credentials=credentials)
gmail_toolkit = GmailToolkit(api_resource=api_resource)

class SqlSearchInput(BaseModel):
    query: str = Field(description="The question that was asked by the user.")

class SqlSearchTool(BaseTool):
    name = "sql_search_tool"
    description = """
    This tool is designed to search the SQL database and retrieve structured data based on a user's question.
    The tool accepts a user question as input, converts it into an appropriate SQL query, and retrieves the corresponding data from the database.
    Inside this tool, the question will be processed by the GPT-3.5-turbo model to generate the SQL query, which will then be executed to fetch the data from the database.
    
    The output of this tool is structured in Chinese (traditional) and may include tables, lists, or detailed numerical data. It ensures that the result is accurate, easy to understand, and formatted properly for readability.
    
    Specific details:
    - The number values are rounded to 2 decimal places.
    - If tables are included in the response, they will be properly formatted with sufficient spacing to enhance clarity.
    - The tool is capable of querying various databases, including:
        - Onglory Overview
        - Onglory Portfolio
        - Quantitative Status
        - Crypto Quant Indicator Status
        - Trading History
        - Value History
        - Whale Tracking
        - Bitcoin ETF History and Netflow
        - News Data
    
    The tool automatically selects the relevant metadata from the appropriate database to generate the SQL query, ensuring the output answers the user's question accurately.
    """
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
        set_env_vars()
        llm_query = get_llm_model(model_name="gpt-3.5-turbo")
        llm = get_llm_model()
        db = get_onglory_db()
        
        print('input:', input)
        
        # Create SQL chain and prompt template
        write_query = create_sql_query_chain(llm_query, db)
        execute_query = QuerySQLDataBaseTool(db=db)
    
        answer_prompt = PromptTemplate.from_template(
            """Given the following user question, corresponding SQL query, and SQL result.
            Answer the user question in Chinese(traditional), make the output be structured, might contain some tables or listed data.
            If the output data contains table, add sufficient tab to make the table looks good.
            Also, please make sure the answer is accurate, easy to understand, and answer the question properly without losing any data.
            The number should be rounded to 2 decimal places.

            Question: {question}
            SQL Query: {query}
            SQL Result: {result}
            Answer: """
        )

        # Chain execution
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
            "question": input,
            "database_metadata": self.database_metadata,
        })
        
        return result
            
    async def _arun(
        self, input: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool to search the SQL database asynchronously."""
        # Initialize environment variables, LLM, and database connection
        set_env_vars()
        llm_query = get_llm_model(model_name="gpt-3.5-turbo")
        llm = get_llm_model()
        db = get_onglory_db()
        
        print('input:', input)

        # Create SQL chain and prompt template
        write_query = create_sql_query_chain(llm_query, db)
        execute_query = QuerySQLDataBaseTool(db=db)
    
        answer_prompt = PromptTemplate.from_template(
            """Given the following user question, corresponding SQL query, and SQL result.
            Answer the user question in Chinese(traditional), make the output be structured, might contain some tables or listed data.
            If the output data contains table, add sufficient tab to make the table looks good.
            Also, please make sure the answer is accurate, easy to understand, and answer the question properly without losing any data.
            The number should be rounded to 2 decimal places.

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

# Uncomment for testing
# search = SqlSearchTool()
# print(search.name)
# print(search.description)
# print(search.args)
# print(search.invoke(input="SELECT * FROM users"))