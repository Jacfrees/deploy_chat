import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def get_gemini_response(prompt: str) -> str:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="Vas a ayudar a un usuario con las dudas que tenga sobre un proyecto,"
                           " respondelas de la mejor manera posible, usa emojis segun lo creas conveniente.")
    try:
        response = model.generate_content(prompt,
                                          generation_config=genai.types.GenerationConfig(
                                              candidate_count=1,
                                              max_output_tokens=200,
                                              temperature=1.0
                                          ),)
        #print(response.text)
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        return ""

