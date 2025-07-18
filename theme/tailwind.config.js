module.exports = {
  darkMode: 'class', // or 'media' or 'class'
  content: [
    './templates/**/*.html',
    '../../templates/**/*.html',
    '../../**/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}