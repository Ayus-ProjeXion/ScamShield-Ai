import React, { useState } from 'react';
import { X, ShieldAlert, Send, CheckCircle2 } from 'lucide-react';

export function ReportModal({ isOpen, onClose, onSubmitReport, themeMode }) {
  const [iocType, setIocType] = useState('phone');
  const [iocValue, setIocValue] = useState('');
  const [category, setCategory] = useState('ELECTRICITY_KYC');
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  if (!isOpen) return null;

  const isDark = themeMode === 'midnight';
  const isCyber = themeMode === 'cyber';
  const isSoothing = themeMode === 'soothing';

  const accentColor = isCyber ? '#E5A83C' : '#FF6F32';
  const modalBg = isCyber ? 'bg-[#110D26] border-[#2A1F52] text-white' : isDark ? 'bg-[#141416] border-[#242428] text-white' : 'bg-[#F6F5F2] border-[#DCD9D2] text-[#1C1B18]';
  const innerBg = isCyber ? 'bg-[#080614] border-[#2A1F52]' : isDark ? 'bg-[#0C0C0C] border-[#242428]' : 'bg-[#ECEAE5] border-[#DCD9D2]';

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!iocValue || !title) return;

    setIsSubmitting(true);
    await onSubmitReport({
      ioc_type: iocType,
      ioc_value: iocValue,
      category,
      title,
      description
    });
    setIsSubmitting(false);
    setIsSuccess(true);
    setTimeout(() => {
      setIsSuccess(false);
      onClose();
      setIocValue('');
      setTitle('');
      setDescription('');
    }, 1800);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md">
      <div 
        className={`relative w-full max-w-lg rounded-2xl border p-6 shadow-2xl space-y-4 transition-colors ${modalBg}`}
        onClick={(e) => e.stopPropagation()}
      >
        <button
          onClick={onClose}
          className={`absolute top-4 right-4 p-2 rounded-xl transition-colors ${
            isCyber ? 'bg-[#181238] text-violet-200 hover:text-white' : isDark ? 'bg-[#18181B] text-zinc-400 hover:text-white' : 'bg-[#ECEAE5] text-[#1C1B18] hover:text-[#FF6F32]'
          }`}
        >
          <X className="w-5 h-5" />
        </button>

        <div className={`flex items-center gap-2.5 pb-2 border-b ${
          isCyber ? 'border-[#2A1F52]' : isDark ? 'border-[#242428]' : 'border-[#DCD9D2]'
        }`}>
          <div 
            className="w-2.5 h-2.5 rounded-full"
            style={{ backgroundColor: accentColor }}
          ></div>
          <div>
            <h3 className={`font-bold text-base ${isSoothing ? 'text-[#1C1B18]' : 'text-white'}`}>
              Crowdsource Scam Incident Report
            </h3>
            <p className={`text-xs ${isCyber ? 'text-violet-200/80' : isDark ? 'text-zinc-400' : 'text-[#57554F]'}`}>
              Help protect citizens across India from fraud
            </p>
          </div>
        </div>

        {isSuccess ? (
          <div className="py-8 text-center space-y-2">
            <CheckCircle2 className="w-12 h-12 mx-auto animate-bounce" style={{ color: accentColor }} />
            <h4 className={`font-bold text-base ${isSoothing ? 'text-[#1C1B18]' : 'text-white'}`}>
              Report Submitted to Threat Feed!
            </h4>
            <p className="text-xs text-zinc-400">Queued for verification and broadcast.</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-3.5 text-xs font-mono">
            <div>
              <label className={`block mb-1 ${isCyber ? 'text-violet-200' : isDark ? 'text-zinc-400' : 'text-[#57554F]'}`}>Target IOC Type</label>
              <select
                value={iocType}
                onChange={(e) => setIocType(e.target.value)}
                className={`w-full rounded-xl px-3 py-2 focus:outline-none border ${innerBg}`}
              >
                <option value="phone">Phone Number (+91)</option>
                <option value="upi">UPI ID (e.g. name@bank)</option>
                <option value="url">Malicious Domain / URL</option>
                <option value="email">Phishing Email Address</option>
                <option value="apk">Rogue Android APK Name</option>
              </select>
            </div>

            <div>
              <label className={`block mb-1 ${isCyber ? 'text-violet-200' : isDark ? 'text-zinc-400' : 'text-[#57554F]'}`}>Scammer Identifier / Value</label>
              <input
                type="text"
                required
                value={iocValue}
                onChange={(e) => setIocValue(e.target.value)}
                placeholder="+91 9876543210 or scammer@upi"
                className={`w-full rounded-xl px-3 py-2 focus:outline-none border ${innerBg}`}
              />
            </div>

            <div>
              <label className={`block mb-1 ${isCyber ? 'text-violet-200' : isDark ? 'text-zinc-400' : 'text-[#57554F]'}`}>Scam Incident Title</label>
              <input
                type="text"
                required
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. Fake Power Bill WhatsApp Video Extortion"
                className={`w-full rounded-xl px-3 py-2 focus:outline-none border ${innerBg}`}
              />
            </div>

            <div>
              <label className={`block mb-1 ${isCyber ? 'text-violet-200' : isDark ? 'text-zinc-400' : 'text-[#57554F]'}`}>Modus Operandi / Message Details</label>
              <textarea
                rows={3}
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Explain what the scammer said, threats made, and payment demands..."
                className={`w-full rounded-xl px-3 py-2 focus:outline-none border resize-none font-sans ${innerBg}`}
              />
            </div>

            <div className="pt-2 flex items-center justify-end gap-2">
              <button
                type="button"
                onClick={onClose}
                className={`px-4 py-2 rounded-xl font-medium transition-colors ${
                  isCyber 
                    ? 'bg-[#181238] text-violet-200 hover:text-white' 
                    : isDark 
                    ? 'bg-[#18181B] text-zinc-400 hover:text-white' 
                    : 'bg-[#ECEAE5] text-[#1C1B18] hover:text-[#FF6F32]'
                }`}
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={isSubmitting}
                className="px-4 py-2 rounded-xl font-bold flex items-center gap-1.5 shadow-md"
                style={{
                  backgroundColor: accentColor,
                  color: isCyber ? '#080614' : '#FFFFFF'
                }}
              >
                {isSubmitting ? (
                  <span>Submitting...</span>
                ) : (
                  <>
                    <Send className="w-3.5 h-3.5" />
                    <span>Submit Report</span>
                  </>
                )}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}
