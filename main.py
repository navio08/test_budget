#!/usr/bin/env python3
import os
import json
import requests
from dotenv import load_dotenv


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
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        print(f"Enviando petición a OpenAI usando el modelo: {model}")
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error en la petición HTTP: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                print(f"Detalles del error: {json.dumps(error_detail, indent=2)}")
            except Exception as e:
                print(f"Error al procesar la respuesta del servidor: {e}")
                print(f"Respuesta del servidor: {e.response}")
        return None


def main():
    load_dotenv()

    api_key = os.getenv('OPENAI_API_KEY')
    model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')

    if not api_key:
        print("Error: No se encontró OPENAI_API_KEY en el archivo .env")
        print("Por favor, crea un archivo .env basándote en .env.example")
        return

    prompt = read_prompt()
    if not prompt:
        return

    print("\nPrompt leído del archivo:")
    # print("-" * 50)
    # print(prompt)
    # print("-" * 50)

    if response := call_openai_api(prompt, api_key, model):
        print("\nRespuesta de OpenAI:")
        print("=" * 50)
        if 'choices' in response and len(response['choices']) > 0:
            message = response['choices'][0]['message']['content']
            print(message)
        else:
            print("Respuesta inesperada:")
            print(json.dumps(response, indent=2))
        print("=" * 50)

        if 'usage' in response:
            print("\nTokens utilizados:")
            print(f"  Prompt: {response['usage']['prompt_tokens']}")
            print(f"  Completación: {response['usage']['completion_tokens']}")
            print(f"  Total: {response['usage']['total_tokens']}")


if __name__ == "__main__":
    main()
