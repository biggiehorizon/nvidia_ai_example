# NVIDIA API Chat Interface

A Python application that provides an interactive command-line interface for the NVIDIA API, allowing you to send prompts to AI models like qwen3-next-80b-a3b-instruct and receive responses in real-time.

## Features

- Interactive command-line chat interface
- Streaming responses for real-time feedback
- Support for command-line arguments to customize behavior
- Secure API key management via environment variables
- Configurable parameters (temperature, top_p, max_tokens)

## Prerequisites

- Python 3.6 or higher
- A virtual environment (recommended)
- NVIDIA API key

## Installation

1. **Clone or download this repository**

2. **Set up a virtual environment** (recommended)

   ```powershell
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment (Windows PowerShell)
   .\venv\Scripts\Activate.ps1
   
   # Activate virtual environment (Windows Command Prompt)
   # .\venv\Scripts\activate.bat
   
   # Activate virtual environment (Linux/Mac)
   # source venv/bin/activate
   ```

3. **Install the required packages**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Set up your API key**

   Create a `.env` file in the root directory and add your NVIDIA API key:

   ```
   NVIDIA_API_KEY="your-api-key-here"
   ```

## Usage

### Interactive Mode

Run the application without any arguments to enter interactive mode:

```powershell
python app.py
```

In this mode, you'll be prompted to enter your queries. Type `exit` or `quit` to end the session.

### Command Line Arguments

You can also use command line arguments to customize the behavior:

```powershell
python app.py --prompt "What is quantum computing?"
```

#### Available Arguments

- `--prompt`: The prompt to send (if omitted, enters interactive mode)
- `--model`: The model to use (default: "qwen/qwen3-next-80b-a3b-instruct")
- `--temperature`: Controls randomness (0.0-1.0, default: 0.6)
- `--top_p`: Controls diversity (0.0-1.0, default: 0.7)
- `--max_tokens`: Maximum length of the generated response (default: 4096)

### Examples

1. **Basic usage with a specific prompt**:
   ```powershell
   python app.py --prompt "Explain machine learning in simple terms"
   ```

2. **Using a different model with custom parameters**:
   ```powershell
   python app.py --prompt "Write a poem about space" --temperature 0.9 --max_tokens 2048
   ```

3. **Interactive mode with custom model**:
   ```powershell
   python app.py --model "alternative/model-name" 
   ```

## Troubleshooting

- **API Key Issues**: Make sure your API key is correctly set in the `.env` file or provided as an environment variable.
- **Model Availability**: Not all models may be available through the API. Check NVIDIA's documentation for available models.
- **Rate Limits**: Be aware of any rate limits that may apply to your API key.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NVIDIA for providing the API
- OpenAI for the client library used to interface with the API