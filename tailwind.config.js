/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html"
  ],
  theme: {
    extend: {},
    colors: {
      'black': '#000000',
      'white': '#ffffff',
      'sd-green': '#009c82',
      'sd-red': '#cc0047',
      'sd-orange': '#F2B00D'
    },
    fontFamily: {
      sans: ['Arial', 'sans-serif']
    },
    container: {
      center: true,
      padding: '2rem',
    },
  },
  plugins: [],
}

