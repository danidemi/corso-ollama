# Riferimenti
# https://python.langchain.com/docs/how_to/lcel_cheatsheet/

from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough

# definite un Runnable
runnable = RunnableLambda(lambda x: f"ciao {x}")

# eseguirlo sincronicamente con 1 input
result = runnable.invoke(5)
print(result)

# eseguirlo sincronicamente con un batch di input, restituisce un batch di risultati
result = runnable.batch(["mario", "luigi", "pippo"])
print(result)

# composizione in sequenza
# il tipo di input della catena deve corrispondere all tipo di input del primo runnable
# l'output del primo runnable deve corrispondere al tipo di input del secondo runnable e così via
# il risultato finale è l'output dell'ultimo runnable
incrementa = RunnableLambda(lambda x: x + 1)
triplica = RunnableLambda(lambda y: y * 3)
sequenza = incrementa | triplica
print(sequenza.invoke(3)) 

# composizione in parallelo
# il tipo di input alla chain deve corrispondere agli input dei singoli runnable
# l'input viene passato a tutti i runnable in parallelo
# l'output è un dizionario con le chiavi corrispondenti ai nomi dei runnable
parallelo = RunnableParallel({"inc": incrementa, "tr" : triplica})
print(parallelo.invoke(3))




# composizione mista
dict_as_string = RunnableLambda(lambda dict: f"Dictionary {dict}")
mista = incrementa | {"inc": incrementa, "tr" : triplica} | dict_as_string
print(mista.invoke(3))


# passthrough passa l'input come output senza modificarlo
chain = RunnablePassthrough()
print(chain.invoke("test"))
print(chain.invoke({"pi":3.14, "e":2.71}))

# ma nel caso di dizionari in input può aggiungere dei campi, in questo caso "total"
chain = RunnablePassthrough.assign(total = lambda d: sum(d.values()))
print(chain.invoke({"pi":3.14, "e":2.71}))


# In caso di errore si può definire un fallback
runnable1 = RunnableLambda(lambda x: x + "foo")
runnable2 = RunnableLambda(lambda x: str(x) + "bar")
chain = runnable1.with_fallbacks([runnable2])
print(chain.invoke(5))
print(chain.invoke("gigi"))

# Richiede uv pip install grandalf
# Stampa il grafo della catena
dict_as_string = RunnableLambda(lambda dict: f"Dictionary {dict}")
mista = incrementa | {"inc": incrementa, "tr" : triplica} | dict_as_string
mista.get_graph().print_ascii()