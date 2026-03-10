/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        slateBrand: "#0f172a",
        accent: "#0ea5e9",
        success: "#10b981",
        warning: "#f59e0b"
      }
    }
  },
  plugins: []
};
