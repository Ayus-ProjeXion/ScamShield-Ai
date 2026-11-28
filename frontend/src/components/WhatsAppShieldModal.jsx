import React, { useState } from 'react';
import {
  MessageSquare,
  ShieldAlert,
  ShieldCheck,
  PhoneCall,
  X,
  ExternalLink,
  Check,
  Sparkles,
  Send,
  Copy,
  AlertTriangle,
  ArrowRight
} from 'lucide-react';

export function WhatsAppShieldModal({ isOpen, onClose, isDark }) {
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [copied, setCopied] = useState(false);

  const botNumber = import.meta.env.VITE_WHATSAPP_BOT_NUMBER || '+91 91193 01930';

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
      title: '✅ Legitimate Bank SMS',
      text: 'Dear Customer, your a/c ending 4821 is debited by Rs. 450.00 on 28-Nov-2026. Avl Bal: Rs. 14,820.50. UPI Ref: 3348192841.'
    }
  ];

  const handleVerify = async (textToScan) => {
    const text = textToScan || inputText;
    if (!text.trim()) return;

    setIsLoading(true);
    setResult(null);

    try {
      const res = await fetch('/api/v1/webhook/whatsapp/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          sender: '+91 98765 43210'
        })
      });

      if (!res.ok) throw new Error('Verification failed');
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error('WhatsApp Shield API error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const openRealWhatsApp = (text, targetNumber = null) => {
    const message = text || inputText || 'Hi, please verify this suspicious message: ';
    const encoded = encodeURIComponent(message);
    let url;
    if (targetNumber) {
      const clean = targetNumber.replace(/[^0-9]/g, '');
      url = `https://wa.me/${clean}?text=${encoded}`;
    } else {
      // Universal WhatsApp intent: opens WhatsApp and lets user select any chat/contact/self
      url = `https://api.whatsapp.com/send?text=${encoded}`;
    }
    window.open(url, '_blank');
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
                Zero-Download
              </span>
            </div>
            <p className="text-xs text-zinc-400">
              Verify suspicious WhatsApp messages, fake police warrants, and electricity cut-off notices directly on WhatsApp or right here.
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

        {/* 1-Click Launch into Real WhatsApp */}
        <div className={`p-4 rounded-2xl border flex flex-col sm:flex-row items-center justify-between gap-3 ${
          isDark ? 'bg-emerald-950/20 border-emerald-800/40' : 'bg-emerald-50 border-emerald-200'
        }`}>
          <div className="space-y-0.5 text-center sm:text-left">
            <h4 className="text-sm font-bold text-emerald-400 flex items-center justify-center sm:justify-start gap-1.5">
              <span>Verified 24/7 WhatsApp Defense</span>
              <Check className="w-3.5 h-3.5 text-emerald-400 stroke-[3]" />
            </h4>
            <p className="text-xs text-zinc-400">
              Helpline: <strong className="font-mono text-zinc-200">{botNumber}</strong> • Forward any message in WhatsApp for instant AI defense.
            </p>
          </div>
          <div className="flex flex-col sm:flex-row items-center gap-2 w-full sm:w-auto">
            <button
              type="button"
              onClick={() => openRealWhatsApp(inputText)}
              className="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center justify-center gap-2 shadow-lg transition-all"
            >
              <ExternalLink className="w-4 h-4" />
              <span>Open in WhatsApp</span>
            </button>
            <button
              type="button"
              onClick={() => openRealWhatsApp(inputText, '+14155238886')}
              className="w-full sm:w-auto px-3.5 py-2.5 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 font-semibold text-xs flex items-center justify-center gap-1.5 transition-all"
              title="Official Twilio live registered WhatsApp test number"
            >
              <MessageSquare className="w-3.5 h-3.5 text-emerald-400" />
              <span>Live Bot (+1 415...)</span>
            </button>
          </div>
        </div>

        {/* Real Live Text Verification Input */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <label className="text-xs font-mono font-semibold text-zinc-400">
              Verify Any Message Text:
            </label>
            <div className="flex items-center gap-1.5">
              {quickSamples.map((sample, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => {
                    setInputText(sample.text);
                    handleVerify(sample.text);
                  }}
                  className="text-[10px] px-2.5 py-1 rounded-lg border border-zinc-700 hover:bg-zinc-800 text-zinc-300 transition-all"
                >
                  {sample.title}
                </button>
              ))}
            </div>
          </div>

          <div className="relative">
            <textarea
              rows={3}
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Paste suspicious WhatsApp message, SMS, or job offer here..."
              className={`w-full p-3.5 rounded-2xl border text-xs font-sans focus:outline-none focus:ring-2 focus:ring-emerald-500/50 transition-all ${
                isDark ? 'bg-zinc-900/80 border-zinc-700 text-white placeholder-zinc-500' : 'bg-zinc-50 border-zinc-300 text-zinc-900'
              }`}
            />
            <div className="flex items-center justify-end gap-2 mt-2">
              <button
                type="button"
                onClick={() => setInputText('')}
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
                    <span>Analyzing...</span>
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

        {/* Real Live Results Card */}
        {result && (
          <div className="rounded-2xl border p-4 space-y-3 bg-[#15161A] border-zinc-700/80 animate-in fade-in duration-200">
            <div className="flex items-center justify-between border-b border-zinc-700 pb-2">
              <div className="flex items-center gap-2">
                <span className={`px-2.5 py-0.5 rounded-full text-xs font-mono font-bold border ${
                  result.is_scam
                    ? 'bg-red-500/20 text-red-400 border-red-500/40'
                    : 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40'
                }`}>
                  {result.threat_level} ({result.risk_score}%)
                </span>
                {result.badges?.map((b, i) => (
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

            {/* Formatted WhatsApp Response Body */}
            <div className="p-3 rounded-xl bg-[#0B141A] border border-zinc-800 font-mono text-[11px] text-zinc-200 whitespace-pre-wrap leading-relaxed">
              {result.whatsapp_formatted_reply}
            </div>

            {/* Direct Action Buttons */}
            <div className="flex flex-wrap items-center gap-2 pt-1">
              {result.is_scam && (
                <a
                  href="tel:1930"
                  className="px-4 py-2 rounded-xl bg-red-600 hover:bg-red-500 text-white text-xs font-bold flex items-center gap-1.5 shadow-md"
                >
                  <PhoneCall className="w-3.5 h-3.5" />
                  <span>Call 1930 Cyber Helpline</span>
                </a>
              )}
              <button
                type="button"
                onClick={() => openRealWhatsApp(`⚠️ SCAM ALERT: Do not click or pay! Analysis from ∀VITR AI:\n${result.whatsapp_formatted_reply}`)}
                className="px-4 py-2 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-xs font-semibold flex items-center gap-1.5"
              >
                <MessageSquare className="w-3.5 h-3.5 text-emerald-400" />
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
