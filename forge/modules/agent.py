from ollama import Client

client = Client(host='http://localhost:11434')
response = client.chat(model='codellama:7b', messages=[
    {"role": "user", "content": "Write a pytest unit test for this function:\ndef is_even(n): return n % 2 == 0"}
])

print(response['message']['content'])
 
