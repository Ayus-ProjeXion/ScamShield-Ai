import React, { useState } from 'react';
import {
  MessageSquare,
  Mail,
  Mic,
  Camera,
  Shield,
  X,
  Sparkles,
  ArrowRight
} from 'lucide-react';

export function OnboardingModal({ isOpen, onClose, onSelectOption, isDark }) {
  const [dontShowAgain, setDontShowAgain] = useState(false);

  if (!isOpen) return null;

  const handleSelect = (optionKey) => {
    if (dontShowAgain) {
      localStorage.setItem('scamshield_hide_welcome', 'true');
    }
    onSelectOption(optionKey);
    onClose();
  };

  const options = [
    {
      key: 'text',
      title: 'SMS or WhatsApp Message',
      desc: 'Verify bank freeze alerts, electricity cut-offs, OTP requests, or lottery links.',
      icon: <MessageSquare className="w-5 h-5 text-[#FF6F32]" />,
      badge: 'Dual ML + Heuristics'
    },
    {
      key: 'email',
      title: 'Suspicious Email / Phishing',
      desc: 'Inspect RFC sender spoofing, fake corporate invoices, and malicious attachments.',
      icon: <Mail className="w-5 h-5 text-blue-500" />,
      badge: 'Domain & Header Audit'
    },
    {
      key: 'audio',
      title: 'Voice Call / Audio Recording',
      desc: 'Analyze threatening voice calls (CBI, Police, Digital Arrest, Customs duty coercion).',
      icon: <Mic className="w-5 h-5 text-purple-500" />,
      badge: 'Voice STT AI'
    },
    {
      key: 'screenshot',
      title: 'Screenshot / Payment QR (OCR)',
      desc: 'Upload a WhatsApp screenshot or QR flyer for on-device WASM text extraction.',
      icon: <Camera className="w-5 h-5 text-emerald-500" />,
      badge: 'Client-Side OCR'
    },
    {
      key: 'shield',
      title: 'Universal Shield Mode',
      desc: 'Simplified high-clarity 3-signal view (🟢 SAFE, 🟡 CAUTION, 🔴 SCAM) for quick decisions.',
      icon: <Shield className="w-5 h-5 text-amber-500" />,
      badge: 'High Clarity'
    }
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-in fade-in duration-200">
      <div className={`relative w-full max-w-xl rounded-2xl border p-6 md:p-8 shadow-2xl space-y-6 max-h-[90vh] overflow-y-auto transition-all ${
        isDark ? 'bg-[#141416] border-[#242428] text-white' : 'bg-[#FDFCFA] border-[#DCD9D2] text-[#1C1B18]'
      }`}>
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-xl text-zinc-400 hover:text-white hover:bg-zinc-800 transition-colors"
          title="Close"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header */}
        <div className="space-y-2">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-mono font-semibold bg-[#FF6F32]/10 text-[#FF6F32] border border-[#FF6F32]/20">
            <Sparkles className="w-3.5 h-3.5" />
            <span>∀VITR Threat Intelligence</span>
          </div>
          <h2 className="text-2xl font-black tracking-tight">
            What would you like to verify today?
          </h2>
          <p className="text-sm text-zinc-400">
            Select the threat type you want to analyze. Our multi-modal engine will prepare the exact scanner for you.
          </p>
        </div>

        {/* Options List */}
        <div className="grid grid-cols-1 gap-3">
          {options.map((opt) => (
            <button
              key={opt.key}
              type="button"
              onClick={() => handleSelect(opt.key)}
              className={`w-full p-4 rounded-xl border text-left flex items-start gap-4 transition-all group hover:scale-[1.01] ${
                isDark
                  ? 'bg-[#1C1C20] border-[#2C2C32] hover:border-[#FF6F32] hover:bg-[#222228]'
                  : 'bg-[#F4F2EC] border-[#DCD9D2] hover:border-[#FF6F32] hover:bg-white'
              }`}
            >
              <div className="p-2.5 rounded-xl bg-black/20 flex-shrink-0 group-hover:scale-110 transition-transform">
                {opt.icon}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between gap-2">
                  <span className="font-bold text-sm tracking-tight group-hover:text-[#FF6F32] transition-colors">
                    {opt.title}
                  </span>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-zinc-500/10 text-zinc-400 border border-zinc-500/20 flex-shrink-0">
                    {opt.badge}
                  </span>
                </div>
                <p className="text-xs text-zinc-400 mt-1 line-clamp-2">
                  {opt.desc}
                </p>
              </div>
              <ArrowRight className="w-4 h-4 text-zinc-500 group-hover:text-[#FF6F32] group-hover:translate-x-1 transition-all self-center" />
            </button>
          ))}
        </div>

        {/* Footer with Checkbox */}
        <div className="pt-2 border-t border-zinc-500/20 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-zinc-400">
          <label className="flex items-center gap-2 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={dontShowAgain}
              onChange={(e) => setDontShowAgain(e.target.checked)}
              className="rounded border-zinc-700 text-[#FF6F32] focus:ring-0 w-4 h-4 bg-transparent"
            />
            <span>Don't show this welcome prompt again</span>
          </label>
          <button
            type="button"
            onClick={onClose}
            className="text-xs font-mono hover:underline text-[#FF6F32]"
          >
            Skip to full dashboard →
          </button>
        </div>
      </div>
    </div>
  );
}
