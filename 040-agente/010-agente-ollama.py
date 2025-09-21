import ollama

response = ollama.chat(
    model='llama3.2:3b',
    messages=[{'role': 'user', 'content':
        'What is the weather in Paris?'}],

		# provide a weather checking tool to the model
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
    },
  ],
)

print(response)
print(response['message']['tool_calls'])

# model='llama3.2:3b' 
# created_at='2025-09-21T13:19:23.302825637Z' 
# done=True 
# done_reason='stop' 
# total_duration=615277327 
# load_duration=71841121 
# prompt_eval_count=166 
# prompt_eval_duration=1514863 
# eval_count=18 
# eval_duration=541122175 
# message=Message(
#     role='assistant', 
#     content='', 
#     thinking=None, 
#     images=None, 
#     tool_name=None, 
#     tool_calls=[ToolCall(function=Function(name='get_current_weather', arguments={'city': 'Toronto'}))])
