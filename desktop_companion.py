"""
ScamShield AI — Native Windows Background Interceptor Companion
==============================================================================
Runs natively in the Windows background and monitors the OS clipboard globally.
The millisecond you press Ctrl+C inside WhatsApp Desktop, Telegram, SMS, or
any application, this companion intercepts it AT THE SOURCE and triggers a
native Windows 10/11 Toast Notification right where you are copying, with zero
need to switch back to the browser.
==============================================================================
"""

import sys
import os
import time
import ctypes
from ctypes import wintypes
import urllib.request
import json

# Try importing winotify for native Windows 10/11 toasts
try:
    from winotify import Notification, audio
    HAS_WINOTIFY = True
except ImportError:
    HAS_WINOTIFY = False

def log(msg):
    print(msg, flush=True)

from ai.detector import ScamDetector

# Initialize Windows API references
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

user32.OpenClipboard.argtypes = [wintypes.HWND]
user32.OpenClipboard.restype = wintypes.BOOL
user32.CloseClipboard.restype = wintypes.BOOL
user32.GetClipboardData.argtypes = [wintypes.UINT]
user32.GetClipboardData.restype = wintypes.HANDLE
user32.GetClipboardSequenceNumber.restype = wintypes.DWORD

kernel32.GlobalLock.argtypes = [wintypes.HGLOBAL]
kernel32.GlobalLock.restype = ctypes.c_void_p
kernel32.GlobalUnlock.argtypes = [wintypes.HGLOBAL]
kernel32.GlobalUnlock.restype = wintypes.BOOL

CF_UNICODETEXT = 13


def get_windows_clipboard_text():
    """Reads current UTF-16 text from Windows system clipboard safely."""
    for _ in range(3):
        if user32.OpenClipboard(None):
            try:
                handle = user32.GetClipboardData(CF_UNICODETEXT)
                if handle:
                    ptr = kernel32.GlobalLock(handle)
                    if ptr:
                        try:
                            return ctypes.c_wchar_p(ptr).value
                        finally:
                            kernel32.GlobalUnlock(handle)
                return None
            finally:
                user32.CloseClipboard()
        time.sleep(0.02)
    return None


def show_native_windows_toast(verdict: str, risk_score: float, threat_type: str, preview: str, advice: str):
    """Fires native Windows 10/11 Action Center notification."""
    # CRITICAL: Never show a toast for a rate-limited or throttling artifact
    if verdict == "RATE_LIMITED":
        return

    clean_preview = preview.replace("\n", " ").strip()
    if len(clean_preview) > 85:
        clean_preview = clean_preview[:82] + "..."

    is_scam = risk_score >= 50 or verdict in ("CRITICAL", "HIGH", "POSSIBLE SCAM")
    is_careful = not is_scam and (risk_score >= 20 or verdict in ("LOW", "MEDIUM", "BE CAREFUL"))

    if is_scam:
        title = f"🚨 ScamShield: SCAM DETECTED! ({int(risk_score)}%)"
        msg = f"[{threat_type}]\n\"{clean_preview}\"\n👉 {advice}"
        sound = audio.Reminder if HAS_WINOTIFY else None
    elif is_careful:
        title = f"🟡 ScamShield: CAUTION RECOMMENDED ({int(risk_score)}%)"
        msg = f"[{threat_type}]\n\"{clean_preview}\"\n👉 {advice}"
        sound = audio.IM if HAS_WINOTIFY else None
    else:
        title = "🟢 ScamShield: Copied Message is SAFE (0%)"
        msg = f"[{threat_type}]\n\"{clean_preview}\"\n👉 No malicious indicators or extortion detected."
        sound = audio.Default if HAS_WINOTIFY else None

    if HAS_WINOTIFY:
        try:
            toast = Notification(
                app_id="ScamShield AI",
                title=title,
                msg=msg
            )
            if sound:
                toast.set_audio(sound, loop=False)

            # 1-Click Action Buttons right on the toast!
            toast.add_actions(label="🛡️ Open Threat Console", launch="http://localhost:5173")
            if is_scam:
                toast.add_actions(label="📞 Dial 1930 Helpline", launch="tel:1930")

            toast.show()
            return
        except Exception as e:
            log(f"[WARN] winotify toast error: {e}")

    log(f"\n{title}\n{msg}\n{'='*60}")


def analyze_text(text: str, detector: ScamDetector):
    """Analyzes text via local FastAPI backend or in-memory fallback."""
    # 1. Attempt FastAPI backend on port 8000
    try:
        req_data = json.dumps({
            "text": text,
            "channel": "WHATSAPP",
            "client_id": "desktop_companion"
        }).encode("utf-8")
        req = urllib.request.Request(
            "http://127.0.0.1:8000/api/v1/scan/text",
            data=req_data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=1.0) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                # If backend returned rate_limited, never treat as safe! Fall through to in-memory detector
                if not data.get("rate_limited") and data.get("threat_level") != "RATE_LIMITED":
                    badges = data.get("badges", [])
                    threat_category = badges[0] if badges else "Cyber-Fraud Risk"
                    return {
                        "verdict": data.get("threat_level", "SAFE"),
                        "risk_score": float(data.get("risk_score", 0.0)),
                        "threat_type": threat_category,
                        "advice": data.get("recommended_actions", ["Do not click links"])[0] if data.get("is_scam") else "Verified legitimate communication."
                    }
    except Exception:
        pass

    # 2. In-memory engine fallback (Zero network delay, zero rate-limiting)
    res = detector.analyze(text, client_id="desktop_companion")
    badges = res.get("badges", [])
    threat_category = badges[0] if badges else ("High-Risk Extortion" if res.get("is_scam") else "Benign Message")
    actions = res.get("recommended_actions", [])
    advice = actions[0] if actions else ("DO NOT click links or pay!" if res.get("is_scam") else "No threats detected.")

    return {
        "verdict": res.get("threat_level", "SAFE"),
        "risk_score": float(res.get("risk_score", 0.0)),
        "threat_type": threat_category,
        "advice": advice
    }


def run_companion():
    log("=" * 70)
    log("🛡️  SCAMSHIELD AI — NATIVE WINDOWS DESKTOP COMPANION")
    log("=" * 70)
    log("Status: ACTIVE & LISTENING TO WINDOWS CLIPBOARD GLOBALLY")
    log("Instructions:")
    log("  • Copy ANY message in WhatsApp Desktop, Telegram, SMS, or Chrome")
    log("  • A native Windows Toast Notification will pop up IMMEDIATELY at")
    log("    the bottom-right of your screen without switching to the browser.")
    log("  • Copying the SAME message again will trigger a fresh re-scan.")
    log("  • Press Ctrl+C in this terminal window to stop.")
    log("=" * 70)

    detector = ScamDetector()

    # Track sequence number increments so copying the SAME message again triggers!
    last_seq = user32.GetClipboardSequenceNumber()
    last_processed_text = ""
    last_processed_time = 0.0

    while True:
        try:
            current_seq = user32.GetClipboardSequenceNumber()

            # Trigger whenever sequence number changes (new copy event in Windows!)
            if current_seq != last_seq:
                last_seq = current_seq
                current = get_windows_clipboard_text()
                
                if current and isinstance(current, str):
                    cleaned = current.strip()
                    now = time.time()
                    
                    # Intercept messages >= 6 chars
                    # Debounce duplicate triggers within 300ms to avoid double-firing
                    if len(cleaned) >= 6 and (cleaned != last_processed_text or (now - last_processed_time > 0.4)):
                        last_processed_text = cleaned
                        last_processed_time = now
                        
                        log(f"\n[⚡ INTERCEPTED] Copy event detected (Seq #{current_seq}, {len(cleaned)} chars): \"{cleaned[:60]}...\"")
                        
                        # Analyze threat
                        analysis = analyze_text(cleaned, detector)
                        log(f"      └─ Verdict: [{analysis['verdict']}] Risk: {analysis['risk_score']}% | Category: {analysis['threat_type']}")
                        
                        # Pop Native Windows Toast Notification!
                        show_native_windows_toast(
                            verdict=analysis["verdict"],
                            risk_score=analysis["risk_score"],
                            threat_type=analysis["threat_type"],
                            preview=cleaned,
                            advice=analysis["advice"]
                        )

            time.sleep(0.12)  # 120ms check cycle (instant response, <0.05% CPU)
        except KeyboardInterrupt:
            log("\n[INFO] ScamShield Companion stopped gracefully.")
            break
        except Exception as e:
            time.sleep(0.2)


if __name__ == "__main__":
    run_companion()
