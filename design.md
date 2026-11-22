# 🎨 Design System & UI/UX Contract — ScamShield AI

**Project:** ScamShield AI  
**Author & Lead Architect:** Ayusman Mishra ([@Ayus-ProjeXion](https://github.com/Ayus-ProjeXion))  
**Theme:** Cyberpunk Mission Control / Dark Glassmorphism  
**Version:** 1.0.0  

---

## 1. Design Philosophy

ScamShield AI projects the high-authority, high-precision aesthetic of an **Enterprise Cyber Defense Operations Center**. It combines deep, low-eye-strain canvases with hyper-visible status indicators and glowing glass surfaces.

---

## 2. Color Tokens & Theme Palette

```css
:root {
  /* Core Background Canvas */
  --bg-primary: #0a0d14;            /* Midnight black / navy base */
  --bg-secondary: #0f172a;          /* Deep container background */
  --bg-card: rgba(15, 23, 42, 0.75);/* Frosted glass surface */
  --bg-card-hover: rgba(30, 41, 59, 0.9);

  /* Border & Glass Accents */
  --border-color: rgba(255, 255, 255, 0.08);
  --border-highlight: rgba(99, 102, 241, 0.4);
  --glass-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);

  /* Threat Severity Palette */
  --threat-critical: #ef4444;       /* 🔴 Red: Confirmed Scam / Malicious */
  --threat-high: #f97316;           /* 🟠 Orange: Suspicious / Impersonation */
  --threat-medium: #f59e0b;         /* 🟡 Amber: Moderate Risk / Unverified */
  --threat-low: #3b82f6;            /* 🔵 Blue: Informational */
  --threat-safe: #10b981;           /* 🟢 Green: Verified Clean / Whitelisted */

  /* Functional Accents */
  --accent-indigo: #6366f1;         /* Primary brand tone */
  --accent-cyan: #06b6d4;           /* AI telemetry & scanning pulses */
  --accent-emerald: #10b981;        /* System online indicator */

  /* Typography */
  --text-main: #f8fafc;             /* High contrast pure white */
  --text-muted: #94a3b8;            /* Slate gray */
  --text-dim: #64748b;              /* Low-contrast details */
}
```

---

## 3. Typography Hierarchy

* **Headings & Display:** `'Outfit', sans-serif` (Weights: 700, 800)
* **Body & Explanations:** `'Inter', sans-serif` (Weights: 400, 500, 600)
* **IOCs, Hashes, IP & Code:** `'JetBrains Mono', monospace` (Weights: 600, 700)

---

## 4. Component Standards

### 4.1 Threat Status Gauge
* Circular SVG or dynamic progress meter with continuous sweep animation.
* Transitions from Green (0-20% risk) to Amber (21-65%) to Red (66-100%).

### 4.2 IOC Card (.ioc-card)
* Monospaced identifier pill with copy-to-clipboard micro-interaction.
* Color-coded tag displaying entity type (URL, Phone, UPI, Domain).

### 4.3 AI Reason Breakdown Chips
* Distinct badges indicating specific heuristics:
  - `[Homoglyph Impersonation]`
  - `[High Linguistic Urgency]`
  - `[Unregistered Payment Gateway]`
  - `[Domain Age < 7 Days]`
