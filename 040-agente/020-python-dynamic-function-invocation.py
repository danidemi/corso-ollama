# Dimostrazione di invocazione dinamica di funzioni in Python

def functions_with_positional_args(city: str, celsius_or_farenaith: str) -> str:
    return f"The current weather in {city} is sunny with a temperature of 25°{celsius_or_farenaith}."

# Nome della funzione da invocare dinamicamente
function_name = "functions_with_positional_args"

# Ottieni la funzione dall'ambiente globale e invocala con argomenti in una tupla
args = ("Rome", "C")
result = globals()[function_name](*args)
print(result)

# Ottieni la funzione dall'ambiente globale e invocala con argomenti in una lista
args = ["Milan", "F"]
result = globals()[function_name](*args)
print(result)


args = {
    "city": "Naples",
    "celsius_or_farenaith": "C"
}
result = globals()[function_name](**args)
print(result)
