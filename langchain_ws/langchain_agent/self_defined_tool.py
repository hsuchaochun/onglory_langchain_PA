import os
import sys
sys.path.append("../")
import config
from operator import itemgetter
from pydantic import PrivateAttr, BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.tools import BaseTool

# Define the SQLTool class
class SQLTool:
    def __init__(self):
        self.set_env_vars()
        
        self.llm = self.get_llm_model()
        self.db = SQLDatabase.from_uri(config.SQL_CONNECT_URL)
        
        self.write_query = create_sql_query_chain(self.llm, self.db)
        self.execute_query = QuerySQLDataBaseTool(db=self.db)
        
        self.answer_prompt = PromptTemplate.from_template(
            """Given the following user question, corresponding SQL query, and SQL result.\
            Answer the user question in Chinese(traditional), make the output be structured, might contain some tables or listed data.\
            If the output data contains table, add sufficient tab to make the table look good.\
            Also, please make sure the answer is accurate, easy to understand, and answer the question properly without losing any data.\
            The number should be rounded to 2 decimal places.\

            Question: {question}
            SQL Query: {query}
            SQL Result: {result}
            Answer: """
        )
        
        self.chain = (
            RunnablePassthrough.assign(query=self.write_query).assign(
                result=itemgetter("query") | self.execute_query
            )
            | self.answer_prompt
            | self.llm
            | StrOutputParser()
        )
    
    def set_env_vars(self):
        os.environ["LANGCHAIN_API_KEY"] = config.LANGCHAIN_API_KEY
        os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY
        os.environ["TAVILY_API_KEY"] = config.TAVILY_API_KEY

    def get_llm_model(self):
        return ChatOpenAI(
            openai_api_key=config.OPENAI_API_KEY,
            model_name="gpt-3.5-turbo",
            temperature=0
        )
    
    def execute_user_query(self, question):
        return self.chain.invoke({"question": question})

    def as_tool(self):
        # This method returns a callable object that the agent can use as a tool
        return QuerySQLDataBaseTool(db=self.db)

class Gojo_satoru(BaseTool):
    name = "gojo_satoru_gentool"
    description = (
        """這是五條體產生器，請從文本找出下面的 parameter ["protagonist", "enemy", "enemy_skill"]，
        然後把下方 parameter 取代掉，output 新的文章：
        protagonist：enemy太強了
            而且enemy還沒有使出全力的樣子
            對方就算沒有enemy_skill也會贏
            我甚至覺得有點對不起他
            我沒能在這場戰鬥讓enemy展現他的全部給我
            殺死我的不是時間或疾病
            而是比我更強的傢伙，真是太好了"""
        )

    def _run(self, 
            protagonist: str = None,
            enemy: str = None,
            enemy_skill: str = None,
            ):
        if protagonist and enemy and enemy_skill:
            print("#############")
            return f"""請把 parameter 取代掉，產出下面這文章：
            {protagonist}：{enemy}太強了啊啊啊啊啊啊
            而且{enemy}還沒有使出全力的樣子
            對方就算沒有{enemy_skill}也會贏
            我甚至覺得有點對不起他
            我沒能在這場戰鬥讓{enemy}展現他的全部給我
            殺死我的不是時間或疾病
            而是比我更強的傢伙，真是太好了"""
        else:
            return "凡夫，ChatGPT 解析不出 protagonist、enemy、enemy_skill，請再試一次。"