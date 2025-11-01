# test_groq.py
import os, requests
from dotenv import load_dotenv
load_dotenv()
key = os.getenv("GROQ_API_KEY")
url = os.getenv("GROQ_API_BASE_URL")  # like https://api.groq.com/openai/v1
if not key or not url:
    raise SystemExit("Set GROQ_API_KEY and GROQ_API_BASE_URL in .env")

print("Groq base URL:", url)
# Do a minimal dry-run if you have an example endpoint (commented by default)
# resp = requests.get(url, headers={"Authorization": f"Bearer {key}"})
# print(resp.status_code, resp.text)
print("API key present — real call will be made by assistant when used.")


