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
import os
import sys

from datetime import datetime
from typing import Final
from dotenv import load_dotenv
from loguru import logger

from tools.tools import create_openai_request

LOGS_PATH: Final[str] = "./logs"


def read_prompt(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


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
    api_key = None if args.debug else os.getenv('OPENAI_API_KEY')
    model = args.model or os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')

    if not api_key and not args.debug:
        logger.error("Error: OPENAI_API_KEY not found in .env file")
        logger.error("Please create a .env file based on .env.example")
        sys.exit(1)

    if api_key:
        logger.warning("API key set, API calls will incurr in costs.")

    if not (prompt := read_prompt(filename=args.prompt)):
        logger.error(f"Error: Prompt not found in file {args.prompt}")
        sys.exit(1)

    logger.info(f"Prompt read from file: {args.prompt}")

    tool = create_openai_request(tool="response", api_key=api_key)
    if response := tool(prompt=prompt, model=model):
        logger.info("\nOpenAI Response:")
        message = tool.output(response, **args.__dict__)
        logger.info(f"Message:\n{message}")
        # log the message to a log file with a custom date and time
        logfilename = ["response", os.path.splitext(os.path.basename(args.prompt))[0], get_date_time_str()]
        log_message(message=message, log_file=os.path.join(LOGS_PATH, "_".join(logfilename) + ".txt") )


if __name__ == "__main__":
    main()
