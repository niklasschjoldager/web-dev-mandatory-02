module.exports = {
  mode: "JIT",
  content: ["../views/**/*.html"],
  theme: {
    colors: {
      transparent: "transparent",
      current: "currentColor",
      white: "hsl(0, 0%, 100%)",
      black: "hsl(213, 27%, 8%)",
      primary: {
        100: "hsl(204, 79%, 47%)",
        200: "hsl(204, 88%, 53%)",
      },
      gray: {
        100: "hsl(192, 20%, 95%)",
        200: "hsl(180, 12%, 97%)",
        300: "hsl(199, 20%, 84%)",
        400: "hsl(206, 15%, 38%)",
        500: "hsl(207, 10%, 17%)",
      },
    },
  },
  plugins: [],
}
