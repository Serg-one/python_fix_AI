from dotenv.main import load_dotenv
import os

import openai
from flask import Flask, request, render_template
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

# Set your OpenAI API key
load_dotenv()
openai.api_key = os.getenv("API_KEY")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/fix-debug", methods=["POST"])
def fix_debug():
    # Get the code from the request body
    code = request.form.get("code")

    # Use OpenAI to fix and debug the code
    model_engine = "text-davinci-003"
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

    # Highlight the input and output code using Pygments
    input_code_highlighted = highlight(code, PythonLexer(), HtmlFormatter(linenos=True, style="github-dark"))
    fixed_code_highlighted = highlight(fixed_code, PythonLexer(), HtmlFormatter(linenos=True, style="github-dark"))

    # Get the CSS style definitions for the highlighted code
    # css_style_defs = HtmlFormatter(style="github-dark").get_style_defs(".highlight")

    # Return the fixed and debugged code in the response
    return render_template(
        "output.html",
        input_code=input_code_highlighted,
        fixed_code=fixed_code_highlighted
    )


@app.route("/chat")
def chat():
    return render_template("chat.html")

# Define route function for handling chat requests
@app.route("/chat", methods=["POST"])
def chatbot():
    # Get user message from request form
    message = request.form.get("message")

    # Call OpenAI API to generate response
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Conversation with user:\nUser: {message}\nAI:",
        temperature=0.7,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Get response text from OpenAI API
    bot_message = response.choices[0].text.strip()

    # Render chat template with user message and chatbot response
    return render_template("chat.html", message=message, bot_message=bot_message)


if __name__ == "__main__":
    app.run(debug=True)
