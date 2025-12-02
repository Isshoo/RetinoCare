import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import cv2
from collections import Counter

# Konfigurasi path
DATASET_PATH = Path("APTOS-2019")
TRAIN_PATH = DATASET_PATH / "train_images/train_images"
TEST_PATH = DATASET_PATH / "test_images/test_images"
VAL_PATH = DATASET_PATH / "validation_images/validation_images"

print(TRAIN_PATH)

# Kategori
CATEGORIES = {
    0: 'No DR',
    1: 'Mild DR',
    2: 'Moderate DR',
    3: 'Severe DR',
    4: 'Proliferative DR'
}

def load_labels(csv_path):
    """Load labels dari CSV file"""
    df = pd.read_csv(csv_path)
    print(f"Total samples: {len(df)}")
    print(f"\nColumns: {df.columns.tolist()}")
    print(f"\nFirst 5 rows:\n{df.head()}")
    return df

def analyze_distribution(df, label_column='diagnosis'):
    """Analisis distribusi kelas"""
    plt.figure(figsize=(12, 5))
    
    # Count plot
    plt.subplot(1, 2, 1)
    counts = df[label_column].value_counts().sort_index()
    plt.bar([CATEGORIES[i] for i in counts.index], counts.values, color='skyblue')
    plt.xlabel('Kategori')
    plt.ylabel('Jumlah Sampel')
    plt.title('Distribusi Kelas Dataset')
    plt.xticks(rotation=45)
    
    # Pie chart
    plt.subplot(1, 2, 2)
    plt.pie(counts.values, labels=[CATEGORIES[i] for i in counts.index], 
            autopct='%1.1f%%', startangle=90)
    plt.title('Proporsi Kelas')
    
    plt.tight_layout()
    plt.savefig('storage/data_exploration/class_distribution.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\nDistribusi Kelas:")
    for idx, count in counts.items():
        print(f"{CATEGORIES[idx]}: {count} ({count/len(df)*100:.2f}%)")
    
    return counts

def check_images(image_path, sample_count=5):
    """Cek sample images dan dimensi"""
    images = list(Path(image_path).glob('*.png')) + list(Path(image_path).glob('*.jpg'))
    
    if len(images) == 0:
        print(f"Tidak ada gambar ditemukan di {image_path}")
        return
    
    print(f"\nTotal images di {image_path}: {len(images)}")
    
    # Cek dimensi beberapa sample
    dimensions = []
    for img_path in images[:sample_count]:
        img = cv2.imread(str(img_path))
        if img is not None:
            dimensions.append(img.shape)
            print(f"{img_path.name}: {img.shape}")
    
    # Hitung rata-rata dimensi
    if dimensions:
        heights = [d[0] for d in dimensions]
        widths = [d[1] for d in dimensions]
        print(f"\nRata-rata dimensi: {np.mean(heights):.0f} x {np.mean(widths):.0f}")
        print(f"Min dimensi: {min(heights)} x {min(widths)}")
        print(f"Max dimensi: {max(heights)} x {max(widths)}")

def visualize_samples(df, image_path, label_column='diagnosis', samples_per_class=2):
    """Visualisasi sample images per kategori"""
    fig, axes = plt.subplots(len(CATEGORIES), samples_per_class, 
                             figsize=(samples_per_class*4, len(CATEGORIES)*3))
    
    for class_idx, class_name in CATEGORIES.items():
        # Ambil sample dari class ini
        class_samples = df[df[label_column] == class_idx].head(samples_per_class)
        
        for idx, (_, row) in enumerate(class_samples.iterrows()):
            ax = axes[class_idx, idx] if samples_per_class > 1 else axes[class_idx]
            
            # Load image
            img_name = row['id_code'] if 'id_code' in row else row.iloc[0]
            img_path = Path(image_path) / f"{img_name}.png"
            
            if not img_path.exists():
                img_path = Path(image_path) / f"{img_name}.jpg"
            
            if img_path.exists():
                img = cv2.imread(str(img_path))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                ax.imshow(img)
                ax.set_title(f"{class_name}\n{img_name}", fontsize=10)
            else:
                ax.text(0.5, 0.5, 'Image not found', ha='center', va='center')
            
            ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('storage/data_exploration/sample_images.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    print("="*60)
    print("EKSPLORASI DATASET APTOS-2019")
    print("="*60)
    
    # Load labels
    train_labels_path = DATASET_PATH / "train.csv"
    if train_labels_path.exists():
        df = load_labels(train_labels_path)
        
        # Analisis distribusi
        print("\n" + "="*60)
        print("ANALISIS DISTRIBUSI KELAS")
        print("="*60)
        analyze_distribution(df)
        
        # Visualisasi samples
        print("\n" + "="*60)
        print("VISUALISASI SAMPLE IMAGES")
        print("="*60)
        visualize_samples(df, TRAIN_PATH)
    else:
        print(f"File {train_labels_path} tidak ditemukan!")
    
    # Check images di setiap folder
    print("\n" + "="*60)
    print("CEK IMAGES DI SETIAP FOLDER")
    print("="*60)
    
    for folder_name, folder_path in [("Train", TRAIN_PATH), 
                                      ("Test", TEST_PATH), 
                                      ("Validation", VAL_PATH)]:
        print(f"\n{folder_name} Images:")
        check_images(folder_path)

if __name__ == "__main__":
    main()