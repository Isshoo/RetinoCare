#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bayesian CNN untuk Diabetic Retinopathy Detection
Script untuk Training Lokal (Non-Colab)

Author: Your Name
Date: 2024
"""

# ============================================================================
# BAGIAN 1: IMPORT LIBRARIES
# ============================================================================
print("="*80)
print("BAYESIAN CNN - DIABETIC RETINOPATHY DETECTION")
print("="*80)

import os
import sys
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Backend untuk save plot tanpa display
import matplotlib.pyplot as plt
import seaborn as sns

# Deep Learning
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout, BatchNormalization
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.optimizers import Adam

# Sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import (confusion_matrix, classification_report, 
                            accuracy_score, precision_recall_fscore_support,
                            cohen_kappa_score)
from sklearn.utils.class_weight import compute_class_weight

# Imbalanced-learn
from imblearn.over_sampling import RandomOverSampler

import warnings
warnings.filterwarnings('ignore')

# Set seeds untuk reproducibility
np.random.seed(42)
tf.random.set_seed(42)

print("\n✅ Libraries imported successfully!")
print(f"TensorFlow version: {tf.__version__}")
print(f"Keras version: {keras.__version__}")

# Check GPU availability
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"✅ GPU Available: {len(gpus)} GPU(s) detected")
    for gpu in gpus:
        print(f"   - {gpu}")
    # Set memory growth untuk prevent OOM
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print("   GPU memory growth enabled")
    except RuntimeError as e:
        print(f"   Warning: {e}")
else:
    print("⚠️  No GPU detected, using CPU")

# ============================================================================
# BAGIAN 2: KONFIGURASI & HYPERPARAMETERS
# ============================================================================
print("\n" + "="*80)
print("CONFIGURATION")
print("="*80)

# Paths
IMAGE_DIR = 'colored_images'  # Sesuaikan dengan path dataset Anda
MODEL_DIR = 'models'
RESULTS_DIR = 'results'
LOGS_DIR = 'logs'

# Hyperparameters
IMG_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 1e-4
DROPOUT_RATE = 0.4
N_CLASSES = 5
MC_SAMPLES = 30  # Monte Carlo samples untuk Bayesian inference

# Class names
CLASS_NAMES = ['No_DR', 'Mild', 'Moderate', 'Severe', 'Proliferate_DR']

print(f"\nDataset directory: {IMAGE_DIR}")
print(f"Image size: {IMG_SIZE}x{IMG_SIZE}")
print(f"Batch size: {BATCH_SIZE}")
print(f"Epochs: {EPOCHS}")
print(f"Learning rate: {LEARNING_RATE}")
print(f"Dropout rate: {DROPOUT_RATE}")
print(f"MC samples: {MC_SAMPLES}")

# Create directories
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
print(f"\n✅ Directories created: {MODEL_DIR}, {RESULTS_DIR}, {LOGS_DIR}")

# ============================================================================
# BAGIAN 3: DATA LOADING
# ============================================================================
print("\n" + "="*80)
print("DATA LOADING")
print("="*80)

# Check if dataset directory exists
if not os.path.exists(IMAGE_DIR):
    print(f"❌ ERROR: Directory '{IMAGE_DIR}' not found!")
    print(f"   Please make sure your dataset is in the correct location.")
    sys.exit(1)

print(f"\nLoading data from: {IMAGE_DIR}")

filename = []
label = []

for dir_name in os.listdir(IMAGE_DIR):
    dir_path = os.path.join(IMAGE_DIR, dir_name)
    if os.path.isdir(dir_path):
        for file in os.listdir(dir_path):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                filename.append(os.path.join(dir_name, file))
                label.append(dir_name)

print(f"✅ Total images loaded: {len(filename)}")
print(f"✅ Total labels: {len(label)}")

# Create DataFrame
data = {"filename": filename, "label": label}
df = pd.DataFrame(data)
df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)

print("\n📊 Class distribution (original):")
class_dist = df_shuffled['label'].value_counts()
print(class_dist)

# Visualize class distribution
plt.figure(figsize=(10, 6))
class_dist.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Original Class Distribution', fontsize=14, fontweight='bold')
plt.xlabel('Class', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f'{RESULTS_DIR}/original_class_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✅ Saved: {RESULTS_DIR}/original_class_distribution.png")

# ============================================================================
# BAGIAN 4: OVERSAMPLING (HANDLE IMBALANCED DATA)
# ============================================================================
print("\n" + "="*80)
print("OVERSAMPLING - HANDLING IMBALANCED DATA")
print("="*80)

class_counts = df_shuffled['label'].value_counts()
majority_class_name = class_counts.index[0]
majority_class_count = class_counts.iloc[0]

print(f"\nMajority class: {majority_class_name} ({majority_class_count} samples)")

# Create sampling strategy
sampling_strategy = {}
for class_name in class_counts.index:
    if class_name != majority_class_name:
        sampling_strategy[class_name] = majority_class_count

print(f"\nApplying RandomOverSampler...")
oversampler = RandomOverSampler(sampling_strategy=sampling_strategy, random_state=42)
X_resampled, y_resampled = oversampler.fit_resample(
    df_shuffled[['filename']], 
    df_shuffled['label']
)

df_oversampled = pd.DataFrame({
    'filename': X_resampled['filename'], 
    'label': y_resampled
})

print("\n📊 Class distribution (after oversampling):")
class_dist_oversampled = df_oversampled['label'].value_counts()
print(class_dist_oversampled)

# Visualize
plt.figure(figsize=(10, 6))
class_dist_oversampled.plot(kind='bar', color='lightgreen', edgecolor='black')
plt.title('Class Distribution After Oversampling', fontsize=14, fontweight='bold')
plt.xlabel('Class', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f'{RESULTS_DIR}/oversampled_class_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✅ Saved: {RESULTS_DIR}/oversampled_class_distribution.png")

# ============================================================================
# BAGIAN 5: TRAIN-TEST SPLIT
# ============================================================================
print("\n" + "="*80)
print("TRAIN-TEST SPLIT")
print("="*80)

train_df, test_df = train_test_split(
    df_oversampled,
    test_size=0.2,
    random_state=42,
    stratify=df_oversampled['label']
)

print(f"\n📊 Train dataset: {len(train_df)} samples")
print(train_df['label'].value_counts())

print(f"\n📊 Test dataset: {len(test_df)} samples")
print(test_df['label'].value_counts())

# ============================================================================
# BAGIAN 6: DATA GENERATORS
# ============================================================================
print("\n" + "="*80)
print("DATA GENERATORS")
print("="*80)

# Training data augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Validation data (only rescaling)
validation_datagen = ImageDataGenerator(rescale=1./255)

print("\nCreating data generators...")

train_data_generator = train_datagen.flow_from_dataframe(
    train_df,
    directory=IMAGE_DIR,
    x_col='filename',
    y_col='label',
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    classes=CLASS_NAMES,
    shuffle=True,
    seed=42
)

valid_data_generator = validation_datagen.flow_from_dataframe(
    test_df,
    directory=IMAGE_DIR,
    x_col='filename',
    y_col='label',
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    classes=CLASS_NAMES,
    shuffle=False
)

print(f"✅ Train generator: {len(train_data_generator)} batches")
print(f"✅ Validation generator: {len(valid_data_generator)} batches")

# ============================================================================
# BAGIAN 7: BUILD BAYESIAN CNN MODEL
# ============================================================================
print("\n" + "="*80)
print("BUILDING BAYESIAN CNN MODEL")
print("="*80)

def build_bayesian_cnn_model(dropout_rate=0.4):
    """
    Build Bayesian CNN Model dengan MC Dropout
    
    Args:
        dropout_rate: Dropout rate (0.3-0.5 recommended)
    
    Returns:
        model: Bayesian CNN model
    """
    print(f"\nBuilding model with dropout rate: {dropout_rate}")
    
    # Load pre-trained DenseNet121
    pretrained_model = DenseNet121(
        input_shape=(IMG_SIZE, IMG_SIZE, 3),
        include_top=False,
        weights='imagenet'
    )
    
    print(f"✅ Loaded DenseNet121 with ImageNet weights")
    
    # Freeze base model
    for layer in pretrained_model.layers:
        layer.trainable = False
    
    print(f"✅ Froze {len(pretrained_model.layers)} base layers")
    
    # Build Bayesian head
    x = GlobalAveragePooling2D(name='global_avg_pool')(pretrained_model.output)
    x = BatchNormalization(name='bn_1')(x)
    
    # Dense Layer 1 with Bayesian Dropout
    x = Dense(512, activation='relu', name='dense_1')(x)
    x = Dropout(dropout_rate, name='bayesian_dropout_1')(x)
    
    # Dense Layer 2 with Bayesian Dropout
    x = Dense(256, activation='relu', name='dense_2')(x)
    x = Dropout(dropout_rate, name='bayesian_dropout_2')(x)
    
    # Dense Layer 3 with Bayesian Dropout
    x = Dense(128, activation='relu', name='dense_3')(x)
    x = Dropout(dropout_rate, name='bayesian_dropout_3')(x)
    
    # Output layer
    output = Dense(N_CLASSES, activation='softmax', name='output')(x)
    
    # Create model
    model = Model(inputs=pretrained_model.input, outputs=output, 
                 name='Bayesian_CNN_DenseNet')
    
    print(f"✅ Model built successfully: {model.name}")
    
    return model

# Build model
model = build_bayesian_cnn_model(dropout_rate=DROPOUT_RATE)

# Compile model
model.compile(
    optimizer=Adam(learning_rate=LEARNING_RATE),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("\n✅ Model compiled successfully!")

# Model summary
print("\n" + "="*80)
print("MODEL ARCHITECTURE")
print("="*80)
model.summary()

# Count parameters
trainable_params = sum([tf.size(w).numpy() for w in model.trainable_weights])
non_trainable_params = sum([tf.size(w).numpy() for w in model.non_trainable_weights])
total_params = trainable_params + non_trainable_params

print(f"\nTrainable parameters: {trainable_params:,}")
print(f"Non-trainable parameters: {non_trainable_params:,}")
print(f"Total parameters: {total_params:,}")

# ============================================================================
# BAGIAN 8: CALLBACKS
# ============================================================================
print("\n" + "="*80)
print("SETTING UP CALLBACKS")
print("="*80)

early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose=1
)

reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=5,
    min_lr=1e-7,
    verbose=1
)

checkpoint = ModelCheckpoint(
    f'{MODEL_DIR}/best_bayesian_densenet.h5',
    monitor='val_loss',
    save_best_only=True,
    verbose=1
)

callbacks = [early_stopping, reduce_lr, checkpoint]

print("✅ Callbacks configured:")
print("   - EarlyStopping (patience=10)")
print("   - ReduceLROnPlateau (patience=5)")
print("   - ModelCheckpoint")

# ============================================================================
# BAGIAN 9: TRAINING
# ============================================================================
print("\n" + "="*80)
print("TRAINING MODEL")
print("="*80)

print(f"\nStarting training for {EPOCHS} epochs...")
print(f"This may take several hours depending on your hardware.\n")

try:
    history = model.fit(
        train_data_generator,
        steps_per_epoch=len(train_data_generator),
        epochs=EPOCHS,
        validation_data=valid_data_generator,
        validation_steps=len(valid_data_generator),
        callbacks=callbacks,
        verbose=1
    )
    
    print("\n✅ Training completed successfully!")
    
except KeyboardInterrupt:
    print("\n⚠️  Training interrupted by user!")
    print("   Saving current model state...")
    model.save(f'{MODEL_DIR}/interrupted_model.h5')
    print(f"   Model saved to: {MODEL_DIR}/interrupted_model.h5")
    sys.exit(0)

except Exception as e:
    print(f"\n❌ Error during training: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Save final model
model.save(f'{MODEL_DIR}/bayesian_densenet_final.h5')
print(f"\n✅ Final model saved to: {MODEL_DIR}/bayesian_densenet_final.h5")

# Save training history
history_dict = {key: [float(val) for val in values] 
                for key, values in history.history.items()}
with open(f'{RESULTS_DIR}/training_history.json', 'w') as f:
    json.dump(history_dict, f, indent=4)
print(f"✅ Training history saved to: {RESULTS_DIR}/training_history.json")

# ============================================================================
# BAGIAN 10: VISUALIZE TRAINING HISTORY
# ============================================================================
print("\n" + "="*80)
print("VISUALIZING TRAINING HISTORY")
print("="*80)

fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Loss
axes[0].plot(history.history['loss'], label='Train Loss', linewidth=2)
axes[0].plot(history.history['val_loss'], label='Val Loss', linewidth=2)
axes[0].set_xlabel('Epoch', fontsize=12)
axes[0].set_ylabel('Loss', fontsize=12)
axes[0].set_title('Model Loss', fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(True, alpha=0.3)

# Accuracy
axes[1].plot(history.history['accuracy'], label='Train Accuracy', linewidth=2)
axes[1].plot(history.history['val_accuracy'], label='Val Accuracy', linewidth=2)
axes[1].set_xlabel('Epoch', fontsize=12)
axes[1].set_ylabel('Accuracy', fontsize=12)
axes[1].set_title('Model Accuracy', fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(f'{RESULTS_DIR}/training_history.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✅ Saved: {RESULTS_DIR}/training_history.png")

# ============================================================================
# BAGIAN 11: BAYESIAN INFERENCE
# ============================================================================
print("\n" + "="*80)
print("BAYESIAN INFERENCE (MC DROPOUT)")
print("="*80)

def bayesian_predict(model, data_generator, n_samples=30, verbose=True):
    """
    Perform Bayesian prediction using Monte Carlo Dropout
    """
    print(f"\nPerforming Bayesian inference with {n_samples} MC samples...")
    print("This may take several minutes...\n")
    
    all_predictions = []
    all_true_labels = []
    
    # Collect all data
    for i in range(len(data_generator)):
        x_batch, y_batch = data_generator[i]
        
        # MC Dropout sampling
        batch_predictions = []
        for sample_idx in range(n_samples):
            pred = model(x_batch, training=True)
            batch_predictions.append(pred.numpy())
        
        batch_predictions = np.array(batch_predictions)
        all_predictions.append(batch_predictions)
        all_true_labels.append(y_batch)
        
        if verbose and (i + 1) % 10 == 0:
            print(f"Processed {i+1}/{len(data_generator)} batches")
    
    # Concatenate all batches
    all_predictions = np.concatenate(all_predictions, axis=1)
    all_true_labels = np.vstack(all_true_labels)
    
    # Calculate statistics
    predictions_mean = np.mean(all_predictions, axis=0)
    predictions_std = np.std(all_predictions, axis=0)
    
    # Calculate uncertainties
    predictive_entropy = -np.sum(
        predictions_mean * np.log(predictions_mean + 1e-10), 
        axis=1
    )
    
    expected_entropy = -np.mean(
        np.sum(all_predictions * np.log(all_predictions + 1e-10), axis=2),
        axis=0
    )
    
    mutual_information = predictive_entropy - expected_entropy
    
    # Get predicted classes
    pred_classes = np.argmax(predictions_mean, axis=1)
    true_classes = np.argmax(all_true_labels, axis=1)
    confidences = np.max(predictions_mean, axis=1)
    
    print("\n✅ Bayesian inference completed!")
    
    return {
        'predictions_mean': predictions_mean,
        'predictions_std': predictions_std,
        'all_predictions': all_predictions,
        'pred_classes': pred_classes,
        'true_classes': true_classes,
        'confidences': confidences,
        'predictive_entropy': predictive_entropy,
        'expected_entropy': expected_entropy,
        'mutual_information': mutual_information,
        'true_labels_onehot': all_true_labels
    }

# Perform Bayesian inference
bayesian_results = bayesian_predict(
    model, 
    valid_data_generator, 
    n_samples=MC_SAMPLES,
    verbose=True
)

# ============================================================================
# BAGIAN 12: EVALUATION & METRICS
# ============================================================================
print("\n" + "="*80)
print("EVALUATION & METRICS")
print("="*80)

# Calculate metrics
accuracy = accuracy_score(bayesian_results['true_classes'], 
                         bayesian_results['pred_classes'])
precision, recall, f1, _ = precision_recall_fscore_support(
    bayesian_results['true_classes'],
    bayesian_results['pred_classes'],
    average='weighted'
)
kappa = cohen_kappa_score(bayesian_results['true_classes'], 
                          bayesian_results['pred_classes'])

print(f"\n📊 Performance Metrics:")
print(f"{'='*50}")
print(f"Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1-Score:  {f1:.4f}")
print(f"Kappa:     {kappa:.4f}")
print(f"{'='*50}")

# Uncertainty analysis
correct_mask = bayesian_results['pred_classes'] == bayesian_results['true_classes']
entropy_correct = bayesian_results['predictive_entropy'][correct_mask]
entropy_incorrect = bayesian_results['predictive_entropy'][~correct_mask]

print(f"\n🎯 Uncertainty Analysis:")
print(f"{'='*50}")
print(f"Mean Entropy (Correct):   {np.mean(entropy_correct):.4f} ± {np.std(entropy_correct):.4f}")
print(f"Mean Entropy (Incorrect): {np.mean(entropy_incorrect):.4f} ± {np.std(entropy_incorrect):.4f}")
print(f"Difference:               {np.mean(entropy_incorrect) - np.mean(entropy_correct):.4f}")
print(f"{'='*50}")

# Classification report
print("\n📋 Classification Report:")
print("="*80)
print(classification_report(
    bayesian_results['true_classes'],
    bayesian_results['pred_classes'],
    target_names=CLASS_NAMES,
    digits=4
))

# ============================================================================
# BAGIAN 13: VISUALIZATIONS
# ============================================================================
print("\n" + "="*80)
print("GENERATING VISUALIZATIONS")
print("="*80)

# 1. Confusion Matrix
cm = confusion_matrix(bayesian_results['true_classes'], 
                     bayesian_results['pred_classes'])

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Regular confusion matrix
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES, ax=axes[0])
axes[0].set_xlabel('Predicted', fontsize=12, fontweight='bold')
axes[0].set_ylabel('True', fontsize=12, fontweight='bold')
axes[0].set_title('Confusion Matrix', fontsize=14, fontweight='bold')

# Normalized confusion matrix
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
sns.heatmap(cm_normalized, annot=True, fmt='.2%', cmap='RdYlGn',
            xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES, 
            ax=axes[1], vmin=0, vmax=1)
axes[1].set_xlabel('Predicted', fontsize=12, fontweight='bold')
axes[1].set_ylabel('True', fontsize=12, fontweight='bold')
axes[1].set_title('Normalized Confusion Matrix', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig(f'{RESULTS_DIR}/confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✅ Saved: {RESULTS_DIR}/confusion_matrix.png")

# 2. Uncertainty Analysis
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Histogram
axes[0, 0].hist(entropy_correct, bins=30, alpha=0.7, label='Correct', 
                color='green', edgecolor='black')
axes[0, 0].hist(entropy_incorrect, bins=30, alpha=0.7, label='Incorrect', 
                color='red', edgecolor='black')
axes[0, 0].set_xlabel('Predictive Entropy', fontsize=12)
axes[0, 0].set_ylabel('Frequency', fontsize=12)
axes[0, 0].set_title('Uncertainty Distribution', fontsize=14, fontweight='bold')
axes[0, 0].legend(fontsize=11)
axes[0, 0].grid(True, alpha=0.3)

# Box plot
data_to_plot = [entropy_correct, entropy_incorrect]
bp = axes[0, 1].boxplot(data_to_plot, labels=['Correct', 'Incorrect'], 
                         patch_artist=True, widths=0.6)
for patch, color in zip(bp['boxes'], ['lightgreen', 'lightcoral']):
    patch.set_facecolor(color)
axes[0, 1].set_ylabel('Predictive Entropy', fontsize=12)
axes[0, 1].set_title('Uncertainty: Correct vs Incorrect', 
                      fontsize=14, fontweight='bold')
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Scatter
colors = ['green' if c else 'red' for c in correct_mask]
axes[1, 0].scatter(bayesian_results['confidences'], 
                   bayesian_results['predictive_entropy'],
                   c=colors, alpha=0.5, s=20)
axes[1, 0].set_xlabel('Confidence', fontsize=12)
axes[1, 0].set_ylabel('Uncertainty', fontsize=12)
axes[1, 0].set_title('Confidence vs Uncertainty', fontsize=14, fontweight='bold')
axes[1, 0].grid(True, alpha=0.3)

# Uncertainty per class
entropies_per_class = [
    bayesian_results['predictive_entropy'][bayesian_results['true_classes'] == i]
    for i in range(N_CLASSES)
]
bp2 = axes[1, 1].boxplot(entropies_per_class, labels=CLASS_NAMES, 
                          patch_artist=True)
for patch in bp2['boxes']:
    patch.set_facecolor('lightblue')
axes[1, 1].set_xlabel('Class', fontsize=12)
axes[1, 1].set_ylabel('Predictive Entropy', fontsize=12)
axes[1, 1].set_title('Uncertainty per Class', fontsize=14, fontweight='bold')
axes[1, 1].tick_params(axis='x', rotation=45)
axes[1, 1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(f'{RESULTS_DIR}/uncertainty_analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✅ Saved: {RESULTS_DIR}/uncertainty_analysis.png")

# ============================================================================
# BAGIAN 14: CLINICAL DECISION SUPPORT
# ============================================================================
print("\n" + "="*80)
print("CLINICAL DECISION SUPPORT")
print("="*80)

thresholds = [0.3, 0.5, 0.7, 1.0]

print("\nReferral Analysis based on Uncertainty:")
print("-" * 70)

for threshold in thresholds:
    high_uncertainty = bayesian_results['predictive_entropy'] > threshold
    n_referred = np.sum(high_uncertainty)
    n_total = len(bayesian_results['predictive_entropy'])
    referral_rate = n_referred / n_total * 100
    
    retained = ~high_uncertainty
    if np.sum(retained) > 0:
        retained_accuracy = accuracy_score(
            bayesian_results['true_classes'][retained],
            bayesian_results['pred_classes'][retained]
        )
    else:
        retained_accuracy = 0
    
    if n_referred > 0:
        errors_in_referred = np.sum(
            (bayesian_results['pred_classes'][high_uncertainty] != 
             bayesian_results['true_classes'][high_uncertainty])
        )
        total_errors = np.sum(~correct_mask)
        error_capture = errors_in_referred / total_errors * 100 if total_errors > 0 else 0
    else:
        error_capture = 0
    
    print(f"\nThreshold > {threshold:.1f}:")
    print(f"  Referral rate:     {referral_rate:.1f}% ({n_referred}/{n_total})")
    print(f"  Retained accuracy: {retained_accuracy:.4f}")
    print(f"  Errors captured:   {error_capture:.1f}%")

# ============================================================================
# BAGIAN 15: SAVE RESULTS
# ============================================================================
print("\n" + "="*80)
print("SAVING RESULTS")
print("="*80)

# Save detailed predictions
results_df = pd.DataFrame({
    'true_class': bayesian_results['true_classes'],
    'pred_class': bayesian_results['pred_classes'],
    'true_label': [CLASS_NAMES[i] for i in bayesian_results['true_classes']],
    'pred_label': [CLASS_NAMES[i] for i in bayesian_results['pred_classes']],
    'confidence': bayesian_results['confidences'],
    'uncertainty_entropy': bayesian_results['predictive_entropy'],
    'mutual_information': bayesian_results['mutual_information'],
    'correct': correct_mask
})
results_df.to_csv(f'{RESULTS_DIR}/detailed_predictions.csv', index=False)
print(f"\n✅ Detailed predictions saved to: {RESULTS_DIR}/detailed_predictions.csv")

summary_metrics = {
    'accuracy': accuracy,
    'precision': precision,
    'recall': recall,
    'f1': f1,
    'cohen_kappa': kappa,
    'entropy_correct': np.mean(entropy_correct),
    'entropy_incorrect': np.mean(entropy_incorrect),
    'n_total_samples': len(bayesian_results['true_classes'])
}

import json
with open(f'{RESULTS_DIR}/summary_metrics.json', 'w') as f:
    json.dump(summary_metrics, f, indent=4)
print(f"✅ Summary metrics saved to: {RESULTS_DIR}/summary_metrics.json")