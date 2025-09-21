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
    Get the current weather for a city.
    """

    weather = ["sunny", "rainy", "cloudy", "windy", "snowy"][hash(city) % 5]
    temperature = -5 + (hash(city) % 40)

    # Simuliamo una risposta meteo
    return f"The current weather in {city} is {weather} with a temperature of {temperature}°C."


model = 'llama3.2:3b'
user_input = None
messages = []
while True:
    
    # controlliamo se l'utente vuole uscire
    user_input = input("Prompt (o exit): ")
    if user_input == "exit":
        break

    # aggiungiamo il messaggio dell'utente alla lista dei messaggi che saranno inviati
    messages.append( {'role': 'user', 'content': user_input} )

    print("=> LLM")
    for message in messages:
        print(f"   {message}")



    response: ollama.ChatResponse = ollama.chat(
        model=model,
        messages=messages,        
        tools=[get_current_weather],
    )

    print("<= LLM")
    print(f"   {response['message']}")   

    messages.append(response['message']) 


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

            messages.append({
                'role': 'tool', 
                'tool_name': tool_name,
                'content': tool_result})

        print("=> LLM")
        for message in messages:
            print(f"   {message}")            

        response : ollama.ChatResponse = ollama.chat(
            tools=tools,
            model=model,
            messages=messages
        )            

        print("<= LLM")
        print(f"   {response.message}")         


