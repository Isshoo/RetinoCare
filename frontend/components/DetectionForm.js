import { useState, useRef } from 'react';
import axios from 'axios';
import { getAccessToken } from '../lib/auth';
import { getApiUrl, ENDPOINTS } from '../lib/apiConfig';

export default function DetectionForm() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const fileInputRef = useRef(null);
  const [dragActive, setDragActive] = useState(false);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (!selectedFile) return;

    if (!selectedFile.type.startsWith('image/')) {
      setError('Format file harus berupa gambar (JPEG, PNG)');
      return;
    }

    setFile(selectedFile);
    setError(null);
    setResult(null);
    
    const objectUrl = URL.createObjectURL(selectedFile);
    setPreviewUrl(objectUrl);
    
    return () => URL.revokeObjectURL(objectUrl);
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (!droppedFile.type.startsWith('image/')) {
        setError('Format file harus berupa gambar (JPEG, PNG)');
        return;
      }
      
      setFile(droppedFile);
      setError(null);
      setResult(null);
      const objectUrl = URL.createObjectURL(droppedFile);
      setPreviewUrl(objectUrl);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    if (!file) {
      setError('Silakan pilih gambar terlebih dahulu');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const accessToken = getAccessToken();
      
      if (!accessToken) {
        setError('Anda harus login untuk mengunggah gambar');
        setLoading(false);
        return;
      }
      
      const response = await axios.post(getApiUrl(ENDPOINTS.UPLOAD), formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${accessToken}`
        }
      });
      
      setResult(response.data.result);
    } catch (err) {
      console.error('Upload error:', err);
      
      if (err.response) {
        const errorMessage = err.response.data?.error || 
          `Error server: ${err.response.status}`;
        setError(errorMessage);
      } else if (err.request) {
        setError('Server tidak merespon. Silakan coba lagi nanti.');
      } else {
        setError(`Gagal mengunggah: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };
  
  const getClassColor = (diagnosisClass) => {
    switch (diagnosisClass.toLowerCase()) {
      case 'normal': return {
        text: 'text-green-600',
        bg: 'bg-green-100 dark:bg-green-900/30',
        border: 'border-green-200 dark:border-green-800'
      };
      case 'mild': return {
        text: 'text-yellow-600 dark:text-yellow-500',
        bg: 'bg-yellow-50 dark:bg-yellow-900/30',
        border: 'border-yellow-200 dark:border-yellow-800'
      };
      case 'moderate': return {
        text: 'text-orange-600',
        bg: 'bg-orange-50 dark:bg-orange-900/30',
        border: 'border-orange-200 dark:border-orange-800'
      };
      case 'severe': return {
        text: 'text-red-600',
        bg: 'bg-red-50 dark:bg-red-900/30',
        border: 'border-red-200 dark:border-red-800'
      };
      case 'proliferative': return {
        text: 'text-red-700',
        bg: 'bg-red-100 dark:bg-red-900/40',
        border: 'border-red-300 dark:border-red-800'
      };
      default: return {
        text: 'text-gray-700 dark:text-gray-300',
        bg: 'bg-gray-50 dark:bg-gray-800/50',
        border: 'border-gray-200 dark:border-gray-700'
      };
    }
  };
  
  const renderResults = () => {
    if (!result) return null;
    
    const diagnosisClass = result.class;
    const confidencePercent = (result.confidence * 100).toFixed(1);
    const colors = getClassColor(diagnosisClass);
    
    return (
      <div className="backdrop-blur-sm bg-white/90 dark:bg-gray-800/90 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 mt-8 overflow-hidden transition-all duration-300 ease-in-out">
        <div className={`py-3 px-4 ${colors.bg} ${colors.border} border-b flex items-center`}>
          <div className="flex-grow">
            <h2 className="text-xl font-bold">Hasil Diagnosis</h2>
            <p className="text-sm text-gray-600 dark:text-gray-400">Deteksi Retinopati Diabetik</p>
          </div>
          <div className={`${colors.text} font-semibold px-3 py-1 rounded-full bg-white/80 dark:bg-black/20 text-sm`}>
            {confidencePercent}% akurat
          </div>
        </div>
        
        <div className="p-6 flex flex-col md:flex-row gap-8">
          <div className="flex-1 space-y-6">
            <div>
              <p className="text-sm uppercase tracking-wider text-gray-500 dark:text-gray-400 font-medium mb-1">Klasifikasi</p>
              <div className={`rounded-lg ${colors.bg} ${colors.border} border p-4 flex items-center`}>
                <div className={`w-3 h-3 rounded-full mr-3 ${colors.text.replace('text', 'bg')}`}></div>
                <h3 className={`text-2xl font-bold ${colors.text}`}>{diagnosisClass}</h3>
              </div>
            </div>
            
            <div className="space-y-2">
              <p className="text-sm uppercase tracking-wider text-gray-500 dark:text-gray-400 font-medium">Tingkat Kepercayaan</p>
              <div className="relative pt-1">
                <div className="flex items-center justify-between mb-2">
                  <div className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300">
                    Akurasi
                  </div>
                  <div className={`text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full ${colors.bg} ${colors.text}`}>
                    {confidencePercent}%
                  </div>
                </div>
                <div className="relative h-2 w-full rounded-full overflow-hidden bg-gray-200 dark:bg-gray-700">
                  <div
                    className="transition-all duration-500 ease-out h-full rounded-full bg-gradient-to-r from-blue-500 to-blue-600 dark:from-blue-600 dark:to-blue-500 shadow-inner"
                    style={{ width: `${confidencePercent}%` }}
                  ></div>
                </div>
              </div>
            </div>
            
            <div className="space-y-2">
              <p className="text-sm uppercase tracking-wider text-gray-500 dark:text-gray-400 font-medium mb-1">Informasi Tambahan</p>
              <p className="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">
                Hasil analisis menunjukkan tingkat retinopati <strong className={colors.text}>{diagnosisClass}</strong>. 
                Disarankan untuk berkonsultasi dengan dokter spesialis mata untuk tindak lanjut.
              </p>
            </div>
          </div>
          
          {previewUrl && (
            <div className="md:w-2/5 flex flex-col">
              <p className="text-sm uppercase tracking-wider text-gray-500 dark:text-gray-400 font-medium mb-2">Gambar Diunggah</p>
              <div className="rounded-lg overflow-hidden border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50 shadow-inner h-full">
                <img 
                  src={previewUrl} 
                  alt="Gambar retina" 
                  className="w-full h-full object-contain"
                />
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="backdrop-blur-sm bg-white/90 dark:bg-gray-800/90 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 overflow-hidden">
        <div className="border-b border-gray-100 dark:border-gray-700 py-4 px-6 bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-100">Unggah Gambar Retina</h3>
          <p className="text-sm text-gray-600 dark:text-gray-400">Format JPG atau PNG untuk hasil terbaik</p>
        </div>
        
        <div className="p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div 
              className={`border-2 ${dragActive ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' : 'border-dashed border-gray-300 dark:border-gray-600'} rounded-xl transition-all duration-200 ease-in-out`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <div className="p-8 text-center">
                {previewUrl ? (
                  <div className="mb-3">
                    <div className="relative mx-auto max-w-xs overflow-hidden rounded-lg shadow-sm">
                      <img 
                        src={previewUrl} 
                        alt="Preview" 
                        className="w-full h-auto max-h-60"
                      />
                      <button 
                        type="button"
                        onClick={() => {
                          setFile(null);
                          setPreviewUrl(null);
                          setResult(null);
                        }}
                        className="absolute top-2 right-2 bg-black/50 hover:bg-black/70 text-white rounded-full p-1 transition-colors"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>
                    <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">{file?.name}</p>
                  </div>
                ) : (
                  <>
                    <div className="mx-auto flex flex-col items-center">
                      <div className="mb-3 rounded-full bg-blue-50 dark:bg-blue-900/30 p-3">
                        <svg 
                          className="mx-auto h-10 w-10 text-blue-500" 
                          fill="none" 
                          viewBox="0 0 24 24" 
                          stroke="currentColor"
                        >
                          <path 
                            strokeLinecap="round" 
                            strokeLinejoin="round" 
                            strokeWidth={1.5} 
                            d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                          />
                        </svg>
                      </div>
                      <p className="text-gray-700 dark:text-gray-300 font-medium">
                        Tarik & letakkan file di sini
                      </p>
                      <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                        atau klik untuk mencari
                      </p>
                      <p className="mt-2 text-xs text-gray-500 dark:text-gray-500">
                        Ukuran maksimal: 10MB
                      </p>
                    </div>
                  </>
                )}
                
                <input 
                  ref={fileInputRef}
                  type="file"
                  id="image-upload"
                  accept="image/jpeg,image/png,image/jpg"
                  onChange={handleFileChange}
                  className="hidden"
                />
                
                <div className="mt-4">
                  <button
                    type="button"
                    onClick={() => fileInputRef.current?.click()}
                    className="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200 dark:text-blue-100 dark:bg-blue-900/50 dark:hover:bg-blue-900/70 transition-colors duration-150 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    {previewUrl ? 'Ganti Gambar' : 'Pilih Gambar'}
                  </button>
                </div>
              </div>
            </div>
            
            {error && (
              <div className="animate-fade-in flex items-center p-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-3 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <span>{error}</span>
              </div>
            )}
            
            <button 
              type="submit"
              disabled={!file || loading}
              className={`w-full relative overflow-hidden ${
                !file || loading 
                  ? 'bg-gray-400 dark:bg-gray-700 cursor-not-allowed' 
                  : 'bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 dark:from-blue-600 dark:to-blue-700'
              } text-white font-medium py-3 px-4 rounded-lg shadow transition-all duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`}
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  <span>Memproses...</span>
                </span>
              ) : (
                <>
                  <span className="relative z-10 flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    Unggah & Analisis
                  </span>
                </>
              )}
            </button>
          </form>
        </div>
      </div>
      
      {/* Display results */}
      {renderResults()}
    </div>
  );
}