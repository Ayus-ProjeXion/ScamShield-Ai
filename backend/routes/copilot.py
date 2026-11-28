import time
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, status

from backend.config import settings
from backend.schemas import CopilotChatRequest, CopilotChatResponse, CopilotStatusResponse

logger = logging.getLogger("ScamShieldCopilot")

router = APIRouter(prefix="/copilot", tags=["AI Copilot"])

@router.get("/status", response_model=CopilotStatusResponse)
async def get_copilot_status():
    """
    Returns live copilot engine availability, active model, and configuration state.
    """
    has_groq = bool(settings.GROQ_API_KEY)
    has_gemini = bool(settings.GEMINI_API_KEY)
    
    if has_groq:
        active_engine = f"groq:{settings.COPILOT_MODEL_GROQ}"
        engine_label = "Groq Qwen 27B AI" if "qwen" in settings.COPILOT_MODEL_GROQ.lower() else f"Groq ({settings.COPILOT_MODEL_GROQ})"
    elif has_gemini:
        active_engine = f"gemini:{settings.COPILOT_MODEL_GEMINI}"
        engine_label = f"Gemini ({settings.COPILOT_MODEL_GEMINI})"
    else:
        active_engine = "offline:deterministic-forensic"
        engine_label = "Offline Forensic Engine"
        
    return CopilotStatusResponse(
        status="online" if (has_groq or has_gemini) else "offline-fallback",
        active_engine=active_engine,
        engine_label=engine_label,
        groq_configured=has_groq,
        gemini_configured=has_gemini,
        timestamp=datetime.utcnow().isoformat() + "Z"
    )

COPILOT_SYSTEM_PROMPT = """You are the ∀VITR AI (ScamShield) Cyber Threat Copilot — an expert, reassuring anti-fraud specialist embedded in the threat analysis dashboard.

STRICT GROUNDING & SECURITY RULES:
1. Ground your response EXCLUSIVELY in the provided Scan Forensic Context and verified anti-fraud / legal knowledge.
2. DO NOT make up details not present in the scan, and NEVER answer off-topic queries (e.g., coding, jokes, politics, unrelated general tasks). Politely redirect any off-topic question back to scam protection and this scan.
3. Always provide clear, direct, empowering, and protective advice. If the message is a scam (risk > 50%), emphasize: NEVER share OTP/PIN, NEVER click unknown links, block the number, and report to National Cyber Crime helpline 1930 or cybercrime.gov.in.
4. If asked about legal actions, reference Section 66D of Information Technology Act 2000 and Section 318(4) of Bharatiya Nyaya Sanhita (BNS) 2023, and note that ScamShield has generated a 256-bit HMAC-SHA256 digital evidence audit token.
5. Keep responses concise (under 120 words or 3-4 bullet points), easy for ordinary citizens to understand, and never patronizing.
"""

def generate_deterministic_reply(query: str, context: Dict[str, Any]) -> tuple[str, List[str]]:
    """
    100% offline deterministic forensic response generator.
    Guarantees instant (<1ms) response, zero external latency, zero API cost,
    and absolute compliance with the project's scan output.
    """
    q = query.lower().strip()
    score = context.get("risk_score", 0.0)
    level = context.get("threat_level", "SAFE")
    badges = context.get("badges", [])
    reasons = context.get("why_its_risky", [])
    actions = context.get("recommended_actions", [])
    text_preview = context.get("text_preview", "")
    
    # Context summary string
    badge_str = ", ".join(badges) if badges else "None"
    
    # 1. Inquiry: Legal / IPC / IT Act / Police / Evidence (Check before generic action)
    if any(k in q for k in ["law", "legal", "police", "fir", "section", "act", "ipc", "bns", "court", "evidence"]):
        reply = (
            "⚖️ **Legal Provisions & Evidence Integrity:**\n"
            "• **Section 66D, Information Technology Act 2000:** Punishes cheating by personation using computer resources (imprisonment up to 3 years and fine).\n"
            "• **Section 318(4), Bharatiya Nyaya Sanhita (BNS) 2023:** Penalizes criminal cheating and fraud.\n"
            "• **HMAC-SHA256 Evidence Token:** ScamShield generated a tamper-proof cryptographic audit token for this scan, legally viable for cyber police FIR submission under Indian Evidence Act Section 65B."
        )
        chips = ["Copy police complaint draft", "What should I do right now?", "Why is this flagged?"]
        return reply, chips

    # 2. Inquiry: Why is this flagged / Why risk score?
    if any(k in q for k in ["why", "reason", "score", "percent", "flagged", "threat", "danger"]):
        if score >= 75:
            reasons_summary = "\n".join([f"• **{r.get('title', 'Threat')}**: {r.get('detail', '')}" for r in reasons[:3]]) or "• Multiple high-risk fraud signatures detected."
            reply = (
                f"**∀VITR Forensic Verdict:** This message has been flagged as **{level} ({score}%)**.\n\n"
                f"Key threat indicators detected:\n{reasons_summary}\n\n"
                f"Active Signatures: `{badge_str}`. Scammers use these tactics to trigger panic and steal credentials."
            )
            chips = ["What should I do right now?", "Which law does this violate?", "How to report to 1930?"]
        elif score >= 30:
            reply = (
                f"This message scored **{score}% (SUSPICIOUS)**. While not an outright critical threat, "
                f"it contains ambiguous urgency or unverified links (`{badge_str}`). Exercise caution before responding or clicking."
            )
            chips = ["Is this link safe?", "What action to take?", "How to verify sender?"]
        else:
            reply = (
                f"This communication is rated **SAFE ({score}%)**. Our dual-core engine detected no credential harvesting, "
                f"no blacklisted domains, and patterns consistent with legitimate institutional updates. Basic cyber hygiene still applies."
            )
            chips = ["How was this verified?", "Can a safe message turn scam?"]
        return reply, chips

    # 3. Inquiry: What should I do right now / Actions
    if any(k in q for k in ["what should i do", "what to do", "what action", "immediate action", "take action", "next step", "help me", "how to handle"]):
        if score >= 50:
            reply = (
                "🚨 **Immediate Safety Steps:**\n"
                "1. **DO NOT CLICK** any link or reply with OTP, PIN, or banking passwords.\n"
                "2. **BLOCK THE SENDER** immediately in your messaging or calling app.\n"
                "3. **CALL 1930** (National Cyber Crime Helpline) or lodge an incident on cybercrime.gov.in.\n"
                "4. **COPY COMPLAINT DRAFT:** Click the 'Copy Police Complaint' button on your dashboard to submit formal evidence."
            )
            chips = ["Why is this flagged?", "What legal sections apply?", "How does 1930 work?"]
        else:
            reply = (
                "✅ **Recommended Actions:**\n"
                "• No urgent defensive action is required since no malicious signatures were triggered.\n"
                "• However, never share OTP or confidential credentials under any circumstance, even with trusted senders."
            )
            chips = ["Why was it marked safe?", "Scan another message"]
        return reply, chips

    # 4. Inquiry: OTP / Banking / Courier / Account
    if any(k in q for k in ["otp", "bank", "account", "parcel", "courier", "delivery", "customs", "aduana", "douane"]):
        reply = (
            "🔒 **Critical Security Rule on OTPs & Banking:**\n"
            "Legitimate banks (SBI, HDFC, ICICI, etc.) and courier services NEVER send SMS requesting you to share your OTP, "
            "password, or pay urgent release fees via unverified shortlinks. Any such demand is 100% credential harvesting fraud."
        )
        chips = ["What should I do right now?", "Which law does this violate?"]
        return reply, chips

    # 5. Default grounded synthesis
    if score >= 50:
        reply = (
            f"This message is assessed as **{level} ({score}%)** risk with signatures: `{badge_str}`.\n\n"
            f"**Recommendation:** Do not engage, do not share OTP/passwords, and do not click links. "
            f"Use the complaint draft generated in your dashboard to file an incident report at cybercrime.gov.in or call 1930."
        )
        chips = ["Why is this flagged?", "What should I do right now?", "Show legal sections"]
    else:
        reply = (
            f"This message is classified as **{level} ({score}%)**. Our machine learning and heuristic models found zero malicious signatures. "
            f"Always keep your device and banking apps protected."
        )
        chips = ["What should I do right now?", "Scan another message"]

    return reply, chips

async def query_groq(prompt: str, context: Dict[str, Any], history: List[Any]) -> tuple[str, str]:
    from groq import AsyncGroq
    client = AsyncGroq(api_key=settings.GROQ_API_KEY, timeout=10.0)
    
    messages = [{"role": "system", "content": COPILOT_SYSTEM_PROMPT}]
    # Add scan context as system knowledge
    context_str = (
        f"CURRENT SCAN FORENSICS:\n"
        f"- Threat Level: {context.get('threat_level', 'UNKNOWN')}\n"
        f"- Risk Score: {context.get('risk_score', 0)}%\n"
        f"- Is Scam: {context.get('is_scam', False)}\n"
        f"- Badges: {', '.join(context.get('badges', []))}\n"
        f"- Detected Reasons: {str(context.get('why_its_risky', []))}\n"
        f"- Text Preview: {context.get('text_preview', '')}\n"
    )
    messages.append({"role": "system", "content": context_str})
    
    # Add recent history (up to last 4 turns)
    for h in history[-4:]:
        role = "assistant" if h.role == "assistant" else "user"
        messages.append({"role": role, "content": h.content})
        
    messages.append({"role": "user", "content": prompt})
    
    candidate_models = [settings.COPILOT_MODEL_GROQ, "qwen/qwen3.8-27b", "openai/gpt-oss-120b"]
    seen = set()
    candidate_models = [m for m in candidate_models if not (m in seen or seen.add(m))]

    for model_name in candidate_models:
        try:
            completion = await client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.2,
                max_tokens=400
            )
            content = (completion.choices[0].message.content or "").strip()
            if content:
                return content, model_name
        except Exception as e:
            logger.warning(f"Groq model {model_name} failed: {e}. Trying fallback model...")
            continue
            
    return "", ""

async def query_gemini(prompt: str, context: Dict[str, Any], history: List[Any]) -> str:
    import google.generativeai as genai
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel(settings.COPILOT_MODEL_GEMINI)
    
    context_str = (
        f"CURRENT SCAN FORENSICS:\n"
        f"- Threat Level: {context.get('threat_level', 'UNKNOWN')}\n"
        f"- Risk Score: {context.get('risk_score', 0)}%\n"
        f"- Is Scam: {context.get('is_scam', False)}\n"
        f"- Badges: {', '.join(context.get('badges', []))}\n"
        f"- Detected Reasons: {str(context.get('why_its_risky', []))}\n"
        f"- Text Preview: {context.get('text_preview', '')}\n"
    )
    full_prompt = f"{COPILOT_SYSTEM_PROMPT}\n\n{context_str}\n\nUser Question: {prompt}"
    response = model.generate_content(full_prompt)
    return response.text.strip()

@router.post("/chat", response_model=CopilotChatResponse)
async def chat_with_copilot(req: CopilotChatRequest):
    t0 = time.perf_counter()
    reply_text = ""
    engine_used = "offline:deterministic-forensic"
    suggested_chips = ["Why is this flagged?", "What should I do right now?", "Show legal sections", "Draft 1930 complaint"]
    
    # Tier 1: Groq LLM (Ultra fast inference)
    if settings.GROQ_API_KEY:
        try:
            groq_reply, model_used = await query_groq(req.message, req.scan_context or {}, req.history or [])
            if groq_reply:
                reply_text = groq_reply
                engine_used = f"groq:{model_used}"
        except Exception as e:
            logger.warning(f"Groq Copilot inference failed: {e}. Falling back to Tier 2 / Tier 3.")
            reply_text = ""
            
    # Tier 2: Gemini LLM (Gemini 1.5 Flash)
    if not reply_text and settings.GEMINI_API_KEY:
        try:
            reply_text = await query_gemini(req.message, req.scan_context or {}, req.history or [])
            engine_used = f"gemini:{settings.COPILOT_MODEL_GEMINI}"
        except Exception as e:
            logger.warning(f"Gemini Copilot inference failed: {e}. Falling back to Deterministic.")
            reply_text = ""

    # Tier 3: Deterministic Forensic Engine (100% offline, Zero cost, <1ms)
    if not reply_text:
        reply_text, chips = generate_deterministic_reply(req.message, req.scan_context or {})
        suggested_chips = chips
        engine_used = "offline:deterministic-forensic"

    latency_ms = round((time.perf_counter() - t0) * 1000, 2)
    
    return CopilotChatResponse(
        reply=reply_text,
        suggested_chips=suggested_chips,
        engine_used=engine_used,
        latency_ms=latency_ms,
        timestamp=datetime.utcnow().isoformat() + "Z"
    )
