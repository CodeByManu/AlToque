/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Paleta verde/beige — placeholders, reemplazar con hex definitivos.
        brand: {
          DEFAULT: "#5C7C4E",
          dark: "#3F5836",
          light: "#A8C09A",
        },
        beige: {
          DEFAULT: "#F5EFE0",
          card: "#FAF6EC",
          deep: "#EAE2CC",
        },
        ink: {
          DEFAULT: "#1F2A1C",
          soft: "#4A5747",
          mute: "#8A9385",
        },
        alert: {
          DEFAULT: "#D97757",
          soft: "#F4D6C8",
        },
      },
      fontFamily: {
        sans: [
          "system-ui",
          "-apple-system",
          "Segoe UI",
          "Helvetica",
          "Arial",
          "sans-serif",
        ],
      },
      boxShadow: {
        card: "0 1px 2px rgba(31,42,28,0.04), 0 4px 12px rgba(31,42,28,0.06)",
      },
    },
  },
  plugins: [],
};
