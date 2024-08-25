from openai import OpenAI
import os
from flask import Flask, render_template, request

app = Flask(__name__)

def get_api_key():
    with open("api_key.txt", "r") as file:
        return file.read()

os.environ["OPENAI_API_KEY"] = get_api_key()

llm = OpenAI()
messages = []

def get_sys_prompt(user_entry):
    with open("system_prompt.txt") as file:
        prompt_placeholder = file.read()
        prompt = prompt_placeholder.replace("<user_entry>", user_entry)
        return prompt
    
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST': 
        user_entry = request.form['user_entry']
        sys_prompt = get_sys_prompt(user_entry)
        messages.append({"role": "system", "content": sys_prompt})
        return render_template('chat.html')
    
    return render_template('index.html')

@app.route('/get', methods=['POST', 'GET'])
def chat():
    input = request.form["msg"]
    return get_response(input)

def get_response(input):
    messages.append({"role": "user", "content": input})

    reply = llm.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7,
    )

    return reply.choices[0].message.content

if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded=True, port=1000)