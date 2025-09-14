## 1. Ingest PDF Files
"""
ollama pull nomic-embed-text

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

# # ===== Split and chunk ===== #
# RecursiveCharacterTextSplitter suddivide il testo in chunk sovrapposti, preservando il contesto e la coerenza delle frasi.
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
chunks = text_splitter.split_documents(data)
print("done splitting....")

print(f"Number of chunks: {len(chunks)}")
for i in range(min(10, len(chunks))):
    random_index = random.randint(0, len(chunks)-1) 
    print(f"Example chunk: {chunks[random_index]}")

# # ===== Add to vector database ===
import ollama
print("Aggiungendo documenti al vector database....")
# Chroma is a class from langchain_community.vectorstores that provides a simple interface to create and manage a Chroma vector database.
vector_db = Chroma.from_documents(
    # I documenti da indicizzare
    documents=chunks,
    # La funzione di embedding da utilizzare per generare i vettori. 
    # Ogni documento viene trasformato in un vettore numerico tramite questa funzione.
    embedding=OllamaEmbeddings(model="nomic-embed-text"),
    # il nome della collezione in cui salvare i vettori.
    collection_name="simple-rag",
)
print("Aggiunta completata.")


## === Retrieval ===
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_ollama import ChatOllama

from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever

# # set up our model to use
llm = ChatOllama(model=model)


# # ===== MultiQueryRetriever =====
# MultiQueryRetriever is a class from langchain.retrievers.multi_query that allows you to create a retriever
# that generates multiple queries from a single user question using a language model (LLM).
# This is useful for improving the retrieval of relevant documents from a vector database by capturing different aspects of the user's intent.
# The MultiQueryRetriever works by taking the user's original question and using the LLM to generate several alternative questions.
# These alternative questions are then used to query the vector database, and the results are aggregated to provide a more comprehensive set of relevant documents.

# a simple technique to generate multiple questions from a single question and then retrieve documents
# based on those questions, getting the best of both worlds.
QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI language model assistant. Your task is to generate five
    different versions of the given user question to retrieve relevant documents from
    a vector database. By generating multiple perspectives on the user question, your
    goal is to help the user overcome some of the limitations of the distance-based
    similarity search. Provide these alternative questions separated by newlines.
    Original question: {question}""",
)

retriever = MultiQueryRetriever.from_llm(
    vector_db.as_retriever(), 
    llm, 
    prompt=QUERY_PROMPT
)


# RAG prompt
template = """Answer the question based ONLY on the following context:
{context}
Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
print(f"Using template {template}")


chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

def question_and_answer(question: str, chain) -> str:
    print(f"Domanda: {question}")
    res = chain.invoke(input=(question,))
    print(f"Risposta: {res}")    

question = "di cosa parla il documento?"
res = chain.invoke(input=(question,))
print(f"Domanda: {question}")
print(f"Risposta: {res}")
question_and_answer("di cosa tratta il documento?", chain)
question_and_answer("quali sono le istruzioni per la compilazione del quadro RW?", chain)
question_and_answer("ho un consorte e dei figli in età scolare. Quali sono i punti di attenzione per me?", chain)
