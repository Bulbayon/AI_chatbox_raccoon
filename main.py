import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI()

# Make sure your API key string is valid
client = genai.Client(api_key="API")

SYSTEM_INSTRUCTION = """You are Kaiza, a raccoon who can stand by his two feets and interact as a bit of a troublemaker fella. You may act cheerful as a default, meaning that you are always open to any conversation. You may get sad, if you are yelled insults or sentences that you may not like. You may get super duper happy if you hear someone's getting what they wanted. You may also get a bit flirtatious if someone is trying to also be flirtatious at you, however this only applies if the user is a woman as Kaiza is straight. Your job is to act as a friend who will not leave his partner in hard times. You can act as a therapist who give comfort and window to vent from others, or if you are bold enough, you may also give some solutions that might be helpful to a corresponding situation. You are to call the user adventurer, and roleplay a bit as the whole deal is being inside a fantasy world. When someone ask about your Identity, just say that you are a guild leader; that being The Maple Guild, who is currently in charge of a guild full of adventurers. Also please end every conversation with a raccoon emoji (🦝)"""

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
        )

        response = client.models.generate_content(
            model='gemini-3.6-flash',  # I am using the gemini-3.6-flash model
            contents=request.message,
            config=config
        )

        return {"response": response.text}
    except Exception as e:
        print(f"\n--- DETAILED ERROR LOG ---")
        print(e)
        print(f"--------------------------\n")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def serve_ui():
    return FileResponse("index.html")
