"use client";

import { useEffect } from "react";
import { isAuthenticated } from "../../lib/auth";
import { useRouter } from "next/navigation";
import DetectionForm from "../../components/DetectionForm";
import Navbar from "../../components/Navbar";
import Footer from "../../components/Footer";

export default function DetectPage() {
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated()) {
      router.push("/");
    }
  }, [router]);

  return (
    <>
      <Navbar />
      <main className="min-h-screen bg-gradient-to-b from-gray-50 to-blue-50 dark:from-gray-900 dark:to-blue-950/30">
        {/* Decorative elements */}
        <div className="absolute top-0 right-0 w-1/3 h-screen bg-gradient-to-b from-blue-500/5 to-transparent -z-10"></div>
        <div className="absolute top-1/4 left-10 w-48 h-48 bg-blue-500/10 rounded-full blur-3xl -z-10"></div>
        <div className="absolute bottom-1/3 right-10 w-64 h-64 bg-accent/10 rounded-full blur-3xl -z-10"></div>

        <div className="container mx-auto px-4 py-16 relative">
          {/* Page header with decorative elements */}
          <div className="relative mb-12">
            <div className="absolute inset-0 -z-10">
              <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-32 h-32 bg-blue-500/20 rounded-full blur-xl"></div>
            </div>

            <div className="text-center">
              <div className="inline-block">
                <span className="inline-block relative">
                  <span className="absolute inset-0 rounded-lg bg-gradient-to-r from-blue-600/20 to-accent/20 blur-xl -z-10"></span>
                  <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r text-white bg-clip-text">
                    Deteksi Retinopati
                  </h1>
                </span>
                <div className="h-1 w-full bg-gradient-to-r from-blue-600 to-accent rounded-full"></div>
              </div>
              <p className="mt-4 text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
                Unggah gambar retina Anda untuk analisis menggunakan teknologi
                kecerdasan buatan kami.
              </p>
            </div>
          </div>

          {/* Content section with animated card */}
          <div className="max-w-5xl mx-auto relative animate-fadeIn">
            {/* Card decorative elements */}
            <div className="absolute -top-4 -left-4 w-24 h-24 bg-blue-500/10 rounded-full blur-xl -z-10"></div>
            <div className="absolute -bottom-4 -right-4 w-32 h-32 bg-accent/10 rounded-full blur-xl -z-10"></div>

            <div className="relative p-1 rounded-2xl bg-gradient-to-r from-blue-500 via-blue-400 to-accent">
              <div className="absolute top-0 left-0 w-full h-full bg-white dark:bg-gray-900 rounded-2xl opacity-80 backdrop-blur-sm -z-10"></div>
              <div className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm rounded-xl p-6 md:p-8 shadow-xl">
                <DetectionForm />
              </div>
            </div>

            {/* Info cards */}
            <div className="grid md:grid-cols-3 gap-6 mt-12">
              {[
                {
                  icon: (
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-7 w-7"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor">
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={1.5}
                        d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                      />
                    </svg>
                  ),
                  title: "Keamanan Data",
                  description:
                    "Semua data yang diunggah dilindungi dengan enkripsi tingkat tinggi",
                },
                {
                  icon: (
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-7 w-7"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor">
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={1.5}
                        d="M13 10V3L4 14h7v7l9-11h-7z"
                      />
                    </svg>
                  ),
                  title: "Analisis Cepat",
                  description: "Hasil deteksi retinopati dalam hitungan detik",
                },
                {
                  icon: (
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-7 w-7"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor">
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={1.5}
                        d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                      />
                    </svg>
                  ),
                  title: "Rekam Medis",
                  description:
                    "Riwayat hasil deteksi tersimpan dalam akun Anda",
                },
              ].map((card, index) => (
                <div
                  key={index}
                  className="relative overflow-hidden group rounded-xl p-6 bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm border border-gray-100 dark:border-gray-700 shadow-lg">
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-accent/5 opacity-0 group-hover:opacity-100 transition-opacity duration-500 -z-10"></div>
                  <div className="absolute -bottom-1.5 left-0 right-0 h-1.5 bg-gradient-to-r from-blue-500 to-accent transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"></div>

                  <div className="rounded-full bg-blue-100 dark:bg-blue-900/40 p-3 w-14 h-14 flex items-center justify-center mb-4 text-blue-600 dark:text-blue-400">
                    {card.icon}
                  </div>
                  <h3 className="text-lg font-bold text-gray-800 dark:text-white mb-2">
                    {card.title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300">
                    {card.description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
