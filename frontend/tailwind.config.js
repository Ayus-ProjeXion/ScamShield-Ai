/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        midnight: {
          base: '#0C0C0C',
          card: '#141416',
          border: '#242428',
          hover: '#1B1B1F',
          muted: '#71717A',
        },
        cyber: {
          base: '#080614',
          card: '#100C24',
          border: '#2E225C',
          hover: '#181238',
          violet: '#5E56FF',
          violetSubtle: '#4B43E926',
          // Rich Radiant 24K Gold
          gold: '#FBBF24',
          goldBright: '#FCD34D',
          goldDeep: '#F59E0B',
          goldGlow: 'rgba(251, 191, 36, 0.4)',
          muted: '#A59EC8',
        },
        soothing: {
          base: '#ECEAE5',
          card: '#F6F5F2',
          border: '#DCD9D2',
          hover: '#E4E2DC',
          text: '#1C1B18',
          muted: '#57554F',
        },
        accent: {
          orange: '#FF6F32',
          orangeHover: '#E55B1F',
          orangeSubtle: '#FF6F321A',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Consolas', 'monospace']
      }
    },
  },
  plugins: [],
}
