import os
import requests

PERPLEXITY_API_TOKEN = os.getenv("PERPLEXITY_API_TOKEN")
GITHUB_REPO_PATH = "."  # Assuming the script is run from the root of the repo


def get_file_structure(repo_path):
    """Generates a string representing the file structure."""
    structure = ""
    for root, dirs, files in os.walk(repo_path):
        # Exclude directories starting with '.'
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        level = root.replace(repo_path, "").count(os.sep)
        indent = " " * 4 * (level)
        structure += f"{indent}{os.path.basename(root)}/\n" if dirs else ""
        sub_indent = " " * 4 * (level + 1)
        for f in files:
            # Exclude files starting with '.' and 'docmaker.py'
            if not f.startswith(".") and f != "docmaker_mmd.py":
                structure += f"{sub_indent}{f}\n"
    return structure


def get_code_content(repo_path):
    """Generates a string of the code content."""
    code_content = ""
    for root, dirs, files in os.walk(repo_path):
        # Exclude directories starting with '.'
        dirs[:] = [d for d in dirs if not d.startswith(".")]

        for file in files:
            # Exclude files starting with '.' and 'docmaker.py'
            if (
                file.endswith(".py")
                and not file.startswith(".")
                and file != "docmaker_mmd.py"
            ):
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

    # Code Architecture Diagram
    architecture_prompt = f"""
    Generate a Mermaid diagram representing the code architecture based on the following code:
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

    return architecture_mermaid


if __name__ == "__main__":
    file_structure = get_file_structure(GITHUB_REPO_PATH)
    code_content = get_code_content(GITHUB_REPO_PATH)
    architecture_diagram = generate_mermaid_diagrams(file_structure, code_content)

    print("\nCode Architecture Diagram:\n")
    print(architecture_diagram)
