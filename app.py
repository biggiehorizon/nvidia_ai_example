from openai import OpenAI
import json
import os
import argparse
import sys
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Available models
AVAILABLE_MODELS = [
    "deepseek-ai/deepseek-v3.1-terminus",
    "qwen/qwen3-next-80b-a3b-instruct"
]

def get_api_key():
    """Get API key from environment variable or prompt user"""
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        # If running interactively, prompt for API key
        if sys.stdin.isatty():
            print("Warning: NVIDIA_API_KEY environment variable not found.")
            api_key = input("Please enter your NVIDIA API key: ")
        else:
            raise ValueError("NVIDIA_API_KEY environment variable is required.")
    return api_key

def display_models():
    """Display available models in numbered alphabetical order"""
    sorted_models = sorted(AVAILABLE_MODELS)
    print("\nAvailable models:")
    print("-" * 80)
    for idx, model in enumerate(sorted_models, 1):
        print(f"{idx}. {model}")
    print("-" * 80)
    return sorted_models

def select_model():
    """Allow user to select a model from the list"""
    sorted_models = display_models()
    
    while True:
        try:
            choice = input("\nEnter model number (or 'cancel' to keep current model): ")
            
            if choice.lower() == 'cancel':
                return None
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(sorted_models):
                selected_model = sorted_models[choice_num - 1]
                print(f"\nSwitched to model: {selected_model}")
                return selected_model
            else:
                print(f"Please enter a number between 1 and {len(sorted_models)}")
        except ValueError:
            print("Invalid input. Please enter a number or 'cancel'")

def generate_response(prompt, model="qwen/qwen3-next-80b-a3b-instruct", temperature=0.6, top_p=0.7, max_tokens=4096):
    """Generate a response from the model"""
    try:
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=get_api_key()
        )
        
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role":"user","content":prompt}],
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            stream=True
        )
        
        print(f"\nResponse to: \"{prompt}\"\n")
        print("-" * 80)
        
        # Stream the response
        for chunk in completion:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        
        print("\n" + "-" * 80)
        
    except Exception as e:
        print(f"Error generating response: {e}")

def main():
    parser = argparse.ArgumentParser(description="Generate text using NVIDIA API")
    parser.add_argument("--model", type=str, default="qwen/qwen3-next-80b-a3b-instruct",
                        help="The model to use")
    parser.add_argument("--temperature", type=float, default=0.6,
                        help="Temperature for sampling (0.0-1.0)")
    parser.add_argument("--top_p", type=float, default=0.7,
                        help="Top-p sampling parameter (0.0-1.0)")
    parser.add_argument("--max_tokens", type=int, default=4096,
                        help="Maximum number of tokens to generate")
    parser.add_argument("--prompt", type=str, 
                        help="Optional prompt to send to the model (if not provided, will prompt user for input)")
                        
    args = parser.parse_args()
    
    # If prompt wasn't provided as an argument, ask for user input
    if args.prompt is None:
        current_model = args.model
        print(f"Current model: {current_model}")
        print("Enter your prompt (type 'exit' to quit, '/model' to switch models):")
        
        while True:
            user_prompt = input("> ")
            
            if user_prompt.lower() in ['exit', 'quit']:
                print("Exiting program...")
                break
            
            if user_prompt.lower() == '/model':
                new_model = select_model()
                if new_model:
                    current_model = new_model
                else:
                    print(f"Keeping current model: {current_model}")
                continue
            
            if user_prompt.strip():  # Check if prompt is not empty
                generate_response(
                    user_prompt,
                    current_model,
                    args.temperature,
                    args.top_p,
                    args.max_tokens
                )
                print("\nEnter another prompt or type 'exit' to quit:")
            else:
                print("Prompt cannot be empty. Please try again.")
    else:
        # Use the prompt provided as an argument
        generate_response(
            args.prompt,
            args.model,
            args.temperature,
            args.top_p,
            args.max_tokens
        )

if __name__ == "__main__":
    main()
