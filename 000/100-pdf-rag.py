## 1. Ingest PDF Files
"""
This script implements a simple Retrieval-Augmented Generation (RAG) pipeline for PDF documents using LangChain and Ollama.
It performs the following steps:

1. Ingests a local PDF file and extracts its text content using UnstructuredPDFLoader.
2. Splits the extracted text into smaller, overlapping chunks using RecursiveCharacterTextSplitter.
    # RecursiveCharacterTextSplitter è uno splitter avanzato che suddivide il testo in chunk di dimensione specificata (chunk_size),
    # mantenendo una sovrapposizione (chunk_overlap) tra i chunk per preservare il contesto tra le parti adiacenti.
    # Utilizza una strategia ricorsiva per evitare di spezzare frasi o paragrafi in modo innaturale, migliorando la qualità dei chunk per l'embedding.
3. Genera embeddings per ciascun chunk tramite OllamaEmbeddings e li salva in un database vettoriale Chroma.
4. Esegue una ricerca di similarità sui vettori per recuperare i documenti più rilevanti rispetto a una query.
5. Utilizza MultiQueryRetriever per generare automaticamente più versioni della domanda dell’utente, migliorando la copertura semantica della ricerca.
6. Passa i documenti recuperati e la domanda a un modello LLM (ChatOllama) per generare una risposta basata solo sul contesto fornito.

Prerequisiti:
- Installare i pacchetti richiesti con `pip install -r requirements.txt`.
- Assicurarsi che il modello di embedding ("nomic-embed-text") sia disponibile su Ollama.

Nota: Il codice è pensato per documenti in italiano, ma può essere adattato ad altre lingue modificando i parametri del loader.
"""
# 2. Extract Text from PDF Files and split into small chunks
# 3. Send the chunks to the embedding model
# 4. Save the embeddings to a vector database
# 5. Perform similarity search on the vector database to find similar documents
# 6. retrieve the similar documents and present them to the user
## run pip install -r requirements.txt to install the required packages

import random
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import OnlinePDFLoader

doc_path = "/home/user/prj/corso-ollama/000/PF_2024_istruzioni.pdf"
model = "phi3"

# Local PDF file uploads
print("Caricamento del documento PDF...")
if doc_path:
    loader = UnstructuredPDFLoader(file_path=doc_path, languages=["ita"])
    data = loader.load()
    print("Fatto")

# Preview first page
print("Anteprima:")
content = data[0].page_content
print(content[:100])
# ==== End of PDF Ingestion ====


# ==== Extract Text from PDF Files and Split into Small Chunks ====
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# Split and chunk
# RecursiveCharacterTextSplitter è uno splitter avanzato che suddivide il testo in chunk di dimensione specificata (chunk_size),
# mantenendo una sovrapposizione (chunk_overlap) tra i chunk per preservare il contesto tra le parti adiacenti.
# Utilizza una strategia ricorsiva per evitare di spezzare frasi o paragrafi in modo innaturale, migliorando la qualità dei chunk per l'embedding.
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
chunks = text_splitter.split_documents(data)
print("done splitting....")

print(f"Number of chunks: {len(chunks)}")
for i in range(min(10, len(chunks))):
    random_index = random.randint(0, len(chunks)-1) 
    print(f"Example chunk: {chunks[random_index]}")

# # ===== Add to vector database ===
# import ollama

# ollama.pull("nomic-embed-text")

# vector_db = Chroma.from_documents(
#     documents=chunks,
#     embedding=OllamaEmbeddings(model="nomic-embed-text"),
#     collection_name="simple-rag",
# )
# print("done adding to vector database....")


# ## === Retrieval ===
# from langchain.prompts import ChatPromptTemplate, PromptTemplate
# from langchain_core.output_parsers import StrOutputParser

# from langchain_ollama import ChatOllama

# from langchain_core.runnables import RunnablePassthrough
# from langchain.retrievers.multi_query import MultiQueryRetriever

# # set up our model to use
# llm = ChatOllama(model=model)

# # a simple technique to generate multiple questions from a single question and then retrieve documents
# # based on those questions, getting the best of both worlds.
# QUERY_PROMPT = PromptTemplate(
#     input_variables=["question"],
#     template="""You are an AI language model assistant. Your task is to generate five
#     different versions of the given user question to retrieve relevant documents from
#     a vector database. By generating multiple perspectives on the user question, your
#     goal is to help the user overcome some of the limitations of the distance-based
#     similarity search. Provide these alternative questions separated by newlines.
#     Original question: {question}""",
# )

# retriever = MultiQueryRetriever.from_llm(
#     vector_db.as_retriever(), llm, prompt=QUERY_PROMPT
# )


# # RAG prompt
# template = """Answer the question based ONLY on the following context:
# {context}
# Question: {question}
# """

# prompt = ChatPromptTemplate.from_template(template)


# chain = (
#     {"context": retriever, "question": RunnablePassthrough()}
#     | prompt
#     | llm
#     | StrOutputParser()
# )


# # res = chain.invoke(input=("what is the document about?",))
# # res = chain.invoke(
# #     input=("what are the main points as a business owner I should be aware of?",)
# # )
# res = chain.invoke(input=("how to report BOI?",))

# print(res)