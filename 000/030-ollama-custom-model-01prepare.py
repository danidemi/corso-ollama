import ollama


print("Creating model 'commentator'...")
ollama.create(
    model="commentator", 
    system=" You are very passionate footbal commentator who emphasize the action of the game. You are quick,very succinct but love hyperboles and giving nicknames to players.",
    from_="phi3",
    parameters={"temperature":0.9}
    )
print("Created model 'commentator'.")

print("Creating model 'boring'...")
ollama.create(
    model="boring", 
    system=" You are very boring, you alway answer using the least amount of words, without bias and not hiding facts.",
    from_="phi3",
    parameters={"temperature":0.0}
    )
print("Created model 'boring'.")

