# OpenAI API Client

Cliente simple de Python para interactuar con la API de OpenAI mediante peticiones HTTP.

## Características

- Lee prompts desde un archivo de texto (`prompt.txt`)
- Configuración mediante variables de entorno (`.env`)
- Soporte para diferentes modelos de OpenAI
- Muestra el uso de tokens
- Manejo de errores detallado

## Instalación

1. Clona el repositorio o descarga los archivos

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Crea tu archivo `.env` basándote en `.env.example`:
```bash
cp .env.example .env
```

4. Edita el archivo `.env` y añade tu API key de OpenAI:
```
OPENAI_API_KEY=tu-api-key-aquí
OPENAI_MODEL=gpt-3.5-turbo
```

## Uso

1. Escribe tu prompt en el archivo `prompt.txt`

2. Ejecuta el script:
```bash
python main.py
```

El script:
- Leerá el prompt desde `prompt.txt`
- Enviará la petición a OpenAI usando el modelo configurado
- Mostrará la respuesta y el uso de tokens

## Modelos disponibles

Puedes cambiar el modelo en el archivo `.env`. Algunos modelos disponibles:
- `gpt-3.5-turbo` (por defecto)
- `gpt-4`
- `gpt-4-turbo`
- `gpt-4o`
- `gpt-4o-mini`

## Estructura del proyecto

```
├── main.py          # Script principal
├── prompt.txt       # Archivo con el prompt
├── .env            # Variables de entorno (no incluido en git)
├── .env.example    # Plantilla para las variables de entorno
├── requirements.txt # Dependencias del proyecto
└── README.md       # Esta documentación
```

## Requisitos

- Python 3.6+
- Una API key válida de OpenAI

## Obtener API Key de OpenAI

1. Ve a [https://platform.openai.com/](https://platform.openai.com/)
2. Regístrate o inicia sesión
3. Ve a la sección de API Keys
4. Crea una nueva API key
5. Copia la key y añádela a tu archivo `.env`

## Notas

- El archivo `.env` contiene información sensible y no debe compartirse
- Cada petición consume tokens que pueden tener costo según tu plan de OpenAI
- Asegúrate de revisar los límites de uso de la API de OpenAI