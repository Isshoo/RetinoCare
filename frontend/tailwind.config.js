
/** @type {import('tailwindcss').Config} */
export const content = [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
];
export const theme = {
    extend: {
        colors: {
            'primary': 'var(--color-primary)',
            'accent': 'var(--color-accent)',
            'success': 'var(--color-success)',
            'danger': 'var(--color-danger)',
            'light': 'var(--color-light)',
            'dark': 'var(--color-dark)',
            'background': 'var(--background)',
            'foreground': 'var(--foreground)',
        },
        fontFamily: {
            'sans': ['var(--font-open-sans)', 'ui-sans-serif', 'system-ui'],
            'inter': ['var(--font-inter)', 'ui-sans-serif', 'system-ui'],
            'mono': ['var(--font-geist-mono)', 'ui-monospace', 'monospace'],
        },
    },
};
export const plugins = [];