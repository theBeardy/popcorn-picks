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
        dark: "var(--accent-light)",
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}