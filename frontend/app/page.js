'use client';
import Link from "next/link";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import Image from "next/image";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";


// Counter component
const CounterAnimation = ({ target, className = "" }) => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const targetNum = parseInt(target);
    const duration = 2000;
    const step = targetNum / (duration / 50);
    let current = 0;
    
    const timer = setInterval(() => {
      current += step;
      if (current >= targetNum) {
        setCount(targetNum);
        clearInterval(timer);
      } else {
        setCount(Math.floor(current));
      }
    }, 50);
    
    return () => clearInterval(timer);
  }, [target]);

  return (
    <span className={`block text-3xl font-bold text-orange-400 ${className}`}>
      {count}
    </span>
  );
};

// Scanner component
const ScanningOverlay = () => {
  const [isScanning, setIsScanning] = useState(false);

  useEffect(() => {
    const scanInterval = setInterval(() => {
      setIsScanning(true);
      setTimeout(() => {
        setIsScanning(false);
      }, 2000);
    }, 4000);
    
    return () => clearInterval(scanInterval);
  }, []);

  return (
    <div className={`absolute inset-0 bg-gradient-to-b from-transparent via-blue-500/10 to-transparent transition-opacity duration-500 ${isScanning ? 'opacity-100 scanning' : 'opacity-0'}`}></div>
  );
};

export default function Home() {
  // Add a state to track current gradient
  const [gradientClass, setGradientClass] = useState('from-blue-900 via-blue-800 to-blue-900');
  const [particles, setParticles] = useState([]);
  
  // Initialize animations on page load
  useEffect(() => {
    // Initialize AOS (Animate On Scroll)
    import('aos').then(({ default: AOS }) => {
      AOS.init({
        duration: 1000,
        easing: 'ease-out-cubic',
        once: false
      });
    });

    // Generate particles
    const newParticles = Array(20).fill().map((_, i) => ({
      id: i,
      top: Math.random() * 100,
      left: Math.random() * 100,
      width: Math.random() * 10 + 5,
      height: Math.random() * 10 + 5,
      opacity: Math.random() * 0.5 + 0.1,
      color: i % 2 === 0 ? '#60A5FA' : '#FB923C',
      animationDuration: Math.random() * 10 + 10,
      animationDelay: Math.random() * 5
    }));
    setParticles(newParticles);
    
    // Gradient animation using React state
    const colors = [
      'from-blue-900 via-blue-800 to-blue-900',
      'from-blue-800 via-blue-700 to-blue-900',
      'from-blue-900 via-blue-700 to-blue-800'
    ];
    
    let currentIndex = 0;
    const gradientInterval = setInterval(() => {
      currentIndex = (currentIndex + 1) % colors.length;
      setGradientClass(colors[currentIndex]);
    }, 5000);
    
    // Cleanup interval on component unmount
    return () => clearInterval(gradientInterval);
  }, []);

  // Variants for staggered animations
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2
      }
    }
  };
  
  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: { type: "spring", stiffness: 100 }
    }
  };

  return (
    <div className={`min-h-screen bg-gradient-to-b ${gradientClass} text-white overflow-hidden relative transition-colors duration-3000`}>
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

      {/* Hero Section with Animated Elements */}
      <section className="relative pt-20 pb-32 px-6 md:px-12 lg:px-24 max-w-7xl mx-auto">
        <motion.div 
          className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center"
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          {/* Left Content with Text Animations */}
          <div className="relative z-10">
            <motion.div 
              className="mb-6 inline-block"
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3, duration: 0.6 }}
            >
              <span className="text-xs font-medium tracking-wider py-1 px-3 rounded-full bg-orange-500/20 text-orange-400 border border-orange-500/30 animate-pulse-slow">
                RetinoCare AI Platform
              </span>
            </motion.div>
            
            <div className="overflow-hidden">
              <motion.h1 
                className="text-5xl md:text-6xl font-bold mb-6 leading-tight"
                initial={{ y: 100, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.4, duration: 0.8, ease: "easeOut" }}
              >
                Deteksi <span className="text-orange-400 glow-text">Retinopati</span> Diabetik Dengan Tepat
              </motion.h1>
            </div>
            
            <motion.p 
              className="text-lg text-blue-100 mb-8 max-w-lg"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6, duration: 0.8 }}
            >
              Solusi inovatif untuk diagnosis dini dengan teknologi kecerdasan buatan canggih yang menganalisis gambar retina secara otomatis dan akurat.
            </motion.p>
            
            <motion.div 
              className="flex flex-wrap gap-4"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8, duration: 0.6 }}
            >
              <Link 
                href="/login" 
                className="relative group px-8 py-4 bg-orange-500 hover:bg-orange-600 text-white font-medium rounded-lg transition-all duration-300 overflow-hidden"
              >
                <span className="relative z-10 flex items-center">
                  Mulai Deteksi
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 ml-2 group-hover:translate-x-1 transition-transform" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                </span>
                <div className="absolute inset-0 w-0 bg-gradient-to-r from-orange-600 to-orange-500 transition-all duration-300 group-hover:w-full"></div>
                <div className="absolute inset-0 w-full scale-x-0 h-full -translate-x-full bg-gradient-to-r from-orange-400/20 to-transparent transform-gpu group-hover:translate-x-0 group-hover:scale-x-100 transition-all duration-700 ease-out"></div>
              </Link>
              
              <button className="relative px-8 py-4 border border-blue-400 hover:border-blue-300 text-blue-100 hover:text-white rounded-lg transition-all duration-300 overflow-hidden group">
                Pelajari Lebih Lanjut
                <span className="absolute inset-0 w-0 bg-blue-700/30 transition-all duration-500 ease-out group-hover:w-full"></span>
              </button>
            </motion.div>
            
            {/* Statistics with Counter Animation */}
            <motion.div 
              className="grid grid-cols-3 gap-4 mt-12"
              variants={containerVariants}
              initial="hidden"
              animate="visible"
            >
              <motion.div 
                className="text-center backdrop-blur-sm bg-blue-900/30 rounded-xl p-4 border border-blue-800/50 hover:border-blue-600/50 transition-all hover:scale-105 hover:shadow-glow"
                variants={itemVariants}
              >
                 <CounterAnimation target="99" />
                <span className="text-sm text-blue-200">Tingkat Akurasi</span>
              </motion.div>
              <motion.div 
                className="text-center backdrop-blur-sm bg-blue-900/30 rounded-xl p-4 border border-blue-800/50 hover:border-blue-600/50 transition-all hover:scale-105 hover:shadow-glow"
                variants={itemVariants}
              >
                 <CounterAnimation target="10" />
                <span className="text-sm text-blue-200">Ribu Pasien Terbantu</span>
              </motion.div>
              <motion.div 
                className="text-center backdrop-blur-sm bg-blue-900/30 rounded-xl p-4 border border-blue-800/50 hover:border-blue-600/50 transition-all hover:scale-105 hover:shadow-glow"
                variants={itemVariants}
              >
                 <CounterAnimation target="5" />
                <span className="text-sm text-blue-200">Menit Pemrosesan</span>
              </motion.div>
            </motion.div>
          </div>

          {/* Right Content - Interactive Dashboard Preview with Animations */}
          <motion.div 
            className="relative z-10 lg:ml-10"
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6, duration: 0.8 }}
          >
            <div className="relative backdrop-blur-md bg-blue-800/20 p-6 rounded-2xl border border-blue-700/50 shadow-xl hover:shadow-2xl hover:border-blue-500/50 transition-all duration-500">
              <div className="absolute -top-3 -left-3 flex space-x-1">
                <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              </div>
              
              <div className="rounded-lg overflow-hidden bg-gray-900 aspect-video relative">
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-blue-500/20 flex items-center justify-center animate-pulse-ring">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                        <path fillRule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <p className="text-sm text-blue-200">Mulai Pemindaian Retina</p>
                    
                    {/* Scan visualization animation */}
                    <div className="scan-line"></div>
                  </div>
                </div>
                
                {/* Scanner visual effect */}
                <ScanningOverlay />
              </div>
              
              <div className="mt-4">
                <div className="space-y-2">
                  <div className="h-2 bg-blue-700/40 rounded w-5/6 loading-bar"></div>
                  <div className="h-2 bg-blue-700/40 rounded w-3/6 loading-bar loading-delay-1"></div>
                  <div className="h-2 bg-blue-700/40 rounded w-4/6 loading-bar loading-delay-2"></div>
                </div>
              </div>
            </div>
          </motion.div>
        </motion.div>
      </section>

      {/* Features Section with Scroll Animations */}
      <section className="relative py-20 px-6 md:px-12 lg:px-24 max-w-7xl mx-auto" data-aos="fade-up">
        <div className="text-center mb-16 relative z-10">
          <h2 className="text-4xl font-bold mb-4 typing-animation">Fitur Unggulan</h2>
          <p className="max-w-2xl mx-auto text-blue-200" data-aos="fade-up" data-aos-delay="200">
            RetinoCare menawarkan solusi lengkap untuk deteksi dini retinopati diabetik dengan teknologi mutakhir.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {/* Feature 1 - with advanced hover and appears on scroll */}
          <motion.div 
            className="group relative backdrop-blur-sm bg-blue-800/10 border border-blue-700/30 p-8 rounded-2xl hover:bg-blue-700/20 transition-all duration-500 feature-card overflow-hidden"
            data-aos="fade-up"
            data-aos-delay="100"
            whileHover={{ y: -10 }}
          >
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-400 to-transparent scale-x-0 group-hover:scale-x-100 transition-transform duration-700 origin-left"></div>
            <div className="bg-blue-600/20 rounded-full p-3 inline-flex mb-6 group-hover:bg-blue-600/30 transition-all group-hover:rotate-[30deg] duration-500">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-blue-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold mb-3 text-white group-hover:text-blue-300 transition-colors">Deteksi Otomatis</h3>
            <p className="text-blue-200 mb-4 relative z-10">
              Sistem AI canggih yang mendeteksi tanda-tanda retinopati diabetik secara otomatis dari gambar retina.
            </p>
            <div className="absolute bottom-8 right-8 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-400 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </div>
            <div className="absolute inset-0 bg-gradient-to-br from-blue-600/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          </motion.div>

          {/* Feature 2 */}
          <motion.div 
            className="group relative backdrop-blur-sm bg-blue-800/10 border border-blue-700/30 p-8 rounded-2xl hover:bg-blue-700/20 transition-all duration-500 feature-card overflow-hidden"
            data-aos="fade-up"
            data-aos-delay="200"
            whileHover={{ y: -10 }}
          >
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-orange-400 to-transparent scale-x-0 group-hover:scale-x-100 transition-transform duration-700 origin-left"></div>
            <div className="bg-orange-500/20 rounded-full p-3 inline-flex mb-6 group-hover:bg-orange-500/30 transition-all group-hover:rotate-[30deg] duration-500">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-orange-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold mb-3 text-white group-hover:text-orange-300 transition-colors">Hasil Akurat</h3>
            <p className="text-blue-200 mb-4 relative z-10">
              Tingkat akurasi hingga 99% berkat model AI yang dilatih dengan dataset medis terbaik.
            </p>
            <div className="absolute bottom-8 right-8 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-orange-400 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </div>
            <div className="absolute inset-0 bg-gradient-to-br from-orange-600/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          </motion.div>

          {/* Feature 3 */}
          <motion.div 
            className="group relative backdrop-blur-sm bg-blue-800/10 border border-blue-700/30 p-8 rounded-2xl hover:bg-blue-700/20 transition-all duration-500 feature-card overflow-hidden"
            data-aos="fade-up"
            data-aos-delay="300"
            whileHover={{ y: -10 }}
          >
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-400 to-transparent scale-x-0 group-hover:scale-x-100 transition-transform duration-700 origin-left"></div>
            <div className="bg-blue-600/20 rounded-full p-3 inline-flex mb-6 group-hover:bg-blue-600/30 transition-all group-hover:rotate-[30deg] duration-500">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-blue-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold mb-3 text-white group-hover:text-blue-300 transition-colors">Laporan Terpandu</h3>
            <p className="text-blue-200 mb-4 relative z-10">
              Dapatkan laporan hasil analisis yang komprehensif dan mudah dipahami oleh dokter maupun pasien.
            </p>
            <div className="absolute bottom-8 right-8 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-400 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </div>
            <div className="absolute inset-0 bg-gradient-to-br from-blue-600/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
          </motion.div>
        </div>
      </section>

      {/* CTA Section with Animated Background */}
      <section className="relative py-20 px-6" data-aos="zoom-in">
        <div className="absolute inset-0 overflow-hidden z-0">
          <div className="cta-bg-animation absolute inset-0"></div>
        </div>
        <div className="max-w-5xl mx-auto backdrop-blur-md bg-gradient-to-r from-blue-800/40 to-blue-700/40 p-10 md:p-16 rounded-3xl border border-blue-600/30 shadow-lg hover:shadow-blue-600/20 transition-all duration-500 relative z-10">
          <div className="flex flex-col md:flex-row items-center justify-between gap-8">
            <div className="flex-1" data-aos="fade-right">
              <h2 className="text-3xl font-bold mb-4">Siap Untuk Memulai?</h2>
              <p className="text-blue-100 mb-8">
                Bergabunglah sekarang dan manfaatkan teknologi AI untuk mendeteksi retinopati diabetik lebih awal.
              </p>
              <div className="flex flex-wrap gap-4">
                <Link href="/register" className="bg-orange-500 hover:bg-orange-600 text-white px-8 py-4 rounded-lg transition-all duration-300 relative overflow-hidden group">
                  <span className="relative z-10">Daftar Sekarang</span>
                  <span className="absolute inset-0 bg-gradient-to-r from-orange-600 to-orange-500 scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"></span>
                </Link>
                <Link href="/login" className="bg-blue-700 hover:bg-blue-600 text-white px-8 py-4 rounded-lg transition-all duration-300 relative overflow-hidden group">
                  <span className="relative z-10">Masuk</span>
                  <span className="absolute inset-0 bg-gradient-to-r from-blue-800 to-blue-600 scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"></span>
                </Link>
              </div>
            </div>
            <div className="flex-1 md:flex md:justify-end" data-aos="fade-left">
              <div className="relative w-full max-w-[220px] aspect-square">
                <div className="absolute inset-0 rounded-full bg-gradient-to-tr from-orange-500 to-blue-500 animate-pulse-ring"></div>
                <div className="absolute inset-2 rounded-full bg-blue-900 flex items-center justify-center text-center">
                  <div>
                  <CounterAnimation target="24" />
                    <p className="text-sm text-blue-200">Jam Dukungan Layanan</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <Footer />

     
    </div>
  );
}