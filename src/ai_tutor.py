import os
import json
import time

from google import genai
from dotenv import load_dotenv

load_dotenv()


def generate_with_gemini(prompt):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("Gemini API key not found.")
        return None

    try:
        client = genai.Client(api_key=api_key)
        models = ["gemini-3.6-flash", "gemini-3.7-flash"]

        for model in models:
            for attempt in range(2):
                try:
                    print(f"Trying Gemini model: {model} (attempt {attempt + 1})")
                    response = client.models.generate_content(
                        model=model,
                        contents=prompt
                    )

                    if response and response.text:
                        return response.text.strip()

                except Exception as e:
                    print(f"Gemini error with {model}: {repr(e)}")
                    time.sleep(3)

        return None

    except Exception as e:
        print("Gemini client error:", repr(e))
        return None


def clean_json_response(result):
    if not result:
        return None

    result = result.strip()

    if result.startswith("```"):
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

    return result


def generate_lesson(text, subject, level):
    prompt = f"""
You are an educational tutor for MasteryPath AI.

Teach the student the following study material.

Subject: {subject}
Knowledge Level: {level}

Create a simple, structured lesson with:
1. A clear title
2. A short overview
3. 3 to 5 learning objectives
4. A simple explanation
5. 2 to 3 real-world examples
6. 5 to 7 key points
7. 3 to 5 common mistakes
8. 5 important concepts

Rules:
- Use simple student-friendly language.
- Explain concepts instead of copying the material.
- Use examples where useful.
- Stay grounded in the study material.
- Do not make the lesson unnecessarily long.

Return ONLY valid JSON using this format:
{{
    "title": "Lesson title",
    "overview": "Short overview",
    "learning_objectives": ["Objective 1", "Objective 2", "Objective 3"],
    "explanation": "Simple explanation",
    "examples": [
        {{"title": "Example title", "example": "Example explanation", "why_it_matters": "Why this example is useful"}}
    ],
    "key_points": ["Key point 1", "Key point 2", "Key point 3"],
    "common_mistakes": ["Common mistake 1", "Common mistake 2"],
    "important_concepts": ["Concept 1", "Concept 2", "Concept 3"]
}}

Study Material:
{text[:15000]}
"""

    result = generate_with_gemini(prompt)

    if not result:
        return {}

    try:
        lesson = json.loads(clean_json_response(result))
        return lesson if isinstance(lesson, dict) else {}
    except Exception as e:
        print("Lesson JSON error:", repr(e))
        return {}


def generate_weak_topic_review(text, weak_topics, subject, level):
    if not weak_topics:
        return {}

    topics = ", ".join(weak_topics)

    prompt = f"""
You are an adaptive learning tutor for MasteryPath AI.

Subject: {subject}
Knowledge Level: {level}
Weak concepts: {topics}

Create a short targeted review ONLY for these weak concepts.
Use only information supported by the study material.
Explain simply, give examples, mention common mistakes, and include a few quick practice questions.

Return ONLY valid JSON:
{{
    "title": "Targeted Review",
    "intro": "Short explanation",
    "weak_concepts": [
        {{
            "concept": "Concept name",
            "explanation": "Simple explanation",
            "example": "Simple example",
            "common_mistake": "Common mistake"
        }}
    ],
    "key_points": ["Important point 1", "Important point 2", "Important point 3"],
    "practice_questions": [
        {{"question": "Practice question", "answer": "Short answer"}}
    ]
}}

Study Material:
{text[:15000]}
"""

    result = generate_with_gemini(prompt)

    if not result:
        return {}

    try:
        review = json.loads(clean_json_response(result))
        return review if isinstance(review, dict) else {}
    except Exception as e:
        print("Weak topic review JSON error:", repr(e))
        return {}