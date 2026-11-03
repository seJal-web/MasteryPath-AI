import os
import json
import time

from google import genai
from dotenv import load_dotenv

load_dotenv()


def generate_ai_questions(text, subject, level, number_of_questions=5):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Gemini API key not found.")
        return []

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
You are an AI quiz generator for MasteryPath AI.

Create exactly {number_of_questions} meaningful multiple-choice questions from the study material.

Student information:
Subject: {subject}
Knowledge Level: {level}

Rules:
1. Use ONLY the study material.
2. Create exactly {number_of_questions} questions.
3. Each question must have exactly 4 options.
4. Only ONE option can be correct.
5. Options must be distinct and plausible.
6. Questions must test understanding, not just copy a sentence.
7. Match the student's knowledge level.
8. Mix conceptual understanding and application where the source supports it.
9. Give the topic tested by each question.
10. Return ONLY valid JSON.
11. Do not use markdown.

Use exactly this structure:
[
    {{
        "question": "Question text",
        "options": ["Option A", "Option B", "Option C", "Option D"],
        "answer": "Option A",
        "topic": "Concept name",
        "difficulty": "Easy"
    }}
]

Study Material:
{text[:15000]}
"""

        models = [
            "gemini-3.8-flash",
            "gemini-3.7-flash"
        ]

        result = None

        for model in models:
            for attempt in range(2):
                try:
                    print(f"Trying quiz model: {model} (attempt {attempt + 1})")
                    response = client.models.generate_content(
                        model=model,
                        contents=prompt
                    )

                    if response and response.text:
                        result = response.text.strip()
                        print(f"Quiz generated successfully using {model}")
                        break

                except Exception as e:
                    print(f"Quiz error with {model}: {repr(e)}")
                    time.sleep(3)

            if result:
                break

        if not result:
            return []

        if result.startswith("```"):
            result = result.replace("```json", "")
            result = result.replace("```", "")
            result = result.strip()

        questions = json.loads(result)

        if not isinstance(questions, list):
            return []

        valid_questions = []

        for question in questions:
            if not isinstance(question, dict):
                continue

            required = [
                "question",
                "options",
                "answer",
                "topic",
                "difficulty"
            ]

            if not all(field in question for field in required):
                continue

            if not isinstance(question["options"], list):
                continue

            if len(question["options"]) != 4:
                continue

            if len(set(question["options"])) != 4:
                continue

            if question["answer"] not in question["options"]:
                continue

            valid_questions.append(question)

        return valid_questions[:number_of_questions]

    except json.JSONDecodeError as e:
        print("Quiz JSON parsing error:", repr(e))
        return []

    except Exception as e:
        print("Quiz generation error:", repr(e))
        return []
