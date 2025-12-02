import tensorflow as tf
import numpy as np
import cv2
from pathlib import Path
import pandas as pd
from sklearn.utils.class_weight import compute_class_weight

# Konfigurasi
IMG_SIZE = 224  # Untuk EfficientNet atau ResNet
BATCH_SIZE = 16
AUTOTUNE = tf.data.AUTOTUNE

class DataPreprocessor:
    def __init__(self, img_size=224):
        self.img_size = img_size
    
    def preprocess_image(self, image_path, apply_clahe=True):
        """Preprocessing untuk retinal images"""
        # Load image
        img = cv2.imread(str(image_path))
        
        if img is None:
            raise ValueError(f"Cannot load image: {image_path}")
        
        # Crop circular region (menghilangkan black borders)
        img = self.crop_image_from_gray(img)
        
        # Resize
        img = cv2.resize(img, (self.img_size, self.img_size))
        
        # Apply CLAHE untuk meningkatkan kontras
        if apply_clahe:
            img = self.apply_clahe_rgb(img)
        
        # Normalize ke [0, 1]
        img = img.astype(np.float32) / 255.0
        
        return img
    
    def crop_image_from_gray(self, img, tol=7):
        """Crop black borders dari retinal images"""
        if img.ndim == 2:
            mask = img > tol
            return img[np.ix_(mask.any(1), mask.any(0))]
        elif img.ndim == 3:
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            mask = gray_img > tol
            
            check_shape = img[:, :, 0][np.ix_(mask.any(1), mask.any(0))].shape[0]
            if check_shape == 0:
                return img
            else:
                img1 = img[:, :, 0][np.ix_(mask.any(1), mask.any(0))]
                img2 = img[:, :, 1][np.ix_(mask.any(1), mask.any(0))]
                img3 = img[:, :, 2][np.ix_(mask.any(1), mask.any(0))]
                img = np.stack([img1, img2, img3], axis=-1)
            return img
    
    def apply_clahe_rgb(self, img):
        """Apply CLAHE untuk setiap channel RGB"""
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        
        # Convert ke LAB color space
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE ke L channel
        l = clahe.apply(l)
        
        # Merge kembali
        lab = cv2.merge([l, a, b])
        img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return img

def create_tf_dataset(df, image_dir, preprocessor, augment=False, shuffle=True):
    """Create TensorFlow dataset"""
    
    def load_and_preprocess(image_path, label):
        # Load image menggunakan tf.py_function
        def _load_img(path):
            path_str = path.numpy().decode('utf-8')
            img = preprocessor.preprocess_image(path_str)
            return img.astype(np.float32)
        
        image = tf.py_function(_load_img, [image_path], tf.float32)
        image.set_shape([preprocessor.img_size, preprocessor.img_size, 3])
        
        return image, label
    
    def augment_image(image, label):
        """Data augmentation"""
        # Random flip
        image = tf.image.random_flip_left_right(image)
        image = tf.image.random_flip_up_down(image)
        
        # Random rotation (small angles)
        image = tf.image.rot90(image, k=tf.random.uniform([], 0, 4, dtype=tf.int32))
        
        # Random brightness
        image = tf.image.random_brightness(image, 0.2)
        
        # Random contrast
        image = tf.image.random_contrast(image, 0.8, 1.2)
        
        # Clip values
        image = tf.clip_by_value(image, 0.0, 1.0)
        
        return image, label
    
    # Buat list image paths dan labels
    image_paths = []
    labels = []
    
    for _, row in df.iterrows():
        img_name = row['id_code'] if 'id_code' in row else row.iloc[0]
        label = row['diagnosis'] if 'diagnosis' in row else row.iloc[1]
        
        # Cek ekstensi file
        img_path = Path(image_dir) / f"{img_name}.png"
        if not img_path.exists():
            img_path = Path(image_dir) / f"{img_name}.jpg"
        
        if img_path.exists():
            image_paths.append(str(img_path))
            labels.append(label)
    
    # Create TF dataset
    dataset = tf.data.Dataset.from_tensor_slices((image_paths, labels))
    
    if shuffle:
        dataset = dataset.shuffle(buffer_size=len(image_paths))
    
    # Load and preprocess
    dataset = dataset.map(load_and_preprocess, num_parallel_calls=AUTOTUNE)
    
    # Apply augmentation
    if augment:
        dataset = dataset.map(augment_image, num_parallel_calls=AUTOTUNE)
    
    # Batch and prefetch
    dataset = dataset.batch(BATCH_SIZE)
    dataset = dataset.prefetch(AUTOTUNE)
    
    return dataset

def compute_class_weights(df, label_column='diagnosis'):
    """Hitung class weights untuk imbalanced dataset"""
    labels = df[label_column].values
    classes = np.unique(labels)
    
    weights = compute_class_weight(
        class_weight='balanced',
        classes=classes,
        y=labels
    )
    
    class_weights = dict(zip(classes, weights))
    
    print("\nClass Weights:")
    for class_idx, weight in class_weights.items():
        print(f"Class {class_idx}: {weight:.4f}")
    
    return class_weights

def prepare_datasets(train_df, val_df, test_df, 
                     train_dir, val_dir, test_dir, 
                     img_size=224):
    """Prepare semua datasets"""
    
    preprocessor = DataPreprocessor(img_size=img_size)
    
    print("Creating training dataset...")
    train_ds = create_tf_dataset(
        train_df, train_dir, preprocessor, 
        augment=True, shuffle=True
    )
    
    print("Creating validation dataset...")
    val_ds = create_tf_dataset(
        val_df, val_dir, preprocessor, 
        augment=False, shuffle=False
    )
    
    print("Creating test dataset...")
    test_ds = create_tf_dataset(
        test_df, test_dir, preprocessor, 
        augment=False, shuffle=False
    )
    
    # Compute class weights
    class_weights = compute_class_weights(train_df)
    
    return train_ds, val_ds, test_ds, class_weights

# Test preprocessing
if __name__ == "__main__":
    from pathlib import Path
    
    # Load sample
    DATASET_PATH = Path("APTOS-2019")
    TRAIN_PATH = DATASET_PATH / "train_images/train_images"
    
    preprocessor = DataPreprocessor(img_size=224)
    
    # Test pada sample image
    sample_images = list(TRAIN_PATH.glob('*.png'))[:3]
    
    import matplotlib.pyplot as plt
    
    fig, axes = plt.subplots(3, 2, figsize=(10, 12))
    
    for idx, img_path in enumerate(sample_images):
        # Original
        original = cv2.imread(str(img_path))
        original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        
        # Preprocessed
        preprocessed = preprocessor.preprocess_image(img_path)
        
        axes[idx, 0].imshow(original)
        axes[idx, 0].set_title('Original')
        axes[idx, 0].axis('off')
        
        axes[idx, 1].imshow(preprocessed)
        axes[idx, 1].set_title('Preprocessed')
        axes[idx, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig('storage/data_preprocessing/preprocessing_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Preprocessing test completed!")