import sys
from dotenv import load_dotenv
from core.speech_service import SpeechService
from core.brain_engine import BrainEngine
from core.product_retriever import ProductRetriever

# Load environment variables from .env
load_dotenv()

def run():
    # Initialize components
    try:
        speech = SpeechService()
        brain = BrainEngine()
        retriever = ProductRetriever()
    except Exception as e:
        print(f" Initialization Error: {e}")
        return

    print("--- Bravado Solutions: Multilingual Support Ready ---")
    print("Commands: Speak to ask about products, or say 'Exit' to quit.")

    while True:
        try:
            # 1. Listen & Detect Language
            text, lang = speech.listen()
            
            # If no speech detected, loop back to listening
            if not text:
                continue

            # 2. Exit condition
            if "exit" in text.lower():
                print(" Closing session. Thank you for using Bravado Solutions.")
                break

            print(f"\n[Customer ({lang})]: {text}")

            # 3. Step 1: Translate input to English for internal processing (RAG)
            english_query = brain.translate_to_english(text)

            # 4. Step 2: Retrieve context from product catalog using Fuzzy Matching
            context = retriever.get_context(english_query)

            # 5. Step 3: Get the answer from the LLM (Reasoning in English)
            answer_en = brain.get_answer(english_query, context)

            # 6. Step 4: Translate the answer back to the customer's detected language
            answer_final = brain.translate_back(answer_en, lang)

            # 7. Step 5: Speak the final answer back to the customer
            print(f"[Bravado AI ({lang})]: {answer_final}")
            speech.speak(answer_final, lang)

        except KeyboardInterrupt:
            print("\nTerminated by user.")
            break
        except Exception as e:
            print(f" An error occurred during the loop: {e}")
            continue

if __name__ == "__main__":
    run()