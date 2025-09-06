import ollama


response = ollama.list()
print(f"Available models: {response}")




# == Generate example ==
res = ollama.generate(
    model="phi3",
    prompt="why is the sky blue?",
)

# show
print(ollama.show("phi3"))


# Create a new model with modelfile
the_modelfile = """
FROM phi3
SYSTEM You are very passionate footbal commentator who emphasize the action of the game. You are quick,very succinct but love hyperboles and giving nicknames to players.
PARAMETER temperature 0.1
"""

ollama.create(model="commentator", modelfile=the_modelfile)

res = ollama.generate(model="commentator", prompt="Describe a goal by Messi against Buffon.")
print(res["response"])


# # delete model
ollama.delete("commentator")