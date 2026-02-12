from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import get_db
from models import ChatMessage
from schemas.chat_schemas import ChatRequest, ChatResponse, ChatMessageResponse
from utils.ai_response import get_completion
from datetime import datetime

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, user_email: str = None, db: Session = Depends(get_db)):
    """Send a message, get AI response, and save both to database."""
    # Use a default email if none provided (for now, we'll get it from query param)
    email = user_email or "anonymous"

    # Save user message to database
    user_msg = ChatMessage(
        user_email=email,
        role="user",
        message=request.message,
        timestamp=datetime.utcnow()
    )
    db.add(user_msg)
    db.commit()

    # Get AI response
    try:
        ai_response = get_completion(request.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Save assistant response to database
    assistant_msg = ChatMessage(
        user_email=email,
        role="assistant",
        message=ai_response,
        timestamp=datetime.utcnow()
    )
    db.add(assistant_msg)
    db.commit()

    return ChatResponse(response=ai_response)


@router.get("/chat/history")
def get_chat_history(user_email: str = None, db: Session = Depends(get_db)):
    """Get chat history for a user."""
    email = user_email or "anonymous"
    messages = db.query(ChatMessage).filter(
        ChatMessage.user_email == email
    ).order_by(ChatMessage.timestamp.asc()).all()

    return [
        {
            "id": msg.id,
            "role": msg.role,
            "message": msg.message,
            "timestamp": str(msg.timestamp)
        }
        for msg in messages
    ]


@router.delete("/chat/history")
def clear_chat_history(user_email: str = None, db: Session = Depends(get_db)):
    """Clear chat history for a user."""
    email = user_email or "anonymous"
    deleted = db.query(ChatMessage).filter(
        ChatMessage.user_email == email
    ).delete()
    db.commit()
    return {"message": f"Deleted {deleted} messages"}
