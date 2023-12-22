/** @type {import('tailwindcss').Config} */

module.exports = {
  content: ['../content/**/*.md', '../layouts/**/*.html'],
  theme: {},
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
  daisyui: {
    themes: ["fantasy", "night"],
  },
}
