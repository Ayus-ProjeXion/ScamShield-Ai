import React, { useState, useEffect } from 'react';
import { 
  ChevronLeft, 
  ChevronRight, 
  MapPin, 
  ExternalLink 
} from 'lucide-react';
import { LIVE_SCAM_NEWS } from '../data/scamNews';

export function LiveScamCarousel({ onSelectScam, onLoadScenario, isDark }) {
  const [startIndex, setStartIndex] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const total = LIVE_SCAM_NEWS.length;

  // Circular Array Auto-Rotation
  useEffect(() => {
    if (isPaused) return;
    const interval = setInterval(() => {
      setStartIndex((prev) => (prev + 1) % total);
    }, 4000);
    return () => clearInterval(interval);
  }, [isPaused, total]);

  const handlePrev = () => {
    setStartIndex((prev) => (prev - 1 + total) % total);
  };

  const handleNext = () => {
    setStartIndex((prev) => (prev + 1) % total);
  };

  // Generate 4 visible cards using true Circular Array indexing: (startIndex + i) % total
  const visibleCards = [0, 1, 2, 3].map((offset) => {
    const itemIndex = (startIndex + offset) % total;
    return {
      ...LIVE_SCAM_NEWS[itemIndex],
      arraySlot: offset,
      originalIndex: itemIndex
    };
  });

  return (
    <section 
      className={`rounded-2xl border p-5 shadow-lg space-y-4 transition-colors duration-200 ${
        isDark 
          ? 'bg-[#141416] border-[#242428]' 
          : 'bg-[#F6F5F2] border-[#DCD9D2]'
      }`}
      onMouseEnter={() => setIsPaused(true)}
      onMouseLeave={() => setIsPaused(false)}
    >
      {/* Header Strip */}
      <div className={`flex flex-wrap items-center justify-between gap-3 pb-3 border-b ${
        isDark ? 'border-[#242428]' : 'border-[#DCD9D2]'
      }`}>
        <div className="flex items-center gap-2">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[#FF6F32] opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-[#FF6F32]"></span>
          </span>
          <h3 className={`font-bold text-sm sm:text-base flex items-center gap-2 ${
            isDark ? 'text-white' : 'text-[#1C1B18]'
          }`}>
            <span>Live Threat Intelligence Feed</span>
            <span className="text-[11px] font-mono text-zinc-400 font-normal hidden sm:inline">
              (Circular Radar Array)
            </span>
          </h3>
        </div>

        {/* Controls */}
        <div className="flex items-center gap-3">
          <span className="text-[11px] text-zinc-400 font-mono hidden md:inline">
            {isPaused ? 'Paused on Hover' : 'Circular Rotating'}
          </span>
          <div className="flex items-center gap-1">
            <button
              onClick={handlePrev}
              className={`p-1.5 rounded-lg border transition-colors ${
                isDark 
                  ? 'bg-[#18181B] border-[#27272A] text-zinc-300 hover:text-white' 
                  : 'bg-[#ECEAE5] border-[#DCD9D2] text-[#1C1B18] hover:bg-[#E4E2DC]'
              }`}
              title="Rotate Left"
            >
              <ChevronLeft className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={handleNext}
              className={`p-1.5 rounded-lg border transition-colors ${
                isDark 
                  ? 'bg-[#18181B] border-[#27272A] text-zinc-300 hover:text-white' 
                  : 'bg-[#ECEAE5] border-[#DCD9D2] text-[#1C1B18] hover:bg-[#E4E2DC]'
              }`}
              title="Rotate Right"
            >
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Circular Array Sliding Card Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 overflow-hidden">
        {visibleCards.map((item) => (
          <div
            key={`${item.id}-${item.originalIndex}`}
            onClick={() => onSelectScam(item)}
            className={`rounded-xl p-3 cursor-pointer border flex flex-col justify-between gap-3 group transition-all duration-300 transform hover:-translate-y-1 ${
              isDark
                ? 'bg-[#0C0C0C] border-[#242428] hover:border-[#FF6F32]/50 hover:bg-[#18181B]'
                : 'bg-[#ECEAE5] border-[#DCD9D2] hover:border-[#FF6F32]/50 hover:bg-[#E4E2DC]'
            }`}
          >
            {/* Thumbnail */}
            <div className="relative w-full h-28 rounded-lg overflow-hidden bg-black/40">
              <img 
                src={item.imageUrl} 
                alt={item.title} 
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300 opacity-85"
              />
              <div className="absolute top-1.5 right-1.5 px-2 py-0.5 rounded-md bg-black/85 text-[11px] font-mono font-bold text-[#FF6F32]">
                {item.riskScore}% SEV
              </div>
              <div className="absolute bottom-1.5 left-1.5 px-2 py-0.5 rounded bg-black/75 text-[10px] font-mono text-zinc-300 flex items-center gap-1">
                <MapPin className="w-3 h-3 text-[#FF6F32]" />
                <span>{item.region}</span>
              </div>
            </div>

            {/* Content */}
            <div className="space-y-1 flex-1 flex flex-col justify-between">
              <div>
                <span className="text-[10px] font-mono font-semibold text-[#FF6F32] uppercase tracking-wide block">
                  {item.badge}
                </span>
                <h4 className={`text-xs sm:text-sm font-semibold line-clamp-2 leading-snug mt-0.5 ${
                  isDark ? 'text-white' : 'text-[#1C1B18]'
                }`}>
                  {item.title}
                </h4>
              </div>

              <p className={`text-[11px] line-clamp-2 leading-relaxed mt-1 ${
                isDark ? 'text-zinc-400' : 'text-[#57554F]'
              }`}>
                {item.summary}
              </p>
            </div>

            {/* Quick Action Button */}
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                onLoadScenario(item.samplePayload);
              }}
              className={`w-full py-1.5 rounded-lg text-xs font-mono font-medium transition-colors flex items-center justify-center gap-1 ${
                isDark
                  ? 'bg-[#18181B] hover:bg-[#FF6F32] text-zinc-300 hover:text-white'
                  : 'bg-[#DCD9D2] hover:bg-[#FF6F32] text-[#1C1B18] hover:text-white'
              }`}
            >
              <span>Test in Scanner</span>
              <ExternalLink className="w-3 h-3" />
            </button>
          </div>
        ))}
      </div>

      {/* Circular Position Dots */}
      <div className="flex items-center justify-center gap-1.5 pt-1">
        {LIVE_SCAM_NEWS.map((_, dotIdx) => (
          <button
            key={dotIdx}
            onClick={() => setStartIndex(dotIdx)}
            className={`h-1.5 rounded-full transition-all ${
              dotIdx === startIndex 
                ? 'w-6 bg-[#FF6F32]' 
                : isDark ? 'w-1.5 bg-zinc-700 hover:bg-zinc-500' : 'w-1.5 bg-zinc-400 hover:bg-zinc-600'
            }`}
            title={`Jump to index ${dotIdx + 1}`}
          />
        ))}
      </div>
    </section>
  );
}
