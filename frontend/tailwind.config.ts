import type { Config } from 'tailwindcss'

export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f5ff',
          100: '#e0ebff',
          200: '#b8d4fe',
          300: '#7ab4fc',
          400: '#3890f9',
          500: '#0f6eeb',
          600: '#0253c9',
          700: '#0342a3',
          800: '#073986',
          900: '#0b316f',
        },
      },
    },
  },
  plugins: [],
} satisfies Config
