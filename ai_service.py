import os
from dotenv import load_dotenv
from google import genai


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)



def get_health_prediction(glucose, hemoglobin, cholesterol):


    prompt = f"""

You are a healthcare AI assistant.

Analyze these patient blood test values:

Glucose: {glucose} mg/dL

Hemoglobin: {hemoglobin} g/dL

Cholesterol: {cholesterol} mg/dL


Provide response in this format:

Risk Level:
(Low Risk / Medium Risk / High Risk)

Remarks:
Give a short health recommendation.

Important:
This is only a risk assessment and not a medical diagnosis.

"""


    response = client.models.generate_content(

        model="gemini-3.1-flash-lite",

        contents=prompt

    )


    return response.text