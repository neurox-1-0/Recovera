import os
import json

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class LLMService:


    def __init__(self):

        api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        self.client = OpenAI(
            api_key=api_key
        )


    def generate(
        self,
        prompt: str
    ):

        response = self.client.chat.completions.create(

            model="gpt-4.1-mini",

            response_format={
                "type": "json_object"
            },

            messages=[

                {
                    "role": "system",
                    "content":
                    """
                    You are RECOVERA AI,
                    an enterprise SLA recovery analyst.

                    Analyse the investigation evidence.

                    Return ONLY valid JSON.

                    Required structure:

                    {
                      "executive_summary": "",
                      "root_cause_analysis": "",
                      "evidence_analysis": [],
                      "recovery_justification": "",
                      "recommended_actions": [],
                      "risk_assessment": ""
                    }

                    Do not add markdown.
                    """
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.2
        )


        content = (
            response
            .choices[0]
            .message
            .content
        )


        return json.loads(content)