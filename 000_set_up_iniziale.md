# Set up ambiente

Installare Python

    sudo apt update
    sudo apt install python3 python3-pip

Installare `uv`, strumento omnicomprensivo per la gestione dei progetti Python:

    # On macOS and Linux.
    curl -LsSf https://astral.sh/uv/install.sh | sh




#  Installare e operare con Ollama

Istruzioni qui https://ollama.com/download/linux. Eseguire da account qualsiasi:

    $ curl -fsSL https://ollama.com/install.sh | sh

Durante l'installazione:

```
Creating ollama systemd service...
Nvidia GPU detected.
The Ollama API is now available at 127.0.0.1:11434.
Install complete. Run "ollama" from the command line.
```

Verificare l'installazione

    $ ollama -v



# Utilizzare un modello
Si cerca il nome del modello da utilizzare sul sito web di Ollama e si trova ad esempio questo LLM https://ollama.com/library/phi3

    ollama pull phi3
    ollama show phi3
    ollama run phi3
    
    Prepara una mail di lamentela da inviare al supermercato dove ho comprato il frullatore nuovo. Il problema è che quando sono arrivato a casa e ho aperto la scatola, dentro non c'era niente. Usa un tono severo e formale. 

    Puoi rendere molto più formale questo invito? Devo inviarlo al Re d'Inghilterra: "Ciao Carlo, sabato al cinema c'è l'ultimo film del nostro regista preferito, ti va di venire con me a vederlo? Ci vediamo alle 22:00 davanti al cinema"

    Spiegami come fossi un bambino di 5 anni come funziona una centrale idroelettrica. Sii breve e conciso.

    Summarize this chapter: "..."

    /?
    /clear
    /show
    (altri comandi visti in seguito)

# Controllare se il modello gira su GPU o CPU

In un'altra finestra eseguire:

    ollama ps

# Altre cose...

/show parameters cos'è? => sono i token di stop delle varie parti della chat, nella rappresentazione interna del testo, con l'indicazione del ruolo che è terminato.
/show template cos'è => il template in linguaggio Jinjia2 che rappresenta la struttura della rappresentazione interna del testo

# API REST

```curl
curl http://localhost:11434/api/generate -d '{
  "model": "phi3",
  "prompt":"Why is the sky blue?"
}'
```

risposta streaming:

```json
{"model":"phi3","created_at":"2025-08-30T15:30:33.243978184Z","response":"The","done":false}
{"model":"phi3","created_at":"2025-08-30T15:30:33.288683397Z","response":" reason","done":false}
{"model":"phi3","created_at":"2025-08-30T15:30:33.297325682Z","response":" for","done":false}
{
    "model":"phi3",
    "created_at":"2025-08-30T15:30:33.297325682Z",
    "response":"",
    "context": [32010,29871,13,11008,338,278,14744,7254,29973]
    "done":true
}

```

```curl
curl http://localhost:11434/api/generate -d '{
  "model": "phi3",
  "prompt":"And why not green?",
  "context": [32010,29871,13,11008,338,278,14744,7254,29973],
  "stream":false
}'
```




```curl
curl http://localhost:11434/api/generate -d '{
  "model": "phi3",
  "prompt":"Generate a JSON object that shows the distances in Km among the main European cities",
  "stream":false,
  "format":"json"
}'
```
Non funziona molto bene con "phi3".




# Client

Visto che è un server, esistono vari client web open source.
https://github.com/ollama/ollama?tab=readme-ov-file#community-integrations

## Hollama

    https://hollama.fernando.is

    sudo systemctl stop ollama    
    OLLAMA_ORIGINS=chrome-extension://*,moz-extension://*,safari-web-extension://*,https://hollama.fernando.is ollama serve

## Open Web Ui

veramente massivo, ha Gb e Gb di librerie

https://github.com/open-webui/open-webui 

uv venv
uv pip install open-webui
open-webui serve


