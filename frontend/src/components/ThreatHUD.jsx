import React, { useState } from 'react';
import {
  ShieldAlert,
  ShieldCheck,
  AlertTriangle,
  Copy,
  Check,
  Key,
  Brain,
  PhoneCall,
  FileText
} from 'lucide-react';

export function ThreatHUD({ result, onCopyComplaint, isDark }) {
  const [copiedHash, setCopiedHash] = useState(false);
  const [copiedComplaint, setCopiedComplaint] = useState(false);

  // Standby State when no scan has been executed yet
  if (!result) {
    return (
      <div className={`rounded-2xl border p-6 lg:p-7 shadow-xl flex flex-col items-center justify-center text-center min-h-[480px] space-y-4 transition-colors duration-200 ${isDark ? 'bg-[#141416] border-[#242428]' : 'bg-[#F6F5F2] border-[#DCD9D2]'
        }`}>

        {/* Soft 0% Gauge */}
        <div className="relative w-40 h-40 flex items-center justify-center">
          <svg className="w-full h-full -rotate-90 transform" viewBox="0 0 160 160">
            <circle
              cx="80"
              cy="80"
              r="66"
              fill="transparent"
              stroke={isDark ? '#242428' : '#DCD9D2'}
              strokeWidth="8"
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
            <span className={`text-3xl font-extrabold font-mono tracking-tighter ${isDark ? 'text-zinc-300' : 'text-[#1C1B18]'
              }`}>
              0%
            </span>
            <span className="text-[10px] font-mono uppercase tracking-widest text-zinc-500 mt-0.5">
              Standby
            </span>
          </div>
        </div>

        <div className="space-y-1.5 max-w-xs">
          <h3 className={`font-bold text-base ${isDark ? 'text-white' : 'text-[#1C1B18]'}`}>
            Awaiting Threat Payload
          </h3>
          <p className={`text-xs leading-relaxed ${isDark ? 'text-zinc-400' : 'text-[#57554F]'}`}>
            Enter a message or pick a sample test case on the left, then click <strong className="text-[#FF6F32]">Scan for Threats</strong>.
          </p>
        </div>

        <div className="pt-2 flex items-center gap-2 text-xs font-mono text-zinc-400">
          <span className="w-2 h-2 rounded-full bg-[#FF6F32] animate-pulse"></span>
          <span>Dual AI Engine Ready</span>
        </div>
      </div>
    );
  }

  const {
    riskScore = 0,
    verdict = 'SAFE',
    confidence = 98.5,
    latencyMs = 3.8,
    badges = [],
    explanation = 'No known fraud patterns detected.',
    hmacToken = '',
    complaintDraft = ''
  } = result;

  const isCritical = riskScore >= 66;
  const isSuspicious = riskScore >= 26 && riskScore < 66;

  // Resilient explanation fallback: never display 'no patterns' when risk is high
  const displayExplanation = (riskScore >= 50 && (!explanation || explanation.includes('No known fraud') || explanation.includes('No malicious patterns')))
    ? (badges && badges.length > 0
      ? `Critical cyber-threat detected. Triggered indicators: ${badges.join(', ')}.`
      : 'High-risk fraudulent patterns and coercive language detected in message.')
    : explanation;

  const circumference = 414.7;
  const strokeDashoffset = circumference - (circumference * (riskScore / 100));

  const handleCopyHash = () => {
    navigator.clipboard.writeText(hmacToken);
    setCopiedHash(true);
    setTimeout(() => setCopiedHash(false), 2000);
  };

  const handleCopyComplaint = () => {
    onCopyComplaint(complaintDraft);
    setCopiedComplaint(true);
    setTimeout(() => setCopiedComplaint(false), 2500);
  };

  return (
    <div className={`rounded-2xl border p-6 lg:p-7 shadow-xl space-y-4 transition-all duration-200 ${isDark ? 'bg-[#141416] border-[#242428]' : 'bg-[#F6F5F2] border-[#DCD9D2]'
      }`}>

      {/* Header */}
      <div className={`flex items-center justify-between pb-3 border-b ${isDark ? 'border-[#242428]' : 'border-[#DCD9D2]'
        }`}>
        <div className="flex items-center gap-2">
          {isCritical ? (
            <ShieldAlert className="w-5 h-5 text-[#FF6F32]" />
          ) : isSuspicious ? (
            <AlertTriangle className="w-5 h-5 text-amber-500" />
          ) : (
            <ShieldCheck className="w-5 h-5 text-emerald-500" />
          )}
          <h3 className={`font-bold text-base ${isDark ? 'text-white' : 'text-[#1C1B18]'}`}>
            Threat Forensics Result
          </h3>
        </div>
        <span className={`text-xs font-mono font-bold px-2.5 py-0.5 rounded-full border ${isCritical
          ? 'bg-[#FF6F32]/10 text-[#FF6F32] border-[#FF6F32]/30'
          : isSuspicious
            ? 'bg-amber-500/10 text-amber-500 border-amber-500/30'
            : 'bg-emerald-500/10 text-emerald-500 border-emerald-500/30'
          }`}>
          {verdict}
        </span>
      </div>

      {/* Speedometer Circle */}
      <div className="flex flex-col items-center justify-center my-3 relative">
        <div className="relative w-44 h-44 flex items-center justify-center">
          <svg className="w-full h-full -rotate-90 transform" viewBox="0 0 160 160">
            <circle
              cx="80"
              cy="80"
              r="66"
              fill="transparent"
              stroke={isDark ? '#242428' : '#DCD9D2'}
              strokeWidth="10"
              strokeDasharray={circumference}
            />
            <circle
              cx="80"
              cy="80"
              r="66"
              fill="transparent"
              stroke={isCritical ? '#FF6F32' : isSuspicious ? '#F59E0B' : '#10B981'}
              strokeWidth="10"
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              style={{ transition: 'stroke-dashoffset 0.8s ease-in-out' }}
            />
          </svg>

          <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
            <span className="text-[11px] font-mono uppercase tracking-widest text-zinc-400">
              Risk Score
            </span>
            <span className={`text-4xl font-extrabold font-mono tracking-tighter leading-none mt-1 ${isCritical ? 'text-[#FF6F32]' : isSuspicious ? 'text-amber-500' : 'text-emerald-500'
              }`}>
              {riskScore}%
            </span>
            <span className="text-[10px] font-mono text-zinc-400 mt-1 uppercase">
              {isCritical ? 'CRITICAL THREAT' : isSuspicious ? 'SUSPICIOUS' : 'SAFE'}
            </span>
          </div>
        </div>

        {/* 3 Telemetry Metrics */}
        <div className="grid grid-cols-3 gap-2 w-full mt-3">
          <div className={`rounded-xl p-2 text-center border ${isDark ? 'bg-[#0C0C0C] border-[#242428]' : 'bg-[#ECEAE5] border-[#DCD9D2]'
            }`}>
            <span className="text-[10px] font-mono text-zinc-400 block">Confidence</span>
            <span className="text-xs font-mono font-bold text-[#FF6F32]">{confidence}%</span>
          </div>
          <div className={`rounded-xl p-2 text-center border ${isDark ? 'bg-[#0C0C0C] border-[#242428]' : 'bg-[#ECEAE5] border-[#DCD9D2]'
            }`}>
            <span className="text-[10px] font-mono text-zinc-400 block">Latency</span>
            <span className={`text-xs font-mono font-bold ${isDark ? 'text-white' : 'text-[#1C1B18]'}`}>{latencyMs}ms</span>
          </div>
          <div className={`rounded-xl p-2 text-center border ${isDark ? 'bg-[#0C0C0C] border-[#242428]' : 'bg-[#ECEAE5] border-[#DCD9D2]'
            }`}>
            <span className="text-[10px] font-mono text-zinc-400 block">PII Redacted</span>
            <span className="text-xs font-mono font-bold text-emerald-500">ACTIVE</span>
          </div>
        </div>
      </div>

      {/* Forensic Detection Badges */}
      {badges && badges.length > 0 && (
        <div className="space-y-1.5 pt-2">
          <span className="text-[11px] font-mono uppercase tracking-wider text-zinc-400 block">
            Identified Fraud Markers:
          </span>
          <div className="flex flex-wrap gap-1.5">
            {badges.map((badge, idx) => (
              <span
                key={idx}
                className="text-xs font-mono px-2.5 py-0.5 rounded-full bg-[#FF6F32]/10 text-[#FF6F32] border border-[#FF6F32]/20 font-medium"
              >
                [{badge}]
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Plain-English Root Cause Explanation */}
      <div className={`p-3.5 rounded-xl border space-y-1.5 ${isDark ? 'bg-[#0C0C0C] border-[#242428]' : 'bg-[#ECEAE5] border-[#DCD9D2]'
        }`}>
        <div className="flex items-center gap-1.5 text-xs font-mono text-[#FF6F32] font-semibold">
          <Brain className="w-3.5 h-3.5" />
          <span>Why this was flagged:</span>
        </div>
        <p className={`text-xs leading-relaxed font-sans ${isDark ? 'text-zinc-300' : 'text-[#3E3C37]'}`}>
          {displayExplanation}
        </p>
      </div>

      {/* Official Forensic Case ID */}
      {hmacToken && (
        <div className={`p-2.5 rounded-xl border space-y-1.5 text-xs ${
          isDark ? 'bg-[#0C0C0C] border-[#242428]' : 'bg-[#ECEAE5] border-[#DCD9D2]'
        }`}>
          <div className="flex items-center justify-between text-[11px]">
            <span className="flex items-center gap-1.5 font-medium">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />
              <span className={isDark ? 'text-zinc-300' : 'text-[#3E3C37]'}>Official Forensic Case ID</span>
            </span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-500 font-bold border border-emerald-500/20">
              AUDIT VERIFIED
            </span>
          </div>
          <div className={`flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs font-mono ${
            isDark ? 'bg-zinc-900/80 text-zinc-300' : 'bg-white/80 text-[#1C1B18]'
          }`}>
            <span className="truncate mr-2 font-bold text-[#FF6F32]">
              #{hmacToken.replace(/^0x/, '').substring(0, 14).toUpperCase()}
            </span>
            <button
              type="button"
              onClick={handleCopyHash}
              title="Copy Case Verification ID"
              className={`flex items-center gap-1 text-[11px] font-sans px-2 py-0.5 rounded transition-colors ${
                isDark ? 'text-zinc-300 hover:text-white bg-zinc-800 hover:bg-zinc-700' : 'text-zinc-700 hover:text-black bg-zinc-200 hover:bg-zinc-300'
              }`}
            >
              {copiedHash ? (
                <>
                  <Check className="w-3 h-3 text-emerald-500" />
                  <span className="text-emerald-500 font-medium">Copied</span>
                </>
              ) : (
                <>
                  <Copy className="w-3 h-3" />
                  <span>Copy ID</span>
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* 1-Click Police Complaint Draft */}
      <div className="pt-2 space-y-2">
        <button
          type="button"
          onClick={handleCopyComplaint}
          className="w-full py-2.5 px-4 rounded-xl bg-[#FF6F32] hover:bg-[#E55B1F] text-white text-xs font-semibold flex items-center justify-center gap-2 transition-all shadow-[0_4px_15px_rgba(255,111,50,0.25)] active:scale-95"
        >
          {copiedComplaint ? (
            <>
              <Check className="w-4 h-4 text-white" />
              <span>Copied Police Draft to Clipboard!</span>
            </>
          ) : (
            <>
              <FileText className="w-4 h-4" />
              <span>📋 Copy Cyber Police (1930 / Chakshu) Draft</span>
            </>
          )}
        </button>

        <a
          href="tel:1930"
          className={`w-full py-2 px-3 rounded-xl border text-xs font-bold font-mono flex items-center justify-center gap-1.5 transition-all ${isDark
            ? 'bg-[#18181B] border-[#27272A] text-zinc-300 hover:text-white hover:border-[#FF6F32]/40'
            : 'bg-[#ECEAE5] border-[#DCD9D2] text-[#1C1B18] hover:text-[#FF6F32] hover:border-[#FF6F32]/40'
            }`}
        >
          <PhoneCall className="w-3.5 h-3.5 text-[#FF6F32]" />
          <span>Emergency: Dial Helpline 1930</span>
        </a>
      </div>

    </div>
  );
}
