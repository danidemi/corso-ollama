import ollama

# Scopo: Interagire con il modello di linguaggio Ollama in una modalità conversazionale.
# Input: Accetta una serie di messaggi che rappresentano una conversazione tra l'utente e il modello.
# Uso: Ideale per scenari in cui vuoi mantenere il contesto di una conversazione, come chatbot o assistenti virtuali.

messages = []
user_message = None
while True:
    user_message = input("Prompt (o exit): ")
    if user_message == "exit":
        break

    messages.append({"role": "user", "content": user_message})

    print(f"Messaggi che saranno inviati: {messages}")

    res = ollama.chat(
        model="phi3",
        messages=messages,
    )
    print(f"LLM: {res}")
    messages.append(res.get("message"))


# # == Chat example streaming ==
# res = ollama.chat(
#     model="phi3",
#     messages=[
#         {
#             "role": "user",
#             "content": "why is the ocean so salty?",
#         },
#     ],
#     stream=True,
# )
# # for chunk in res:
# #     print(chunk["message"]["content"], end="", flush=True)


# # ==================================================================================
# # ==== The Ollama Python library's API is designed around the Ollama REST API ====
# # ==================================================================================

# # == Generate example ==
# res = ollama.generate(
#     model="llama3.2",
#     prompt="why is the sky blue?",
# )

# # show
# # print(ollama.show("llama3.2"))


# # Create a new model with modelfile
# modelfile = """
# FROM llama3.2
# SYSTEM You are very smart assistant who knows everything about oceans. You are very succinct and informative.
# PARAMETER temperature 0.1
# """

# ollama.create(model="knowitall", modelfile=modelfile)

# res = ollama.generate(model="knowitall", prompt="why is the ocean so salty?")
# print(res["response"])


# # delete model
# ollama.delete("knowitall")