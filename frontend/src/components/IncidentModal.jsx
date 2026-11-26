import React, { useState } from 'react';
import { 
  X, 
  MapPin, 
  Clock, 
  Copy, 
  Check, 
  ArrowRight, 
  Terminal, 
  AlertTriangle, 
  Info 
} from 'lucide-react';

export function IncidentModal({ scam, onClose, onLoadScenario, themeMode }) {
  const [copied, setCopied] = useState(false);

  if (!scam) return null;

  const isDark = themeMode === 'midnight';
  const isCyber = themeMode === 'cyber';
  const isSoothing = themeMode === 'soothing';

  const accentColor = isCyber ? '#E5A83C' : '#FF6F32';
  const modalBg = isCyber ? 'bg-[#110D26] border-[#2A1F52] text-white' : isDark ? 'bg-[#141416] border-[#242428] text-white' : 'bg-[#F6F5F2] border-[#DCD9D2] text-[#1C1B18]';
  const innerBg = isCyber ? 'bg-[#080614] border-[#2A1F52]' : isDark ? 'bg-[#0C0C0C] border-[#242428]' : 'bg-[#ECEAE5] border-[#DCD9D2]';

  const handleCopySummary = () => {
    const textToCopy = `[SCAM ALERT] ${scam.title}\nCategory: ${scam.category}\nThreat Severity: ${scam.riskScore}%\nRegion: ${scam.region}\n\nAttack Vector:\n${scam.attackVector}\n\nOfficial Advisory:\n${scam.advisory}`;
    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleLoadAndClose = () => {
    onLoadScenario(scam.samplePayload);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-black/85 backdrop-blur-md">
      <div 
        className={`relative w-full max-w-2xl max-h-[90vh] overflow-y-auto rounded-2xl border shadow-2xl p-6 space-y-5 transition-colors ${modalBg}`}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <button
          onClick={onClose}
          className={`absolute top-4 right-4 p-2 rounded-xl transition-colors ${
            isCyber ? 'bg-[#181238] text-violet-200 hover:text-white' : isDark ? 'bg-[#18181B] text-zinc-400 hover:text-white' : 'bg-[#ECEAE5] text-[#1C1B18] hover:text-[#FF6F32]'
          }`}
        >
          <X className="w-5 h-5" />
        </button>

        {/* Modal Header & Hero */}
        <div className="space-y-3">
          <div className="flex flex-wrap items-center gap-2">
            <span 
              className="text-xs font-mono font-bold px-2.5 py-0.5 rounded-full border"
              style={{
                backgroundColor: `${accentColor}1A`,
                color: accentColor,
                borderColor: `${accentColor}4D`
              }}
            >
              {scam.riskScore}% SEVERITY • {scam.severity}
            </span>
            <span className="text-xs text-zinc-400 font-mono flex items-center gap-1">
              <MapPin className="w-3.5 h-3.5" style={{ color: accentColor }} />
              {scam.region}
            </span>
          </div>

          <h2 className={`text-xl sm:text-2xl font-bold leading-tight ${isSoothing ? 'text-[#1C1B18]' : 'text-white'}`}>
            {scam.title}
          </h2>

          <div className="flex items-center gap-3 text-xs text-zinc-400 font-mono">
            <span className="flex items-center gap-1">
              <Clock className="w-3.5 h-3.5" />
              {scam.timeAgo}
            </span>
            <span>•</span>
            <span className="font-semibold" style={{ color: accentColor }}>
              {scam.incidentCount} incidents reported today
            </span>
          </div>
        </div>

        {/* Hero Visual Thumbnail */}
        <div className="relative w-full h-48 sm:h-56 rounded-xl overflow-hidden border border-zinc-800 bg-zinc-950">
          <img 
            src={scam.imageUrl} 
            alt={scam.title} 
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent"></div>
        </div>

        {/* Detailed Attack Vector Breakdown */}
        <div className="space-y-2">
          <h4 className="text-xs font-mono uppercase tracking-wider text-zinc-400 flex items-center gap-1.5">
            <Terminal className="w-4 h-4" style={{ color: accentColor }} />
            <span>Modus Operandi & Psychological Exploitation:</span>
          </h4>
          <p className={`text-sm leading-relaxed p-3.5 rounded-xl border ${innerBg}`}>
            {scam.attackVector}
          </p>
        </div>

        {/* Attacker IOCs */}
        {scam.iocs && scam.iocs.length > 0 && (
          <div className="space-y-2">
            <h4 className="text-xs font-mono uppercase tracking-wider text-zinc-400 flex items-center gap-1.5">
              <AlertTriangle className="w-4 h-4 text-amber-500" />
              <span>Flagged Attacker Identifiers (Redacted IOCs):</span>
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
              {scam.iocs.map((ioc, idx) => (
                <div key={idx} className={`p-2.5 rounded-xl border font-mono text-xs ${innerBg}`}>
                  <span className="text-zinc-500 block text-[10px] uppercase">{ioc.type}</span>
                  <span className="font-semibold truncate block mt-0.5" style={{ color: accentColor }}>{ioc.value}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Official Advisory */}
        <div className="p-3.5 rounded-xl border space-y-1 bg-amber-500/10 border-amber-500/30">
          <div className="flex items-center gap-1.5 text-xs font-mono font-semibold text-amber-500">
            <Info className="w-4 h-4 text-amber-500" />
            <span>Official Cyber Defense & Police Advisory:</span>
          </div>
          <p className="text-xs leading-relaxed text-amber-200/90">
            {scam.advisory}
          </p>
        </div>

        {/* Actions: Load into Scanner & Copy Alert */}
        <div className={`pt-2 flex flex-col sm:flex-row items-center gap-2.5 border-t ${
          isCyber ? 'border-[#2A1F52]' : isDark ? 'border-[#242428]' : 'border-[#DCD9D2]'
        }`}>
          <button
            onClick={handleLoadAndClose}
            className="w-full sm:flex-1 py-3 px-4 rounded-xl font-bold text-xs flex items-center justify-center gap-2 shadow-lg transition-all active:scale-95"
            style={{
              backgroundColor: accentColor,
              color: isCyber ? '#080614' : '#FFFFFF'
            }}
          >
            <span>⚡ Load this Case into Threat Scanner</span>
            <ArrowRight className="w-4 h-4" />
          </button>

          <button
            onClick={handleCopySummary}
            className={`w-full sm:w-auto py-3 px-4 rounded-xl font-medium text-xs font-mono flex items-center justify-center gap-2 border transition-all ${
              isCyber
                ? 'bg-[#181238] border-[#312563] text-violet-200 hover:text-white'
                : isDark 
                ? 'bg-[#18181B] border-[#27272A] text-zinc-300 hover:text-white' 
                : 'bg-[#ECEAE5] border-[#DCD9D2] text-[#1C1B18] hover:text-[#FF6F32]'
            }`}
          >
            {copied ? (
              <>
                <Check className="w-4 h-4 text-emerald-500" />
                <span>Copied Advisory</span>
              </>
            ) : (
              <>
                <Copy className="w-4 h-4" />
                <span>Copy Alert Text</span>
              </>
            )}
          </button>
        </div>

      </div>
    </div>
  );
}
