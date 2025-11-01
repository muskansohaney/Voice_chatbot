# api_server.py
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from assistant_app import handle_user_input  # import from above
from fastapi import FastAPI, File, UploadFile
from assistant_app import handle_user_input, transcribe_audio
app = FastAPI()
@app.post("/api/voice")
async def voice_message(file: UploadFile = File(...)):
    """
    Endpoint to process uploaded voice message.
    """
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Step 1: Convert speech → text
    text = transcribe_audio(file_path)

    # Step 2: Get assistant reply
    reply, _ = handle_user_input(text)

    return {"input_text": text, "reply": reply}


class MessageIn(BaseModel):
    text: str

class MessageOut(BaseModel):
    assistant: str

@app.post("/api/message", response_model=MessageOut)
def message(inmsg: MessageIn):
    assistant_text, _ = handle_user_input(inmsg.text)
    return {"assistant": assistant_text}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

