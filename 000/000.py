import requests
import json

# Whether to pretty print the output or not
pretty_print = False

# Extended doc at:
# https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-completion
response = requests.post(
    "http://localhost:11434/api/generate", 
    json = {
        "model": "phi3",
        "prompt": "tell me a very short story and make it funny. No more than 20 words.",
    }, 
    stream=True
)  # remove the stream=True to get the full response


# check the response status
if response.status_code == 200:
    print("Generated Text:", end=" ", flush=True)
    # Iterate over the streaming response
    for line in response.iter_lines():
        if line:
            if pretty_print:
                # Decode the line and parse the JSON
                decoded_line = line.decode("utf-8")
                result = json.loads(decoded_line)
                # Get the text from the response
                generated_text = result.get("response", "")
                print(generated_text, end="", flush=True)
            else:
                # Decode the line and parse the JSON
                decoded_line = line.decode("utf-8")
                result = json.loads(decoded_line)
                print(json.dumps(result, indent=2))

else:
    print("Error:", response.status_code, response.text)