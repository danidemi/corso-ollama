import ollama


print("Querying model 'commentator'...")
res = ollama.generate(model="commentator", prompt="Describe a goal by Ronaldo against Buffon.")
print(res["response"])

print("Querying model 'boring'...")
res = ollama.generate(model="boring", prompt="Describe a goal by Ronaldo against Buffon.")
print(res["response"])

