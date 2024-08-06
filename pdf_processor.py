import os
import openai
import PyPDF2
import re
from typing import List, Dict, Any

OPENAI_API_KEY = "api_key_placeholder"

def setup_openai_api() -> None:
    """Set up the OpenAI API key."""
    if OPENAI_API_KEY.startswith("sk-") and len(OPENAI_API_KEY) > 20:
        openai.api_key = OPENAI_API_KEY
    else:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            api_key = input("Please enter your OpenAI API key: ").strip()
            if not api_key:
                raise ValueError("API key is required to run this script.")
        os.environ['OPENAI_API_KEY'] = api_key
        openai.api_key = api_key

def read_pdf(file_path: str) -> str:
    """Read the contents of a PDF file."""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def create_messages(system_content: str, user_content: str) -> List[Dict[str, Any]]:
    """Create a list of messages for the OpenAI Chat API."""
    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content}
    ]

def get_ai_response(messages: List[Dict[str, Any]]) -> str:
    """Get a response from the OpenAI Chat API using GPT-4."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-0125-preview",  #This GPT-4 Turbo
            messages=messages
        )
        return response.choices[0].message['content'].strip()
    except openai.error.AuthenticationError:
        print("Authentication error: Your API key may be invalid or expired.")
        return "I'm sorry, there was an authentication error. Please check your API key."
    except openai.error.RateLimitError:
        print("Rate limit exceeded: Please try again later.")
        return "I'm sorry, the rate limit has been exceeded. Please try again later."
    except Exception as e:
        print(f"An error occurred: {e}")
        return "I'm sorry, I encountered an error while processing your request."

def extract_data_from_pdf(pdf_text: str, data_fields: List[str]) -> Dict[str, str]:
    """Extract specific data from PDF text using GPT-4."""
    system_message = """You are an AI assistant tasked with extracting specific information from PDF text. 
    Please extract the requested information and format your response as a Python dictionary."""

    user_message = f"""Please extract the following information from the given PDF text:
    {', '.join(data_fields)}

    PDF Text:
    {pdf_text[:4000]}  # Limiting to first 4000 characters to avoid token limit

    Format your response as a Python dictionary with the field names as keys and the extracted information as values.
    If a piece of information is not found, use "N/A" as the value."""

    messages = create_messages(system_message, user_message)
    ai_response = get_ai_response(messages)
    
    # Use regex to extract the dictionary from the AI's response
    dict_match = re.search(r'\{.*?\}', ai_response, re.DOTALL)
    if dict_match:
        # Using eval to convert the string representation of the dictionary to an actual dictionary
        extracted_data = eval(dict_match.group())
    else:
        extracted_data = {field: "N/A" for field in data_fields}
    
    return extracted_data