import { Inter, Open_Sans, Geist_Mono } from "next/font/google";
import "./globals.css";

// Font untuk judul
const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  weight: ['500', '600', '700', '800'],
  display: 'swap',
});

// Font untuk teks utama
const openSans = Open_Sans({
  variable: "--font-open-sans",
  subsets: ["latin"],
  weight: ['400', '500', '600'],
  display: 'swap',
});

// Font monospace untuk bagian teknis
const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "RetinoCare - Deteksi Retinopati berbasis AI",
  description: "Deteksi dini retinopati diabetik menggunakan teknologi kecerdasan buatan",
};

export default function RootLayout({ children }) {
  return (
    <html lang="id" className="scroll-smooth">
      <body
        className={`${inter.variable} ${openSans.variable} ${geistMono.variable} 
        font-sans antialiased bg-background text-foreground 
        selection:bg-blue-200 selection:text-blue-800 dark:selection:bg-blue-800 dark:selection:text-blue-200
        min-h-screen flex flex-col`}
      >
        <div className="flex flex-col flex-1 overflow-hidden">
          {children}
        </div>
        
        {/* Gradient decoration elements */}
        <div className="fixed inset-x-0 top-0 -z-10 transform-gpu overflow-hidden blur-3xl" aria-hidden="true">
          <div className="relative left-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] -translate-x-1/2 rotate-[30deg] bg-gradient-to-tr from-blue-700 to-accent opacity-20 sm:left-[calc(50%-30rem)] sm:w-[72.1875rem]"></div>
        </div>
        
        <div className="fixed inset-x-0 bottom-0 -z-10 transform-gpu overflow-hidden blur-3xl" aria-hidden="true">
          <div className="relative right-[calc(50%-11rem)] aspect-[1155/678] w-[36.125rem] translate-x-1/2 rotate-[210deg] bg-gradient-to-tr from-accent to-blue-700 opacity-20 sm:right-[calc(50%-36rem)] sm:w-[72.1875rem]"></div>
        </div>
      </body>
    </html>
  );
}