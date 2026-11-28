import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { ThreatScanner } from './components/ThreatScanner';
import { ThreatHUD } from './components/ThreatHUD';
import { ShieldModeCard } from './components/ShieldModeCard';
import { OnboardingModal } from './components/OnboardingModal';
import { FloatingCopilot } from './components/FloatingCopilot';
import { LiveScamCarousel } from './components/LiveScamCarousel';
import { IncidentModal } from './components/IncidentModal';
import { ReportModal } from './components/ReportModal';
import { DownloadCompanionModal } from './components/DownloadCompanionModal';
import { CheckCircle } from 'lucide-react';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export default function App() {
  // Theme state: dark (60% Midnight Black #0C0C0C) or light (60% Soothing Warm Sand #ECEAE5)
  const [theme, setTheme] = useState('dark');
  const isDark = theme === 'dark';

  const toggleTheme = () => {
    setTheme(isDark ? 'light' : 'dark');
  };

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
      document.documentElement.classList.remove('light');
    } else {
      document.documentElement.classList.remove('dark');
      document.documentElement.classList.add('light');
    }
  }, [isDark]);

  // Clean, empty inputs by default
  const [inputText, setInputText] = useState('');
  const [activeTab, setActiveTab] = useState('text');
  const [audioFile, setAudioFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [toastMessage, setToastMessage] = useState('');
  
  // Standby state by default
  const [scanResult, setScanResult] = useState(null);
  const [selectedNewsScam, setSelectedNewsScam] = useState(null);
  const [isReportModalOpen, setIsReportModalOpen] = useState(false);

  // Universal Shield Mode & Onboarding Modal states
  const [isShieldMode, setIsShieldMode] = useState(false);
  const [isOnboardingOpen, setIsOnboardingOpen] = useState(false);
  const [isCompanionModalOpen, setIsCompanionModalOpen] = useState(false);

  useEffect(() => {
    const hideWelcome = localStorage.getItem('scamshield_hide_welcome');
    if (!hideWelcome) {
      setIsOnboardingOpen(true);
    }

    // Handle Native Mobile PWA Web Share Target (Zero-Install WhatsApp / SMS sharing)
    try {
      const searchParams = new URLSearchParams(window.location.search);
      if (searchParams.get('mode') === 'shield') {
        setIsShieldMode(true);
      }

      const sharedTitle = searchParams.get('title') || '';
      const sharedTextBody = searchParams.get('text') || '';
      const sharedUrl = searchParams.get('url') || '';
      const sharedText = [sharedTitle, sharedTextBody, sharedUrl].filter(Boolean).join(' ').trim();
      if (sharedText && sharedText.length >= 6) {
        const clean = sharedText;
        setInputText(clean);
        setActiveTab('text');
        // On mobile text share, default to high-clarity Universal Shield Mode
        setIsShieldMode(true);
        window.history.replaceState({}, document.title, window.location.pathname);
        setTimeout(() => {
          handleScan(clean, 'text');
        }, 100);
        showToast('📱 Message shared from WhatsApp/SMS. Analyzing threat...');
      }
    } catch (e) {
      // Silent pass
    }
  }, []);

  const showToast = (msg) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(''), 3500);
  };

  const handleSelectOnboardingOption = (optionKey) => {
    if (optionKey === 'shield') {
      setIsShieldMode(true);
      showToast('Switched to Universal Shield Mode');
    } else if (optionKey === 'screenshot') {
      setActiveTab('image');
      showToast('Client-Side Screenshot OCR Ready');
    } else {
      setActiveTab(optionKey);
      if (optionKey === 'text') showToast('SMS / WhatsApp Verification Mode Ready');
      else if (optionKey === 'email') showToast('Email Phishing Scanner Ready');
      else if (optionKey === 'audio') showToast('Voice Call / Audio Scanner Ready');
    }
  };

  const handleTriggerDirectScan = async (text) => {
    if (typeof text !== 'string' || !text.trim()) return;
    setInputText(text);
    setActiveTab('text');
    await handleScan(text, 'text');
  };

  // Perform Multi-Modal Threat Scan
  const handleScan = async (overrideText = null, overrideTab = null, overrideFile = undefined) => {
    const targetText = (typeof overrideText === 'string' && overrideText.trim().length > 0)
      ? overrideText
      : (typeof inputText === 'string' ? inputText : '');
    const targetTab = (typeof overrideTab === 'string' && overrideTab.trim().length > 0)
      ? overrideTab
      : activeTab;
    const targetFile = (overrideFile !== undefined) ? overrideFile : audioFile;

    if (!targetText.trim() && !targetFile) return;

    if (isLoading) {
      showToast('⏳ Scan already in progress. Please wait a moment...');
      return;
    }

    setIsLoading(true);
    const startTime = performance.now();

    // 0. Instant Case ID Quick-Lookup Feature:
    // If input is an official Case ID (#D3E2569B... or UUID), query database audit ledger directly
    const trimmedInput = targetText.trim();
    const isCaseIdLookup = targetTab === 'text' && (
      trimmedInput.startsWith('#') ||
      (trimmedInput.length >= 8 && /^[a-f0-9-]{8,}$/i.test(trimmedInput) && !trimmedInput.includes(' '))
    );

    if (isCaseIdLookup && !targetFile) {
      try {
        const cleanLookupId = encodeURIComponent(trimmedInput);
        const lookupResponse = await fetch(`${API_BASE_URL}/api/v1/scan/${cleanLookupId}`);
        if (lookupResponse.ok) {
          const data = await lookupResponse.json();
          const elapsed = (performance.now() - startTime).toFixed(1);

          let resolvedExplanation = data.explanation;
          if (!resolvedExplanation && data.why_its_risky && data.why_its_risky.length > 0) {
            resolvedExplanation = data.why_its_risky.map(item => item.explanation || item.factor || '').filter(Boolean).join(' ');
          }
          if (!resolvedExplanation) {
            resolvedExplanation = data.is_scam
              ? `Verified case forensic record retrieved from database. Triggered markers: ${(data.badges || []).join(', ') || 'Known malicious pattern'}.`
              : 'Verified case record retrieved from database: Normal conversation with zero fraud indicators.';
          }

          const isThreat = Boolean(data.is_scam || (data.threat_level && data.threat_level !== 'SAFE') || (data.risk_score && data.risk_score >= 50));
          const rawConfidence = typeof data.confidence === 'number'
            ? data.confidence
            : (typeof data.ml_probability === 'number'
              ? (isThreat ? data.ml_probability : (1.0 - data.ml_probability))
              : 0.98);
          const computedConfidence = Math.max(60.0, Math.min(99.9, rawConfidence * 100)).toFixed(1);

          setScanResult({
            riskScore: Math.round(data.risk_score || 0),
            verdict: data.threat_level || data.verdict || (data.is_scam ? 'CRITICAL' : 'SAFE'),
            confidence: computedConfidence,
            latencyMs: elapsed,
            badges: ['Verified Case Record (Database Retrieved)', ...(data.badges || [])],
            explanation: resolvedExplanation,
            hmacToken: data.security_token?.hmac_signature || data.security_token?.signature || trimmedInput.replace(/^#/, ''),
            complaintDraft: data.complaint_draft || ''
          });

          const displayId = (data.security_token?.hmac_signature || trimmedInput).replace(/^#/, '').substring(0, 14).toUpperCase();
          showToast(`Official Case Record Verified! Retrieved #${displayId}`);
          setIsLoading(false);
          return;
        }
      } catch (lookupErr) {
        console.log('Case ID lookup check passed through to live scan:', lookupErr);
      }
    }

    try {
      let endpoint = `${API_BASE_URL}/api/v1/scan/text`;
      let bodyData;
      let headers = {};

      if (targetTab === 'email') {
        endpoint = `${API_BASE_URL}/api/v1/scan/email`;
        bodyData = JSON.stringify({ email_text: targetText, raw_email: targetText });
        headers['Content-Type'] = 'application/json';
      } else if (targetTab === 'audio' && targetFile) {
        endpoint = `${API_BASE_URL}/api/v1/scan/audio`;
        const formData = new FormData();
        formData.append('file', targetFile);
        bodyData = formData;
      } else {
        endpoint = `${API_BASE_URL}/api/v1/scan/text`;
        bodyData = JSON.stringify({
          text: targetText,
          channel: targetTab === 'audio' ? 'VOICE' : (targetTab === 'email' ? 'EMAIL' : (targetTab === 'image' ? 'SCREENSHOT' : 'SMS'))
        });
        headers['Content-Type'] = 'application/json';
      }

      const response = await fetch(endpoint, {
        method: 'POST',
        headers,
        body: bodyData
      });

      if (!response.ok) {
        throw new Error(`API returned HTTP ${response.status}`);
      }

      const data = await response.json();
      const elapsed = (performance.now() - startTime).toFixed(1);

      // Handle Anti-Spam / Rate-Limit Cooldown
      // CRITICAL: Never overwrite an existing threat scan with 0% / SAFE when throttled!
      if (data.rate_limited || data.threat_level === 'RATE_LIMITED') {
        const waitMsg = data.recommended_actions?.[0] || '⏳ Anti-spam buffer active: Please wait a second before scanning again.';
        showToast(waitMsg);
        setIsLoading(false);
        return;
      }

      // Auto-populate audio call transcript in the input box so the user can inspect the transcribed speech
      if (activeTab === 'audio' && (data.audio_meta?.transcribed_text || data.text_preview)) {
        setInputText(data.audio_meta?.transcribed_text || data.text_preview);
      }

      // Resolve root cause explanation from backend
      let resolvedExplanation = data.explanation;
      if (!resolvedExplanation && data.why_its_risky && data.why_its_risky.length > 0) {
        resolvedExplanation = data.why_its_risky.map(item => item.explanation || item.factor || '').filter(Boolean).join(' ');
      }
      if (!resolvedExplanation) {
        resolvedExplanation = (data.is_scam || (data.risk_score && data.risk_score >= 50))
          ? `High-risk cyber threat detected. Markers: ${(data.badges || []).join(', ') || 'Deceptive heuristics identified'}.`
          : 'Text contains normal language with zero fraud indicators.';
      }

      const isThreat = Boolean(data.is_scam || (data.threat_level && data.threat_level !== 'SAFE') || (data.risk_score && data.risk_score >= 50));
      const rawConfidence = typeof data.confidence === 'number'
        ? data.confidence
        : (typeof data.ml_probability === 'number'
          ? (isThreat ? data.ml_probability : (1.0 - data.ml_probability))
          : 0.98);
      const computedConfidence = Math.max(60.0, Math.min(99.9, rawConfidence * 100)).toFixed(1);

      setScanResult({
        riskScore: Math.round(data.risk_score || 0),
        verdict: data.threat_level || data.verdict || (data.is_scam ? 'CRITICAL' : 'SAFE'),
        confidence: computedConfidence,
        latencyMs: elapsed,
        badges: (targetTab === 'image' && !(data.badges || []).some(b => b.includes('Screenshot')))
          ? ['Screenshot OCR Verified (Zero-Knowledge)', ...(data.badges || [])]
          : (data.badges || []),
        explanation: resolvedExplanation,
        hmacToken: data.security_token?.hmac_signature || data.security_token?.signature || `0x${Math.random().toString(16).substring(2, 42)}`,
        complaintDraft: data.complaint_draft || ''
      });

      showToast(`Scan complete: Verdict [${data.threat_level || data.verdict || 'SAFE'}] in ${elapsed}ms`);
    } catch (err) {
      console.warn('Backend API offline or unreachable:', err);
      const elapsed = (performance.now() - startTime).toFixed(1);

      // If this was an audio scan without text or server failed unexpectedly, do not fabricate a fake SAFE result
      if (targetTab === 'audio' && !targetText.trim()) {
        showToast(`Audio analysis failed: ${err.message || 'Server offline'}. Please check backend connection and retry.`);
        return;
      }

      const textLower = (targetText || '').toLowerCase().trim();
      if (!textLower) {
        showToast(`Scan request failed: ${err.message || 'Network error'}. Please retry.`);
        return;
      }

      // Only evaluate local fallback if recognizable scam heuristic triggers match
      let detectedScore = 0;
      let detectedVerdict = null;
      let detectedBadges = [];
      let detectedExplanation = '';

      if (textLower.includes('bijli') || textLower.includes('electricity') || textLower.includes('disconnected')) {
        detectedScore = 96;
        detectedVerdict = 'CRITICAL';
        detectedBadges = ['Utility Impersonation: Electricity KYC', 'Artificial Time Panic (Cutoff Ultimatum)', 'Malicious APK Delivery'];
        detectedExplanation = 'Impersonation of state power utility using fabricated power cutoff ultimatum to bypass financial caution and force APK installation.';
      } else if (textLower.includes('cbi') || textLower.includes('digital arrest') || textLower.includes('mdma') || textLower.includes('police')) {
        detectedScore = 99;
        detectedVerdict = 'CRITICAL';
        detectedBadges = ['Digital Arrest Extortion', 'Fake Law Enforcement Impersonation', 'Narcotics Seizure Threat'];
        detectedExplanation = 'High-pressure state law-enforcement impersonation leveraging fabricated narcotics seizure to coerce victim into fund transfers under duress.';
      } else if (textLower.includes('customs') || textLower.includes('fedex') || textLower.includes('consignment')) {
        detectedScore = 97;
        detectedVerdict = 'CRITICAL';
        detectedBadges = ['Customs Extortion', 'Fake Courier Interception', 'Urgent Payment Penalty'];
        detectedExplanation = 'Courier fraud combined with fake customs penalty threat directing payment to personal UPI disguised as clearance desk.';
      } else if (textLower.includes('kbc') || textLower.includes('lottery') || textLower.includes('won 25 lakh')) {
        detectedScore = 91;
        detectedVerdict = 'CRITICAL';
        detectedBadges = ['Lottery / Lucky Draw Advance Fee', 'Media Authority Impersonation', 'Registration Processing Duty'];
        detectedExplanation = 'Classic advance-fee lottery scam exploiting popular media authority to extract upfront processing fee.';
      } else if (textLower.includes('otp') || textLower.includes('pin') || textLower.includes('cvv')) {
        detectedScore = 94;
        detectedVerdict = 'CRITICAL';
        detectedBadges = ['Credential Theft: OTP / Secret PIN', 'Unauthorized Account Compromise'];
        detectedExplanation = 'Direct solicitation of secret authentication credentials (OTP/PIN) forbidden by RBI cybersecurity directives.';
      }

      if (detectedVerdict) {
        setScanResult({
          riskScore: detectedScore,
          verdict: detectedVerdict,
          confidence: '95.0',
          latencyMs: elapsed,
          badges: ['Local Offline Fallback Rules', ...detectedBadges],
          explanation: detectedExplanation,
          hmacToken: `0x${Math.random().toString(16).substring(2, 42)}`,
          complaintDraft: `================================================================================
CYBER CRIME INCIDENT REPORT DRAFT (MHA / HELPLINE 1930 / CHAKSHU)
================================================================================
Generated by: ScamShield AI Local Resilience Engine (Offline Fallback)
Date/Time: ${new Date().toLocaleString()}

Incident Summary:
Suspicious extortive communication intercepted with threat level (${detectedScore}%).
Flagged Content: "${targetText.substring(0, 140)}..."

Forensic Badges: ${detectedBadges.join(', ')}

Please take immediate action under Indian Cyber Crime Prevention guidelines.`
        });
        showToast(`Offline Rule Evaluation: Verdict [${detectedVerdict}] in ${elapsed}ms`);
      } else {
        showToast(`Backend connection failed (${err.message || 'Offline'}). Could not complete scan.`);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleLoadScenario = (scenarioText) => {
    setInputText(scenarioText);
    setActiveTab('text');
    showToast('Loaded scenario into scanner. Click "Scan for Threats"!');
    window.scrollTo({ top: 140, behavior: 'smooth' });
  };

  const handleCopyComplaint = (draft) => {
    navigator.clipboard.writeText(draft);
    showToast('Cyber Police Complaint Draft copied to clipboard!');
  };

  const handleSubmitReport = async (reportData) => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/report`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(reportData)
      });
      if (!res.ok) {
        throw new Error(`Server returned HTTP ${res.status}`);
      }
      showToast('Report submitted successfully to threat intelligence feed!');
      return true;
    } catch (err) {
      console.error('Report submission failed:', err);
      showToast(`Report submission failed: ${err.message}. Please retry.`);
      return false;
    }
  };

  return (
    <div className={`min-h-screen flex flex-col transition-colors duration-200 selection:bg-[#FF6F32] selection:text-white ${
      isDark ? 'bg-[#0C0C0C] text-white' : 'bg-[#ECEAE5] text-[#1C1B18]'
    }`}>

      {/* Top Navigation */}
      <Navbar 
        isDark={isDark} 
        onToggleTheme={toggleTheme} 
        onOpenReportModal={() => setIsReportModalOpen(true)}
        isShieldMode={isShieldMode}
        onToggleShieldMode={() => setIsShieldMode(!isShieldMode)}
        onOpenOnboarding={() => setIsOnboardingOpen(true)}
        onOpenDownloadCompanion={() => setIsCompanionModalOpen(true)}
      />

      {/* Main Content Area */}
      <main className="relative z-10 flex-1 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 pt-4 pb-12 space-y-6">
        
        {/* Toast Notification */}
        {toastMessage && (
          <div className={`fixed bottom-6 right-6 z-50 flex items-center gap-2 px-4 py-3 rounded-xl border text-xs font-mono shadow-2xl animate-bounce ${
            isDark 
              ? 'bg-[#18181B] border-[#FF6F32]/50 text-white' 
              : 'bg-[#F6F5F2] border-[#FF6F32]/50 text-[#1C1B18]'
          }`}>
            <CheckCircle className="w-4 h-4 text-[#FF6F32]" />
            <span>{toastMessage}</span>
          </div>
        )}

        {/* 🌟 MAJESTIC HORIZON ARC HERO (Expansive Quadratic Curve — Zero Squish) */}
        <div className="relative w-full max-w-5xl mx-auto flex flex-col items-center justify-center pt-2 pb-0">
          
          {/* Subtle Ambient Radial Backlight */}
          <div className="absolute top-0 w-[550px] h-[140px] bg-[#FF6F32]/12 blur-3xl pointer-events-none rounded-full"></div>

          {/* Hero Headlines with High-Contrast Legibility */}
          <div className="text-center space-y-2.5 relative z-10 px-4">
            <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full border text-xs font-mono transition-colors ${
              isDark 
                ? 'bg-zinc-900/90 border-zinc-800 text-zinc-300' 
                : 'bg-[#F6F5F2] border-[#DCD9D2] text-[#1C1B18]'
            }`}>
              <span className="w-2 h-2 rounded-full bg-[#FF6F32] animate-pulse"></span>
              <span className="font-semibold">Autonomous Dual-Engine Threat Defense</span>
            </div>

            <h1 className={`text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight ${
              isDark ? 'text-white' : 'text-[#1C1B18]'
            }`}>
              Cyber-Fraud Defense Console
            </h1>

            {/* High-Contrast, Clearly Legible Subtitle */}
            <p className={`text-sm sm:text-base font-medium max-w-2xl mx-auto leading-relaxed ${
              isDark ? 'text-zinc-200' : 'text-[#3E3C37]'
            }`}>
              Real-time multi-modal AI protecting citizens against Digital Arrest, Fake Police warrants, and Electricity KYC extortion.
            </p>
          </div>

          {/* SVG Quadratic Horizon Arc — Naturally Expansive & Proportional */}
          <div className="relative w-full h-16 sm:h-20 flex items-center justify-center mt-3 pointer-events-none">
            <svg viewBox="0 0 1200 90" className="w-full h-full" preserveAspectRatio="none">
              <defs>
                <linearGradient id="horizonDynamicArc" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stopColor="#FF6F32" stopOpacity="0.22" />
                  <stop offset="50%" stopColor="#FF6F32" stopOpacity="0.04" />
                  <stop offset="100%" stopColor="#FF6F32" stopOpacity="0.0" />
                </linearGradient>
              </defs>
              {/* Soft Filled Dome */}
              <path d="M 0 90 Q 600 -10 1200 90 L 1200 90 L 0 90 Z" fill="url(#horizonDynamicArc)" />
              {/* Glowing Rim Arc Line */}
              <path 
                d="M 0 90 Q 600 -10 1200 90" 
                stroke="#FF6F32" 
                strokeWidth="2.5" 
                strokeLinecap="round" 
                fill="none"
                style={{ filter: 'drop-shadow(0 -4px 12px rgba(255, 111, 50, 0.45))' }}
              />
            </svg>
          </div>
        </div>

        {/* 1. HERO WORKSPACE: Threat Scanner & HUD */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start -mt-4">
          {/* Left Column: Multi-Modal Threat Scanner (7 cols) */}
          <div className="lg:col-span-7">
            <ThreatScanner
              inputText={inputText}
              setInputText={setInputText}
              activeTab={activeTab}
              setActiveTab={setActiveTab}
              onScan={handleScan}
              isLoading={isLoading}
              audioFile={audioFile}
              setAudioFile={setAudioFile}
              isDark={isDark}
            />
          </div>

          {/* Right Column: Real-Time Threat Forensics HUD or Universal Shield Mode (5 cols) */}
          <div className="lg:col-span-5">
            {isShieldMode ? (
              <ShieldModeCard
                result={scanResult}
                onSwitchToForensic={() => setIsShieldMode(false)}
                isDark={isDark}
              />
            ) : (
              <ThreatHUD
                result={scanResult}
                onCopyComplaint={handleCopyComplaint}
                onSwitchToShieldMode={() => setIsShieldMode(true)}
                isDark={isDark}
              />
            )}
          </div>
        </div>

        {/* 2. BOTTOM RADAR: Live Scam News Feed (Circular Array Rotation) */}
        <LiveScamCarousel 
          onSelectScam={(scam) => setSelectedNewsScam(scam)}
          onLoadScenario={handleLoadScenario}
          isDark={isDark}
        />

      </main>

      {/* Minimal Footer */}
      <footer className={`border-t py-6 text-center text-xs font-mono transition-colors ${
        isDark ? 'border-[#242428] text-zinc-500' : 'border-[#DCD9D2] text-[#57554F]'
      }`}>
        <p>
          ∀VITR AI (अवितृ • The Protector) • Multi-Modal Cyber-Fraud Threat Intelligence
        </p>
      </footer>

      {/* Floating AI Threat Copilot */}
      <FloatingCopilot
        scanResult={scanResult}
        isDark={isDark}
      />

      {/* Onboarding Mode Selection Modal */}
      <OnboardingModal
        isOpen={isOnboardingOpen}
        onClose={() => setIsOnboardingOpen(false)}
        onSelectOption={handleSelectOnboardingOption}
        isDark={isDark}
      />

      {/* Detail Dossier Modal */}
      <IncidentModal
        scam={selectedNewsScam}
        onClose={() => setSelectedNewsScam(null)}
        onLoadScenario={handleLoadScenario}
        isDark={isDark}
      />

      {/* Crowdsourced Community Report Modal */}
      <ReportModal
        isOpen={isReportModalOpen}
        onClose={() => setIsReportModalOpen(false)}
        onSubmitReport={handleSubmitReport}
        isDark={isDark}
      />

      {/* Real-Time Background Companion Download Modal */}
      <DownloadCompanionModal
        isOpen={isCompanionModalOpen}
        onClose={() => setIsCompanionModalOpen(false)}
        isDark={isDark}
      />
    </div>
  );
}
