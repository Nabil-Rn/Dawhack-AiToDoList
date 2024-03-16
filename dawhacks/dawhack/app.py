from flask import Flask, render_template, request
from openai import OpenAI
# sk-pN7LxK7bSd6dlAR0vJhYT3Bl
client = OpenAI(api_key="bkFJaFcwObEpyhf8kAdQGrN7")
app = Flask(__name__)

@app.route("/")
@app.route("/home", methods=('GET', 'POST'))
def home():
    return render_template("index.html")
    
@app.route("/list.html", methods=('GET', 'POST'))
def list():
    input_value = request.args.get("input")
    print(input_value)
    list_content = loadNewList(input_value)
    
    content = render_template("list.html") + list_content + "</div></body></html>"
    return content

def loadNewList(list_text):
    response = client.chat.completions.create(
        temperature=0,
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are supplying HTML code. Please only write in code, and without line breaks, or else our app will break."},
            {"role": "assistant", "content": "You are being fed a CSV of to-do list elements. Add details and sublists to each list element. Please respond only as an HTML unorganized list, each item having 3 sublists."},
            {"role": "user", "content": list_text}
        ]
    )
    return response.choices[0].message.content

if __name__ == '__main__': 
    app.run(port=5002)