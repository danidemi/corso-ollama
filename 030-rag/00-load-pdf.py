import os

## 1. Ingest PDF Files
"""
ollama pull nomic-embed-text

Questo script implementa una semplice pipeline di Retrieval-Augmented Generation (RAG) per documenti PDF utilizzando LangChain e Ollama.
Esegue i seguenti passaggi:

1. Acquisisce un file PDF locale ed estrae il suo contenuto testuale tramite UnstructuredPDFLoader.
2. Suddivide il testo estratto in piccoli chunk sovrapposti utilizzando RecursiveCharacterTextSplitter.
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
import random
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.document_loaders import OnlinePDFLoader
from langchain_community.document_loaders import PyPDFLoader

doc_path = f".{os.sep}PF_2024_istruzioni.pdf"
model = "phi3"
embedding_model = "nomic-embed-text"

print(f"Caricamento del documento PDF from {os.getcwd()}...")    
#data = UnstructuredPDFLoader(file_path=doc_path, languages=["ita"]).load()
data = PyPDFLoader(file_path=doc_path).load()
print("Fatto")

# Anteprima del contenuto
print(f"### Testa del documento. {len(data)}:")
content = data[0].page_content
print(content[0:1000])
input("Premi invio per continuare...")







from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

print("Suddivisione del documento in chunk...")

# RecursiveCharacterTextSplitter suddivide il testo in chunk sovrapposti, preservando il contesto e la coerenza delle frasi.
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
chunks = text_splitter.split_documents(data)
print("Chunking completato....")

print(f"Numero di chunks: {len(chunks)}")
for i in range(min(10, len(chunks))):
    random_index = random.randint(0, len(chunks)-1) 
    print(f"Chunk {random_index}/{len(chunks)}:\n{chunks[random_index]}")
input("Premi invio per continuare...")  






import ollama
print("Aggiunta dei documenti al database vettoriale...")
# Chroma è una classe di langchain_community.vectorstores che fornisce un'interfaccia semplice per creare e gestire un database vettoriale Chroma.
vector_db = Chroma.from_documents(
    # I chunks da indicizzare
    documents=chunks,
    # La funzione di embedding da utilizzare per generare i vettori.
    # Ogni documento viene trasformato in un vettore numerico tramite questa funzione.
    embedding=OllamaEmbeddings(model=embedding_model),
    # Il nome della collezione in cui salvare i vettori.
    collection_name="simple-rag",
    persist_directory="./chroma_db"
)
print("Aggiunta completata.")

