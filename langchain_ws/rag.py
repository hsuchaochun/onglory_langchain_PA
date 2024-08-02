import os
import config
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from typing import List
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# export
os.environ["LANGCHAIN_API_KEY"] = config.LANGCHAIN_API_KEY
os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY

model = ChatOpenAI(model="gpt-4o")

documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Goldfish are popular pets for beginners, requiring relatively simple care.",
        metadata={"source": "fish-pets-doc"},
    ),
    Document(
        page_content="Parrots are intelligent birds capable of mimicking human speech.",
        metadata={"source": "bird-pets-doc"},
    ),
    Document(
        page_content="Rabbits are social animals that need plenty of space to hop around.",
        metadata={"source": "mammal-pets-doc"},
    ),
]

vectorstore = Chroma.from_documents(
    documents,
    embedding=OpenAIEmbeddings(),
)

# print(vectorstore.similarity_search("cat"))

# Note that providers implement different scores; Chroma here
# returns a distance metric that should vary inversely with
# similarity.
# print(vectorstore.similarity_search_with_score("cat"))

# embedding = OpenAIEmbeddings().embed_query("cat")
# print(vectorstore.similarity_search_by_vector(embedding))


# retriever = RunnableLambda(vectorstore.similarity_search).bind(k=1)  # select top result
# retriever.batch(["cat", "shark"])

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 1},
)
# retriever.batch(["cat", "shark"])

message = '''
Answer this question using the provided context only.

{question}

Context:
{context}
'''

prompt = ChatPromptTemplate.from_messages([("human", message)])

rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | model

response = rag_chain.invoke("tell me about cats")

print(response.content)
