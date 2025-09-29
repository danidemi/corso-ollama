import ollama

# ollama è una libreria Python per interagire con il modello di linguaggio Ollama tramite la sua API REST.
# la libreria riproduce le funzionalità principali dell'API REST di Ollama in modo più semplice e Pythonico.

llms = ollama.list()
print(f"Modelli disponibili: {[m.model for m in llms.models]}")

print(f"\n\n {ollama.show(llms.models[0].model)}")

# ollama.pull("modelname")

generated = ollama.generate(
    model="phi3",
    prompt="why is the sky blue?",
).response

print(f"\n\n{generated}")

embed = ollama.embed(
    model="phi3",
    input="Hello, world!")
print(f"\n\n{embed}...")  # Stampa i primi 10 valori dell'embedding
