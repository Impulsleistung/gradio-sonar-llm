import gradio as gr
import requests
import os
from dotenv import load_dotenv

load_dotenv()

PERPLEXITY_API_TOKEN = os.getenv("PERPLEXITY_API_TOKEN")
PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"


def generate_response(prompt):
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {PERPLEXITY_API_TOKEN}",
        "content-type": "application/json",
    }
    payload = {
        "model": "sonar",
        "messages": [{"role": "user", "content": prompt}],
    }
    try:
        response = requests.post(PERPLEXITY_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"
    except (KeyError, IndexError, TypeError) as e:
        return f"Error parsing API response: {e}"


iface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=5, placeholder="Enter your prompt here..."),
    outputs=gr.Textbox(),
    title="Sonar App by Kevin",
    description="Use Sonar to get answers.",
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
