import React, { useState } from 'react';
import {
  MessageSquare,
  ShieldAlert,
  ShieldCheck,
  PhoneCall,
  X,
  Check,
  Sparkles,
  Send,
  Copy,
  AlertTriangle,
  ArrowRight,
  Share2
} from 'lucide-react';

export function WhatsAppShieldModal({ isOpen, onClose, isDark }) {
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const quickSamples = [
    {
      title: '⚡ Electricity KYC Scam',
      text: 'URGENT: Your Bijli (Electricity) bill was not updated. Power supply will be disconnected tonight at 09:30 PM by Electricity Officer. Immediately call 9876543210 or install MahaVitaran_Update.apk to verify UPI payment.'
    },
    {
      title: '🚨 CBI Digital Arrest',
      text: 'CENTRAL BUREAU OF INVESTIGATION (CBI) NOTICE: Your Aadhaar is linked to illegal MDMA courier seized at Mumbai Airport. You are placed under DIGITAL ARREST. Join immediate video interrogation or warrant will be executed.'
    },
    {
      title: '✅ Legitimate Bank Alert',
      text: 'Dear Customer, your a/c ending 4821 is debited by Rs. 450.00 on 28-Nov-2026. Avl Bal: Rs. 14,820.50. UPI Ref: 3348192841.'
    }
  ];

  const formatWhatsAppText = (data) => {
    const isScam = data.is_scam || (data.risk_score >= 50);
    const riskScore = Math.round(data.risk_score || 0);
    const threatLevel = data.threat_level || (isScam ? 'CRITICAL' : 'SAFE');
    const badges = data.badges || [];
    const explanation = data.explanation || '';
    const actions = data.recommended_actions || [];

    const divider = '━━━━━━━━━━━━━━━━━━━━━\n';
    const header = '🛡️ *∀VITR AI Threat Intelligence* 🛡️\n';

    let verdictBanner = '';
    let category = '';

    if (isScam || riskScore >= 50) {
      verdictBanner = `🚨 *VERDICT: ${threatLevel} (${riskScore}% Risk)*\n`;
      category = `🏷️ *Threat Type:* ${badges[0] || 'High Risk Cyber-Fraud'}\n`;
    } else if (riskScore >= 20) {
      verdictBanner = `⚠️ *VERDICT: SUSPICIOUS SIGNAL (${riskScore}% Risk)*\n`;
      category = `🏷️ *Signal Category:* ${badges[0] || 'Unverified Message'}\n`;
    } else {
      verdictBanner = `🟢 *VERDICT: SAFE COMMUNICATION (${riskScore}% Risk)*\n`;
      category = `🏷️ *Category:* ${badges[0] || 'Legitimate Notice'}\n`;
    }

    const body = `\n*AI Threat Analysis:*\n${explanation}\n`;

    let actionsBlock = '';
    if (actions.length > 0) {
      actionsBlock = '\n*Protective Steps:*\n' + actions.slice(0, 3).map(a => `• ${a}`).join('\n') + '\n';
    }

    let emergencyBlock = '';
    if (isScam || riskScore >= 40) {
      emergencyBlock = (
        `\n${divider}` +
        '🚨 *EMERGENCY ACTIONS (MHA GOVT OF INDIA):*\n' +
        '1️⃣ *DO NOT* click any links, send money, or share OTPs.\n' +
        '2️⃣ *Call 1930* immediately (National Cyber Crime Helpline).\n' +
        '3️⃣ Report incident on: https://cybercrime.gov.in\n'
      );
    } else {
      emergencyBlock = (
        `\n${divider}` +
        '💡 *Security Hygiene:* Never share banking OTPs, PINs, or install APK files received via chat.\n'
      );
    }

    const footer = `${divider}_Scanned with ∀VITR AI • Real-Time Cyber-Fraud Defense_`;

    return `${header}${verdictBanner}${category}${divider}${body}${actionsBlock}${emergencyBlock}${footer}`;
  };

  const handleVerify = async (textToScan) => {
    const text = textToScan || inputText;
    if (!text.trim()) return;

    setIsLoading(true);
    setResult(null);

    try {
      const apiBase = import.meta.env.VITE_API_BASE_URL || '';
      const res = await fetch(`${apiBase}/api/v1/scan/text`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: text,
          sender: '+91 98765 43210'
        })
      });

      if (!res.ok) throw new Error('Verification failed');
      const data = await res.json();
      const formatted = formatWhatsAppText(data);
      setResult({
        ...data,
        whatsapp_formatted_reply: formatted
      });
    } catch (err) {
      console.error('WhatsApp Shield API error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const shareOnWhatsApp = (text) => {
    const message = text || result?.whatsapp_formatted_reply || inputText || 'Hi, please verify this suspicious message with ∀VITR AI.';
    const encoded = encodeURIComponent(message);
    window.open(`https://api.whatsapp.com/send?text=${encoded}`, '_blank');
  };

  const copyResponse = () => {
    if (!result?.whatsapp_formatted_reply) return;
    navigator.clipboard.writeText(result.whatsapp_formatted_reply);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-black/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className={`relative w-full max-w-3xl max-h-[92vh] overflow-y-auto rounded-3xl border shadow-2xl p-5 sm:p-7 space-y-6 transition-all ${
        isDark ? 'bg-[#121214] border-[#27272A] text-white' : 'bg-white border-[#DCD9D2] text-zinc-900'
      }`}>
        {/* Header */}
        <div className="flex items-start justify-between pb-4 border-b border-zinc-500/20">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="p-2 rounded-xl bg-emerald-500/10 text-emerald-500">
                <MessageSquare className="w-5 h-5" />
              </span>
              <h2 className="text-lg sm:text-xl font-bold tracking-tight">
                WhatsApp Cyber Shield
              </h2>
              <span className="px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 text-[10px] font-mono font-bold">
                Instant Scanner
              </span>
            </div>
            <p className="text-xs text-zinc-400">
              Verify suspicious WhatsApp forwards, fake police notices, UPI links, and electricity cutoff alerts.
            </p>
          </div>
          <button
            onClick={onClose}
            type="button"
            className="p-2 rounded-xl hover:bg-zinc-800/40 text-zinc-400 hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Message Input Section */}
        <div className="space-y-3">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <label className="text-xs font-mono font-semibold text-zinc-400">
              Verify Suspicious Message or Forward:
            </label>
            <div className="flex flex-wrap items-center gap-1.5">
              {quickSamples.map((sample, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => {
                    setInputText(sample.text);
                    handleVerify(sample.text);
                  }}
                  className="text-[10px] px-2.5 py-1 rounded-lg border border-zinc-700 hover:bg-zinc-800 text-zinc-300 transition-all font-mono"
                >
                  {sample.title}
                </button>
              ))}
            </div>
          </div>

          <div className="relative">
            <textarea
              rows={4}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Paste suspicious WhatsApp message, fake courier notice, or bank alert here..."
              className={`w-full p-3.5 rounded-2xl border text-xs font-sans focus:outline-none focus:ring-2 focus:ring-emerald-500/50 transition-all ${
                isDark ? 'bg-zinc-900/80 border-zinc-700 text-white placeholder-zinc-500' : 'bg-zinc-50 border-zinc-300 text-zinc-900'
              }`}
            />
            <div className="flex items-center justify-end gap-2 mt-2">
              <button
                type="button"
                onClick={() => {
                  setInputText('');
                  setResult(null);
                }}
                className="px-3 py-1.5 rounded-xl text-xs text-zinc-400 hover:text-white"
              >
                Clear
              </button>
              <button
                type="button"
                onClick={() => handleVerify()}
                disabled={isLoading || !inputText.trim()}
                className="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white text-xs font-bold flex items-center gap-1.5 shadow-md transition-all"
              >
                {isLoading ? (
                  <>
                    <Sparkles className="w-3.5 h-3.5 animate-spin" />
                    <span>Analyzing with AI...</span>
                  </>
                ) : (
                  <>
                    <Send className="w-3.5 h-3.5" />
                    <span>Verify Message</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Live Threat Intelligence Results */}
        {result && (
          <div className="rounded-2xl border p-4 space-y-3 bg-[#15161A] border-zinc-700/80 animate-in fade-in duration-200">
            <div className="flex flex-wrap items-center justify-between gap-2 border-b border-zinc-700 pb-2">
              <div className="flex items-center gap-2">
                <span className={`px-2.5 py-0.5 rounded-full text-xs font-mono font-bold border ${
                  result.is_scam || (result.risk_score >= 50)
                    ? 'bg-red-500/20 text-red-400 border-red-500/40'
                    : 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40'
                }`}>
                  {result.threat_level} ({Math.round(result.risk_score)}% Risk)
                </span>
                {result.badges?.slice(0, 2).map((b, i) => (
                  <span key={i} className="text-[10px] font-mono text-zinc-400 hidden sm:inline">
                    • {b}
                  </span>
                ))}
              </div>

              <button
                type="button"
                onClick={copyResponse}
                className="text-xs px-2.5 py-1 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 flex items-center gap-1 font-mono transition-colors"
              >
                {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                <span>{copied ? 'Copied' : 'Copy Formatted Text'}</span>
              </button>
            </div>

            {/* Formatted WhatsApp Markdown Body */}
            <div className="p-3.5 rounded-xl bg-[#0B141A] border border-zinc-800 font-mono text-[11px] text-zinc-200 whitespace-pre-wrap leading-relaxed select-text">
              {result.whatsapp_formatted_reply}
            </div>

            {/* Action Buttons */}
            <div className="flex flex-wrap items-center gap-2 pt-1">
              {(result.is_scam || result.risk_score >= 50) && (
                <a
                  href="tel:1930"
                  className="px-4 py-2 rounded-xl bg-red-600 hover:bg-red-500 text-white text-xs font-bold flex items-center gap-1.5 shadow-md transition-all"
                >
                  <PhoneCall className="w-3.5 h-3.5" />
                  <span>Call 1930 Cyber Helpline</span>
                </a>
              )}
              <button
                type="button"
                onClick={() => shareOnWhatsApp()}
                className="px-4 py-2 rounded-xl bg-emerald-700 hover:bg-emerald-600 text-white text-xs font-semibold flex items-center gap-1.5 shadow transition-all"
              >
                <Share2 className="w-3.5 h-3.5" />
                <span>Share Warning on WhatsApp</span>
              </button>
            </div>
          </div>
        )}

        {/* Footer with Helpline */}
        <div className="flex items-center justify-between pt-3 border-t border-zinc-500/20 text-xs text-zinc-400">
          <span className="font-mono text-[11px]">
            National Cyber Crime Helpline: <strong className="text-red-400">1930</strong> | <a href="https://cybercrime.gov.in" target="_blank" rel="noreferrer" className="underline hover:text-white">cybercrime.gov.in</a>
          </span>
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-1.5 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-white text-xs font-semibold transition-all"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
