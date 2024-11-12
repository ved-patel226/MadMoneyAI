module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  daisyui: {
    themes: [
      "lofi",
      "dim",
    ],
  },
  plugins: [require('daisyui')],
}
