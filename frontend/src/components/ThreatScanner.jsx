import React, { useRef } from 'react';
import {
  MessageSquare,
  Mail,
  Mic,
  Sparkles,
  Eraser,
  ShieldCheck,
  Volume2,
  ArrowRight
} from 'lucide-react';

export const TEST_PRESETS = [
  {
    id: 'electricity',
    name: '⚡ Electricity KYC Scam',
    text: 'URGENT: Your Bijli (Electricity) bill was not updated. Power supply will be disconnected tonight at 09:30 PM by Electricity Officer. Immediately call 9876543210 or install MahaVitaran_Update.apk to verify UPI payment.'
  },
  {
    id: 'digital_arrest',
    name: '🚨 Fake CBI Digital Arrest',
    text: 'FINAL LEGAL WARNING: This is Inspector Ajay Kumar from Mumbai Cyber Crime Cell & CBI Headquarters. A parcel containing 140g MDMA and 5 fake passports in your name has been confiscated at Delhi IGI Airport. You are under immediate Digital Arrest. Do not disconnect this video call or local police will raid your premises.'
  },
  {
    id: 'fedex',
    name: '📦 FedEx Drugs Threat',
    text: 'FedEx Notice: Consignment #FX-884012 on hold at Mumbai Customs. Unregistered overseas shipment requires immediate clearance fee of INR 24,500. Pay to UPI handle customsclear@axis via official gateway within 40 minutes to avoid MHA FIR registration.'
  },
  {
    id: 'safe',
    name: '✅ Safe Bank SMS (0% False Alarm)',
    text: 'Dear Customer, INR 2,500.00 debited from A/C XX1290 on 22-Nov-26 at ATM HDFC001. Available balance is INR 34,210.45. If this transaction was not done by you, call 18002664332.'
  }
];

export function ThreatScanner({
  inputText,
  setInputText,
  activeTab,
  setActiveTab,
  onScan,
  isLoading,
  audioFile,
  setAudioFile,
  isDark
}) {
  const fileInputRef = useRef(null);

  const handlePresetClick = (presetText) => {
    setInputText(presetText);
  };

  const handleKeyDown = (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      onScan();
    }
  };

  const handleAudioUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setAudioFile(file);
    }
  };

  return (
    <div className={`rounded-2xl border p-6 lg:p-7 shadow-xl space-y-5 transition-colors duration-200 ${
      isDark 
        ? 'bg-[#141416] border-[#242428]' 
        : 'bg-[#F6F5F2] border-[#DCD9D2]'
      }`}>

      {/* Station Header */}
      <div className={`flex flex-wrap items-center justify-between gap-3 pb-3 border-b ${
        isDark ? 'border-[#242428]' : 'border-[#DCD9D2]'
      }`}>
        <div className="flex items-center gap-2.5">
          <div className="w-2.5 h-2.5 rounded-full bg-[#FF6F32]"></div>
          <h2 className={`text-lg font-bold tracking-tight ${isDark ? 'text-white' : 'text-[#1C1B18]'}`}>
            Threat Analysis Console
          </h2>
        </div>

        <span className="text-xs font-mono text-zinc-400 flex items-center gap-1.5">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
          <span>Local Privacy Protected</span>
        </span>
      </div>

      {/* 3 Real Modality Tabs */}
      <div className={`grid grid-cols-3 gap-1.5 p-1.5 rounded-xl border ${
        isDark 
          ? 'bg-[#0C0C0C] border-[#242428]' 
          : 'bg-[#ECEAE5] border-[#DCD9D2]'
        }`}>
        <button
          type="button"
          onClick={() => setActiveTab('text')}
          className={`flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs font-semibold transition-all ${
            activeTab === 'text'
              ? 'bg-[#FF6F32] text-white shadow-sm'
              : isDark 
                ? 'text-zinc-400 hover:text-white hover:bg-zinc-900' 
                : 'text-[#57554F] hover:text-[#1C1B18] hover:bg-[#F6F5F2]'
            }`}
        >
          <MessageSquare className="w-3.5 h-3.5" />
          <span>SMS</span>
        </button>

        <button
          type="button"
          onClick={() => setActiveTab('email')}
          className={`flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs font-semibold transition-all ${
            activeTab === 'email'
              ? 'bg-[#FF6F32] text-white shadow-sm'
              : isDark 
                ? 'text-zinc-400 hover:text-white hover:bg-zinc-900' 
                : 'text-[#57554F] hover:text-[#1C1B18] hover:bg-[#F6F5F2]'
            }`}
        >
          <Mail className="w-3.5 h-3.5" />
          <span>Email (.eml)</span>
        </button>

        <button
          type="button"
          onClick={() => setActiveTab('audio')}
          className={`flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs font-semibold transition-all ${
            activeTab === 'audio'
              ? 'bg-[#FF6F32] text-white shadow-sm'
              : isDark 
                ? 'text-zinc-400 hover:text-white hover:bg-zinc-900' 
                : 'text-[#57554F] hover:text-[#1C1B18] hover:bg-[#F6F5F2]'
            }`}
        >
          <Mic className="w-3.5 h-3.5" />
          <span>Voice Call (.wav)</span>
        </button>
      </div>

      {/* Quick Test Preset Buttons */}
      <div className="space-y-2">
        <div className="flex items-center justify-between text-xs text-zinc-400 font-mono">
          <span className="flex items-center gap-1.5">
            <Sparkles className="w-3 h-3 text-[#FF6F32]" />
            <span className={isDark ? 'text-zinc-300' : 'text-[#3E3C37]'}>
              Try sample test cases:
            </span>
          </span>
          <span className="text-[11px] text-zinc-500">1-Click load</span>
        </div>

        <div className="flex flex-wrap gap-2">
          {TEST_PRESETS.map((preset) => (
            <button
              key={preset.id}
              type="button"
              onClick={() => handlePresetClick(preset.text)}
              className={`text-xs px-3 py-1.5 rounded-xl border transition-all font-medium ${
                isDark 
                  ? 'bg-[#18181B] border-[#27272A] text-zinc-300 hover:text-white hover:border-[#FF6F32]/50 hover:bg-[#202024]' 
                  : 'bg-[#ECEAE5] border-[#DCD9D2] text-[#1C1B18] hover:text-[#FF6F32] hover:border-[#FF6F32]/50 hover:bg-[#E4E2DC]'
                }`}
            >
              {preset.name}
            </button>
          ))}
        </div>
      </div>

      {/* Audio File Upload Box */}
      {activeTab === 'audio' && (
        <div className={`p-4 rounded-xl border border-dashed text-center space-y-2 ${
          isDark 
            ? 'bg-[#0C0C0C] border-[#FF6F32]/40' 
            : 'bg-[#ECEAE5] border-[#FF6F32]/40'
        }`}>
          <input
            type="file"
            ref={fileInputRef}
            accept=".wav,.mp3,.m4a"
            onChange={handleAudioUpload}
            className="hidden"
          />
          <div className="w-10 h-10 mx-auto rounded-full bg-[#FF6F32]/10 border border-[#FF6F32]/30 flex items-center justify-center text-[#FF6F32]">
            <Volume2 className="w-5 h-5" />
          </div>
          <div>
            <p className={`text-sm font-semibold ${isDark ? 'text-white' : 'text-[#1C1B18]'}`}>
              {audioFile ? `Uploaded: ${audioFile.name}` : 'Drop or upload scam call recording'}
            </p>
            <p className="text-xs text-zinc-400 font-mono mt-0.5">
              Supports .wav, .mp3 • Auto-transcribed via Whisper STT / SpeechRecognition
            </p>
          </div>
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            className="px-4 py-1.5 rounded-xl bg-[#FF6F32] hover:bg-[#E55B1F] text-white text-xs font-semibold transition-all shadow-sm"
          >
            {audioFile ? 'Change File' : 'Browse Audio File'}
          </button>
        </div>
      )}

      {/* Main Clean Input Box */}
      <div className={`rounded-xl border p-4 transition-colors space-y-3 ${
        isDark 
          ? 'bg-[#0C0C0C] border-[#242428] focus-within:border-[#FF6F32]' 
          : 'bg-[#ECEAE5] border-[#DCD9D2] focus-within:border-[#FF6F32]'
      }`}>
        <div className="flex items-center justify-between text-xs font-mono text-zinc-400">
          <span className={isDark ? 'text-zinc-300' : 'text-[#3E3C37]'}>
            {activeTab === 'email' ? 'RFC Email Headers / Body:' : activeTab === 'audio' ? 'Call Transcript / Notes:' : 'Message Content:'}
          </span>
          {inputText && (
            <button
              type="button"
              onClick={() => {
                setInputText('');
                setAudioFile(null);
              }}
              className="hover:text-rose-400 transition-colors flex items-center gap-1 text-[11px]"
            >
              <Eraser className="w-3.5 h-3.5" />
              <span>Clear</span>
            </button>
          )}
        </div>

        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={6}
          placeholder={
            activeTab === 'email'
              ? "Paste email headers (From, Return-Path, DKIM) or suspicious email body here..."
              : activeTab === 'audio'
                ? "Paste audio call transcript here or upload a .wav audio file above..."
                : "Type or paste suspicious SMS or WhatsApp message here..."
          }
          className={`w-full bg-transparent font-sans text-sm resize-none focus:outline-none placeholder:text-zinc-500 leading-relaxed ${
            isDark ? 'text-white' : 'text-[#1C1B18]'
          }`}
        />

        <div className={`flex items-center justify-between pt-2 border-t text-xs font-mono text-zinc-400 ${
          isDark ? 'border-[#242428]' : 'border-[#DCD9D2]'
        }`}>
          <span>
            <strong className={isDark ? 'text-white' : 'text-[#1C1B18]'}>{inputText.length}</strong> / 10,000 characters
          </span>
          <span className="text-zinc-500 hidden sm:inline">
            Press <kbd className={`px-1.5 py-0.5 rounded text-[11px] ${
              isDark ? 'bg-zinc-800 text-zinc-300' : 'bg-[#DCD9D2] text-[#1C1B18]'
              }`}>Ctrl + Enter</kbd> to scan
          </span>
        </div>
      </div>

      {/* Primary Scan Button (10% Accent Orange) */}
      <button
        type="button"
        onClick={onScan}
        disabled={isLoading || (!inputText.trim() && !audioFile)}
        className={`w-full py-3.5 px-6 rounded-xl font-bold text-sm tracking-wide flex items-center justify-center gap-2 transition-all ${
          isLoading || (!inputText.trim() && !audioFile)
            ? isDark ? 'bg-zinc-800 text-zinc-500 cursor-not-allowed' : 'bg-[#DCD9D2] text-zinc-500 cursor-not-allowed'
            : 'bg-[#FF6F32] hover:bg-[#E55B1F] text-white shadow-[0_4px_20px_rgba(255,111,50,0.3)] active:scale-[0.99]'
        }`}
      >
        {isLoading ? (
          <>
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            <span>Analyzing Threat Patterns...</span>
          </>
        ) : (
          <>
            <span>Scan for Threats</span>
            <ArrowRight className="w-4 h-4" />
          </>
        )}
      </button>

    </div>
  );
}
