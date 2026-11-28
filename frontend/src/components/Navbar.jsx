import React from 'react';
import { Sun, Moon, PhoneCall, PlusCircle, Shield, Sparkles, MessageSquare } from 'lucide-react';

export function Navbar({
  isDark,
  onToggleTheme,
  onOpenReportModal,
  isShieldMode,
  onToggleShieldMode,
  onOpenOnboarding,
  onOpenWhatsAppModal
}) {
  return (
    <header className={`sticky top-0 z-40 w-full border-b backdrop-blur-md transition-colors duration-200 ${isDark
      ? 'bg-[#0C0C0C]/90 border-[#242428]'
      : 'bg-[#ECEAE5]/90 border-[#DCD9D2]'
      }`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">

        {/* AVITR AI — Unified Geometric Brand Identity */}
        <div className="flex items-center gap-3">
          <div className="flex items-center select-none">
            <span className={`flex items-center text-2xl font-black tracking-tight ${isDark ? 'text-white' : 'text-[#1C1B18]'
              }`}>
              {/* Precision Inverted 'A' Logo Mark — Perfectly Proportioned & Matched to VITR */}
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="3.2"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="w-[0.85em] h-[0.85em] inline-block mr-[1px] translate-y-[-1px]"
              >
                <line x1="3.5" y1="3.5" x2="12" y2="20.5" />
                <line x1="20.5" y1="3.5" x2="12" y2="20.5" />
                <line x1="6.8" y1="10" x2="17.2" y2="10" />
              </svg>
              <span>VITR</span>
            </span>
            <span className="ml-1.5 px-1.5 py-0.5 text-[10px] font-mono font-extrabold rounded-md bg-[#FF6F32]/15 text-[#FF6F32] border border-[#FF6F32]/30">
              AI
            </span>
          </div>
          <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full font-semibold border ${isDark
            ? 'bg-zinc-900 text-zinc-300 border-zinc-800'
            : 'bg-[#F6F5F2] text-[#1C1B18] border-[#DCD9D2]'
            }`}>
            v4.2
          </span>
        </div>

        {/* Live Engine Status Badge */}
        <div className={`hidden lg:flex items-center gap-2.5 px-3.5 py-1.5 rounded-full border text-xs font-mono ${isDark
          ? 'bg-[#141416] border-[#242428] text-zinc-300'
          : 'bg-[#F6F5F2] border-[#DCD9D2] text-[#1C1B18]'
          }`}>
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#FF6F32] opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-[#FF6F32]"></span>
          </span>
          <span className="font-medium">AI Dual Engine Active</span>
          <span className={isDark ? 'text-zinc-600' : 'text-zinc-400'}>•</span>
          <span className="text-zinc-400">1.7ms Latency</span>
          <span className={isDark ? 'text-zinc-600' : 'text-zinc-400'}>•</span>
          <span className="text-[#FF6F32] font-medium">Zero Cloud Storage</span>
        </div>

        {/* Action Controls & Theme Toggle */}
        <div className="flex items-center gap-2.5">
          {/* Quick Start / Verification Guide */}
          <button
            onClick={onOpenOnboarding}
            className={`hidden sm:flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl border text-xs font-mono font-medium transition-all ${isDark
              ? 'bg-zinc-900 border-zinc-800 text-zinc-300 hover:text-white hover:border-[#FF6F32]/40'
              : 'bg-[#F6F5F2] border-[#DCD9D2] text-[#1C1B18] hover:text-[#FF6F32]'
              }`}
            title="Choose which threat to verify"
            type="button"
          >
            <Sparkles className="w-3.5 h-3.5 text-[#FF6F32]" />
            <span>Modes</span>
          </button>

          {/* WhatsApp Cyber Shield */}
          <button
            onClick={onOpenWhatsAppModal}
            className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl border text-xs font-mono font-medium transition-all ${isDark
              ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400 hover:bg-emerald-500/20'
              : 'bg-emerald-50 border-emerald-200 text-emerald-700 hover:bg-emerald-100'
              }`}
            title="Verify suspicious WhatsApp messages & forwards"
            type="button"
          >
            <MessageSquare className="w-3.5 h-3.5 text-emerald-500" />
            <span>WhatsApp Shield</span>
          </button>

          {/* Shield Mode Toggle */}
          <button
            onClick={onToggleShieldMode}
            className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-xl border text-xs font-mono font-semibold transition-all ${isShieldMode
              ? 'bg-emerald-500/15 border-emerald-500/40 text-emerald-400'
              : (isDark
                ? 'bg-zinc-900 border-zinc-800 text-zinc-400 hover:text-zinc-200'
                : 'bg-[#F6F5F2] border-[#DCD9D2] text-zinc-600 hover:text-zinc-900')
              }`}
            title={isShieldMode ? 'Switch back to Forensic HUD' : 'Switch to High-Clarity Shield Mode'}
            type="button"
          >
            <Shield className="w-3.5 h-3.5 text-emerald-500" />
            <span className="hidden sm:inline">{isShieldMode ? 'Shield: Active' : 'Shield Mode'}</span>
          </button>

          {/* Light / Dark Mode Toggle Button */}
          <button
            onClick={onToggleTheme}
            className={`p-2 rounded-xl border transition-all ${isDark
              ? 'bg-[#141416] border-[#242428] text-zinc-300 hover:text-white hover:border-zinc-700'
              : 'bg-[#F6F5F2] border-[#DCD9D2] text-[#1C1B18] hover:text-[#FF6F32] hover:border-[#FF6F32]/40'
              }`}
            title={isDark ? 'Switch to Soothing Light Mode' : 'Switch to Midnight Dark Mode'}
            type="button"
          >
            {isDark ? (
              <Sun className="w-4 h-4 text-amber-400" />
            ) : (
              <Moon className="w-4 h-4 text-[#1C1B18]" />
            )}
          </button>

          {/* Emergency 1930 Helpline Button */}
          <a
            href="tel:1930"
            className={`hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-semibold transition-all ${isDark
              ? 'bg-zinc-900 border-zinc-800 text-zinc-300 hover:border-[#FF6F32]/50 hover:text-white'
              : 'bg-[#F6F5F2] border-[#DCD9D2] text-[#1C1B18] hover:border-[#FF6F32]/50 hover:text-[#FF6F32]'
              }`}
            title="National Cyber Crime Helpline"
          >
            <PhoneCall className="w-3.5 h-3.5 text-[#FF6F32]" />
            <span>1930</span>
          </a>

          {/* Report Scam Button */}
          <button
            onClick={onOpenReportModal}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-[#FF6F32] hover:bg-[#E55B1F] text-white text-xs font-semibold shadow-[0_2px_10px_rgba(255,111,50,0.25)] transition-all active:scale-95"
            type="button"
          >
            <PlusCircle className="w-3.5 h-3.5" />
            <span>Report Scam</span>
          </button>
        </div>

      </div>
    </header>
  );
}
