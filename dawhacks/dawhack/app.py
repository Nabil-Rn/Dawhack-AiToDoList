from flask import Flask, render_template, request
from openai import OpenAI

client = OpenAI(api_key="erm")
app = Flask(__name__)

@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("index.html")
@app.route("/list", methods=['GET', 'POST'])
def list():
    if request.method == 'POST':
        input_value = request.form.get("input")
        if input_value and input_value.strip():
            try:
                list_content = loadNewList(input_value)
                return render_template("list.html", list_content=list_content)
            except Exception as e:
                error_message = f"Error: {str(e)}"
                return render_template("error.html", error_message=error_message)

def loadNewList(list_text):
    response = client.chat.completions.create(
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