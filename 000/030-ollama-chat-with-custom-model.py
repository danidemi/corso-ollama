import ollama


print("Creating model 'commentator'...")
ollama.create(
    model="commentator", 
    #modelfile=the_modelfile)
    system=" You are very passionate footbal commentator who emphasize the action of the game. You are quick,very succinct but love hyperboles and giving nicknames to players.",
    from_="phi3",
    parameters={"temperature":0.1}
    )
print("Created model 'commentator'.")

print("Querying model 'commentator'...")
res = ollama.generate(model="commentator", prompt="Describe a goal by Messi against Buffon.")
print(res["response"])

print("Deleting model 'commentator'...")
# # delete model
ollama.delete("commentator")