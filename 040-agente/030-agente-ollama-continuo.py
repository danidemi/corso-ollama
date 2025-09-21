import ollama

tools=[{
  'type': 'function',
  'function': {
    'name': 'get_current_weather',
    'description': 'Get the current weather for a city',
    'parameters': {
      'type': 'object',
      'properties': {
        'city': {
          'type': 'string',
          'description': 'The name of the city',
        },
      },
      'required': ['city'],
    },
  },
}]

def get_current_weather(city: str) -> str:
    """
    Simula il recupero delle informazioni meteo per una città specifica.
    In un'applicazione reale, questa funzione potrebbe fare una chiamata API a un servizio meteo.
    """
    # Simuliamo una risposta meteo
    return f"The current weather in {city} is sunny with a temperature of 25°C."



user_input = None
messages = []
while True:
    
    # controlliamo se l'utente vuole uscire
    user_input = input("Prompt (o exit): ")
    if user_input == "exit":
        break

    # aggiungiamo il messaggio dell'utente alla lista dei messaggi che saranno inviati
    messages.append( [{'role': 'user', 'content': user_input}] )

    print("=> LLM")
    for message in messages:
        print(f"   {message}")

    
    model = 'llama3.2:3b'
    response = ollama.chat(
        tools=tools,
        model=model,
        messages=messages
    )

    print("<= LLM")
    print(f"   {response['message']}")    


    while ('tool_calls' in response['message']):
        # iteriamo sulle chiamate agli strumenti (tool calls)
        for tool_call in response['message']['tool_calls']:
            print(f"Chiamata allo strumento: {tool_call}")
            tool_name = tool_call['function']['name']
            tool_args = tool_call['function']['arguments']
            print("=> Tool")
            print(f"   {tool_name}({tool_args})")

            tool_result = globals()[tool_name](**tool_args)
            print("<= Tool")
            print(f"   {tool_result}")

            messages.append({'role': 'tool', 'content': tool_result})

        print("=> LLM")
        for message in messages:
            print(f"   {message}")            

        response = ollama.chat(
            tools=tools,
            model=model,
            messages=messages
        )            

        print("<= LLM")
        print(f"   {response['message']}")         


