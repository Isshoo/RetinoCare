import AuthForm from '../../components/AuthForm';

export default function LoginPage() {
  return (
    <div className="relative min-h-screen w-full overflow-hidden flex">
      {/* Left side - decorative panel (visible on md and up) */}
      <div className="hidden md:block md:w-1/2 bg-gradient-to-br from-blue-600 to-blue-800 relative">
        {/* Pola titik dekoratif */}
        <div className="absolute inset-0 opacity-20"
             style={{ 
               backgroundImage: 'radial-gradient(circle, #FFFFFF 1px, transparent 1px)', 
               backgroundSize: '30px 30px' 
             }}>
        </div>
        
        {/* Elemen visual blur */}
        <div className="absolute top-1/3 right-0 w-32 h-32 bg-accent/30 rounded-full blur-xl transform translate-x-1/2"></div>
        <div className="absolute bottom-1/3 left-1/4 w-40 h-40 bg-white/10 rounded-full blur-xl"></div>
        
        {/* Konten panel kiri */}
        <div className="relative h-full flex flex-col items-center justify-center p-12 text-center">
          <div className="mb-8">
            <div className="relative h-24 w-24 mx-auto">
              <div className="absolute inset-0 bg-gradient-to-br from-white/30 to-accent/30 rounded-full animate-pulse-ring"></div>
              <div className="absolute inset-[4px] bg-blue-700 flex items-center justify-center rounded-full">
                <span className="text-white font-bold text-4xl">R</span>
              </div>
            </div>
          </div>
          
          <h1 className="text-4xl font-bold text-white mb-6">RetinoCare</h1>
          <p className="text-white/90 text-lg mb-8">Deteksi dini retinopati diabetik menggunakan teknologi AI</p>
          
          <div className="w-20 h-1 bg-accent/70 rounded-full mb-8"></div>
          
          <p className="text-white/70">Masuk untuk melanjutkan perjalanan kesehatan mata Anda</p>
        </div>
      </div>
      
      {/* Right side - login form */}
      <div className="w-full md:w-1/2 flex items-center justify-center p-6">
        <div className="w-full max-w-md">
          {/* Mobile-only logo header */}
          <div className="md:hidden flex flex-col items-center justify-center mb-8">
            <div className="relative h-16 w-16 mb-4">
              <div className="absolute inset-0 bg-gradient-to-br from-blue-600 to-accent rounded-full animate-pulse-ring"></div>
              <div className="absolute inset-[3px] bg-white dark:bg-gray-800 flex items-center justify-center rounded-full">
                <span className="text-blue-600 font-bold text-2xl">R</span>
              </div>
            </div>
            <h1 className="text-3xl font-bold text-center bg-gradient-to-r from-blue-600 to-accent bg-clip-text text-transparent mb-2">
              RetinoCare
            </h1>
            <p className="text-gray-600 dark:text-gray-400 text-center">Deteksi dini retinopati diabetik</p>
          </div>
          
          <AuthForm isLogin={true} />
        </div>
      </div>
    </div>
  );
}