from langchain_google_community import GmailToolkit
from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

toolkit = GmailToolkit()

# Can review scopes here https://developers.google.com/gmail/api/auth/scopes
# For instance, readonly scope is 'https://www.googleapis.com/auth/gmail.readonly'
credentials = get_gmail_credentials(
    # token_file="token.json",
    # scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
)
api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)

tools = toolkit.get_tools()

# ======================================================================================================
import os
import sys
sys.path.append("../")
import config

os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY
llm = ChatOpenAI(model="gpt-4o")
agent_executor = create_react_agent(llm, tools)

example_query = "Review all the emails give me the FCN product details which the strike percent is higher than 90%."

events = agent_executor.stream(
    {"messages": [("user", example_query)]},
    stream_mode="values",
)
for event in events:
    event["messages"][-1].pretty_print()