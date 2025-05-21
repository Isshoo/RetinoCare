"use client";

import Link from "next/link";
import Image from "next/image";
import { useState } from "react";

export default function Footer() {
  const [hoverState, setHoverState] = useState({
    beranda: false,
    tentang: false,
    layanan: false,
    kontak: false,
  });

  const currentYear = new Date().getFullYear();

  return (
    <footer className="relative mt-auto pt-10 overflow-hidden">
      {/* Glass effect divider */}
      <div className="absolute top-0 left-0 right-0 h-[2px] bg-gradient-to-r from-blue-500/5 via-blue-600/30 to-blue-500/5"></div>
      
      <div className="container mx-auto px-6 pb-8">
        <div className="flex flex-wrap md:flex-row justify-between">
          {/* Logo and description */}
          <div className="w-full md:w-1/3 mb-6 md:mt-0">
            <div className="flex items-center mb-4">
              <div className="relative h-10 w-10 mr-3">
                <div className="absolute inset-0 bg-gradient-to-br from-blue-600 to-accent rounded-lg animate-pulse-ring"></div>
                <div className="absolute inset-[3px] bg-background flex items-center justify-center rounded-lg">
                  <span className="text-blue-600 font-bold text-xl">R</span>
                </div>
              </div>
              <h2 className="text-2xl font-bold text-blue-600">RetinoCare</h2>
            </div>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Deteksi dini retinopati diabetik menggunakan teknologi kecerdasan buatan untuk membantu pencegahan kebutaan.
            </p>
            
            {/* Social icons */}
            <div className="flex space-x-4">
              {['instagram', 'twitter', 'facebook', 'linkedin'].map((social) => (
                <Link 
                  href="#" 
                  key={social}
                  className="w-9 h-9 rounded-full bg-white/10 hover:bg-white/20 transition-all flex items-center justify-center border border-white/20 group"
                  aria-label={`Kunjungi ${social} kami`}
                >
                  <div className="w-5 h-5 text-gray-400 group-hover:text-white">
                    {socialIcon(social)}
                  </div>
                </Link>
              ))}
            </div>
          </div>
          
          {/* Links section */}
          <div className="w-full md:flex md:flex-1 md:justify-center space-y-6 md:space-y-0">
            <div className="w-full md:w-1/3 mb-4">
              <h3 className="font-bold text-lg mb-4 text-foreground">Tautan</h3>
              <ul className="space-y-2">
                {[
                  { name: 'Beranda', href: '/' },
                  { name: 'Tentang Kami', href: '/tentang' },
                  { name: 'Layanan', href: '/layanan' },
                  { name: 'Kontak', href: '/kontak' },
                ].map((link) => (
                  <li key={link.name}>
                    <Link 
                      href={link.href}
                      className="group flex items-center"
                      onMouseEnter={() => setHoverState({...hoverState, [link.name.toLowerCase()]: true})}
                      onMouseLeave={() => setHoverState({...hoverState, [link.name.toLowerCase()]: false})}
                    >
                      <span className="w-1 h-0.5 bg-accent mr-3 origin-left transition-all scale-x-0 group-hover:scale-x-100"></span>
                      <span className="text-gray-600 dark:text-gray-400 group-hover:text-blue-600 dark:group-hover:text-blue-500 transition-colors">
                        {link.name}
                      </span>
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="w-full md:w-1/3">
              <h3 className="font-bold text-lg mb-4 text-foreground">Informasi</h3>
              <address className="not-italic">
                <p className="mb-2 text-gray-600 dark:text-gray-400">
                  Sulawesi Utara<br />
                  Manado
                </p>
                <p className="flex items-center text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-500 transition-colors">
                  <span className="mr-3">📧</span>
                  <a href="mailto:info@retinocare.id">info@retinocare.id</a>
                </p>
                <p className="flex items-center text-gray-600 dark:text-gray-400 mt-1.5">
                  <span className="mr-3">📞</span>
                  <a href="tel:+6221123456" className="hover:text-blue-600 dark:hover:text-blue-500 transition-colors">
                    +62 21 123 456
                  </a>
                </p>
              </address>
            </div>
          </div>
        </div>
        
        {/* Copyright bar with subtle glass effect */}
        <div className="mt-8 pt-4 border-t border-gray-300 dark:border-white/10">
          <div className="flex flex-col md:flex-row md:items-center justify-between text-sm text-gray-600 dark:text-gray-400">
            <div>
              © {currentYear} RetinoCare. Hak Cipta Dilindungi.
            </div>
            <div className="flex space-x-6 mt-2 md:mt-0">
              <Link href="/privasi" className="hover:text-blue-600 dark:hover:text-blue-500 transition-colors">
                Kebijakan Privasi
              </Link>
              <Link href="/syarat" className="hover:text-blue-600 dark:hover:text-blue-500 transition-colors">
                Syarat Penggunaan
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}

// Social media icons
function socialIcon(platform) {
  switch (platform) {
    case 'instagram':
      return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 3c-2.444 0-2.75.01-3.71.054-.959.044-1.613.196-2.185.419A4.412 4.412 0 0 0 4.51 4.51c-.5.5-.809 1.002-1.039 1.594-.222.572-.374 1.226-.418 2.184C3.01 9.25 3 9.556 3 12s.01 2.75.054 3.71c.044.959.196 1.613.418 2.185.23.592.538 1.094 1.039 1.595.5.5 1.002.808 1.594 1.038.572.222 1.226.374 2.184.418C9.25 20.99 9.556 21 12 21s2.75-.01 3.71-.054c.959-.044 1.613-.196 2.185-.419a4.412 4.412 0 0 0 1.595-1.038c.5-.5.808-1.002 1.038-1.594.222-.572.374-1.226.418-2.184.044-.96.054-1.267.054-3.711s-.01-2.75-.054-3.71c-.044-.959-.196-1.613-.419-2.185A4.412 4.412 0 0 0 19.49 4.51c-.5-.5-1.002-.809-1.594-1.039-.572-.222-1.226-.374-2.184-.418C14.75 3.01 14.444 3 12 3Zm0 1.622c2.403 0 2.688.009 3.637.052.877.04 1.354.187 1.67.31.42.163.72.358 1.036.673.315.315.51.615.673 1.035.123.317.27.794.31 1.671.043.95.052 1.234.052 3.637s-.009 2.688-.052 3.637c-.04.877-.187 1.354-.31 1.67-.163.42-.358.72-.673 1.036a2.79 2.79 0 0 1-1.035.673c-.317.123-.794.27-1.671.31-.95.043-1.234.052-3.637.052s-2.688-.009-3.637-.052c-.877-.04-1.354-.187-1.67-.31a2.789 2.789 0 0 1-1.036-.673 2.79 2.79 0 0 1-.673-1.035c-.123-.317-.27-.794-.31-1.671-.043-.95-.052-1.234-.052-3.637s.009-2.688.052-3.637c.04-.877.187-1.354.31-1.67.163-.42.358-.72.673-1.036.315-.315.615-.51 1.035-.673.317-.123.794-.27 1.671-.31.95-.043 1.234-.052 3.637-.052Z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 15a3 3 0 1 1 0-6 3 3 0 0 1 0 6Zm0-7.622a4.622 4.622 0 1 0 0 9.244 4.622 4.622 0 0 0 0-9.244Zm5.884-.182a1.08 1.08 0 1 1-2.16 0 1.08 1.08 0 0 1 2.16 0Z" />
        </svg>
      );
    case 'twitter':
      return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M22 4s-1.325 1.572-2.121 1.855c-1.172-1.26-2.924-1.635-4.481-0.929-1.557 0.707-2.56 2.299-2.423 4.071-2.49-0.12-4.832-1.294-6.444-3.262-0.82 1.423-0.403 3.248 0.961 4.166-0.506-0.016-0.992-0.153-1.433-0.399 0 0.016 0 0.033 0 0.048C6.059 11.14 7.267 12.537 8.889 12.885c-0.465 0.127-0.959 0.147-1.434 0.055 0.567 1.59 2.093 2.676 3.833 2.708-1.41 1.107-3.157 1.703-4.949 1.701-0.317 0-0.634-0.018-0.95-0.055 1.825 1.171 3.953 1.792 6.13 1.79C16.99 19.084 20.028 15.065 20.028 10.062c0-0.137-0.004-0.273-0.01-0.409 0.73-0.527 1.364-1.184 1.866-1.934C21.333 8.059 20.761 8.256 20.167 8.339c0.675-0.405 1.194-1.045 1.438-1.806C20.989 6.831 20.301 7.115 19.571 7.261 18.961 6.637 18.114 6.27 17.221 6.273C15.514 6.276 14.075 7.334 13.6 9" />
        </svg>
      );
    case 'facebook':
      return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z" />
        </svg>
      );
    case 'linkedin':
      return (
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M16 8a6 6 0 016 6v7h-4v-7a2 2 0 00-2-2 2 2 0 00-2 2v7h-4v-7a6 6 0 016-6zM2 9h4v12H2z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M2 9h4v12H2z" />
          <circle cx="4" cy="4" r="2" strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} />
        </svg>
      );
    default:
      return null;
  }
}