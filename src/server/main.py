import openai
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder="../frontend", static_folder="../static")
CORS(app)

separator = "----------"


@app.route("/")
def get_home_page():
    return render_template("index.html")


@app.route("/get_grade", methods=["POST"])
def get_grade():
    try:
        setup_gpt_api()
        data = request.get_json()
        context = data.get("context", None)
        code = data.get("code", None)
        if not context or not code:
            return jsonify({"error": "context or code were missing"}), 400

        return jsonify(get_grade(context, code))

    except Exception as e:
        print("failed", e)
        return jsonify({"error": str(e)}), 500


def parse_grade(raw_text):
    split_text = raw_text.split(separator)

    if len(split_text) != 2:
        return {"grade": "ERROR", "explanation": "ERROR"}

    grade, explanation = split_text
    return {"grade": grade, "explanation": explanation}


def setup_gpt_api():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    openai.api_key = api_key


def get_grade(context: str, code: str):
    ai_instructions = """
        Grade my code and provide feedback. First provide the letter grade, with A+ being the highest grade and F being the lowest grade.
        Then add a separator "${0}". 
        After the separator, provide the explanation for the grade.

        Use the following context in your grading:

        ${1}

        
    """.format(
        separator, context
    )

    messages = [
        {
            "role": "system",
            "content": ai_instructions,
        },
        {
            "role": "user",
            "content": "Grade this code: \n\n " + code,
        },
    ]

    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    return parse_grade(chat.choices[0].message.content)


if __name__ == "__main__":
    app.run()
