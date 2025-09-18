
# LangChain Travel Planner

## Overview
A Flask web app that generates **tourist attractions**, **detailed travel plans**, and **JSON routes** for any location using LangChain and multiple LLMs.

## Features
- Lists top tourist places with highlights.  
- Creates travel plans with timings, transportation, and costs.  
- Extracts structured route data in JSON.  
- Supports **Gemini**, **Groq**, and **Ollama LLaMA3** models.  

## LLM Models
- **Gemini** – Cloud-based, highly accurate, requires API key.  
- **Groq** – Fast, structured outputs, cloud API.  
- **Ollama LLaMA3** – Local, offline, ideal for privacy.  

## Setup
1. Create and activate a Python virtual environment.  
2. Install dependencies:
```bash
pip install -r requirements.txt
````

3. Set API keys (Gemini/Groq) or run local Ollama server.
4. Run the app:

```bash
python app.py
```

## License

MIT License

