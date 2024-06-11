/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./src/**/*.{html,js,jsx,ts,tsx}"],
    theme: {
        colors: {
            gray: {
                900: "#121212",
                800: "#1c1c1c",
                700: "#292929",
                600: "#373737",
                500: "#4c4c4c",
                300: "#8c8c8c",
                200: "#dededf",
                100: "#f9fafb",
            },


            primary: {
                900: "#6E1B00",
                700: "#B22C00",
                500: "#F6521D",
                200: "#FFDED2",
                100: "#FFEEE8",
            },

            error: {
                900: "#7F1D1D",
                500: "#EF4444",
                400: "#FF5252",
                50: "#FEF2F2",
            },

            info: {
                900: "#1E3A8A",
                500: "#3B82F6",
                50: "#EFF6FF",
            },

            warning: {
                900: "#78350F",
                500: "#F59E0B",
                50: "#FFFBEB",
            },

            success: {
                900: "#064e3b",
                500: "#65c366",
                400: "#5AE05F",
                50: "#ecfdf5",
            },

            black: "#111",
            white: "#fff",
        },
    },
    plugins: []
};
