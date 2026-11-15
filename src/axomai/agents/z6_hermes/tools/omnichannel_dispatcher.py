"""
Z6 Hermes - Omnichannel Notification & Messaging Dispatcher Tool.
Formats notifications for WhatsApp, Telegram, Slack, and REST Webhooks.
"""

from typing import Dict, Any

class OmnichannelDispatcher:
    """Prepares structured payloads for mobile and chat channels."""

    def format_whatsapp(self, title: str, summary: str, action_url: str = "") -> str:
        url_part = f"\n\n🔗 *Action Link:* {action_url}" if action_url else ""
        return f"🔔 *[AxomAI AGI Notification]*\n\n📌 *{title}*\n{summary}{url_part}\n\n_Sent autonomously via Z6 Hermes_"

    def format_telegram(self, title: str, summary: str, action_url: str = "") -> str:
        url_part = f"\n\n👉 [Open Workspace]({action_url})" if action_url else ""
        return f"🚀 **{title}**\n\n{summary}{url_part}\n\n*AxomAI AGI • Z6 Hermes*"

    def prepare_dispatch(self, title: str, summary: str, action_url: str = "") -> Dict[str, Any]:
        return {
            "whatsapp_message": self.format_whatsapp(title, summary, action_url),
            "telegram_message": self.format_telegram(title, summary, action_url),
            "dispatch_status": "READY_FOR_BROADCAST",
            "channels": ["WhatsApp", "Telegram", "Slack", "Email Webhook"]
        }

omnichannel_dispatcher = OmnichannelDispatcher()

