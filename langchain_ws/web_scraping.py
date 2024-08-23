from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.chains import create_extraction_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
import pprint
from functions import get_llm_model

# urls = ["https://www.espn.com", "https://lilianweng.github.io/posts/2023-06-23-agent/"]
# loader = AsyncHtmlLoader(urls)
# docs = loader.load()

# html2text = Html2TextTransformer()
# docs_transformed = html2text.transform_documents(docs)
# docs_transformed[0].page_content[0:500]

llm = get_llm_model()

schema = {
    "properties": {
        "news_article_title": {"type": "string"},
        "news_article_summary": {"type": "string"},
    },
    "required": ["news_article_title", "news_article_summary"],
}

def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).invoke(content)

def scrape_with_playwright(urls, schema):
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    print(f"Documents loaded: {len(docs)}")  # Check how many documents are loaded

    if not docs:
        raise ValueError("No documents loaded from the URLs")

    # Continue with document processing
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, 
        # tags_to_extract=["span"]
    )
    print(f"Documents transformed: {len(docs_transformed)}")  # Check the transformation
    
    # If no content is transformed, return early
    if not docs_transformed:
        raise ValueError("No documents were transformed")

    # Proceed with splitting and extraction
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    splits = splitter.split_documents(docs_transformed)
    print(f"Splits generated: {len(splits)}")  # Check how many splits are generated
    
    if not splits:
        raise ValueError("No splits were generated from the documents")

    # Process the first split
    extracted_content = extract(schema=schema, content=splits[0].page_content)
    pprint.pprint(extracted_content['text'])
    return extracted_content

# urls = ['https://cointelegraph.com/']
urls = ['https://decrypt.co/news']
extracted_content = scrape_with_playwright(urls, schema=schema)