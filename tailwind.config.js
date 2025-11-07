/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'active-red': '#e60021',
        'active-black': '#231916',
      },
      fontFamily: {
        'montserrat': ['Montserrat', 'sans-serif'],
        'noto-sans': ['Noto Sans', 'sans-serif'],
        'roboto': ['Roboto', 'sans-serif'],
      },
      animation: {
        'ken-burns': 'ken-burns 5s ease-in-out infinite',
      },
      keyframes: {
        'ken-burns': {
          '0%, 100%': { transform: 'scale(1) translate(0, 0)' },
          '50%': { transform: 'scale(1.1) translate(-2%, -2%)' },
        }
      }
    },
  },
  plugins: [],
}