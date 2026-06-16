from crewai.tools import BaseTool
from typing import Any, Type
from pydantic import BaseModel, Field
import os
import requests


class PushNotificationInput(BaseModel):
    """A message to be sent to user on pushover."""
    argument: str = Field(..., description="The message to be pushed.")

class PushNotificationTool(BaseTool):
    name: str = "Send a push notification to user"
    description: str = (
        "This tool is used to send a push notification to user on pushover."
        " It takes a message as input and sends it to the user."
    )
    args_schema: Type[BaseModel] = PushNotificationInput

    def _run(self, argument: str) -> str:
        pushover_user = os.getenv("PUSHOVER_USER")
        pushover_token = os.getenv("PUSHOVER_TOKEN")

        if not pushover_user or not pushover_token:
            raise RuntimeError("PUSHOVER_USER and PUSHOVER_TOKEN must be set to send notifications.")
        pushover_url = "https://api.pushover.net/1/messages.json"

        print(f"Push: {argument}")
        payload: dict[str, Any] = {
            "user": pushover_user,
            "token": pushover_token,
            "message": argument,
        }
        requests.post(pushover_url, data=payload)
        return '{"notification": "ok"}'
        
