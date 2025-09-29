import requests
import json

# Scopo: Generazione di testo a partire da un singolo prompt.
# Input: Accetta un prompt singolo (una stringa di testo) e genera una risposta basata su di esso.
# Uso: Ideale per scenari in cui vuoi una risposta diretta a una domanda o un compito specifico, senza contesto conversazionale.

# Documentazione completa:
# https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-completion
# llama3.2:3b, alibayram/smollm3, phi3
response = requests.post(
    "http://localhost:11434/api/generate", 
    json = {
        "model": "llama3.2:3b",
        "prompt": "Explain me the history of Italy in no more than 50 words.",
    }, 
    stream=False # Se la risposta deve essere in streaming o no
)  


# Controlla se la richiesta è andata a buon fine verificando lo status code HTTP
if response.status_code == 200:

    # Se stampare il dettaglio JSON restituito
    print_json_response = False    
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode("utf-8")
            result = json.loads(decoded_line)            
            if print_json_response:
                print(json.dumps(result, indent=2))
            else:
                generated_text = result.get("response", "")
                print(generated_text, end="", flush=True)                
                

else:
    print("Error:", response.status_code, response.text)