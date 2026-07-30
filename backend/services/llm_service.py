import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class LLMService:


    def __init__(self):

        api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        if not api_key:
            raise Exception(
                "OPENAI_API_KEY missing"
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

            messages=[

                {
                    "role": "system",
                    "content":
                    """
                    You are RECOVERA AI.

                    You are an expert SLA
                    contract recovery analyst.

                    Analyse evidence from:
                    - contracts
                    - monitoring logs
                    - incidents
                    - emails
                    - invoices

                    Generate:
                    1. Executive summary
                    2. Root cause analysis
                    3. Recovery justification
                    4. Recommended action
                    """
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0.2
        )


        return (
            response
            .choices[0]
            .message
            .content
        )