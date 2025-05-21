import AuthForm from '../../components/AuthForm';
import Link from 'next/link';

export default function RegisterPage() {
  return (
    <div className="min-h-screen flex flex-col md:flex-row overflow-hidden">
      {/* Left side decorative panel - visible only on medium screens and up */}
      <div className="hidden md:flex md:w-1/3 bg-gradient-to-br from-blue-600 to-blue-800 relative overflow-hidden">
        <div className="absolute inset-0">
          <div className="absolute top-1/3 left-1/4 w-40 h-40 bg-white/10 rounded-full blur-xl"></div>
          <div className="absolute bottom-1/3 right-1/4 w-64 h-64 bg-white/10 rounded-full blur-xl"></div>
        </div>
        <div className="relative z-10 flex flex-col items-center justify-center h-full text-white p-12">
          <h2 className="text-3xl md:text-5xl font-bold tracking-tight mb-4">RetinoCare</h2>
          <p className="text-lg text-white/90 text-center">Deteksi dini retinopati diabetik menggunakan AI</p>
        </div>
      </div>
      
      {/* Right side form */}
      <div className="flex-1 flex flex-col items-center justify-center p-6 md:p-12 relative">
        {/* Decorative blurred circles */}
        <div className="absolute top-20 right-10 w-40 h-40 bg-blue-500/5 rounded-full blur-xl"></div>
        <div className="absolute bottom-40 left-10 w-64 h-64 bg-orange-600/5 rounded-full blur-xl"></div>
        
        {/* Card container with glass effect */}
        <div className="bg-white/80 dark:bg-gray-800/50 backdrop-blur-sm border border-gray-200 dark:border-white/10 p-8 rounded-2xl shadow-lg w-full max-w-md relative z-10">
          <div className="text-center mb-6">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-r from-blue-600 to-blue-700 shadow-md mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" className="w-8 h-8 text-white">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </div>
            <h1 className="text-3xl font-bold text-blue-700 dark:text-blue-400">Daftar Akun</h1>
          </div>

          {/* Auth form */}
          <AuthForm isLogin={false} />
          
          {/* Footer link */}
          <div className="mt-6 text-center">
            <p className="text-gray-600 dark:text-gray-400">
              Sudah memiliki akun?{' '}
              <Link href="/login" className="text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-500 font-medium transition-colors">
                Masuk
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}