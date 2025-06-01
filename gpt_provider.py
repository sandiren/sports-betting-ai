# gpt_provider.py

import openai
import requests
import config

# Set API keys
openai.api_key = config.OPENAI_API_KEY
GEMINI_API_KEY = config.GEMINI_API_KEY
OPENROUTER_API_KEY = config.OPENROUTER_API_KEY

# Models
OPENAI_MODEL = "gpt-4o"  # or "gpt-3.5-turbo"
GEMINI_MODEL = "gemini-1.5-pro"  # For Google AI Studio
OPENROUTER_MODEL = "openai/gpt-3.5-turbo"  # or any supported model

# ----- OpenAI -----
def call_openai(prompt):
    print("▶️ Calling OpenAI...")
    response = openai.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    print("✅ OpenAI success!")
    return response.choices[0].message.content

# ----- Gemini (Google AI Studio) -----
def call_gemini(prompt):
    print("▶️ Calling Gemini (Google AI Studio)...")

    url = f"https://generativelanguage.googleapis.com/v1/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

    body = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(url, json=body)
    print(f"Gemini status code: {response.status_code}")

    if response.status_code != 200:
        print(f"Gemini error: {response.text}")
        response.raise_for_status()

    gemini_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    print("✅ Gemini success!")
    return gemini_text

# ----- OpenRouter -----
def call_openrouter(prompt):
    print("▶️ Calling OpenRouter...")
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(url, headers=headers, json=body)
    print(f"OpenRouter status code: {response.status_code}")

    if response.status_code != 200:
        print(f"OpenRouter error: {response.text}")
        response.raise_for_status()

    router_text = response.json()["choices"][0]["message"]["content"]
    print("✅ OpenRouter success!")
    return router_text

# ----- Fallback flow -----
def get_ai_prediction(prompt):
    try:
        print("🔹 Trying OpenAI...")
        return call_openai(prompt)
    except Exception as e1:
        print(f"⚠️ OpenAI failed: {e1}")
        try:
            print("🔹 Trying Gemini...")
            return call_gemini(prompt)
        except Exception as e2:
            print(f"⚠️ Gemini failed: {e2}")
            try:
                print("🔹 Trying OpenRouter...")
                return call_openrouter(prompt)
            except Exception as e3:
                print(f"❌ All providers failed: {e3}")
                return "⚠️ All AI providers failed. Please try again later."