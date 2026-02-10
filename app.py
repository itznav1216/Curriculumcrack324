from flask import Flask, render_template, request
from openai import OpenAI
import os

app = Flask(__name__)

# Groq OpenAI-compatible client
client = OpenAI(
    api_key="",
    base_url="https://api.groq.com/openai/v1"
)

def generate_curriculum(skill, level, semesters, industry):
    prompt = f"""
You are a senior academic curriculum designer.

Create a semester-wise curriculum for the following details:

Skill: {skill}
Level: {level}
Number of Semesters: {semesters}
Industry Focus: {industry}

For each semester provide:
- Semester title
- Key subjects
- Learning outcomes
- Industry relevance

Make it concise, structured, and professional.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an expert curriculum designer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content


@app.route("/", methods=["GET", "POST"])
def index():
    curriculum = None
    error = None

    if request.method == "POST":
        try:
            skill = request.form["skill"]
            level = request.form["level"]
            semesters = request.form["semesters"]
            industry = request.form["industry"]

            curriculum = generate_curriculum(skill, level, semesters, industry)

        except Exception as e:
            error = str(e)

    return render_template("index.html", curriculum=curriculum, error=error)


if __name__ == "__main__":
    app.run(debug=True)
