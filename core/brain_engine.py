import os
from openai import AzureOpenAI

class BrainEngine:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version="2024-02-15-preview"
        )
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

    def translate_to_english(self, text):
        try:
            res = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[{"role": "user", "content": f"Translate to English: {text}"}]
            )
            return res.choices[0].message.content
        except Exception as e:
            print(f" Translation error: {e}")
            return text  # fallback

    def translate_back(self, text, target_lang):
        try:
            res = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[{"role": "user", "content": f"Translate to {target_lang}: {text}"}]
            )
            return res.choices[0].message.content
        except Exception as e:
            print(f" Reverse translation error: {e}")
            return text  # fallback

    def get_answer(self, english_query, context):
        prompt = f"You are a Bravado Support Agent. Context: {context}. Reply concisely and clearly in English."
        try:
            res = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[{"role": "system", "content": prompt},
                          {"role": "user", "content": english_query}]
            )
            return res.choices[0].message.content
        except Exception as e:
            print(f" OpenAI error: {e}")
            return "Sorry, I could not process your request at the moment."