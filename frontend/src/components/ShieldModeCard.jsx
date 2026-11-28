import React, { useState } from 'react';
import {
  Shield,
  ShieldCheck,
  ShieldAlert,
  AlertTriangle,
  PhoneCall,
  Share2,
  Sliders,
  Check,
  Info
} from 'lucide-react';

/**
 * Universal Shield Mode Component
 * Designed for all users seeking crystal-clear, high-legibility fraud signals:
 * 🟢 SAFE SIGNAL: No suspicious indicators detected. Still exercise caution.
 * 🟡 BE CAREFUL: Some suspicious characteristics detected.
 * 🔴 POSSIBLE SCAM: Do not click links or share personal information.
 */
export function ShieldModeCard({ result, onSwitchToForensic, isDark }) {
  const [copiedFamily, setCopiedFamily] = useState(false);

  // Standby State — Neutral Waiting Screen (Never claim "Safe" before scanning!)
  if (!result) {
    return (
      <div className={`rounded-2xl border p-6 lg:p-7 shadow-xl space-y-5 transition-all duration-200 ${
        isDark ? 'bg-[#141416] border-[#242428]' : 'bg-[#F6F5F2] border-[#DCD9D2]'
      }`}>
        {/* Top Header & Switcher */}
        <div className="flex items-center justify-between pb-3 border-b border-zinc-500/20">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-zinc-400"></span>
            <span className="text-xs font-mono font-bold tracking-wider uppercase text-zinc-400">
              Universal Shield
            </span>
          </div>
          <button
            type="button"
            onClick={onSwitchToForensic}
            className={`text-xs font-mono px-3 py-1 rounded-lg border flex items-center gap-1.5 transition-colors ${
              isDark ? 'border-zinc-700 text-zinc-300 hover:bg-zinc-800' : 'border-zinc-300 text-zinc-700 hover:bg-zinc-200'
            }`}
            title="Switch to Pro Forensic HUD"
          >
            <Sliders className="w-3.5 h-3.5" />
            Pro Forensic HUD
          </button>
        </div>

        {/* Neutral Standby Card — Clearly awaiting user input */}
        <div className={`p-6 rounded-2xl border text-center space-y-3 ${
          isDark ? 'bg-[#1C1C20] border-[#2C2C32]' : 'bg-[#ECEAE5] border-[#DCD9D2]'
        }`}>
          <div className="w-16 h-16 mx-auto rounded-full bg-zinc-500/10 flex items-center justify-center">
            <Shield className="w-9 h-9 text-zinc-400" />
          </div>
          <div className="space-y-1">
            <h2 className={`text-xl font-bold tracking-tight ${isDark ? 'text-white' : 'text-[#1C1B18]'}`}>
              Universal Shield Ready
            </h2>
            <p className="text-xs font-medium text-zinc-400">
              Awaiting message to evaluate
            </p>
          </div>
          <p className="text-xs text-zinc-400 max-w-sm mx-auto leading-relaxed">
            Enter, paste, or copy any SMS, WhatsApp message, or email on the left to verify if it is safe or a scam.
          </p>
          <div className="pt-2 flex items-center justify-center gap-2 text-[11px] font-mono text-zinc-500">
            <span className="w-2 h-2 rounded-full bg-[#FF6F32] animate-pulse"></span>
            <span>3-Signal High-Clarity Engine Ready</span>
          </div>
        </div>

        {/* Emergency Helpline Link */}
        <div className="pt-1">
          <a
            href="tel:1930"
            className="w-full py-2.5 px-4 rounded-xl border text-xs font-semibold font-mono flex items-center justify-center gap-2 transition-all text-zinc-400 hover:text-white hover:border-red-500/50"
          >
            <PhoneCall className="w-3.5 h-3.5 text-red-500" />
            <span>National Cyber Crime Helpline: 1930</span>
          </a>
        </div>
      </div>
    );
  }

  // Active Scan Analysis
  const riskScore = Number(result.riskScore || 0);
  const verdict = (result.verdict || '').toUpperCase();
  const badges = result.badges || [];
  const explanation = result.explanation || '';
  const textPreview = result.textPreview || '';

  // Cooldown / Rate-Limited State (Never falsely mark as Safe)
  if (verdict === 'RATE_LIMITED') {
    return (
      <div className={`rounded-2xl border p-6 lg:p-7 shadow-xl space-y-4 transition-all ${
        isDark ? 'bg-[#141416] border-[#242428]' : 'bg-[#F6F5F2] border-[#DCD9D2]'
      }`}>
        <div className="flex items-center gap-2">
          <span className="w-2.5 h-2.5 rounded-full bg-amber-400 animate-ping"></span>
          <span className="text-xs font-mono font-bold tracking-wider uppercase text-amber-400">
            Scanning Cooldown
          </span>
        </div>
        <div className="text-center py-6 space-y-2">
          <p className="text-lg font-bold text-amber-400">⏳ Please Wait A Moment</p>
          <p className="text-xs text-zinc-400">Anti-spam buffer active to maintain AI detection precision.</p>
        </div>
      </div>
    );
  }

  // 3 Clear Universal Outcomes
  const isScam = riskScore >= 50 || verdict === 'CRITICAL' || verdict === 'HIGH';
  const isCareful = !isScam && (riskScore >= 20 || verdict === 'LOW' || verdict === 'MEDIUM');
  const isSafe = !isScam && !isCareful && verdict !== 'RATE_LIMITED';

  let signalConfig = {
    title: 'SAFE SIGNAL',
    subtext: 'No suspicious indicators detected. Still exercise caution.',
    badgeClass: 'bg-emerald-500/15 text-emerald-500 border-emerald-500/30',
    cardBg: isDark ? 'bg-emerald-950/20 border-emerald-500/30' : 'bg-emerald-50 border-emerald-300',
    icon: <ShieldCheck className="w-12 h-12 text-emerald-500" />,
    heading: 'You are protected!',
    statusLabel: 'No malicious pattern was triggered.',
    textColor: 'text-emerald-500'
  };

  if (isScam) {
    signalConfig = {
      title: 'POSSIBLE SCAM',
      subtext: 'Do not click links, share OTPs, or pay any money.',
      badgeClass: 'bg-red-500/15 text-red-500 border-red-500/30',
      cardBg: isDark ? 'bg-red-950/20 border-red-500/30' : 'bg-red-50 border-red-300',
      icon: <ShieldAlert className="w-12 h-12 text-red-500 animate-pulse" />,
      heading: 'Possible Scam Detected!',
      statusLabel: 'High probability of fraud. Immediate caution required.',
      textColor: 'text-red-500'
    };
  } else if (isCareful) {
    signalConfig = {
      title: 'BE CAREFUL',
      subtext: 'Some suspicious characteristics detected. Verify independently.',
      badgeClass: 'bg-amber-500/15 text-amber-500 border-amber-500/30',
      cardBg: isDark ? 'bg-amber-950/20 border-amber-500/30' : 'bg-amber-50 border-amber-300',
      icon: <AlertTriangle className="w-12 h-12 text-amber-500" />,
      heading: 'Caution Recommended',
      statusLabel: 'Unverified sender or urgency markers detected.',
      textColor: 'text-amber-500'
    };
  }

  // Simplified plain-English reason
  let simpleExplanation = explanation;
  if (!simpleExplanation || simpleExplanation.includes('No known fraud') || simpleExplanation.includes('No malicious patterns')) {
    simpleExplanation = isScam
      ? (badges.length > 0
          ? `The message asks for sensitive details or urges immediate action (${badges.slice(0, 2).join(', ')}). This is a common trick used by fraudsters.`
          : 'This message shows clear patterns of coercive fraud or impersonation.')
      : isCareful
      ? 'This message contains unfamiliar links or hurried wording. Never reply with passwords or bank details.'
      : 'No threat indicators found. Normal communication patterns detected.';
  }

  const handleAlertFamily = () => {
    const alertMessage = `⚠️ ScamShield Alert: I checked this message using ∀VITR AI and it scored ${riskScore}% [${signalConfig.title}]. Please do not click any link or send money!\n\nMessage preview: "${(textPreview || explanation).slice(0, 100)}..."`;
    
    if (navigator.share) {
      navigator.share({
        title: 'Scam Alert - Please Be Careful',
        text: alertMessage,
        url: window.location.href
      }).catch(() => {
        navigator.clipboard.writeText(alertMessage);
        setCopiedFamily(true);
        setTimeout(() => setCopiedFamily(false), 2500);
      });
    } else {
      const whatsappUrl = `https://api.whatsapp.com/send?text=${encodeURIComponent(alertMessage)}`;
      window.open(whatsappUrl, '_blank');
      setCopiedFamily(true);
      setTimeout(() => setCopiedFamily(false), 2500);
    }
  };

  return (
    <div className={`rounded-2xl border p-6 lg:p-7 shadow-xl space-y-5 transition-all duration-200 ${
      isDark ? 'bg-[#141416] border-[#242428]' : 'bg-[#F6F5F2] border-[#DCD9D2]'
    }`}>
      {/* Top Controls: Mode Switcher */}
      <div className="flex items-center justify-between pb-3 border-b border-zinc-500/20">
        <div className="flex items-center gap-2">
          <span className={`w-2.5 h-2.5 rounded-full ${isScam ? 'bg-red-500' : isCareful ? 'bg-amber-500' : 'bg-emerald-500'}`}></span>
          <span className="text-xs font-mono font-bold tracking-wider uppercase text-zinc-400">
            Universal Shield View
          </span>
        </div>
        <button
          type="button"
          onClick={onSwitchToForensic}
          className={`text-xs font-mono px-3 py-1 rounded-lg border flex items-center gap-1.5 transition-colors ${
            isDark ? 'border-zinc-700 text-zinc-300 hover:bg-zinc-800' : 'border-zinc-300 text-zinc-700 hover:bg-zinc-200'
          }`}
          title="Switch to advanced forensic HUD with raw metrics and case tokens"
        >
          <Sliders className="w-3.5 h-3.5" />
          Pro Forensic HUD
        </button>
      </div>

      {/* Main Signal Banner */}
      <div className={`p-6 rounded-2xl border text-center space-y-3 transition-colors ${signalConfig.cardBg}`}>
        <div className="flex justify-center">
          {signalConfig.icon}
        </div>
        <div>
          <span className={`inline-block text-xs font-mono font-extrabold px-3 py-1 rounded-full border mb-1.5 ${signalConfig.badgeClass}`}>
            ● {signalConfig.title}
          </span>
          <h2 className={`text-2xl font-black tracking-tight ${isDark ? 'text-white' : 'text-[#1C1B18]'}`}>
            {signalConfig.heading}
          </h2>
          <p className="text-sm font-medium mt-1 text-zinc-400">
            {signalConfig.subtext}
          </p>
        </div>

        {/* Telemetry bullets for clarity */}
        <div className="pt-2 text-xs font-mono text-zinc-400 space-y-0.5">
          {isScam ? (
            <>
              <div className="text-red-400 font-semibold">● Threat Score: {riskScore}% (High Threat)</div>
              <div>● Action: Block sender immediately • Do not reply</div>
            </>
          ) : isCareful ? (
            <>
              <div className="text-amber-400 font-semibold">● Threat Score: {riskScore}% (Suspicious)</div>
              <div>● Action: Verify sender identity independently</div>
            </>
          ) : (
            <>
              <div className="text-emerald-400 font-semibold">● Threat Score: {riskScore}% (Safe)</div>
              <div>● 0 malicious signatures triggered</div>
            </>
          )}
        </div>
      </div>

      {/* Identified Markers if Scam */}
      {badges && badges.length > 0 && isScam && (
        <div className="space-y-1.5">
          <span className="text-[11px] font-mono uppercase tracking-wider text-zinc-400 block">
            Identified Threat Markers:
          </span>
          <div className="flex flex-wrap gap-1.5">
            {badges.map((b, idx) => (
              <span
                key={idx}
                className="text-xs font-mono px-2.5 py-0.5 rounded-full bg-red-500/10 text-red-400 border border-red-500/20 font-medium"
              >
                [{b}]
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Simple Explanation for All Users */}
      <div className={`p-4 rounded-xl border space-y-2 ${
        isDark ? 'bg-[#0C0C0C] border-[#242428]' : 'bg-[#ECEAE5] border-[#DCD9D2]'
      }`}>
        <div className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wider text-zinc-400">
          <Info className="w-4 h-4 text-[#FF6F32]" />
          <span>Why this matters:</span>
        </div>
        <p className={`text-sm leading-relaxed ${isDark ? 'text-zinc-200' : 'text-[#1C1B18]'}`}>
          {simpleExplanation}
        </p>
      </div>

      {/* 2 Primary Big Action Buttons */}
      <div className="space-y-3 pt-2">
        <button
          type="button"
          onClick={handleAlertFamily}
          className="w-full py-3.5 px-4 rounded-xl bg-amber-500 hover:bg-amber-600 text-white font-bold text-sm flex items-center justify-center gap-2.5 transition-all shadow-md active:scale-95"
        >
          {copiedFamily ? (
            <>
              <Check className="w-5 h-5" />
              <span>Warning Copied / Shared!</span>
            </>
          ) : (
            <>
              <Share2 className="w-5 h-5" />
              <span>Alert a Family Member or Friend</span>
            </>
          )}
        </button>

        <a
          href="tel:1930"
          className="w-full py-3.5 px-4 rounded-xl bg-red-600 hover:bg-red-700 text-white font-bold text-sm flex items-center justify-center gap-2.5 transition-all shadow-md active:scale-95"
        >
          <PhoneCall className="w-5 h-5" />
          <span>Emergency: Call 1930 Cyber Helpline</span>
        </a>
      </div>

      {/* Reassurance Footer */}
      <div className="text-center text-[10px] text-zinc-500 font-mono pt-1">
        ScamShield AI • Verified on-device privacy • Free for public safety
      </div>
    </div>
  );
}
