import React, { useState, useEffect, useRef } from 'react';
import {
  ShieldAlert,
  ShieldCheck,
  AlertTriangle,
  Ban,
  X,
  Bell,
  Check,
  Radio,
  Power
} from 'lucide-react';

/**
 * Ultra-Low Latency Sound Feedback (< 1ms Web Audio)
 * Provides instant acoustic confirmation the exact millisecond text is copied.
 */
function playAlertChime(isScam) {
  try {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextClass) return;
    const ctx = new AudioContextClass();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.connect(gain);
    gain.connect(ctx.destination);

    if (isScam) {
      // 🚨 High-urgency alert ping (Dual tone 880Hz -> 440Hz)
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(880, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(440, ctx.currentTime + 0.18);
      gain.gain.setValueAtTime(0.18, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.18);
      osc.start(ctx.currentTime);
      osc.stop(ctx.currentTime + 0.18);
    } else {
      // 🟢 Gentle high-clarity safe chime (587Hz -> 880Hz)
      osc.type = 'sine';
      osc.frequency.setValueAtTime(587.33, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.14);
      gain.gain.setValueAtTime(0.12, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.14);
      osc.start(ctx.currentTime);
      osc.stop(ctx.currentTime + 0.14);
    }
  } catch (err) {
    // Audio context may be muted or require user gesture - silent pass
  }
}

/**
 * LiveInterceptorBanner
 * Delivers instant real-time threat interception for copied text.
 * Starts PAUSED by default on page load. Turns on ONLY when explicitly clicked by user.
 */
export function LiveInterceptorBanner({ onTriggerScan, onOpenReport, isDark }) {
  // STRICT REQUIREMENT: Defaults to FALSE (PAUSED). Turns on only when user explicitly clicks!
  const [isLiveActive, setIsLiveActive] = useState(false);
  const [lastProcessedText, setLastProcessedText] = useState('');
  const [interceptedThreat, setInterceptedThreat] = useState(null);
  const [hasNotificationPermission, setHasNotificationPermission] = useState(
    typeof window !== 'undefined' && 'Notification' in window ? Notification.permission === 'granted' : false
  );

  const lastProcessedRef = useRef('');
  const lastProcessedTimeRef = useRef(0);
  const lastNotifiedTextRef = useRef('');
  const isCheckingRef = useRef(false);

  // Fast autonomous heuristic engine (< 0.05ms execution)
  const classifyMessage = (rawText) => {
    const textLower = rawText.toLowerCase();

    // 1. Critical Scam Signatures (90% - 98%)
    const isElectricity = (textLower.includes('bijli') || textLower.includes('electricity')) &&
      (textLower.includes('disconnect') || textLower.includes('update') || textLower.includes('bill') || textLower.includes('officer') || textLower.includes('tonight'));
    
    const isDigitalArrest = (textLower.includes('cbi') || textLower.includes('police') || textLower.includes('digital arrest') || textLower.includes('warrant')) &&
      (textLower.includes('court') || textLower.includes('customs') || textLower.includes('narcotics') || textLower.includes('mdma') || textLower.includes('arrest') || textLower.includes('money laundering'));

    const isCustomsCourier = (textLower.includes('customs') || textLower.includes('fedex') || textLower.includes('consignment') || textLower.includes('parcel')) &&
      (textLower.includes('clearance') || textLower.includes('penalty') || textLower.includes('pay') || textLower.includes('fee'));

    const isCredentialTheft = textLower.includes('otp') && (textLower.includes('share') || textLower.includes('send') || textLower.includes('tell') || textLower.includes('call') || textLower.includes('kyc') || textLower.includes('pin'));

    const isLotteryKbc = (textLower.includes('kbc') || textLower.includes('lottery') || textLower.includes('25 lakh') || textLower.includes('lucky draw')) &&
      (textLower.includes('won') || textLower.includes('winner') || textLower.includes('prize') || textLower.includes('claim'));

    const isMaliciousApk = textLower.includes('.apk') || textLower.includes('install update') || textLower.includes('quicksupport');

    if (isElectricity || isDigitalArrest || isCustomsCourier || isCredentialTheft || isLotteryKbc || isMaliciousApk) {
      let threatType = 'High-Risk Cyber Fraud';
      if (isElectricity) threatType = 'Electricity KYC Disconnection Scam';
      else if (isDigitalArrest) threatType = 'Fake Police / CBI Digital Arrest Extortion';
      else if (isCustomsCourier) threatType = 'Customs / Courier Drug Extortion';
      else if (isCredentialTheft) threatType = 'Credential Phishing (OTP / PIN Solicitation)';
      else if (isLotteryKbc) threatType = 'KBC / Lottery Advance-Fee Scam';
      else if (isMaliciousApk) threatType = 'Malicious Android APK Delivery';

      return {
        isScam: true,
        isCareful: false,
        isSafe: false,
        risk: 96,
        verdict: 'POSSIBLE SCAM',
        threatType,
        badgeClass: 'bg-red-500/20 text-red-400 border-red-500/40',
        advice: 'DO NOT click links, download APK files, or transfer funds!'
      };
    }

    // 2. Safe Message Signatures (0% - 5%)
    const isBankTxn = (textLower.includes('debited') || textLower.includes('credited')) &&
      (textLower.includes('a/c') || textLower.includes('account') || textLower.includes('bal') || textLower.includes('vpa') || textLower.includes('upi ref'));

    const isBenignChat = !textLower.includes('http') && !textLower.includes('urgent') && !textLower.includes('verify') && !textLower.includes('blocked') && (
      textLower.includes('bhai') || textLower.includes('hello') || textLower.includes('hi ') || textLower.includes('meeting') ||
      textLower.includes('dinner') || textLower.includes('call you later') || textLower.includes('how are you') || textLower.includes('thank')
    );

    if (isBankTxn || isBenignChat) {
      return {
        isScam: false,
        isCareful: false,
        isSafe: true,
        risk: 0,
        verdict: 'SAFE SIGNAL',
        threatType: isBankTxn ? 'Legitimate Bank Transaction Alert' : 'Normal Benign Communication',
        badgeClass: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40',
        advice: 'No suspicious indicators or extortion heuristics detected.'
      };
    }

    // 3. Medium / Caution Signatures (30% - 60%)
    if (textLower.includes('http') || textLower.includes('urgent') || textLower.includes('immediate') || textLower.includes('verify') || textLower.includes('block')) {
      return {
        isScam: false,
        isCareful: true,
        isSafe: false,
        risk: 45,
        verdict: 'BE CAREFUL',
        threatType: 'Unverified Urgent Link / Notice',
        badgeClass: 'bg-amber-500/20 text-amber-400 border-amber-500/40',
        advice: 'Exercise caution. Verify the official sender before proceeding.'
      };
    }

    return {
      isScam: false,
      isCareful: false,
      isSafe: true,
      risk: 10,
      verdict: 'SAFE SIGNAL',
      threatType: 'Standard Communication',
      badgeClass: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/40',
      advice: 'No urgent coercion or threat indicators detected.'
    };
  };

  const triggerLiveDetection = (cleanText, allowDesktopPush = true) => {
    // 1. Instant autonomous classification
    const analysis = classifyMessage(cleanText);

    const alertPayload = {
      ...analysis,
      text: cleanText,
      timestamp: new Date().toLocaleTimeString(),
      source: 'Clipboard Copy'
    };

    setInterceptedThreat(alertPayload);

    // 2. Play acoustic chime feedback
    playAlertChime(alertPayload.isScam);

    // 3. Desktop Native Push Notification (debounced per unique text)
    if (allowDesktopPush && hasNotificationPermission && lastNotifiedTextRef.current !== cleanText) {
      lastNotifiedTextRef.current = cleanText;
      if (typeof window !== 'undefined' && 'Notification' in window && Notification.permission === 'granted') {
        const preview = cleanText.length > 70 ? cleanText.substring(0, 67) + '...' : cleanText;
        try {
          if (alertPayload.isScam) {
            new Notification('🚨 ∀VITR AI: SCAM INTERCEPTED!', {
              body: `[🚨 Scam Detected ${alertPayload.risk}%] ${alertPayload.threatType}\n"${preview}"\n👉 ${alertPayload.advice}`,
              icon: '/favicon.ico',
              tag: 'avitr-live-alert',
              renotify: true
            });
          } else if (alertPayload.isCareful) {
            new Notification('🟡 ∀VITR AI: CAUTION RECOMMENDED', {
              body: `[🟡 Be Careful ${alertPayload.risk}%] ${alertPayload.threatType}\n"${preview}"\n${alertPayload.advice}`,
              icon: '/favicon.ico',
              tag: 'avitr-live-alert',
              renotify: true
            });
          }
        } catch (notifErr) {
          console.warn('Desktop notification dispatch:', notifErr);
        }
      }
    }

    // 4. Asynchronous Background Sync to Deep Neural Engine
    if (onTriggerScan) {
      setTimeout(() => {
        onTriggerScan(cleanText);
      }, 0);
    }
  };

  // Continuous background listener ONLY runs when isLiveActive is TRUE
  useEffect(() => {
    if (!isLiveActive) return;

    const checkClipboardNow = async (allowDesktopPush = true, isExplicitCopy = false) => {
      if (isCheckingRef.current) return;
      isCheckingRef.current = true;
      try {
        if (!navigator.clipboard || !navigator.clipboard.readText) {
          isCheckingRef.current = false;
          return;
        }

        const text = await navigator.clipboard.readText();
        if (text && typeof text === 'string') {
          const clean = text.trim();
          const now = Date.now();
          const isNewText = clean !== lastProcessedRef.current;
          const isReCopy = isExplicitCopy || (now - lastProcessedTimeRef.current > 1000);

          if (clean.length >= 6 && (isNewText || isReCopy)) {
            lastProcessedRef.current = clean;
            lastProcessedTimeRef.current = now;
            setLastProcessedText(clean);
            triggerLiveDetection(clean, allowDesktopPush);
          }
        }
      } catch (err) {
        // Document not focused or permission pending - silent pass
      } finally {
        isCheckingRef.current = false;
      }
    };

    // Initial check when activated
    checkClipboardNow(false, false);

    // 120ms cycle for instant response while active
    const intervalId = setInterval(() => checkClipboardNow(true, false), 120);

    const handleFocus = () => checkClipboardNow(false, false);
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        checkClipboardNow(false, false);
      }
    };
    const handleCopy = () => setTimeout(() => checkClipboardNow(true, true), 10);
    const handlePaste = () => setTimeout(() => checkClipboardNow(true, true), 10);

    window.addEventListener('focus', handleFocus);
    document.addEventListener('visibilitychange', handleVisibilityChange);
    window.addEventListener('copy', handleCopy);
    window.addEventListener('paste', handlePaste);

    return () => {
      clearInterval(intervalId);
      window.removeEventListener('focus', handleFocus);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      window.removeEventListener('copy', handleCopy);
      window.removeEventListener('paste', handlePaste);
    };
  }, [isLiveActive, hasNotificationPermission]);

  const requestNotificationPermission = async () => {
    if (typeof window !== 'undefined' && 'Notification' in window) {
      try {
        const perm = await Notification.requestPermission();
        setHasNotificationPermission(perm === 'granted');
      } catch (e) {
        console.warn('Notification permission error:', e);
      }
    }
  };

  const toggleLiveInterceptor = () => {
    const nextState = !isLiveActive;
    setIsLiveActive(nextState);
    if (nextState && typeof window !== 'undefined' && 'Notification' in window && Notification.permission === 'default') {
      requestNotificationPermission();
    }
  };

  return (
    <div className="w-full space-y-3">
      {/* Interceptor Status Strip */}
      <div className={`w-full py-2.5 px-4 rounded-2xl border flex flex-wrap items-center justify-between gap-3 text-xs font-mono transition-all ${
        isLiveActive
          ? (isDark ? 'bg-emerald-950/20 border-emerald-500/30 text-emerald-400' : 'bg-emerald-50 border-emerald-300 text-emerald-900')
          : (isDark ? 'bg-zinc-900/60 border-zinc-800 text-zinc-400' : 'bg-[#F6F5F2] border-[#DCD9D2] text-zinc-600')
      }`}>
        {/* Status Indicator */}
        <div className="flex items-center gap-2.5">
          <span className="relative flex h-2.5 w-2.5">
            {isLiveActive ? (
              <>
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
              </>
            ) : (
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-zinc-500"></span>
            )}
          </span>
          <span className={`font-bold ${isLiveActive ? 'text-emerald-400' : 'text-zinc-400'}`}>
            {isLiveActive ? 'Live Clipboard Interceptor: ACTIVE' : 'Live Clipboard Interceptor: PAUSED (Click to Turn On)'}
          </span>
          <span className="text-zinc-500 hidden md:inline">•</span>
          <span className="text-zinc-400 hidden md:inline text-[11px]">
            {isLiveActive ? 'Monitoring clipboard for copied scams in real time' : 'Turn on to automatically scan copied messages'}
          </span>
        </div>

        {/* Controls */}
        <div className="flex items-center gap-2">
          {/* Notification Permission Button */}
          {!hasNotificationPermission && isLiveActive && (
            <button
              type="button"
              onClick={requestNotificationPermission}
              className="px-2.5 py-1 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 border border-amber-500/30 flex items-center gap-1.5 transition-all text-[11px] font-semibold"
              title="Enable native desktop notifications when scam messages are copied"
            >
              <Bell className="w-3 h-3 text-amber-400 animate-bounce" />
              <span>Allow Desktop Alerts</span>
            </button>
          )}

          {/* User-Triggered Activation Button */}
          <button
            type="button"
            onClick={toggleLiveInterceptor}
            className={`px-3 py-1.5 rounded-xl border text-xs font-semibold flex items-center gap-1.5 transition-all shadow-sm ${
              isLiveActive
                ? (isDark ? 'border-zinc-700 bg-zinc-800 text-zinc-300 hover:text-white' : 'border-zinc-300 bg-zinc-100 text-zinc-700 hover:text-black')
                : 'border-emerald-500/60 bg-emerald-500/15 text-emerald-400 hover:bg-emerald-500/25 hover:border-emerald-500'
            }`}
          >
            <Power className={`w-3.5 h-3.5 ${isLiveActive ? 'text-zinc-400' : 'text-emerald-400'}`} />
            <span>{isLiveActive ? 'Pause Interceptor' : 'Turn On Live Interceptor'}</span>
          </button>
        </div>
      </div>

      {/* Immediate Autonomous Notification Pop-Card */}
      {interceptedThreat && (
        <div className="w-full animate-in slide-in-from-top-3 duration-150">
          <div className={`p-4 rounded-2xl border shadow-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4 ${
            interceptedThreat.isScam
              ? (isDark ? 'bg-red-950/40 border-red-500/50 text-white' : 'bg-red-50 border-red-300 text-red-950')
              : interceptedThreat.isCareful
                ? (isDark ? 'bg-amber-950/40 border-amber-500/50 text-white' : 'bg-amber-50 border-amber-300 text-amber-950')
                : (isDark ? 'bg-emerald-950/40 border-emerald-500/50 text-white' : 'bg-emerald-50 border-emerald-300 text-emerald-950')
          }`}>
            <div className="flex items-start gap-3.5">
              <div className={`p-2.5 rounded-xl flex-shrink-0 ${
                interceptedThreat.isScam
                  ? 'bg-red-500 text-white animate-pulse'
                  : interceptedThreat.isCareful
                    ? 'bg-amber-500 text-white'
                    : 'bg-emerald-500 text-white'
              }`}>
                {interceptedThreat.isScam ? (
                  <ShieldAlert className="w-6 h-6" />
                ) : interceptedThreat.isCareful ? (
                  <AlertTriangle className="w-6 h-6" />
                ) : (
                  <ShieldCheck className="w-6 h-6" />
                )}
              </div>

              <div className="space-y-1">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-[11px] font-mono font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-black/20">
                    ⚡ {interceptedThreat.source}
                  </span>
                  <span className={`text-[10px] font-mono font-extrabold px-2 py-0.5 rounded-full border ${interceptedThreat.badgeClass}`}>
                    {interceptedThreat.verdict} ({interceptedThreat.risk}%)
                  </span>
                  <span className="text-xs font-semibold text-zinc-300">
                    • {interceptedThreat.threatType}
                  </span>
                </div>
                <p className="text-xs line-clamp-2 italic font-sans opacity-95">
                  "{interceptedThreat.text}"
                </p>
                <p className={`text-[11px] font-medium ${
                  interceptedThreat.isScam ? 'text-red-400' : interceptedThreat.isCareful ? 'text-amber-400' : 'text-emerald-400'
                }`}>
                  👉 {interceptedThreat.advice}
                </p>
              </div>
            </div>

            {/* Quick Actions */}
            <div className="flex items-center gap-2 w-full md:w-auto justify-end flex-shrink-0">
              {interceptedThreat.isScam && (
                <button
                  type="button"
                  onClick={() => {
                    onOpenReport('Intercepted Threat', interceptedThreat.text);
                    setInterceptedThreat(null);
                  }}
                  className="px-3 py-1.5 rounded-xl bg-red-600 hover:bg-red-700 text-white text-xs font-semibold flex items-center gap-1.5 transition-all shadow-sm active:scale-95"
                >
                  <Ban className="w-3.5 h-3.5" />
                  <span>Block & Report</span>
                </button>
              )}

              <button
                type="button"
                onClick={() => setInterceptedThreat(null)}
                className="p-1.5 rounded-xl hover:bg-black/20 text-zinc-400 hover:text-white transition-colors"
                title="Dismiss"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
