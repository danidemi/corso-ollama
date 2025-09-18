## === Retrieval ===
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_ollama import ChatOllama

from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

model = "phi3"
embedding_model = "nomic-embed-text"
chroma_directory = "./chroma_db"








embedding_function = OllamaEmbeddings(model=embedding_model)

vector_db = Chroma(
    persist_directory=chroma_directory,
    embedding_function=embedding_function,
    collection_name="simple-rag",
)
quanti_embedding = len( vector_db.get(limit=1)['ids'] )
print(quanti_embedding)
if quanti_embedding==0:
    print(f"ERRORE: il database vettoriale in {chroma_directory} non contiene embeddings. Esegui prima 00-load-pdf.py")
    exit(1)
input("Premi invio per continuare...")




# MultiQueryRetriever è una classe di langchain.retrievers.multi_query che permette di creare un retriever
# in grado di generare più query a partire da una singola domanda dell'utente utilizzando un modello linguistico (LLM).
# Questo è utile per migliorare il recupero di documenti rilevanti da un database vettoriale, catturando diversi aspetti dell'intento dell'utente.
# MultiQueryRetriever funziona prendendo la domanda originale dell'utente e utilizzando l'LLM per generare diverse domande alternative.
# Queste domande alternative vengono poi utilizzate per interrogare il database vettoriale e i risultati vengono aggregati
# per fornire un insieme più completo di documenti rilevanti.
# Una tecnica semplice per generare più domande a partire da una singola domanda e poi recuperare i documenti
# in base a queste domande, ottenendo il meglio da entrambe le strategie.
generate_multiple_questions_prompt = PromptTemplate(
    input_variables=["question"],
#     template="""
# You are an AI language model assistant. Your task is to generate three
# different versions of the given user question to retrieve relevant documents from
# a vector database. By generating multiple perspectives on the user question, your
# goal is to help the user overcome some of the limitations of the distance-based
# similarity search. Provide these alternative questions separated by newlines.
# Original question: {question}
#     """,    
    template="""
Sei un assistente AI. Il tuo compito è generare tre
versioni diverse della domanda dell'utente per recuperare documenti rilevanti da
un database vettoriale. Generando più prospettive sulla domanda dell'utente,
l'obiettivo è aiutare l'utente a superare alcune delle limitazioni della ricerca
di similarità basata sulla distanza. Fornisci queste domande alternative separate da una nuova riga.
Domanda originale: {question}
    """,
)
print(generate_multiple_questions_prompt.invoke({"question":"XYZ"}))
input("Premi invio per continuare...")





llm = ChatOllama(model=model)
retriever = MultiQueryRetriever.from_llm(
    vector_db.as_retriever(), 
    llm, 
    prompt=generate_multiple_questions_prompt
)
print(retriever.invoke("Quali dati richiede il quadro RU?"))
input("Premi invio per continuare...")





# RAG prompt
prompt_template = ChatPromptTemplate.from_template("""
Answer the question based ONLY on the following context:
{context}
Question: {question}
""")


chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt_template
    | llm
    | StrOutputParser()
)

 

print(chain.invoke(input=("Quali dati richiede il quadro RU?",)))


