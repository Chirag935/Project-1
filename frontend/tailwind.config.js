/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'climate': {
          'excellent': '#10B981',
          'good': '#34D399',
          'moderate': '#FBBF24',
          'poor': '#F87171',
          'very-poor': '#EF4444'
        }
      }
    },
  },
  plugins: [],
}