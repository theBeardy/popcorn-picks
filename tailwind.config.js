// Example `tailwind.config.js` file
const colors = require('tailwindcss/colors')

module.exports = {
  content: [
    '../templates/**/*.html',
    '../../templates/**/*.html',
    './templates/**/*.html',
    './**/templates/**/*.html',
    './**/*.py',
    './src/**/*.{js,ts,jsx,tsx,html}'
  ],
  theme: {
    colors: {
      gray: colors.coolGray,
      blue: colors.lightBlue,
      red: colors.rose,
      pink: colors.fuchsia,
    },
    fontFamily: {
      sans: ['Graphik', 'sans-serif'],
      serif: ['Merriweather', 'serif'],
    },
    extend: {
      spacing: {
        '128': '32rem',
        '144': '36rem',
      },
      borderRadius: {
        '4xl': '2rem',
      }
    }
  },
  variants: {
    extend: {
      borderColor: ['focus-visible'],
      opacity: ['disabled'],
    }
  }
}