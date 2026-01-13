import requests
import json

GEMINI_KEY = "AIzaSyAXMoNXcR1JthKt2g3OSEI3xMj6NYlzXs4"

URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=" + GEMINI_KEY

headers = {
    "Content-Type": "application/json"
}
def get_ai_response(question):
    """
    This function sends the user's question to Gemini
    and returns the AI's reply.

    It supports:
    - Normal Q&A
    - Notes mode  (notes: topic)
    - Quiz mode   (quiz: topic)
    """

    # Convert question to lowercase for checking mode
    lower_q = question.lower()

    # ----- NOTES MODE -----
    if lower_q.startswith("notes:"):
        topic = question.replace("notes:", "").strip()

        final_prompt = (
            "Create short, clear, exam-ready notes in bullet points on this topic:\n"
            + topic
        )

    # ----- QUIZ MODE -----
    elif lower_q.startswith("quiz:"):
        topic = question.replace("quiz:", "").strip()

        final_prompt = (
             "Create 5 multiple choice questions (MCQs) in the following strict format:\n\n"
             "Q1. Question text\n"
             "A) Option\n"
              "B) Option\n"
              "C) Option\n"
             "D) Option\n"
             "Correct Answer: X\n\n"
             "Repeat this format for all questions.\n\n"
             "Topic:\n" + topic
    )

    


    # ----- NORMAL MODE -----
    else:
        final_prompt = question

    # Data format required by Gemini API
    data = {
        "contents": [
            {
                "parts": [
                    {"text": final_prompt}
                ]
            }
        ]
    }

    # Send request to Gemini
    response = requests.post(URL, headers=headers, data=json.dumps(data))
    result = response.json()

    # Extract and return AI text
    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "Gemini error: " + str(result)
