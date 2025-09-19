from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_core.tools import tool

# Importiamo le librerie necessarie da LangChain

# Creiamo una funzione che simula uno strumento (tool) semplice
# https://python.langchain.com/docs/concepts/tools/
@tool
def saluta(nome: str) -> str:
    """
    Questa funzione prende un nome e restituisce un saluto personalizzato.
    """
    return f"Ciao, {nome}! Benvenuto nel mondo degli agenti LLM."

# Creiamo un oggetto Tool che LangChain può usare
print(saluta.name) # multiply
print(saluta.description) # Multiply two numbers.
print(saluta.args)
input("Premi invio per continuare...")



strumento_saluto = Tool(
    name="Saluta",
    func=saluta,
    description="Usa questo strumento per salutare una persona fornendo il suo nome."
)

# Inizializziamo il modello LLM (Large Language Model) usando Ollama
modello_llm = ChatOllama(model="llama3.2:3b")  

# Inizializziamo l'agente con il modello LLM e lo strumento creato
agente = initialize_agent(
    tools=[saluta],           # Lista degli strumenti che l'agente può usare
    llm=modello_llm,                    # Il modello LLM che genera le risposte
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Tipo di agente (zero-shot, reagisce in base alla descrizione degli strumenti)
    verbose=True,                        # Mostra informazioni dettagliate durante l'esecuzione
    
)

# Esempio di utilizzo dell'agente
domanda_utente = "Saluta Mario"

# L'agente analizza la domanda e decide se usare uno degli strumenti disponibili
risposta = agente.invoke(domanda_utente)

# Stampiamo la risposta dell'agente
print(risposta)

# --- Spiegazione dei passaggi ---
# 1. Importiamo le classi principali di LangChain.
# 2. Definiamo uno strumento semplice che saluta una persona.
# 3. Inizializziamo il modello LLM (Ollama con modello phi3).
# 4. Creiamo l'agente, collegando il modello e lo strumento.
# 5. L'agente riceve una domanda e decide come rispondere, usando il modello LLM e gli strumenti disponibili.
# 6. Stampiamo la risposta per vedere il risultato.