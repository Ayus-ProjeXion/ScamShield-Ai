import React, { useState, useRef, useEffect } from 'react';
import {
  Bot,
  X,
  Send,
  Sparkles,
  ShieldAlert,
  ShieldCheck,
  RotateCcw,
  ExternalLink,
  MessageSquare
} from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

async function fetchCopilotApi(endpoint, options = {}) {
  // 1. Try relative / configured URL first (handles Vite proxy, same-origin, LAN)
  try {
    const res = await fetch(`${API_BASE_URL}${endpoint}`, options);
    if (res.ok) return res;
  } catch (e) {
    // Relative call network failure
  }

  // 2. If running on localhost and relative failed, try direct backend port 8000
  if (typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')) {
    try {
      const res = await fetch(`http://127.0.0.1:8000${endpoint}`, options);
      if (res.ok) return res;
    } catch (e) {
      // Direct localhost fallback failed
    }
  }

  throw new Error(`Copilot endpoint ${endpoint} unreachable`);
}

function formatEngineLabel(engine) {
  if (!engine || engine.startsWith('offline')) return 'Offline Forensic Engine';
  if (engine.includes('groq')) {
    const raw = engine.replace('groq:', '');
    if (raw.toLowerCase().includes('qwen')) return 'Groq Qwen 27B AI';
    return `Groq AI (${raw.split('/').pop()})`;
  }
  if (engine.includes('gemini')) return 'Gemini 1.5 Flash';
  return engine;
}

export function FloatingCopilot({ scanResult, isDark }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hello! I am your **∀VITR Threat Copilot**. I analyze your current scan results, explain threat patterns, and guide you on immediate safety and cyber-police complaint steps. How can I help you?",
      chips: ["Why is this flagged?", "What should I do right now?", "Which law does this violate?"]
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [engineUsed, setEngineUsed] = useState('groq:qwen/qwen3.8-27b');
  const [isOnline, setIsOnline] = useState(true);
  const messagesEndRef = useRef(null);

  // Sync live copilot engine status on mount & drawer open
  useEffect(() => {
    let isMounted = true;
    const fetchStatus = async () => {
      try {
        const res = await fetchCopilotApi('/api/v1/copilot/status');
        const data = await res.json();
        if (isMounted) {
          setEngineUsed(data.active_engine || 'groq:qwen/qwen3.8-27b');
          setIsOnline(data.status === 'online');
        }
      } catch (err) {
        if (isMounted) {
          setEngineUsed('offline:deterministic-forensic');
          setIsOnline(false);
        }
      }
    };

    fetchStatus();
    return () => { isMounted = false; };
  }, [isOpen]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  // When a new scan result arrives, post an auto-update in copilot
  useEffect(() => {
    if (scanResult) {
      const risk = scanResult.riskScore || 0;
      const level = scanResult.verdict || (risk >= 66 ? 'CRITICAL' : (risk >= 26 ? 'SUSPICIOUS' : 'SAFE'));
      const newPrompt = risk >= 50
        ? `⚠️ I've loaded your latest scan: **${level} (${risk}%)**. Threat markers detected: ${(scanResult.badges || []).slice(0, 3).join(', ') || 'High-risk fraud pattern'}. Ask me how to protect yourself or copy a formal 1930 complaint.`
        : `✅ I've loaded your latest scan: **${level} (${risk}%)**. No malicious patterns were triggered. Feel free to ask any verification questions.`;

      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: newPrompt,
          chips: ["Why is this flagged?", "What should I do right now?", "Show legal sections"]
        }
      ]);
    }
  }, [scanResult?.hmacToken, scanResult?.riskScore]);

  const handleSendMessage = async (textToSend = null) => {
    const text = (textToSend || inputValue).trim();
    if (!text || isTyping) return;

    const userMessage = { role: 'user', content: text };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);

    try {
      // Build scan context payload from current scanResult
      const contextPayload = scanResult ? {
        threat_level: scanResult.verdict || 'UNKNOWN',
        risk_score: scanResult.riskScore || 0,
        is_scam: Boolean(scanResult.riskScore >= 50),
        badges: scanResult.badges || [],
        why_its_risky: scanResult.why_its_risky || [{ title: 'Detected Marker', detail: scanResult.explanation || '' }],
        explanation: scanResult.explanation || '',
        complaint_draft: scanResult.complaintDraft || '',
        text_preview: scanResult.textPreview || ''
      } : {};

      const response = await fetchCopilotApi('/api/v1/copilot/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          scan_context: contextPayload,
          history: messages.slice(-4).map(m => ({ role: m.role, content: m.content }))
        })
      });

      const data = await response.json();
      const used = data.engine_used || 'offline:deterministic-forensic';
      setEngineUsed(used);
      setIsOnline(!used.startsWith('offline'));
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: data.reply,
          chips: data.suggested_chips || []
        }
      ]);
    } catch (err) {
      console.warn('Copilot call fallback:', err);
      setEngineUsed('offline:deterministic-forensic');
      setIsOnline(false);
      // Fallback offline message
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: "I am operating in offline safety mode. Based on current forensic standards: **Never share OTP/PINs, block unknown numbers**, and call helpline **1930** if you suspect financial theft.",
          chips: ["What should I do right now?", "Show legal sections"]
        }
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleClear = () => {
    setMessages([
      {
        role: 'assistant',
        content: "Conversation cleared. Ask me any question about your scan result or cybersecurity safeguards.",
        chips: ["Why is this flagged?", "What should I do right now?"]
      }
    ]);
  };

  return (
    <>
      {/* Floating Circular Trigger Button */}
      <div className="fixed bottom-6 right-6 z-40">
        {!isOpen && (
          <button
            type="button"
            onClick={() => setIsOpen(true)}
            className="group relative flex items-center justify-center w-14 h-14 rounded-full bg-gradient-to-tr from-[#FF6F32] to-[#FF8C5A] text-white shadow-2xl hover:scale-105 active:scale-95 transition-all duration-200"
            title="Open ∀VITR AI Copilot"
          >
            <span className="absolute -inset-1 rounded-full bg-[#FF6F32]/40 animate-ping opacity-60"></span>
            <Bot className="w-7 h-7" />
            <span className={`absolute -top-1 -right-1 w-3.5 h-3.5 border-2 border-[#141416] rounded-full ${isOnline && !engineUsed.startsWith('offline') ? 'bg-emerald-500' : 'bg-amber-500'}`}></span>
          </button>
        )}
      </div>

      {/* Floating Drawer / Card */}
      {isOpen && (
        <div className={`fixed bottom-6 right-4 sm:right-6 z-50 w-[92vw] sm:w-[420px] h-[540px] max-h-[85vh] rounded-2xl border shadow-2xl flex flex-col overflow-hidden animate-in slide-in-from-bottom-5 duration-200 ${
          isDark ? 'bg-[#141416] border-[#2C2C32] text-white' : 'bg-[#FDFCFA] border-[#DCD9D2] text-[#1C1B18]'
        }`}>
          {/* Header */}
          <div className={`px-4 py-3 border-b flex items-center justify-between ${
            isDark ? 'bg-[#1A1A1E] border-[#2C2C32]' : 'bg-[#F4F2EC] border-[#DCD9D2]'
          }`}>
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-full bg-[#FF6F32] flex items-center justify-center text-white shadow-md">
                <Bot className="w-4 h-4" />
              </div>
              <div>
                <div className="flex items-center gap-1.5">
                  <h4 className="text-xs font-bold font-mono tracking-tight">∀VITR Threat Copilot</h4>
                  <span className={`text-[9px] font-mono px-1.5 py-0.5 rounded font-semibold border flex items-center gap-1 ${
                    isOnline && !engineUsed.startsWith('offline')
                      ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                      : 'bg-amber-500/10 text-amber-400 border-amber-500/30'
                  }`}>
                    <span className={`w-1.5 h-1.5 rounded-full ${isOnline && !engineUsed.startsWith('offline') ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`}></span>
                    {isOnline && !engineUsed.startsWith('offline') ? 'ONLINE AI' : 'OFFLINE SECURE'}
                  </span>
                </div>
                <p className="text-[10px] text-zinc-400 font-mono truncate max-w-[200px]">
                  {scanResult ? `Grounded: ${scanResult.verdict || 'Scan'} (${scanResult.riskScore || 0}%)` : 'Grounded: Project Intelligence'}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-1">
              <button
                type="button"
                onClick={handleClear}
                className="p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-800 transition-colors"
                title="Reset Conversation"
              >
                <RotateCcw className="w-3.5 h-3.5" />
              </button>
              <button
                type="button"
                onClick={() => setIsOpen(false)}
                className="p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-800 transition-colors"
                title="Minimize Copilot"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Conversation Body */}
          <div className="flex-1 p-4 overflow-y-auto space-y-3 text-xs leading-relaxed">
            {messages.map((m, idx) => (
              <div
                key={idx}
                className={`flex flex-col ${m.role === 'user' ? 'items-end' : 'items-start'}`}
              >
                <div className={`p-3 rounded-2xl max-w-[88%] whitespace-pre-line ${
                  m.role === 'user'
                    ? 'bg-[#FF6F32] text-white rounded-br-none shadow-sm'
                    : (isDark ? 'bg-[#202024] text-zinc-200 border border-[#2C2C32] rounded-bl-none' : 'bg-[#ECEAE5] text-[#1C1B18] border border-[#DCD9D2] rounded-bl-none')
                }`}>
                  {m.content}
                </div>

                {/* Suggested Action Chips (only on latest assistant message) */}
                {m.role === 'assistant' && m.chips && m.chips.length > 0 && idx === messages.length - 1 && (
                  <div className="flex flex-wrap gap-1.5 mt-2 pt-1">
                    {m.chips.map((chip, cIdx) => (
                      <button
                        key={cIdx}
                        type="button"
                        onClick={() => handleSendMessage(chip)}
                        className={`text-[10px] font-mono px-2 py-1 rounded-full border transition-colors ${
                          isDark
                            ? 'bg-zinc-800/80 border-zinc-700 text-zinc-300 hover:border-[#FF6F32] hover:text-[#FF6F32]'
                            : 'bg-white border-zinc-300 text-zinc-700 hover:border-[#FF6F32] hover:text-[#FF6F32]'
                        }`}
                      >
                        {chip}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            ))}

            {isTyping && (
              <div className="flex items-center gap-1.5 text-zinc-400 text-xs font-mono py-1">
                <span className="w-2 h-2 rounded-full bg-[#FF6F32] animate-bounce"></span>
                <span className="w-2 h-2 rounded-full bg-[#FF6F32] animate-bounce [animation-delay:0.2s]"></span>
                <span className="w-2 h-2 rounded-full bg-[#FF6F32] animate-bounce [animation-delay:0.4s]"></span>
                <span className="text-[10px] ml-1">Analyzing scan forensics...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Footer Engine Info */}
          <div className={`px-4 py-1.5 border-t text-[10px] font-mono flex items-center justify-between text-zinc-500 ${
            isDark ? 'bg-[#111113] border-[#2C2C32]' : 'bg-[#EAE8E3] border-[#DCD9D2]'
          }`}>
            <span className="flex items-center gap-1.5">
              <span className="text-zinc-400">Engine:</span>
              <span className={isOnline && !engineUsed.startsWith('offline') ? 'text-zinc-300 font-semibold' : 'text-amber-500/90 font-medium'}>
                {formatEngineLabel(engineUsed)}
              </span>
            </span>
            <span className={isOnline && !engineUsed.startsWith('offline') ? 'text-emerald-500 font-semibold' : 'text-zinc-400'}>
              {isOnline && !engineUsed.startsWith('offline') ? '100% Grounded' : 'Rule-Based & Safe'}
            </span>
          </div>

          {/* Chat Input */}
          <div className={`p-3 border-t flex items-center gap-2 ${
            isDark ? 'bg-[#18181C] border-[#2C2C32]' : 'bg-white border-[#DCD9D2]'
          }`}>
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Ask about this scan or legal steps..."
              className={`flex-1 px-3 py-2 rounded-xl text-xs outline-none border transition-colors ${
                isDark
                  ? 'bg-[#101012] border-[#2C2C32] text-white focus:border-[#FF6F32]'
                  : 'bg-[#F4F2EC] border-[#DCD9D2] text-[#1C1B18] focus:border-[#FF6F32]'
              }`}
            />
            <button
              type="button"
              onClick={() => handleSendMessage()}
              disabled={!inputValue.trim() || isTyping}
              className="p-2 rounded-xl bg-[#FF6F32] hover:bg-[#E55B1F] text-white disabled:opacity-40 transition-all active:scale-95"
              title="Send"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </>
  );
}
