# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python client for OpenAI API that reads prompts from a text file and makes HTTP requests to OpenAI's chat completions endpoint.

## Development Setup

1. Create and activate virtual environment:
   - `python -m venv venv`
   - `source venv/bin/activate` (Unix/macOS) or `venv\Scripts\activate` (Windows)

2. Install dependencies:
   - `pip install -r requirements.txt`

3. Configure environment:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key and select model in `.env`

## Running the Application

- `python main.py` - Reads prompt from `prompt.txt` and sends request to OpenAI

## Project Structure

- `main.py` - Main script that handles API requests
- `prompt.txt` - Text file containing the prompt to send
- `.env` - Environment variables (API key and model selection)
- `requirements.txt` - Python dependencies (requests, python-dotenv)