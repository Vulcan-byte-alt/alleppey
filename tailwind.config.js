/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./*.html'],
  theme: {
    extend: {
      colors: {
        'neon-green': '#00ff88',
        'dark-green': '#10b981',
        'electric-green': '#22c55e',
        'deep-black': '#0a0a0a',
        'soft-black': '#1a1a1a',
        'light-gray': '#f8fafc',
        'border-gray': '#2a2a2a',
        'glass-white': 'rgba(255, 255, 255, 0.1)',
        'glass-green': 'rgba(0, 255, 136, 0.1)',
        'glass-dark': 'rgba(26, 26, 26, 0.8)'
      },
      fontFamily: {
        'sans': ['Source Sans Pro', 'system-ui', 'sans-serif'],
        'serif': ['Playfair Display', 'serif'],
        'display': ['Playfair Display', 'serif']
      },
      backdropBlur: {
        'xs': '2px',
      }
    }
  },
  plugins: [],
}
