import openai
from flask import Flask, request, jsonify, render_template

# Set your OpenAI API key
openai.api_key = "YOUR_API_KEY_HERE"

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/fix-debug", methods=["POST"])
def fix_debug():
    # Get the code from the request body
    code = request.form.get("code")

    # Use OpenAI to fix and debug the code
    model_engine = "davinci-codex"
    prompt = f"Please fix and debug the following Python code:\n\n{code}\n\nFixed code:"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    fixed_code = response.choices[0].text.strip()

    # Return the fixed and debugged code in the response
    return render_template("index.html", fixed_code=fixed_code)

if __name__ == "__main__":
    app.run(debug=True)
