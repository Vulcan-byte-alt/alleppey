/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./*.html'],
  theme: {
    extend: {
      colors: {
        'neon-green': '#9bd8b8',
        'dark-green': '#5aa882',
        'electric-green': '#6fbf96',
        'deep-black': '#0b1411',
        'soft-black': '#1a1a1a',
        'light-gray': '#f8fafc',
        'border-gray': '#2a2a2a',
        'glass-white': 'rgba(255, 255, 255, 0.1)',
        'glass-green': 'rgba(155, 216, 184, 0.1)',
        green: { 200: '#d3eee0', 300: '#b4e3cb', 400: '#9bd8b8', 500: '#6fbf96', 600: '#4f9f78', 700: '#3f8564' },
        emerald: { 400: '#9bd8b8', 500: '#6fbf96', 600: '#4f9f78', 700: '#3f8564' },
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
