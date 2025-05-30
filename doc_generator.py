import os
import openai
import google.generativeai as genai
from pathlib import Path
import subprocess

# === CONFIGURATION ===
GENAI_API_KEY = "apikey"  # Replace with your actual Gemini API key
MODEL_NAME = "models/gemini-2.0-flash"
PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "output"

# === INIT GOOGLE GEMINI ===
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# === UTILITY FUNCTIONS ===

def get_git_modified_files():
    try:
        result = subprocess.run(['git', 'diff', '--name-only'], stdout=subprocess.PIPE, text=True, check=True)
        changed_files = result.stdout.strip().split('\n')
        return [f for f in changed_files if f.endswith('.py')]
    except Exception:
        return []

def read_file_content(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def generate_doc_for_file(file_path, content):
    prompt = f"""You are an expert Python code documenter.
Analyze the following Python code and generate a clear, professional Markdown documentation for it.
Include description of the module's purpose, its key functions/classes, and how it fits into a larger project.

Code:
```python
{content}
```"""
    response = model.generate_content(prompt)
    return response.text

def write_doc(file_path, doc_content):
    rel_path = file_path.relative_to(PROJECT_ROOT)
    output_file = OUTPUT_DIR / rel_path.with_suffix('.md')
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(doc_content)

def collect_all_code_files():
    return [p for p in PROJECT_ROOT.rglob("*.py") if "output" not in str(p) and p.name != Path(__file__).name]

def summarize_project(all_file_data):
    joined_code = "\n\n".join([f"# File: {str(p)}\n```python\n{c}\n```" for p, c in all_file_data])
    prompt = f"""You are a senior software architect.
You are given multiple Python source files from a project. Please analyze them and provide a **high-level architecture summary** in Markdown.

For each component/file:
- Briefly describe its role.
- Mention how it interacts with others.
- Provide an overview of the structure (e.g., modules, flow, design choices).

Files:
{joined_code}
"""
    response = model.generate_content(prompt)
    summary_file = OUTPUT_DIR / "summary.md"
    summary_file.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(response.text)

# === MAIN LOGIC ===

def main():
    print("🔍 Collecting files...")

    changed_files = get_git_modified_files()
    if changed_files:
        print("📄 Using git diff to find modified files.")
        code_files = [PROJECT_ROOT / f for f in changed_files if (PROJECT_ROOT / f).exists()]
    else:
        print("📁 No git changes detected, using all files.")
        code_files = collect_all_code_files()

    all_file_data = []

    for file_path in code_files:
        print(f"📘 Documenting: {file_path}")
        content = read_file_content(file_path)
        doc = generate_doc_for_file(file_path, content)
        write_doc(file_path, doc)
        all_file_data.append((file_path, content))

    print("🧠 Generating high-level project summary...")
    summarize_project(all_file_data)

    print(f"✅ Documentation generated in: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
