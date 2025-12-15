"use client";
import Link from "next/link";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";

export default function NotFound() {
  const [gradientClass, setGradientClass] = useState(
    "from-blue-900 via-blue-800 to-blue-900"
  );
  const [particles, setParticles] = useState([]);

  useEffect(() => {
    // Generate particles
    const newParticles = Array(15)
      .fill()
      .map((_, i) => ({
        id: i,
        top: Math.random() * 100,
        left: Math.random() * 100,
        width: Math.random() * 10 + 5,
        height: Math.random() * 10 + 5,
        opacity: Math.random() * 0.5 + 0.1,
        color: i % 2 === 0 ? "#60A5FA" : "#FB923C",
        animationDuration: Math.random() * 10 + 10,
        animationDelay: Math.random() * 5,
      }));
    setParticles(newParticles);

    // Gradient animation
    const colors = [
      "from-blue-900 via-blue-800 to-blue-900",
      "from-blue-800 via-blue-700 to-blue-900",
      "from-blue-900 via-blue-700 to-blue-800",
    ];

    let currentIndex = 0;
    const gradientInterval = setInterval(() => {
      currentIndex = (currentIndex + 1) % colors.length;
      setGradientClass(colors[currentIndex]);
    }, 5000);

    return () => clearInterval(gradientInterval);
  }, []);

  return (
    <div
      className={`min-h-screen bg-gradient-to-b ${gradientClass} text-white overflow-hidden relative transition-colors duration-3000 flex flex-col`}
    >
      {/* Animated particles background */}
      <div className="particles-container absolute inset-0 z-0">
        {particles.map((particle) => (
          <div
            key={particle.id}
            className="particle absolute rounded-full"
            style={{
              top: `${particle.top}%`,
              left: `${particle.left}%`,
              width: `${particle.width}px`,
              height: `${particle.height}px`,
              opacity: particle.opacity,
              backgroundColor: particle.color,
              animation: `float ${particle.animationDuration}s linear infinite`,
              animationDelay: `${particle.animationDelay}s`,
              transform: `translateY(0px)`,
            }}
          />
        ))}
      </div>

      {/* Animated decorative elements */}
      <div className="absolute top-40 left-10 w-64 h-64 bg-blue-500 rounded-full opacity-10 blur-3xl floating-slow"></div>
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-orange-500 rounded-full opacity-10 blur-3xl floating"></div>
      <div className="absolute -top-20 -right-20 w-64 h-64 bg-blue-400 rounded-full opacity-5 blur-xl floating-reverse"></div>

      <Navbar />

      {/* 404 Content Section */}
      <section className="relative flex-1 flex items-center justify-center py-20 px-6 md:px-12 lg:px-24 max-w-7xl mx-auto w-full">
        <div className="text-center relative z-10">
          {/* 404 Number with Animation */}
          <motion.div
            className="relative mb-4"
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ duration: 0.8, type: "spring", stiffness: 100 }}
          >
            <div className="relative inline-block">
              <h1 className="text-[150px]  font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-orange-400 to-blue-400 leading-none glow-text">
                404
              </h1>
              <div className="absolute inset-0 blur-3xl opacity-30 bg-gradient-to-r from-blue-500 to-orange-500"></div>
            </div>
          </motion.div>

          {/* Icon with Pulse Animation */}
          <motion.div
            className="mb-10 flex justify-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.6 }}
          >
            <div className="relative">
              <div className="absolute inset-0 bg-orange-500 rounded-full blur-xl opacity-30 animate-pulse-ring"></div>
              <div className="relative bg-blue-800/40 backdrop-blur-sm border border-blue-700/50 rounded-full p-6">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="size-12 text-orange-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
            </div>
          </motion.div>

          {/* Text Content */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.6 }}
          >
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Halaman Tidak Ditemukan
            </h2>
            <p className="text-lg text-blue-100 mb-8 max-w-md mx-auto">
              Maaf, halaman yang Anda cari tidak dapat ditemukan atau mungkin
              telah dipindahkan.
            </p>
          </motion.div>

          {/* Action Buttons */}
          <motion.div
            className="flex flex-wrap gap-4 justify-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7, duration: 0.6 }}
          >
            <Link
              href="/"
              className="relative group px-8 py-4 bg-orange-500 hover:bg-orange-600 text-white font-medium rounded-lg transition-all duration-300 overflow-hidden"
            >
              <span className="relative z-10 flex items-center">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-5 w-5 mr-2"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
                </svg>
                Kembali ke Beranda
              </span>
              <div className="absolute inset-0 w-0 bg-gradient-to-r from-orange-600 to-orange-500 transition-all duration-300 group-hover:w-full"></div>
            </Link>

            {/* <Link
              href="/detect"
              className="relative px-8 py-4 border border-blue-400 hover:border-blue-300 text-blue-100 hover:text-white rounded-lg transition-all duration-300 overflow-hidden group"
            >
              <span className="relative z-10">Mulai Deteksi</span>
              <span className="absolute inset-0 w-0 bg-blue-700/30 transition-all duration-500 ease-out group-hover:w-full"></span>
            </Link> */}
          </motion.div>

          {/* Helpful Links */}
          <motion.div
            className="mt-12 backdrop-blur-sm bg-blue-800/20 border border-blue-700/30 rounded-2xl p-6 max-w-2xl mx-auto"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.9, duration: 0.6 }}
          >
            <h3 className="text-lg font-semibold mb-4 text-blue-200">
              Mungkin Anda mencari:
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* <Link
                href="/"
                className="group p-4 rounded-lg bg-blue-700/20 hover:bg-blue-700/40 border border-blue-600/30 hover:border-blue-500/50 transition-all duration-300"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-6 w-6 text-blue-400 mb-2 mx-auto"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
                  />
                </svg>
                <p className="text-sm text-blue-200 group-hover:text-white transition-colors">
                  Beranda
                </p>
              </Link> */}

              <Link
                href="/detect"
                className="group p-4 rounded-lg bg-blue-700/20 hover:bg-blue-700/40 border border-blue-600/30 hover:border-blue-500/50 transition-all duration-300"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-6 w-6 text-orange-400 mb-2 mx-auto"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"
                  />
                </svg>
                <p className="text-sm text-blue-200 group-hover:text-white transition-colors">
                  Deteksi
                </p>
              </Link>

              <Link
                href="/register"
                className="group p-4 rounded-lg bg-blue-700/20 hover:bg-blue-700/40 border border-blue-600/30 hover:border-blue-500/50 transition-all duration-300"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-6 w-6 text-blue-400 mb-2 mx-auto"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"
                  />
                </svg>
                <p className="text-sm text-blue-200 group-hover:text-white transition-colors">
                  Daftar
                </p>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
