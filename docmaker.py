import os
import requests

PERPLEXITY_API_TOKEN = os.getenv("PERPLEXITY_API_TOKEN")
GITHUB_REPO_PATH = "."  # Assuming the script is run from the root of the repo


def get_file_structure(repo_path):
    """Generates a string representing the file structure."""
    structure = ""
    for root, dirs, files in os.walk(repo_path):
        level = root.replace(repo_path, "").count(os.sep)
        indent = " " * 4 * (level)
        structure += f"{indent}{os.path.basename(root)}/\n" if dirs else ""
        sub_indent = " " * 4 * (level + 1)
        for f in files:
            structure += f"{sub_indent}{f}\n"
    return structure


def get_code_content(repo_path):
    """Generates a string of the code content."""
    code_content = ""
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r") as f:
                    code_content += f"\n\n--- {filepath} ---\n\n" + f.read()
    return code_content


def generate_mermaid_diagrams(file_structure, code_content):
    """Generates Mermaid diagrams using Perplexity API."""

    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_TOKEN}",
        "Content-Type": "application/json",
    }

    # Project Structure Diagram
    structure_prompt = f"""
    Generate a simple Mermaid diagram representing the following project structure:

    {file_structure}

    Use a simple tree or flowchart representation.
    """

    structure_payload = {
        "model": "sonar",
        "messages": [{"role": "user", "content": structure_prompt}],
    }

    structure_response = requests.post(
        "https://api.perplexity.ai/chat/completions",
        headers=headers,
        json=structure_payload,
    ).json()

    structure_mermaid = structure_response["choices"][0]["message"]["content"]

    # Code Architecture Diagram
    architecture_prompt = f"""
    Generate a simple Mermaid diagram representing the code architecture based on the following code:

    {code_content}

    Focus on the main modules and their relationships. Use a simple flowchart or sequence diagram.
    """

    architecture_payload = {
        "model": "sonar",
        "messages": [{"role": "user", "content": architecture_prompt}],
    }

    architecture_response = requests.post(
        "https://api.perplexity.ai/chat/completions",
        headers=headers,
        json=architecture_payload,
    ).json()

    architecture_mermaid = architecture_response["choices"][0]["message"]["content"]

    return structure_mermaid, architecture_mermaid


if __name__ == "__main__":
    file_structure = get_file_structure(GITHUB_REPO_PATH)
    code_content = get_code_content(GITHUB_REPO_PATH)
    structure_diagram, architecture_diagram = generate_mermaid_diagrams(
        file_structure, code_content
    )

    print("Project Structure Diagram:\n")
    print(structure_diagram)
    print("\nCode Architecture Diagram:\n")
    print(architecture_diagram)
