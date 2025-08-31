#!/usr/bin/env python3
"""
OpenAI API Client Script (Using OpenAI SDK)

This script reads prompts from text files and sends them to OpenAI's chat completions API.
It supports debug mode, custom models, and automatic response logging.

Usage:
    python main_openai.py [OPTIONS]

Options:
    --debug         Enable debug mode (skips API call, uses mock data)
    --model MODEL   Override the OpenAI model (default: from .env or gpt-3.5-turbo)
    --prompt FILE   Path to prompt file (default: ./prompts/prompt_perplexity_deep_research.txt)

Examples:
    python main_openai.py
    python main_openai.py --debug
    python main_openai.py --model gpt-4 --prompt ./my_prompt.txt
    python main_openai.py --prompt ./prompts/prompt_01.txt --model gpt-5 --debug

Output:
    - Console output shows the API response
    - Responses are automatically logged to ./logs/ directory
    - Log files are named: response_[prompt_name]_[timestamp].txt
"""
import argparse
from datetime import datetime
from typing import Final
from dotenv import load_dotenv
import json
from loguru import logger
import os
from openai import OpenAI

LOGS_PATH: Final[str] = "./logs"

def read_prompt(filename='./prompts/prompt_perplexity_deep_research.txt'):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{filename}'")
        return None
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None


def call_openai_api(prompt, api_key, model):
    # when api_key=None, the OpenAI SDK might be falling back to environment variables or other default authentication methods.
    # add an explicit check to avoid incurring into costs, e.g. when debug mode is on and no api calls are expected.
    if not api_key:
        logger.info("No API key provided, skipping OpenAI call")
        return None

    try:
        client = OpenAI(api_key=api_key)
        print(f"Enviando petición a OpenAI usando el modelo: {model}")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response
    except Exception as e:
        print(f"Error en la petición a OpenAI: {e}")
        return None
    
def compose_log_message(response, **kwargs) -> str:
    result = ["=" * 50]
    # Handle OpenAI SDK response object
    if hasattr(response, 'choices') and len(response.choices) > 0:
        message = response.choices[0].message.content
        result.append(message)
    else:
        result.append("Respuesta inesperada:")
        result.append(str(response))

    if hasattr(response, 'usage') and response.usage:
        result.append("=" * 50)
        result.append("\nTokens utilizados:")
        result.append(f"  Prompt: {response.usage.prompt_tokens}")
        result.append(f"  Completación: {response.usage.completion_tokens}")
        result.append(f"  Total: {response.usage.total_tokens}")


    if kwargs:
        result.append("=" * 50)
        result.append("kwargs:")
        [result.append(f"\t{k}:{v}") for k,v in kwargs.items()]
        # for k,v in kwargs:
        #     result.append(f"{k}:{v}")
    return "\n".join(result)

def get_date_time_str() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def log_message(message: str, log_file: str) -> bool:
    try:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(message)
        logger.info(f"Message logged to {log_file}")
        return True
    except Exception as e:
        logger.error(f"Error logging message to {log_file}: {e}")
        return False

def parse_arguments():
    parser = argparse.ArgumentParser(description='OpenAI API client for sending prompts')
    parser.add_argument("--debug", action='store_true', help='Enable debug mode')
    parser.add_argument("--model", required=False, default=None)
    parser.add_argument("--prompt", required=False, default="./prompts/prompt_perplexity_deep_research.txt")
    return parser.parse_args()


def main():
    # load input args
    args = parse_arguments()
    load_dotenv()
    logger.debug(f"Input arguments: {args}")

    # load api and model
    api_key = os.getenv('OPENAI_API_KEY') if not args.debug else None
    model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo') if not args.model else args.model

    if not api_key and not args.debug:
        print("Error: No se encontró OPENAI_API_KEY en el archivo .env")
        print("Por favor, crea un archivo .env basándote en .env.example")
        return
    
    if api_key:
        logger.warning("API key set, API calls will incurr in costs.")

    prompt = read_prompt(filename=args.prompt)
    if not prompt:
        return

    logger.info(f"Prompt leído del archivo: {args.prompt}")

    if response := call_openai_api(prompt, api_key, model):
        logger.info("\nRespuesta de OpenAI:")
        message = compose_log_message(response, **args.__dict__)
        logger.info(f"Message:\n{message}")
        # log the message to a log file with a custom date and time
        logfilename = ["response", os.path.splitext(os.path.basename(args.prompt))[0], get_date_time_str()]
        log_message(message=message, log_file=os.path.join(LOGS_PATH, "_".join(logfilename) + ".txt") )
    

if __name__ == "__main__":
    main()