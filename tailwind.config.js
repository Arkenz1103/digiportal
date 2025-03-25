import defaultTheme from 'tailwindcss/defaultTheme';

/** @type {import('tailwindcss').Config} */
export default {
    content: [
        './vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php',
        './storage/framework/views/*.php',
        './resources/**/*.blade.php',
        './resources/**/*.js',
        './resources/**/*.vue',
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Poppins', ...defaultTheme.fontFamily.sans],
            },
        },
    },
    plugins: [require('tailwindcss-primeui')],
    safelist: [
        // Header backgrounds
        'bg-emerald-400', 'bg-blue-400', 'bg-purple-400', 'bg-rose-400', 'bg-amber-400', 'bg-teal-400',
        // Badge backgrounds
        'bg-emerald-200', 'bg-blue-200', 'bg-purple-200', 'bg-rose-200', 'bg-amber-200', 'bg-teal-200',
        // Member header and buttons
        'bg-emerald-500', 'bg-blue-500', 'bg-purple-500', 'bg-rose-500', 'bg-amber-500', 'bg-teal-500',
        'bg-emerald-600', 'bg-blue-600', 'bg-purple-600', 'bg-rose-600', 'bg-amber-600', 'bg-teal-600',
    ],
};
