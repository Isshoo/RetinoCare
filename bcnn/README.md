# Bayesian CNN untuk Deteksi Retinopati Diabetik

Panduan lengkap untuk melatih model Bayesian Convolutional Neural Network untuk deteksi Retinopati Diabetik menggunakan dataset APTOS-2019.

## 📋 Daftar Isi

- [Persiapan](#persiapan)
- [Struktur Dataset](#struktur-dataset)
- [Instalasi Dependencies](#instalasi-dependencies)
- [Cara Menjalankan](#cara-menjalankan)
- [Hasil yang Dihasilkan](#hasil-yang-dihasilkan)
- [Troubleshooting](#troubleshooting)

## 🚀 Persiapan

### 1. Struktur Folder

Pastikan struktur folder Anda seperti ini:

```
project/
├── APTOS-2019/
│   ├── train_images/           # 2930 images
│   ├── test_images/            # 366 images
│   ├── validation_images/      # 366 images
│   ├── train.csv               # Label untuk training
│   ├── validation.csv          # Label untuk validation
│   └── test.csv                # Label untuk testing
├── pipes/
    ├── 1_data_exploration.py
    ├── 2_data_preprocessing.py
    ├── 3_bayesian_cnn_model.py
    ├── 4_train_model.py
    └── 5_evaluation.py
├── main_pipeline.py
└── README.md
```

### 2. Format CSV Files

Setiap CSV file harus memiliki format:

```csv
id_code,diagnosis
image_001,0
image_002,1
image_003,2
...
```

Keterangan diagnosis:

- 0: No DR (No Diabetic Retinopathy)
- 1: Mild DR
- 2: Moderate DR
- 3: Severe DR
- 4: Proliferative DR

## 📦 Instalasi Dependencies

### Buat Virtual Environment (Recommended)

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### Install Required Packages

```bash
pip install tensorflow==2.15.0
pip install tensorflow-probability==0.23.0
pip install numpy pandas matplotlib seaborn
pip install scikit-learn opencv-python pillow
pip install albumentations
```

Atau gunakan requirements.txt:

```bash
pip install -r requirements.txt
```

**requirements.txt:**

```
tensorflow==2.15.0
tensorflow-probability==0.23.0
numpy==1.24.3
pandas==2.0.3
matplotlib==3.7.2
seaborn==0.12.2
scikit-learn==1.3.0
opencv-python==4.8.0.76
Pillow==10.0.0
albumentations==1.3.1
```

## 🎯 Cara Menjalankan

### Metode 1: Jalankan Pipeline Lengkap (RECOMMENDED)

Jalankan semua proses dari eksplorasi hingga evaluasi:

```bash
python main_pipeline.py --explore --epochs 50 --batch-size 16
```

**Parameter yang tersedia:**

- `--explore`: Jalankan eksplorasi data sebelum training
- `--img-size`: Ukuran input image (default: 224)
- `--backbone`: Backbone architecture - 'efficientnet' atau 'resnet' (default: efficientnet)
- `--dropout-rate`: Dropout rate (default: 0.3)
- `--batch-size`: Batch size (default: 16)
- `--epochs`: Jumlah epochs (default: 50)
- `--learning-rate`: Learning rate (default: 1e-4)
- `--mc-iterations`: Iterasi Monte Carlo untuk uncertainty (default: 50)
- `--seed`: Random seed (default: 42)

**Contoh dengan custom parameters:**

```bash
python main_pipeline.py \
    --explore \
    --epochs 100 \
    --batch-size 32 \
    --learning-rate 0.0001 \
    --dropout-rate 0.4 \
    --mc-iterations 100
```

### Metode 2: Jalankan Step by Step

#### Step 1: Eksplorasi Data

```bash
python 1_data_exploration.py
```

Output: Visualisasi distribusi kelas, sample images

#### Step 2: Test Preprocessing

```bash
python 2_data_preprocessing.py
```

Output: Comparison preprocessing results

#### Step 3: Test Model Architecture

```bash
python 3_bayesian_cnn_model.py
```

Output: Model summary dan test uncertainty prediction

#### Step 4: Training

```bash
python 4_train_model.py
```

Output: Trained model, training history, evaluation results

#### Step 5: Detailed Evaluation

```bash
python 5_evaluation.py
```

Output: Confusion matrix, ROC curves, uncertainty analysis

## 📊 Hasil yang Dihasilkan

Setelah training selesai, Anda akan mendapatkan:

### 1. Models (`models/`)

- `bayesian_cnn_best.keras` - Model dengan validation accuracy terbaik
- `bayesian_cnn_final.keras` - Model final setelah training

### 2. Training Logs (`logs/`)

- `bayesian_cnn_dr/` - TensorBoard logs
- `bayesian_cnn_dr_training.csv` - Training metrics per epoch

### 3. Visualisasi (`visualizations/`)

- `class_distribution.png` - Distribusi kelas dataset
- `sample_images.png` - Sample images per kategori
- `preprocessing_comparison.png` - Hasil preprocessing
- `training_history.png` - Training & validation curves

### 4. Evaluation Results (`evaluation_results/`)

- `confusion_matrix.png` - Confusion matrix
- `roc_curves.png` - ROC curves per class
- `uncertainty_analysis.png` - Analisis uncertainty
- `high_uncertainty_samples.csv` - Samples dengan uncertainty tinggi

### 5. Final Results (`results/`)

- `config.json` - Konfigurasi training
- `training_history.csv` - History lengkap
- `predictions.csv` - Predictions dengan uncertainty

## 📈 Monitoring Training

### Menggunakan TensorBoard

```bash
tensorboard --logdir=logs/
```

Buka browser ke: `http://localhost:6006`

### Monitoring Real-time

Training progress akan ditampilkan di console dengan informasi:

- Loss & Accuracy per epoch
- Validation metrics
- Learning rate changes
- Best model checkpoints

## 🔧 Troubleshooting

### Problem: Out of Memory (OOM)

**Solusi:**

```bash
# Kurangi batch size
python main_pipeline.py --batch-size 8

# Atau gunakan image size lebih kecil
python main_pipeline.py --img-size 128 --batch-size 16
```

### Problem: Training Terlalu Lambat

**Solusi:**

```bash
# Gunakan GPU jika tersedia
# Check GPU availability
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

# Kurangi MC iterations
python main_pipeline.py --mc-iterations 20
```

### Problem: Dataset tidak ditemukan

**Solusi:**

- Pastikan folder APTOS-2019 ada di direktori yang sama dengan script
- Check path di script jika Anda menggunakan struktur berbeda
- Pastikan CSV files memiliki kolom 'id_code' dan 'diagnosis'

### Problem: Import Error

**Solusi:**

```bash
# Re-install dependencies
pip uninstall tensorflow tensorflow-probability
pip install tensorflow==2.15.0 tensorflow-probability==0.23.0

# Check installation
python -c "import tensorflow as tf; import tensorflow_probability as tfp; print('OK')"
```

## 📝 Tips Optimasi

### 1. Fine-tuning Hyperparameters

Untuk hasil terbaik, coba kombinasi:

- Learning rate: 1e-4, 5e-5, 1e-5
- Dropout rate: 0.2, 0.3, 0.4, 0.5
- Batch size: 8, 16, 32 (tergantung GPU memory)

### 2. Data Augmentation

Augmentation sudah included dalam preprocessing:

- Random flip (horizontal & vertical)
- Random rotation
- Random brightness & contrast

### 3. Class Imbalance

Model sudah handle class imbalance dengan:

- Class weights otomatis
- Balanced sampling

### 4. Uncertainty Threshold

Setelah training, analisis uncertainty untuk menentukan threshold:

```python
# Lihat di high_uncertainty_samples.csv
# Set threshold berdasarkan percentile (90th, 95th, 99th)
```

## 🎓 Interpretasi Hasil

### Metrics Penting:

1. **Accuracy**: Overall correctness
2. **Cohen's Kappa**: Agreement accounting for chance
3. **ROC-AUC**: Discrimination ability per class
4. **Uncertainty**: Confidence dalam prediksi

### Interpretasi Uncertainty:

- **Low uncertainty + Correct**: Model confident dan benar ✓
- **Low uncertainty + Incorrect**: Model overconfident ⚠️
- **High uncertainty + Correct**: Model uncertain tapi benar
- **High uncertainty + Incorrect**: Model uncertain dan salah - REVIEW MANUAL ⚠️

## 📞 Support

Jika ada pertanyaan atau masalah:

1. Check troubleshooting section
2. Review error messages
3. Check TensorBoard logs
4. Verify dataset structure

## 📄 License

Dataset APTOS-2019 dari Kaggle - pastikan mengikuti terms of use.

---

**Good luck dengan training! 🚀**
