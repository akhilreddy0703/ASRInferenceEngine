from fastapi import APIRouter, Form, HTTPException, Depends
from server.utils.logger import llm_logger
from server.utils.auth import get_api_key
from openai import OpenAI

router = APIRouter()

@router.post("/llm")
async def call_llm(
    text: str = Form(...),
    model: str = Form("gpt-3.5-turbo"),
    api_key: str = Depends(get_api_key)
):
    try:
        client = OpenAI(api_key=api_key)

        llm_logger.info(f"Calling LLM with model: {model}")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an assistant that helps complete sentences for speech-impaired individuals. Please provide a natural and coherent completion based on the given input."},
                {"role": "user", "content": text}
            ],
            max_tokens=100,
            n=1,
            temperature=0.7,
        )
        completed_text = response.choices[0].message.content.strip()
        llm_logger.info("LLM call completed successfully")
        return {"text": completed_text}
    except Exception as e:
        error_message = f"LLM call failed: {str(e)}"
        llm_logger.error(error_message)
        raise HTTPException(status_code=500, detail=error_message)