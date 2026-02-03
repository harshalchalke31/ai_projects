from pydantic import BaseModel, Field
from typing import Optional

class GeneralResponse(BaseModel):
    timestamp: str = Field(description="Get current date and time as a string.")   
    answer: str

class EmailResponse(BaseModel):
    timestamp: str = Field(description="Get current date and time as a string.")
    recipant: str = Field(description='Use recipant name specified by user. Else use `[recipant]`.')
    subject: str
    body: str

class EssayResponse(BaseModel):
    timestamp: str = Field(description="Get current date and time as a string.")
    title: str
    introduction: str
    body: str
    conclusion: str