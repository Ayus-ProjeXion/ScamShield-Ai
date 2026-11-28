import React, { useRef, useState, useEffect } from 'react';
import { createWorker } from 'tesseract.js';
import {
  MessageSquare,
  Mail,
  Mic,
  Camera,
  Sparkles,
  Eraser,
  ShieldCheck,
  Volume2,
  ArrowRight,
  UploadCloud,
  X,
  Loader2,
  Image as ImageIcon
} from 'lucide-react';

export const MODALITY_PRESETS = {
  text: [
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
  ],
  email: [
    {
      id: 'tax_refund',
      name: '💸 Income Tax Refund Phishing',
      text: 'From: Income Tax Department <incometax.refunds@gmail.com>\nSubject: Notice: Tax Refund of Rs 24,500 Approved\nDate: Sun, 22 Nov 2026 11:30:00 +0530\n\nDear Taxpayer,\nYour IT department refund of Rs 24,500 has been credited.\nSubmit your bank account details here to receive funds: http://incometax-portal.online'
    },
    {
      id: 'hdfc_reward',
      name: '💳 HDFC Reward Points Trap',
      text: 'From: HDFC Credit Card Center <hdfc.rewards.claim@yahoo.com>\nSubject: FINAL NOTICE: Redeem 35,400 HDFC Reward Points before midnight\nDate: Sun, 22 Nov 2026 14:00:00 +0530\n\nDear Cardholder,\nThis is the final notification regarding your HDFC Regalia Credit Card reward balance.\nYou have 35,400 unredeemed reward points valued at Rs 17,700 expiring tonight at 11:59 PM.\nTo convert your points into direct cash, verify your card details immediately: http://hdfc-rewards-portal.xyz/cashback'
    },
    {
      id: 'ceo_bec',
      name: '👔 CEO Wire Transfer Fraud (BEC)',
      text: 'From: Vikram Malhotra <ceo.office.corp@mail-director.top>\nSubject: Urgent: Confidential Project Wire Transfer Required\nDate: Sun, 22 Nov 2026 09:15:00 +0530\n\nHi Finance Team,\nI am currently in an offshore board meeting with limited connectivity. We need an immediate wire transfer of INR 8,40,000 to vendor account #0921882190 to secure an acquisition deposit before 2 PM. Please process ASAP and send confirmation.'
    },
    {
      id: 'safe_amazon',
      name: '✅ Safe Amazon Order (0% False Alarm)',
      text: 'From: auto-confirm@amazon.in\nSubject: Your Amazon.in order #402-8819201-1928301 has shipped\nDate: Sun, 22 Nov 2026 10:00:00 +0530\n\nHi Customer,\nYour package with order #402-8819201-1928301 has been dispatched via BlueDart and is expected to arrive tomorrow by 8 PM. You can track your package directly inside your Amazon App.'
    }
  ],
  audio: [
    {
      id: 'scam_police_transcript',
      name: '🚨 Police Digital Arrest Transcript',
      text: 'You are under digital arrest by Delhi Police cyber cell. Do not disconnect this call or transfer to anyone else. An illegal parcel with drugs has been intercepted in your name at customs.'
    },
    {
      id: 'safe_family_transcript',
      name: '✅ Safe Family Call Transcript (0% False Alarm)',
      text: 'Hey bro, reaching home in 10 minutes. See you for dinner. Let me know if you need anything from the grocery store.'
    }
  ],
  image: [
    {
      id: 'img_cbi',
      name: '🚨 Fake CBI FIR Notice Screenshot',
      text: 'CENTRAL BUREAU OF INVESTIGATION (CBI) - CYBER CRIME CELL\nNOTICE OF ARREST UNDER SECTION 420/467/468 IPC\nCase Ref: CBI-MUM-2026-9912\nTo: Accused Person\nYou are hereby notified that a consignment seized at Delhi Airport contained 150g narcotics and forged documents in your name. You are placed under DIGITAL ARREST. Contact Inspector Verma at 9876543210 immediately.'
    },
    {
      id: 'img_job',
      name: '💼 WhatsApp Part-Time Job Offer',
      text: 'GLOBAL MEDIA MARKETING LTD - WORK FROM HOME OFFER\nEarn Rs 3,000 - 8,000 Daily by liking 3 YouTube videos per task.\nTo activate your Merchant Task Wallet, deposit registration fee of Rs 1,500 to UPI: taskdeposit@icici.\nImmediate withdrawal guaranteed after task completion!'
    },
    {
      id: 'img_electricity',
      name: '⚡ Electricity Cutoff WhatsApp Notice',
      text: 'MAHADISCOM URGENT ALERT\nConsumer No: 0284719201\nYour electricity bill payment of Rs 1,840 is pending. Power disconnection scheduled for tonight at 9:30 PM.\nDownload Bijli_Bill_Pay.apk from http://bit.ly/mhavitaran-pay or call 9123456789.'
    },
    {
      id: 'img_safe_swiggy',
      name: '✅ Safe Order Receipt (0% False Alarm)',
      text: 'Swiggy Order #SW-881920\nDelivered to: 4th Floor, Galaxy Apartments\nItems: 1x Paneer Butter Masala, 2x Butter Naan\nTotal Paid: Rs 420.00 via GPay\nDelivery Partner: Rahul Kumar (Rating: 4.9)'
    }
  ]
};

export const TEST_PRESETS = MODALITY_PRESETS.text;

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
  const imageInputRef = useRef(null);

  // OCR state for screenshot analysis
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [isOcrProcessing, setIsOcrProcessing] = useState(false);
  const [ocrProgress, setOcrProgress] = useState(0);
  const [ocrStatus, setOcrStatus] = useState('');

  const currentPresets = MODALITY_PRESETS[activeTab] || MODALITY_PRESETS.text;

  // Process OCR on image file using client-side Tesseract.js (100% on-device Zero-Knowledge)
  const processImageOcr = async (file) => {
    if (!file || !file.type.startsWith('image/')) return;

    setImageFile(file);
    const objectUrl = URL.createObjectURL(file);
    setImagePreview(objectUrl);
    setIsOcrProcessing(true);
    setOcrProgress(10);
    setOcrStatus('Initializing On-Device Zero-Knowledge OCR...');

    try {
      const worker = await createWorker('eng', 1, {
        logger: (m) => {
          if (m.status === 'recognizing text') {
            const pct = Math.round((m.progress || 0) * 100);
            setOcrProgress(pct);
            setOcrStatus(`Extracting text from screenshot... ${pct}%`);
          } else if (m.status) {
            setOcrStatus(`${m.status.charAt(0).toUpperCase() + m.status.slice(1)}...`);
          }
        }
      });

      const { data: { text } } = await worker.recognize(file);
      await worker.terminate();

      const cleanedText = text.trim();
      if (cleanedText) {
        setInputText(cleanedText);
        const wordCount = cleanedText.split(/\s+/).filter(Boolean).length;
        setOcrStatus(`✓ OCR Complete: Extracted ${wordCount} words. Ready for Threat Scan.`);
      } else {
        setOcrStatus('No readable text found in screenshot. You can type contents below.');
      }
    } catch (err) {
      console.error('OCR Error:', err);
      setOcrStatus('Could not read image text. Please ensure screenshot is legible.');
    } finally {
      setIsOcrProcessing(false);
    }
  };

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      processImageOcr(file);
    }
  };

  const clearImage = () => {
    setImageFile(null);
    if (imagePreview) {
      URL.revokeObjectURL(imagePreview);
    }
    setImagePreview(null);
    setOcrStatus('');
    setOcrProgress(0);
    if (imageInputRef.current) {
      imageInputRef.current.value = '';
    }
  };

  // Global Ctrl + V paste listener: paste a screenshot from anywhere!
  useEffect(() => {
    const handlePaste = (e) => {
      if (e.clipboardData && e.clipboardData.files && e.clipboardData.files.length > 0) {
        const file = e.clipboardData.files[0];
        if (file.type.startsWith('image/')) {
          e.preventDefault();
          setActiveTab('image');
          setAudioFile(null);
          processImageOcr(file);
        }
      }
    };

    window.addEventListener('paste', handlePaste);
    return () => window.removeEventListener('paste', handlePaste);
  }, []);

  const handlePresetClick = (presetText) => {
    setAudioFile(null);
    setInputText(presetText);
    if (onScan) {
      onScan(presetText, activeTab, null);
    }
  };

  const loadSampleAudio = async (filename, label) => {
    try {
      const res = await fetch(`/${filename}`);
      if (!res.ok) throw new Error('Could not fetch sample audio');
      const blob = await res.blob();
      const file = new File([blob], filename, { type: 'audio/wav' });
      setAudioFile(file);
      setInputText(`[Attached Voice Recording: ${label} (${filename}) — Press 'Scan for Threats' to execute AI transcription & scam detection]`);
    } catch (err) {
      console.error('Failed to load sample audio:', err);
    }
  };

  const loadSampleScreenshot = async (filename, label) => {
    try {
      setOcrStatus(`Loading test screenshot: ${filename}...`);
      const res = await fetch(`/test_screenshots/${filename}`);
      if (!res.ok) throw new Error('Could not fetch sample screenshot');
      const blob = await res.blob();
      const file = new File([blob], filename, { type: 'image/png' });
      await processImageOcr(file);
    } catch (err) {
      console.error('Failed to load sample screenshot:', err);
      setOcrStatus(`Could not load ${filename}. Select manually from test_screenshots/ folder.`);
    }
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
    <div className={`rounded-2xl border p-6 lg:p-7 shadow-xl space-y-5 transition-colors duration-200 ${isDark
      ? 'bg-[#141416] border-[#242428]'
      : 'bg-[#F6F5F2] border-[#DCD9D2]'
      }`}>

      {/* Station Header */}
      <div className={`flex flex-wrap items-center justify-between gap-3 pb-3 border-b ${isDark ? 'border-[#242428]' : 'border-[#DCD9D2]'
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

      {/* 4 Modality Tabs */}
      <div className={`grid grid-cols-2 sm:grid-cols-4 gap-1.5 p-1.5 rounded-xl border ${isDark
        ? 'bg-[#0C0C0C] border-[#242428]'
        : 'bg-[#ECEAE5] border-[#DCD9D2]'
        }`}>
        <button
          type="button"
          onClick={() => {
            setActiveTab('text');
            setAudioFile(null);
          }}
          className={`flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs font-semibold transition-all ${activeTab === 'text'
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
          onClick={() => {
            setActiveTab('email');
            setAudioFile(null);
          }}
          className={`flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs font-semibold transition-all ${activeTab === 'email'
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
          onClick={() => {
            setActiveTab('audio');
          }}
          className={`flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs font-semibold transition-all ${activeTab === 'audio'
            ? 'bg-[#FF6F32] text-white shadow-sm'
            : isDark
              ? 'text-zinc-400 hover:text-white hover:bg-zinc-900'
              : 'text-[#57554F] hover:text-[#1C1B18] hover:bg-[#F6F5F2]'
            }`}
        >
          <Mic className="w-3.5 h-3.5" />
          <span>Voice (.wav)</span>
        </button>

        <button
          type="button"
          onClick={() => {
            setActiveTab('image');
            setAudioFile(null);
          }}
          className={`flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs font-semibold transition-all ${activeTab === 'image'
            ? 'bg-[#FF6F32] text-white shadow-sm'
            : isDark
              ? 'text-zinc-400 hover:text-white hover:bg-zinc-900'
              : 'text-[#57554F] hover:text-[#1C1B18] hover:bg-[#F6F5F2]'
            }`}
        >
          <Camera className="w-3.5 h-3.5" />
          <span>Screenshot</span>
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
          {currentPresets.map((preset) => (
            <button
              key={preset.id}
              type="button"
              onClick={() => handlePresetClick(preset.text)}
              className={`text-xs px-3 py-1.5 rounded-xl border transition-all font-medium ${isDark
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
        <div className={`p-4 rounded-xl border border-dashed text-center space-y-3 ${isDark
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
          <div>
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="px-4 py-1.5 rounded-xl bg-[#FF6F32] hover:bg-[#E55B1F] text-white text-xs font-semibold transition-all shadow-sm"
            >
              {audioFile ? 'Change File' : 'Browse Audio File'}
            </button>
          </div>

          {/* 1-Click Load Sample Audio Files */}
          <div className={`flex flex-wrap items-center justify-center gap-2 pt-3 border-t border-dashed ${
            isDark ? 'border-zinc-800' : 'border-[#DCD9D2]'
          }`}>
            <span className="text-[11px] text-zinc-500 font-mono">1-Click Sample Audio:</span>
            <button
              type="button"
              onClick={() => loadSampleAudio('test_scam_call.wav', 'CBI Digital Arrest Call')}
              className={`text-xs px-2.5 py-1 rounded-lg border font-medium transition-all ${
                isDark ? 'bg-zinc-900 border-zinc-700 text-amber-400 hover:bg-zinc-800 hover:border-amber-400/50' : 'bg-white border-zinc-300 text-amber-600 hover:bg-zinc-50 hover:border-amber-500/50'
              }`}
            >
              🎧 Load test_scam_call.wav (Scam)
            </button>
            <button
              type="button"
              onClick={() => loadSampleAudio('test_safe_call.wav', 'Safe Family Call')}
              className={`text-xs px-2.5 py-1 rounded-lg border font-medium transition-all ${
                isDark ? 'bg-zinc-900 border-zinc-700 text-emerald-400 hover:bg-zinc-800 hover:border-emerald-400/50' : 'bg-white border-zinc-300 text-emerald-600 hover:bg-zinc-50 hover:border-emerald-500/50'
              }`}
            >
              🎧 Load test_safe_call.wav (Safe)
            </button>
          </div>
        </div>
      )}

      {/* Screenshot / Image Upload & OCR Box */}
      {activeTab === 'image' && (
        <div className={`p-4 rounded-xl border border-dashed text-center space-y-3 transition-all ${isDark
          ? 'bg-[#0C0C0C] border-[#FF6F32]/40'
          : 'bg-[#ECEAE5] border-[#FF6F32]/40'
          }`}>
          <input
            type="file"
            ref={imageInputRef}
            accept="image/*"
            onChange={handleImageUpload}
            className="hidden"
          />

          {!imagePreview ? (
            <div className="space-y-2">
              <div className="w-10 h-10 mx-auto rounded-full bg-[#FF6F32]/10 border border-[#FF6F32]/30 flex items-center justify-center text-[#FF6F32]">
                <Camera className="w-5 h-5" />
              </div>
              <div>
                <p className={`text-sm font-semibold ${isDark ? 'text-white' : 'text-[#1C1B18]'}`}>
                  Drop screenshot, click to browse, or paste directly with <kbd className={`px-1.5 py-0.5 rounded text-xs font-mono font-bold ${
                    isDark ? 'bg-zinc-800 text-amber-400 border border-zinc-700' : 'bg-white text-amber-600 border border-zinc-300'
                  }`}>Ctrl + V</kbd>
                </p>
                <p className="text-xs text-zinc-400 font-mono mt-0.5">
                  Supports WhatsApp chats, fake FIRs, electricity notices • 100% On-Device Zero-Knowledge OCR
                </p>
              </div>
              <button
                type="button"
                onClick={() => imageInputRef.current?.click()}
                className="px-4 py-1.5 rounded-xl bg-[#FF6F32] hover:bg-[#E55B1F] text-white text-xs font-semibold transition-all shadow-sm"
              >
                Browse Screenshot Image
              </button>
            </div>
          ) : (
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 py-1">
              <div className="relative group">
                <img
                  src={imagePreview}
                  alt="Screenshot preview"
                  className="max-h-24 max-w-xs rounded-lg border border-zinc-700 object-contain shadow-md"
                />
                <button
                  type="button"
                  onClick={clearImage}
                  className="absolute -top-2 -right-2 p-1 rounded-full bg-rose-600 text-white hover:bg-rose-500 shadow"
                  title="Remove screenshot"
                >
                  <X className="w-3.5 h-3.5" />
                </button>
              </div>

              <div className="text-left space-y-1.5">
                <p className={`text-xs font-semibold ${isDark ? 'text-white' : 'text-[#1C1B18]'}`}>
                  {imageFile?.name || 'Pasted Clipboard Screenshot'}
                </p>
                <p className={`text-[11px] font-mono ${
                  ocrStatus.includes('✓') ? 'text-emerald-400' : isDark ? 'text-zinc-400' : 'text-zinc-600'
                }`}>
                  {ocrStatus || 'Ready to analyze'}
                </p>
                {isOcrProcessing && (
                  <div className="w-48 bg-zinc-800 rounded-full h-1.5 overflow-hidden">
                    <div
                      className="bg-[#FF6F32] h-full transition-all duration-200"
                      style={{ width: `${ocrProgress}%` }}
                    />
                  </div>
                )}
                <div>
                  <button
                    type="button"
                    onClick={() => imageInputRef.current?.click()}
                    className="text-[11px] text-[#FF6F32] hover:underline"
                  >
                    Change Screenshot
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* 1-Click Load Sample Test Screenshots */}
          <div className={`flex flex-wrap items-center justify-center gap-2 pt-3 border-t border-dashed ${
            isDark ? 'border-zinc-800' : 'border-[#DCD9D2]'
          }`}>
            <span className="text-[11px] text-zinc-500 font-mono">1-Click Test Screenshots:</span>
            <button
              type="button"
              onClick={() => loadSampleScreenshot('scam_whatsapp_cbi_digital_arrest.png', 'CBI Digital Arrest Notice')}
              className={`text-xs px-2.5 py-1 rounded-lg border font-medium transition-all ${
                isDark ? 'bg-zinc-900 border-zinc-700 text-rose-400 hover:bg-zinc-800 hover:border-rose-400/50' : 'bg-white border-zinc-300 text-rose-600 hover:bg-zinc-50 hover:border-rose-500/50'
              }`}
            >
              📸 CBI Digital Arrest Notice (Scam)
            </button>
            <button
              type="button"
              onClick={() => loadSampleScreenshot('scam_electricity_bill_cutoff.png', 'MahaVitaran Cutoff Notice')}
              className={`text-xs px-2.5 py-1 rounded-lg border font-medium transition-all ${
                isDark ? 'bg-zinc-900 border-zinc-700 text-amber-400 hover:bg-zinc-800 hover:border-amber-400/50' : 'bg-white border-zinc-300 text-amber-600 hover:bg-zinc-50 hover:border-amber-500/50'
              }`}
            >
              ⚡ Electricity Cutoff Notice (Scam)
            </button>
            <button
              type="button"
              onClick={() => loadSampleScreenshot('safe_swiggy_delivery_receipt.png', 'Swiggy Food Receipt')}
              className={`text-xs px-2.5 py-1 rounded-lg border font-medium transition-all ${
                isDark ? 'bg-zinc-900 border-zinc-700 text-emerald-400 hover:bg-zinc-800 hover:border-emerald-400/50' : 'bg-white border-zinc-300 text-emerald-600 hover:bg-zinc-50 hover:border-emerald-500/50'
              }`}
            >
              🥗 Swiggy Order Receipt (Safe)
            </button>
          </div>
        </div>
      )}

      {/* Main Clean Input Box */}
      <div className={`rounded-xl border p-4 transition-colors space-y-3 ${isDark
        ? 'bg-[#0C0C0C] border-[#242428] focus-within:border-[#FF6F32]'
        : 'bg-[#ECEAE5] border-[#DCD9D2] focus-within:border-[#FF6F32]'
        }`}>
        <div className="flex items-center justify-between text-xs font-mono text-zinc-400">
          <span className={isDark ? 'text-zinc-300' : 'text-[#3E3C37]'}>
            {activeTab === 'email'
              ? 'RFC Email Headers / Body:'
              : activeTab === 'audio'
                ? 'Call Transcript / Notes:'
                : activeTab === 'image'
                  ? 'Extracted Screenshot Text (OCR):'
                  : 'Message Content or Case ID:'}
          </span>
          {inputText && (
            <button
              type="button"
              onClick={() => {
                setInputText('');
                setAudioFile(null);
                clearImage();
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
                : activeTab === 'image'
                  ? "Screenshot text will automatically be extracted here via on-device OCR, or you can paste / edit here..."
                  : "Type or paste suspicious SMS, WhatsApp message, or enter Case ID (#D3E256...)..."
          }
          className={`w-full bg-transparent font-sans text-sm resize-none focus:outline-none placeholder:text-zinc-500 leading-relaxed ${isDark ? 'text-white' : 'text-[#1C1B18]'
            }`}
        />

        <div className={`flex items-center justify-between pt-2 border-t text-xs font-mono text-zinc-400 ${isDark ? 'border-[#242428]' : 'border-[#DCD9D2]'
          }`}>
          <span>
            <strong className={isDark ? 'text-white' : 'text-[#1C1B18]'}>{inputText.length}</strong> / 10,000 characters
          </span>
          <span className="text-zinc-500 hidden sm:inline">
            Press <kbd className={`px-1.5 py-0.5 rounded text-[11px] ${isDark ? 'bg-zinc-800 text-zinc-300' : 'bg-[#DCD9D2] text-[#1C1B18]'
              }`}>Ctrl + Enter</kbd> to scan
          </span>
        </div>
      </div>

      {/* Primary Scan Button (10% Accent Orange) */}
      <button
        type="button"
        onClick={() => onScan()}
        disabled={isLoading || isOcrProcessing || (!inputText.trim() && !audioFile)}
        className={`w-full py-3.5 px-6 rounded-xl font-bold text-sm tracking-wide flex items-center justify-center gap-2 transition-all ${
          isLoading || isOcrProcessing || (!inputText.trim() && !audioFile)
            ? isDark ? 'bg-zinc-800 text-zinc-500 cursor-not-allowed' : 'bg-[#DCD9D2] text-zinc-500 cursor-not-allowed'
            : 'bg-[#FF6F32] hover:bg-[#E55B1F] text-white shadow-[0_4px_20px_rgba(255,111,50,0.3)] active:scale-[0.99]'
        }`}
      >
        {isLoading ? (
          <>
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            <span>Analyzing Threat Patterns...</span>
          </>
        ) : isOcrProcessing ? (
          <>
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
            <span>Extracting Screenshot Text...</span>
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
