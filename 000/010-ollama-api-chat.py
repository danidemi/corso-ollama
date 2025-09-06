import ollama


response = ollama.list()
print(f"Available models: {response}")

# == Chat example ==
res = ollama.chat(
    model="phi3",
    messages=[
        {"role": "user", "content": "why is the yolk predominantly yellow?"},
    ],
)
print(res)

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