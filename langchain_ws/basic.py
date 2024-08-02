# import getpass
import os
import config
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

system_template = "Translate the following into {language}:"

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)

os.environ["LANGCHAIN_API_KEY"] = config.LANGCHAIN_API_KEY
os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY

model = ChatOpenAI(model="gpt-4o")

parser = StrOutputParser()

chain = prompt_template | model | parser
result = chain.invoke({"language": "Italian", "text": "hi!"})

print(result)