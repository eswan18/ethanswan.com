/** @type {import('tailwindcss').Config} */

module.exports = {
  content: ['../content/**/*.md', '../layouts/**/*.html'],
  theme: {
    extend: {
      colors: {
        "muted-heading": "var(--fallback-bc,oklch(var(--bc)/0.5))",
      },
    },
  },
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
  daisyui: {
    themes: [
      {
        light: {
          ...require("daisyui/src/theming/themes")["cmyk"],
        }
      },
      {
        dark: {
          ...require("daisyui/src/theming/themes")["night"],
        }
      },
    ],
  },
}
