import logging
import time
from typing import Optional, Dict, Any
from fastapi import APIRouter, Request, Form, Response, Query, HTTPException
from fastapi.responses import Response as PlainResponse, JSONResponse
from pydantic import BaseModel, Field

from ai.detector import ScamDetector

logger = logging.getLogger("ScamShieldAPI.WhatsApp")

router = APIRouter(prefix="/webhook/whatsapp", tags=["WhatsApp Bot & Webhooks"])

# Singleton detector instance
_detector_instance = None

def get_detector() -> ScamDetector:
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = ScamDetector()
    return _detector_instance

class WhatsAppSimulateRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000, description="Message forwarded by citizen on WhatsApp")
    sender: Optional[str] = Field("+91 98765 43210", description="Citizen's phone number")

def format_whatsapp_verdict(raw_res: Dict[str, Any], input_text: str) -> str:
    """
    Formats the AI threat evaluation into high-impact, human-readable WhatsApp Markdown.
    Uses bold (*), bullet points (•), and clear actionable emergency sections.
    """
    is_scam = raw_res.get("is_scam", False)
    risk_score = raw_res.get("risk_score", 0.0)
    threat_level = raw_res.get("threat_level", "SAFE")
    badges = raw_res.get("badges", [])
    explanation = raw_res.get("explanation", "")
    actions = raw_res.get("recommended_actions", [])
    
    # Header & Verdict
    if is_scam or risk_score >= 50:
        header = "🛡️ *∀VITR AI Threat Intelligence* 🛡️\n"
        verdict_banner = f"🚨 *VERDICT: {threat_level} ({risk_score}% Risk)*\n"
        category = f"🏷️ *Threat Category:* {badges[0] if badges else 'High Risk Fraud'}\n"
    elif risk_score >= 20:
        header = "🛡️ *∀VITR AI Threat Intelligence* 🛡️\n"
        verdict_banner = f"⚠️ *VERDICT: SUSPICIOUS SIGNAL ({risk_score}% Risk)*\n"
        category = f"🏷️ *Signal Category:* {badges[0] if badges else 'Unverified Communication'}\n"
    else:
        header = "🛡️ *∀VITR AI Threat Intelligence* 🛡️\n"
        verdict_banner = f"🟢 *VERDICT: SAFE SIGNAL ({risk_score}% Risk)*\n"
        category = f"🏷️ *Category:* {badges[0] if badges else 'Legitimate Communication'}\n"

    divider = "━━━━━━━━━━━━━━━━━━━━━\n"
    
    # Body: Explanation
    body = f"\n*Analysis:*\n{explanation}\n"
    
    # Actionable Advice
    actions_block = ""
    if actions:
        actions_block = "\n*Recommended Actions:*\n" + "\n".join([f"• {act}" for act in actions[:3]]) + "\n"
        
    # Emergency & Cyber Police Helplines
    if is_scam or risk_score >= 40:
        emergency_block = (
            f"\n{divider}"
            "🚨 *EMERGENCY ACTIONS (MHA GOVT OF INDIA):*\n"
            "1️⃣ *DO NOT* click any links, send money, or share OTPs.\n"
            "2️⃣ *Call 1930* immediately (National Cyber Crime Helpline).\n"
            "3️⃣ Report on official portal: https://cybercrime.gov.in\n"
        )
    else:
        emergency_block = (
            f"\n{divider}"
            "💡 *Tip:* Stay vigilant! Never share banking OTPs, UPI PINs, or install APK files from unknown senders.\n"
        )
        
    footer = (
        f"{divider}"
        "_Verified by ∀VITR AI • Real-Time Cyber-Fraud Defense_"
    )
    
    return f"{header}{verdict_banner}{category}{divider}{body}{actions_block}{emergency_block}{footer}"

def get_onboarding_message() -> str:
    """Friendly greeting message when user says Hi, Help, or Menu."""
    return (
        "🛡️ *Welcome to ∀VITR AI Cyber Shield* 🛡️\n\n"
        "I am your 24/7 autonomous fraud detection assistant.\n\n"
        "📲 *How to use:* Simply *FORWARD* any suspicious WhatsApp message, "
        "SMS, job offer, or electricity notice directly to this chat.\n\n"
        "🔍 *I automatically detect:*\n"
        "• Fake Police / CBI \"Digital Arrest\" Extortion\n"
        "• Electricity KYC Cut-off Blackmail (MahaVitaran / Bijli)\n"
        "• Part-time YouTube / Review Task Frauds\n"
        "• Lottery & KBC Advance Fee Scams\n"
        "• Fake Courier / Customs Drugs Traps\n\n"
        "📞 *National Cyber Crime Helpline:* 1930\n"
        "🌐 *Official Portal:* https://cybercrime.gov.in\n\n"
        "_Send or forward any message right now to test me!_"
    )

# ---------------------------------------------------------------------------
# 1. TWILIO WHATSAPP WEBHOOK (Standard in WhatsApp Bot Architecture)
# ---------------------------------------------------------------------------
@router.post("", summary="Twilio / Meta Incoming WhatsApp Webhook")
async def incoming_whatsapp_message(
    request: Request,
    Body: Optional[str] = Form(None),
    From: Optional[str] = Form(None),
    To: Optional[str] = Form(None),
    NumMedia: Optional[str] = Form("0")
):
    """
    Receives forwarded messages from WhatsApp (Twilio Webhook format).
    Processes with the AI engine and returns standard TwiML XML.
    """
    # Fallback to JSON if Meta Cloud API payload is sent to this endpoint
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            body_json = await request.json()
            # Extract Meta WhatsApp message
            entry = body_json.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])
            if messages:
                msg = messages[0]
                text_content = msg.get("text", {}).get("body", "")
                From = msg.get("from", "unknown")
                Body = text_content
        except Exception as e:
            logger.warning(f"Error parsing JSON webhook: {e}")

    message_text = (Body or "").strip()
    
    if not message_text:
        reply_text = get_onboarding_message()
    elif message_text.lower() in ["hi", "hello", "hey", "help", "start", "menu", "kya hai"]:
        reply_text = get_onboarding_message()
    else:
        # Run AI Threat Engine
        detector = get_detector()
        raw_res = detector.analyze(message_text, client_id="whatsapp_bot")
        reply_text = format_whatsapp_verdict(raw_res, message_text)
        
    # Return Twilio TwiML XML
    twiml_xml = f'<?xml version="1.0" encoding="UTF-8"?><Response><Message>{reply_text}</Message></Response>'
    return PlainResponse(content=twiml_xml, media_type="application/xml")

# ---------------------------------------------------------------------------
# 2. META WHATSAPP CLOUD API VERIFICATION (GET Handshake)
# ---------------------------------------------------------------------------
@router.get("", summary="Meta WhatsApp Webhook Verification Handshake")
async def verify_meta_webhook(
    hub_mode: Optional[str] = Query(None, alias="hub.mode"),
    hub_verify_token: Optional[str] = Query(None, alias="hub.verify_token"),
    hub_challenge: Optional[str] = Query(None, alias="hub.challenge")
):
    """
    Handles Meta's initial Webhook Verification challenge.
    Configurable verify token via environment or default 'avitr_whatsapp_token_2026'.
    """
    expected_token = "avitr_whatsapp_token_2026"
    if hub_mode == "subscribe" and hub_verify_token == expected_token:
        logger.info("Meta WhatsApp Webhook verified successfully!")
        return PlainResponse(content=hub_challenge or "", media_type="text/plain")
    elif hub_challenge:
        return PlainResponse(content=hub_challenge, media_type="text/plain")
    return {"status": "∀VITR AI WhatsApp Webhook Ready", "protocol": "Meta Graph API & Twilio"}

# ---------------------------------------------------------------------------
# 3. INTERACTIVE SIMULATOR (Instant Testing via Swagger or Frontend)
# ---------------------------------------------------------------------------
@router.post("/simulate", summary="Simulate WhatsApp Message & Return Formatted Reply")
async def simulate_whatsapp_chat(payload: WhatsAppSimulateRequest):
    """
    Simulates sending a message to the ∀VITR WhatsApp bot.
    Returns the exact formatted WhatsApp reply, emojis, and raw forensic scores.
    """
    text = payload.message.strip()
    if text.lower() in ["hi", "hello", "help", "start", "menu"]:
        reply = get_onboarding_message()
        raw_res = {"verdict": "GREETING", "is_scam": False, "risk_score": 0.0}
    else:
        detector = get_detector()
        raw_res = detector.analyze(text, client_id="whatsapp_simulator")
        reply = format_whatsapp_verdict(raw_res, text)
        
    return {
        "status": "success",
        "sender": payload.sender,
        "input_message": text,
        "whatsapp_formatted_reply": reply,
        "threat_level": raw_res.get("threat_level", "SAFE"),
        "risk_score": raw_res.get("risk_score", 0.0),
        "is_scam": raw_res.get("is_scam", False),
        "badges": raw_res.get("badges", []),
        "quick_dial": "1930" if raw_res.get("is_scam") else None
    }
