import os
import numpy as np
from getpass import getpass
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

import os
from getpass import getpass

#hfapi_key = getpass("Enter you HuggingFace access token:")
hfapi_key="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"
os.environ["HF_TOKEN"] = hfapi_key
os.environ["HUGGINGFACEHUB_API_TOKEN"] = hfapi_key

# importing HuggingFace model abstraction class from langchain
from langchain_huggingface import HuggingFaceEndpoint

llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",       # Model card: https://huggingface.co/HuggingFaceH4/zephyr-7b-beta
    task="text-generation",
    max_new_tokens = 512,
    top_k = 30,
    temperature = 0.1,
    repetition_penalty = 1.03,
)

# UPLOAD the Docs first to this notebook, then run this cell

from langchain_community.document_loaders import PyPDFLoader

# Load PDF
loaders = [
    PyPDFLoader(".\content\context_kb.pdf")

]

docs = []
for loader in loaders:
    docs.extend(loader.load())

len(docs)
docs

"""# Splitting of document"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

# Split
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50
)

splits = text_splitter.split_documents(docs)

print(len(splits))
print(len(splits[0].page_content) )
splits[0].page_content

"""# Embeddings"""

import torch

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Device: {device}")

# Embedding Model

from langchain_huggingface import HuggingFaceEmbeddings

modelPath ="mixedbread-ai/mxbai-embed-large-v1"                  # Model card: https://huggingface.co/mixedbread-ai/mxbai-embed-large-v1
                                                                 # Find other Emb. models at: https://huggingface.co/spaces/mteb/leaderboard

# Create a dictionary with model configuration options, specifying to use the CPU for computations
model_kwargs = {'device': device}      # cuda/cpu

# Create a dictionary with encoding options, specifically setting 'normalize_embeddings' to False
encode_kwargs = {'normalize_embeddings': False}

embedding =  HuggingFaceEmbeddings(
    model_name=modelPath,     # Provide the pre-trained model's path
    model_kwargs=model_kwargs, # Pass the model configuration options
    encode_kwargs=encode_kwargs # Pass the encoding options
)

embedding

"""# Vectorstores"""

from langchain_chroma import Chroma

persist_directory = 'docs/chroma/'
#!rm -rf ./docs/chroma  # remove old database files if any

vectordb = Chroma.from_documents(
    documents=splits,                    # splits we created earlier
    embedding=embedding,
    persist_directory=persist_directory, # save the directory
)

print(vectordb._collection.count()) # same as number of splits

"""# Retrieval"""

question = "What is openstack?"
retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 2, "fetch_k":5})
docs = retriever.invoke(question)
docs

"""# Augmentation"""

from langchain_core.prompts import PromptTemplate                                    # To format prompts
from langchain_core.output_parsers import StrOutputParser                            # to transform the output of an LLM into a more usable format
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough          # Required by LCEL (LangChain Expression Language)

# Build prompt
template = """Use the following pieces of context to explain the openstack log. Explain what that log means and provide a potential solution to fix it

  Always say "thanks for asking!" at the end of the answer.

{context}
Question: {question}
Helpful Answer:"""

QA_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

"""# Creating final RAG Chain"""

retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 7, "fetch_k":15})
retriever

retrieval = RunnableParallel(
    {
        "context": RunnablePassthrough(context= lambda x: x["question"] | retriever),
        "question": RunnablePassthrough()
        }
    )


# RAG Chain

rag_chain = (retrieval                     # Retrieval
             | QA_PROMPT                   # Augmentation
             | llm                         # Generation
             | StrOutputParser()
             )

response = rag_chain.invoke({"question": "What is openstack??"})

print (response)



def ragFunction(question):

  QA_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template,)
  rag_chain= {"context":RunnablePassthrough(context= lambda x:x["question"] | retriever),
         "question": lambda x:x["question"]}|QA_PROMPT | llm |StrOutputParser()

  print(question)
  #response=rag_chain.invoke(question)
  #response=rag_chain.invoke({"question" :"what is a package?"})
  response=rag_chain.invoke({"question" : question})
  print(response)
  return response

