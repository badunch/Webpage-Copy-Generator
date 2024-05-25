import os
import time
import re
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, Any, List
import google.generativeai as genai
from google.api_core import exceptions, retry

# Load environment variables from .env file
load_dotenv()

# Configure the API key from the environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("API key not found. Ensure that the .env file contains the 'GOOGLE_API_KEY' variable.")
genai.configure(api_key=GOOGLE_API_KEY)

# Define the models with descriptions
MODELS: Dict[str, Dict[str, Any]] = {
    "gemini-1.5-flash-latest": {
        "model": genai.GenerativeModel("gemini-1.5-flash-latest"),
        "description": "Powerful model capable of handling text and image inputs, optimized for various language tasks like code generation, text editing, and problem solving.",
        "rate_limit": (15, 60),  # 2 queries per minute
        "daily_limit": 1000,
    },
    "gemini-1.0-pro-latest": {
        "model": genai.GenerativeModel("gemini-1.0-pro-latest"),
        "description": "Versatile model for text generation and multi-turn conversations, suitable for zero-shot, one-shot, and few-shot tasks.",
        "rate_limit": (60, 60),  # 60 queries per minute
    },
    "gemini-1.5-pro-latest": {
        "model": genai.GenerativeModel("gemini-1.5-pro-latest"),
        "description": "Versatile model for text generation and multi-turn conversations, suitable for zero-shot, one-shot, and few-shot tasks.",
        "rate_limit": (2, 60),  # 60 queries per minute
    },
}

@retry.Retry(
    initial=0.1,
    maximum=60.0,
    multiplier=2.0,
    deadline=600.0,
    exceptions=(exceptions.GoogleAPICallError,),
)
def generate_with_retry(model: genai.GenerativeModel, prompt: str) -> Any:
    try:
        return model.generate_content(prompt)
    except exceptions.InvalidArgument as e:
        raise ValueError(f"Invalid input provided: {e}")
    except exceptions.DeadlineExceeded as e:
        raise exceptions.DeadlineExceeded(f"Deadline exceeded while generating content: {e}")
    except exceptions.ResourceExhausted as e:
        raise exceptions.ResourceExhausted(f"Resource exhausted (quota limit reached): {e}")

def sanitize_title(title: str) -> str:
    sanitized_title = re.sub(r"[^\w\-_\. ]", "_", title)
    return sanitized_title[:100]

def extract_text(response: Any) -> str:
    for part in response.parts:
        if hasattr(part, "text"):
            return part.text
    return ""

def create_copy_directory() -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    copy_dir = f"web_copy_{timestamp}"
    os.makedirs(copy_dir, exist_ok=True)
    return copy_dir

def generate_copy_prompt(draft: str, page_name: str) -> str:
    return (
        f"Generate detailed and engaging copy for a webpage titled '{page_name}'. "
        f"Here is the text generated so far:\n\n"
        f"{draft}\n"
    )

def ask_user_for_page_names() -> List[str]:
    page_names = input("Enter the names of the webpages you need copy for, separated by commas: ").strip().split(',')
    return [name.strip() for name in page_names]

def write_copy(model_name: str, page_names: List[str]) -> None:
    model_config = MODELS[model_name]
    model = model_config["model"]
    rate_limit = model_config.get("rate_limit")
    daily_limit = model_config.get("daily_limit")

    # Create a directory for the copy
    copy_dir = create_copy_directory()

    query_count = 0
    max_iterations = 150

    for i, page_name in enumerate(page_names):
        print(f"Generating copy for page '{page_name}' ({i + 1} out of {len(page_names)})...")
        if query_count >= max_iterations:
            break

        # Generate copy for each page
        copy_prompt = generate_copy_prompt("", page_name)
        continuation = extract_text(generate_with_retry(model, copy_prompt))
        
        # Save each page's copy
        page_filename = f"{copy_dir}/{sanitize_title(page_name)}.txt"
        with open(page_filename, "w", encoding="utf-8") as file:
            file.write(continuation)

        query_count += 1

        if rate_limit and query_count % rate_limit[0] == 0:
            time.sleep(rate_limit[1])

        if daily_limit and query_count >= daily_limit:
            print("Daily query limit reached. Please try again tomorrow.")
            break

    print(f"Copy for the pages has been saved in the directory '{copy_dir}'.")

def select_model() -> str:
    print("Available models:")
    for i, (model_name, model_info) in enumerate(MODELS.items(), start=1):
        print(f"{i}. {model_name} - {model_info['description']}")

    while True:
        try:
            choice = int(input("Enter the number corresponding to the model you want to use: "))
            if 1 <= choice <= len(MODELS):
                return list(MODELS.keys())[choice - 1]
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    selected_model = select_model()
    page_names = ask_user_for_page_names()
    write_copy(selected_model, page_names)
