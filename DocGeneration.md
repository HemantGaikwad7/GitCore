# doc_generator.py - AI-Powered Documentation Generator

An intelligent documentation generator that uses Google's Gemini AI to automatically create comprehensive Markdown documentation for Python projects.

## Features

- **Automatic Code Analysis**: Analyzes Python source files and generates detailed documentation
- **Git Integration**: Automatically detects modified files using `git diff`
- **Smart File Discovery**: Falls back to scanning all Python files if no Git changes detected
- **Project-Level Summary**: Generates high-level architecture overviews
- **Markdown Output**: Creates clean, professional Markdown documentation
- **Batch Processing**: Handles multiple files in a single run

## Prerequisites

- Python 3.7+
- Google Gemini API key
- Git (optional, for change detection)

## Installation

1. **Install Required Packages**:
```bash
pip install google-generativeai
```

2. **Get a Gemini API Key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Replace `"apikey"` in the script with your actual key

3. **Configure the Script**:
```python
GENAI_API_KEY = "your-actual-api-key-here"
MODEL_NAME = "models/gemini-2.0-flash"  # Or your preferred model
```

## Usage

### Basic Usage
```bash
python doc_generator.py
```

### How It Works

1. **File Detection**: 
   - First tries to use `git diff --name-only` to find modified Python files
   - If no Git repository or changes found, scans all `.py` files in the project

2. **Documentation Generation**:
   - Analyzes each Python file using Gemini AI
   - Generates comprehensive Markdown documentation
   - Saves documentation to `output/` directory with same structure as source

3. **Project Summary**:
   - Creates a high-level architecture summary in `output/summary.md`
   - Shows how different components interact
   - Provides project structure overview

## Output Structure

```
output/
├── summary.md              # High-level project overview
├── git.py.md              # Documentation for git.py
├── doc_generator.py.md    # Documentation for doc_generator.py
└── [other-files].md       # Documentation for other Python files
```

## Configuration Options

### API Configuration
```python
GENAI_API_KEY = "your-api-key"     # Your Gemini API key
MODEL_NAME = "models/gemini-2.0-flash"  # Gemini model to use
```

### Path Configuration
```python
PROJECT_ROOT = Path(__file__).parent  # Project root directory
OUTPUT_DIR = PROJECT_ROOT / "output"  # Output directory for docs
```

## Features in Detail

### Git Integration
- Automatically detects modified files using Git
- Only documents changed files for efficiency
- Falls back to full project scan if Git is unavailable

### AI-Powered Analysis
- Uses Google's Gemini AI for intelligent code analysis
- Generates context-aware documentation
- Explains complex code patterns and architecture decisions

### Smart File Filtering
- Excludes the documentation generator itself
- Skips files in the output directory
- Focuses on Python source files only

### Batch Processing
- Processes multiple files efficiently
- Maintains project context across files
- Generates coherent project-wide documentation

## Example Output

The generator creates documentation that includes:

- **Module Purpose**: Clear explanation of what each file does
- **Key Functions/Classes**: Detailed breakdown of important components
- **Usage Examples**: How to use the code
- **Architecture Notes**: How the component fits into the larger project
- **Dependencies**: What the code relies on
- **Technical Details**: Implementation specifics

## Customization

### Modify the Documentation Prompt
```python
def generate_doc_for_file(file_path, content):
    prompt = f"""Your custom prompt here...
    
Code:
```python
{content}
```"""
    response = model.generate_content(prompt)
    return response.text
```

### Change Output Format
The script can be easily modified to generate different output formats by changing the file extension and prompt instructions.

### Add More File Types
Extend the file collection logic to include other programming languages:
```python
def collect_all_code_files():
    extensions = ["*.py", "*.js", "*.java", "*.cpp"]
    files = []
    for ext in extensions:
        files.extend(PROJECT_ROOT.rglob(ext))
    return files
```

## Error Handling

The script includes error handling for:
- Missing or invalid API keys
- Git command failures
- File I/O errors
- API rate limiting
- Malformed Python files

## Best Practices

1. **API Key Security**: Store your API key in environment variables
2. **Rate Limiting**: Be mindful of API usage limits
3. **Review Output**: Always review generated documentation for accuracy
4. **Version Control**: Consider versioning your generated documentation
5. **Incremental Updates**: Use Git integration for efficient updates

## Limitations

- **API Dependency**: Requires internet connection and valid Gemini API key
- **Python Focus**: Currently optimized for Python projects
- **Rate Limits**: Subject to Google's API rate limiting
- **Cost**: API usage may incur costs depending on your plan
- **Accuracy**: AI-generated content should be reviewed for accuracy

## Troubleshooting

### Common Issues

**API Key Error**:
```
Make sure GENAI_API_KEY is set to your actual API key
```

**Git Not Found**:
```
The script will automatically fall back to scanning all files
```

**Permission Errors**:
```
Ensure the script has write permissions for the output directory
```

## Integration Ideas

- **CI/CD Pipeline**: Integrate into build process for automatic documentation updates
- **Pre-commit Hooks**: Generate docs automatically before commits
- **Documentation Website**: Use output to build documentation sites
- **Code Review**: Include generated docs in pull request reviews

## License

This tool is designed for educational and productivity purposes. Ensure compliance with Google's Gemini API terms of service.
