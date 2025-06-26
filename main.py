from fastapi import FastAPI
from pydantic import BaseModel
import httpx

app = FastAPI()

class AchievementData(BaseModel):
    achievements: list[str]

@app.post("/summarize")
async def summarize(data: AchievementData):
    prompt = f"""Summarize the following achievements in a crisp, professional, newsletter-friendly tone in 3–4 sentences:\n\n""" + \
             "\n".join(f"- {item}" for item in data.achievements)

    # Call local Ollama instance
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "llama3",
                "messages": [{"role": "user", "content": prompt}]
            }
        )

    result = response.json()
    return {"summary": result["message"]["content"]}

