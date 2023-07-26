import os
import replicate
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import clear

print("Llama2 Chatbot")


#ok so basically i added the credentials that i generated but if this was replicate_api=input() then it would make sure the user's llama2 key was valid
replicate_api = "r8_JLSjaG25irDyQWSQRDvWhFJuiyP4ShA1VmHzb"
if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
    print('Please enter valid credentials!')
    exit()

os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Store LLM generated responses
messages = [{"role": "assistant", "content": "How may I assist you today?"}]

def clear_chat_history():
    messages.clear()
    messages.append({"role": "assistant", "content": "How may I assist you today?"})

def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5',
                           input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                  "temperature":0.1, "top_p":0.9, "max_length":512, "repetition_penalty":1})
    return output

# Main loop
while True:
    user_input = prompt("You: ")
    if not user_input:
        continue

    messages.append({"role": "user", "content": user_input})

    if user_input.lower() == 'clear':
        clear_chat_history()
        continue

    clear()

    for message in messages:
        role, content = message["role"], message["content"]
        if role == "user":
            print("You:", content)
        else:
            print("Assistant:", content)

    if messages[-1]["role"] != "assistant":
        print("Assistant is thinking...")

        response = generate_llama2_response(user_input)

        full_response = ''
        for item in response:
            full_response += item
        print(full_response)
        

        messages.append({"role": "assistant", "content": full_response})
