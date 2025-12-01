"use client";
import { useRouter } from "next/navigation";
import AuthForm from "../../components/AuthForm";
import { useEffect } from "react";
import { isAuthenticated } from "@/lib/auth";
import Link from "next/link";

export default function LoginPage() {
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated()) {
      router.push("/");
    }
  }, [router]);

  if (isAuthenticated()) {
    return null;
  }

  return (
    <div className="relative min-h-screen w-full overflow-hidden flex">
      {/* Left side - decorative panel (visible on md and up) */}
      <div className="hidden md:block md:w-1/2 bg-gradient-to-br from-blue-600 to-blue-800 relative">
        {/* Pola titik dekoratif */}
        <div
          className="absolute inset-0 opacity-20"
          style={{
            backgroundImage:
              "radial-gradient(circle, #FFFFFF 1px, transparent 1px)",
            backgroundSize: "30px 30px",
          }}
        ></div>

        {/* Elemen visual blur */}
        <div className="absolute top-1/3 right-0 w-32 h-32 bg-accent/30 rounded-full blur-xl transform translate-x-1/2"></div>
        <div className="absolute bottom-1/3 left-1/4 w-40 h-40 bg-white/10 rounded-full blur-xl"></div>

        {/* Konten panel kiri */}

        <div className="relative z-10 flex flex-col items-center justify-center h-full w-full text-white ">
          <h2 className="text-3xl md:text-5xl font-bold tracking-tight mb-4 dark:text-white">
            RetinoCare
          </h2>
          <p className="text-lg text-white/90 text-center">
            Deteksi dini retinopati diabetik menggunakan AI
          </p>
        </div>
      </div>

      {/* Right side - login form */}
      <div className="w-full md:w-1/2 flex items-center justify-center p-6">
        <div className="w-full max-w-md">
          {/* Mobile-only logo header */}
          <div className=" flex flex-col items-center justify-center mb-6">
            <div className="relative h-24 w-24 mx-auto mb-2">
              <div className="absolute inset-0 bg-gradient-to-br from-white/30 to-accent/30 rounded-full animate-pulse-ring"></div>
              <div className="absolute inset-[4px] bg-blue-700 flex items-center justify-center rounded-full">
                <span className="text-white font-bold text-4xl">R</span>
              </div>
            </div>
            <h1 className="md:hidden text-3xl font-bold text-center bg-gradient-to-r from-white to-blue-400 bg-clip-text text-transparent mb-2">
              RetinoCare
            </h1>
            <p className="md:hidden text-gray-600 dark:text-gray-400 text-center">
              Deteksi dini retinopati diabetik
            </p>
          </div>

          <AuthForm isLogin={true} />
          <div className="mt-6 text-center">
            <p className="text-gray-600 dark:text-gray-400">
              Belum memiliki akun?{" "}
              <Link
                href="/register"
                className="text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-500 font-medium transition-colors"
              >
                Daftar
              </Link>
            </p>
          </div>
          <div className="mt-1 text-center">
            <p className="text-gray-600 dark:text-gray-600">atau</p>
          </div>
          <div className="mt-1 text-center">
            <p className="text-gray-600 dark:text-gray-400">
              Ke halaman{" "}
              <Link
                href="/"
                className="text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-500 font-medium transition-colors"
              >
                Beranda
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
