from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_core.tools import tool

def conta_occorrenze(parola: str, lettera: str) -> int:
    """
    Conta quante volte una lettera appare in una parola.
    """
    return parola.count(lettera)

@tool
def conta_occorrenze_tool(parola: str, lettera: str) -> int:
    """Restituisce il numero di volte che una lettera appare in una parola."""
    return parola.count(lettera)

strumento_conta_occorrenze = Tool(
    name="Contatore di occorrenze",
    func=conta_occorrenze,
    description="Usa questo strumento per sapere quante occorrenze di una lettera esistono in una parola."

)

strumento_conta_occorrenze = Tool.from_function(
    func=conta_occorrenze,
    name="Contatore di occorrenze",
    description="Usa questo strumento per sapere quante occorrenze di una lettera esistono in una parola. Devi fornire una parola e una lettera."

)

# Inizializziamo il modello LLM (Large Language Model) usando Ollama
modello_llm = ChatOllama(model="llama3.2:3b")  

# Inizializziamo l'agente con il modello LLM e lo strumento creato
agente = initialize_agent(
    tools=[conta_occorrenze_tool],           # Lista degli strumenti che l'agente può usare
    llm=modello_llm,                    # Il modello LLM che genera le risposte
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,  # Tipo di agente (zero-shot, reagisce in base alla descrizione degli strumenti)
    verbose=True,                        # Mostra informazioni dettagliate durante l'esecuzione
    
)

# Esempio di utilizzo dell'agente
domanda_utente = "Quante volte appare la lettera a nella parola banana?"

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