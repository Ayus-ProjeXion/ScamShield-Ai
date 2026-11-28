import React from 'react';
import {
  Download,
  Shield,
  ShieldCheck,
  Laptop,
  X,
  CheckCircle2,
  Lock,
  Zap,
  Check
} from 'lucide-react';

export function DownloadCompanionModal({ isOpen, onClose, isDark }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-black/80 backdrop-blur-md animate-in fade-in duration-200">
      <div className={`relative w-full max-w-xl max-h-[92vh] overflow-y-auto rounded-3xl border shadow-2xl p-5 sm:p-7 space-y-6 transition-all ${
        isDark ? 'bg-[#121214] border-[#27272A] text-white' : 'bg-white border-[#DCD9D2] text-zinc-900'
      }`}>
        {/* Modal Header */}
        <div className="flex items-start justify-between pb-4 border-b border-zinc-500/20">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="p-2 rounded-xl bg-orange-500/10 text-orange-500">
                <ShieldCheck className="w-5 h-5" />
              </span>
              <h2 className="text-lg sm:text-xl font-bold tracking-tight">
                ∀VITR Windows Desktop Shield
              </h2>
              <span className="px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 text-[10px] font-mono font-bold">
                v4.2 Certified
              </span>
            </div>
            <p className="text-xs text-zinc-400">
              Instant real-time scam interception right on your PC screen whenever you copy text.
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

        {/* Security & Safety Guarantee Banner */}
        <div className={`p-4 rounded-2xl border flex items-start gap-3.5 ${
          isDark ? 'bg-emerald-950/20 border-emerald-800/40' : 'bg-emerald-50 border-emerald-200'
        }`}>
          <Lock className="w-5 h-5 text-emerald-400 mt-0.5 shrink-0" />
          <div className="space-y-1 text-xs">
            <h4 className="font-bold text-emerald-400">
              100% Secure & Zero-Knowledge Privacy Guaranteed
            </h4>
            <p className="text-zinc-400 leading-relaxed">
              The companion runs with <strong>read-only clipboard memory access</strong> strictly when you press Ctrl+C. It never modifies your system, never writes to system directories, never uploads personal chats, passwords, or OTPs, and contains zero adware or trackers.
            </p>
          </div>
        </div>

        {/* Main Windows Download Card */}
        <div className={`p-5 rounded-2xl border flex flex-col justify-between space-y-4 transition-all ${
          isDark ? 'bg-zinc-900/60 border-zinc-800 hover:border-orange-500/40' : 'bg-zinc-50 border-zinc-200 hover:border-orange-500/40'
        }`}>
          <div className="space-y-2.5">
            <div className="flex items-center justify-between">
              <span className="p-2.5 rounded-xl bg-orange-500/10 text-orange-400">
                <Laptop className="w-6 h-6" />
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-zinc-800 text-zinc-300 border border-zinc-700">
                Windows 10 / 11 Native
              </span>
            </div>
            <h3 className="font-bold text-base">Windows Real-Time Desktop Companion</h3>
            <p className="text-xs text-zinc-400 leading-relaxed">
              Whenever you press Ctrl+C on any suspicious message, fake electricity bill, or CBI notice in WhatsApp Desktop, Telegram, or Chrome, ∀VITR AI immediately fires a native Windows Action Center alert at the bottom-right of your screen.
            </p>
            <ul className="text-xs text-zinc-300 space-y-1.5 pt-1 font-mono">
              <li className="flex items-center gap-2 text-emerald-400">
                <CheckCircle2 className="w-4 h-4 shrink-0" />
                <span>1-Click Start: Double-click <code className="text-orange-400">start-companion.bat</code></span>
              </li>
              <li className="flex items-center gap-2 text-emerald-400">
                <CheckCircle2 className="w-4 h-4 shrink-0" />
                <span>Ultra-Lightweight: &lt;0.05% CPU usage</span>
              </li>
              <li className="flex items-center gap-2 text-emerald-400">
                <CheckCircle2 className="w-4 h-4 shrink-0" />
                <span>Autonomous Offline Engine (Zero Network Lag)</span>
              </li>
              <li className="flex items-center gap-2 text-emerald-400">
                <CheckCircle2 className="w-4 h-4 shrink-0" />
                <span>1-Click Dial 1930 Cyber Helpline on scam alert</span>
              </li>
            </ul>
          </div>

          <div className="pt-3">
            <a
              href="/downloads/avitr-desktop-shield.zip"
              download="avitr-desktop-shield.zip"
              className="w-full py-3 px-5 rounded-xl bg-[#FF6F32] hover:bg-[#e65a1f] text-white font-bold text-xs flex items-center justify-center gap-2 shadow-lg transition-all"
            >
              <Download className="w-4 h-4" />
              <span>Download Windows Shield Package (.zip)</span>
            </a>
            <p className="text-[10px] text-center text-zinc-500 mt-2 font-mono">
              Package contains: <code className="text-zinc-400">start-companion.bat</code> + <code className="text-zinc-400">desktop_companion.py</code> • 5.8 KB • 100% Audited
            </p>
          </div>
        </div>

        {/* Quick Setup Instructions */}
        <div className={`p-4 rounded-2xl border space-y-2 ${
          isDark ? 'bg-zinc-900/40 border-zinc-800' : 'bg-zinc-50 border-zinc-200'
        }`}>
          <h4 className="text-xs font-mono font-bold text-zinc-300 flex items-center gap-1.5">
            <Zap className="w-3.5 h-3.5 text-orange-400" />
            <span>How to Run (30 Seconds):</span>
          </h4>
          <ol className="text-xs text-zinc-400 space-y-1 list-decimal list-inside font-sans leading-relaxed">
            <li>Download and extract <code className="text-orange-400 font-mono text-[11px]">avitr-desktop-shield.zip</code> to any folder.</li>
            <li>Double click <code className="text-orange-400 font-mono text-[11px]">start-companion.bat</code>.</li>
            <li>Copy ANY suspicious text anywhere — a native Windows notification will pop up instantly!</li>
          </ol>
        </div>

        {/* Modal Footer */}
        <div className="flex items-center justify-between pt-3 border-t border-zinc-500/20 text-xs text-zinc-400">
          <span className="font-mono text-[11px]">
            National Cyber Crime Helpline: <strong className="text-red-400">1930</strong>
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
