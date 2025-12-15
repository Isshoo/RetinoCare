#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bayesian CNN - Analisis Probabilitas Detail
Script untuk analisis probabilitas dari trained model

Author: Your Name
Date: 2024
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model

# ============================================================================
# CONFIGURATION
# ============================================================================
MODEL_PATH = 'models/bayesian_densenet_final.h5'
IMAGE_DIR = 'colored_images'
RESULTS_DIR = 'results/probability_analysis'
IMG_SIZE = 224
MC_SAMPLES = 30
CLASS_NAMES = ['No_DR', 'Mild', 'Moderate', 'Severe', 'Proliferate_DR']

# Create output directory
os.makedirs(RESULTS_DIR, exist_ok=True)

print("="*80)
print("BAYESIAN PROBABILITY ANALYSIS")
print("="*80)
print(f"\nModel: {MODEL_PATH}")
print(f"Output directory: {RESULTS_DIR}")
print(f"MC Samples: {MC_SAMPLES}")

# ============================================================================
# LOAD MODEL
# ============================================================================
print("\n" + "="*80)
print("LOADING MODEL")
print("="*80)

if not os.path.exists(MODEL_PATH):
    print(f"❌ Error: Model not found at {MODEL_PATH}")
    print("   Please train the model first using the main script.")
    exit(1)

model = load_model(MODEL_PATH)
print(f"✅ Model loaded successfully from: {MODEL_PATH}")

# ============================================================================
# FUNGSI: EKSTRAK PROBABILITAS BAYESIAN
# ============================================================================

def get_detailed_probabilities(model, image, n_samples=30):
    """
    Ekstrak probabilitas Bayesian lengkap untuk satu image
    
    Args:
        model: Trained Bayesian model
        image: Input image (224, 224, 3) normalized
        n_samples: Number of MC samples
    
    Returns:
        dict dengan semua statistik probabilitas
    """
    # Ensure 4D input
    if len(image.shape) == 3:
        image = np.expand_dims(image, axis=0)
    
    # MC Dropout sampling
    predictions = []
    for i in range(n_samples):
        pred = model(image, training=True)
        predictions.append(pred.numpy()[0])
    
    predictions = np.array(predictions)
    
    # Calculate statistics
    mean_probs = np.mean(predictions, axis=0)
    std_probs = np.std(predictions, axis=0)
    median_probs = np.median(predictions, axis=0)
    min_probs = np.min(predictions, axis=0)
    max_probs = np.max(predictions, axis=0)
    q25_probs = np.percentile(predictions, 25, axis=0)
    q75_probs = np.percentile(predictions, 75, axis=0)
    
    # Confidence intervals (95%)
    ci_lower = mean_probs - 1.96 * std_probs
    ci_upper = mean_probs + 1.96 * std_probs
    ci_lower = np.clip(ci_lower, 0, 1)
    ci_upper = np.clip(ci_upper, 0, 1)
    
    # Predicted class
    predicted_idx = np.argmax(mean_probs)
    predicted_class = CLASS_NAMES[predicted_idx]
    
    # Uncertainty metrics
    entropy = -np.sum(mean_probs * np.log(mean_probs + 1e-10))
    cv = (std_probs[predicted_idx] / mean_probs[predicted_idx]) * 100
    
    return {
        'class_names': CLASS_NAMES,
        'predicted_class_idx': predicted_idx,
        'predicted_class': predicted_class,
        'mean_probabilities': mean_probs,
        'std_probabilities': std_probs,
        'median_probabilities': median_probs,
        'min_probabilities': min_probs,
        'max_probabilities': max_probs,
        'q25_probabilities': q25_probs,
        'q75_probabilities': q75_probs,
        'ci_95_lower': ci_lower,
        'ci_95_upper': ci_upper,
        'confidence': mean_probs[predicted_idx],
        'uncertainty_entropy': entropy,
        'coefficient_variation_pct': cv,
        'all_mc_samples': predictions
    }


def print_probability_report(prob_results):
    """Print detailed probability report"""
    
    print("\n" + "="*80)
    print("BAYESIAN PROBABILITY REPORT")
    print("="*80)
    
    print(f"\n🎯 PREDICTION: {prob_results['predicted_class']}")
    print(f"   Confidence: {prob_results['confidence']:.4f} ({prob_results['confidence']*100:.2f}%)")
    print(f"   Uncertainty: {prob_results['uncertainty_entropy']:.4f}")
    print(f"   CV: {prob_results['coefficient_variation_pct']:.2f}%")
    
    # Interpretation
    entropy = prob_results['uncertainty_entropy']
    if entropy < 0.5:
        status = "✅ LOW (Very confident)"
        recommendation = "Safe for automated diagnosis"
    elif entropy < 1.0:
        status = "⚠️ MEDIUM (Moderately confident)"
        recommendation = "Monitor or second check"
    else:
        status = "❌ HIGH (Not confident)"
        recommendation = "MUST refer to expert!"
    
    print(f"\n📊 UNCERTAINTY: {status}")
    print(f"   Recommendation: {recommendation}")
    
    print(f"\n{'='*80}")
    print("DETAILED PROBABILITIES PER CLASS")
    print("="*80)
    print(f"{'Class':<15} {'Mean':<8} {'Std':<8} {'95% CI':<20} {'Range':<20}")
    print("-"*80)
    
    for i, cls in enumerate(prob_results['class_names']):
        mean_val = prob_results['mean_probabilities'][i]
        std_val = prob_results['std_probabilities'][i]
        ci_low = prob_results['ci_95_lower'][i]
        ci_high = prob_results['ci_95_upper'][i]
        min_val = prob_results['min_probabilities'][i]
        max_val = prob_results['max_probabilities'][i]
        
        marker = "→ " if i == prob_results['predicted_class_idx'] else "  "
        
        print(f"{marker}{cls:<13} {mean_val:.4f}  ±{std_val:.4f}  "
              f"[{ci_low:.4f}, {ci_high:.4f}]  "
              f"[{min_val:.4f}, {max_val:.4f}]")
    
    print("="*80)


def visualize_single_prediction(prob_results, image=None, save_path=None):
    """Visualize probabilities untuk satu prediksi"""
    
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    mean_probs = prob_results['mean_probabilities']
    std_probs = prob_results['std_probabilities']
    all_samples = prob_results['all_mc_samples']
    predicted_idx = prob_results['predicted_class_idx']
    
    # 1. Image (if provided)
    if image is not None:
        ax1 = fig.add_subplot(gs[0, 0])
        if len(image.shape) == 4:
            image = image[0]
        ax1.imshow(image)
        ax1.axis('off')
        ax1.set_title(f'Input Image\nPrediction: {prob_results["predicted_class"]}',
                     fontsize=12, fontweight='bold')
    
    # 2. Bar chart dengan error bars
    ax2 = fig.add_subplot(gs[0, 1:])
    x_pos = np.arange(len(CLASS_NAMES))
    colors = ['green' if i == predicted_idx else 'skyblue' for i in range(len(CLASS_NAMES))]
    bars = ax2.bar(x_pos, mean_probs, yerr=std_probs, capsize=8, 
                   color=colors, edgecolor='black', linewidth=1.5, alpha=0.7)
    ax2.set_xlabel('Class', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Probability', fontsize=12, fontweight='bold')
    ax2.set_title('Mean Probability ± Std', fontsize=14, fontweight='bold')
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(CLASS_NAMES, rotation=45, ha='right')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_ylim([0, 1])
    
    for i, (m, s) in enumerate(zip(mean_probs, std_probs)):
        ax2.text(i, m + s + 0.03, f'{m*100:.1f}%\n±{s*100:.1f}%', 
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # 3. Box plot
    ax3 = fig.add_subplot(gs[1, :])
    bp = ax3.boxplot([all_samples[:, i] for i in range(len(CLASS_NAMES))],
                     labels=CLASS_NAMES, patch_artist=True, widths=0.6,
                     showmeans=True, meanline=True)
    
    for i, patch in enumerate(bp['boxes']):
        if i == predicted_idx:
            patch.set_facecolor('lightgreen')
        else:
            patch.set_facecolor('lightblue')
        patch.set_alpha(0.7)
    
    ax3.set_xlabel('Class', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Probability', fontsize=12, fontweight='bold')
    ax3.set_title('Probability Distribution per Class', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.set_ylim([0, 1])
    
    # 4. Violin plot for predicted class
    ax4 = fig.add_subplot(gs[2, 0])
    predicted_samples = all_samples[:, predicted_idx]
    parts = ax4.violinplot([predicted_samples], positions=[0], widths=0.7,
                           showmeans=True, showmedians=True)
    for pc in parts['bodies']:
        pc.set_facecolor('lightgreen')
        pc.set_alpha(0.7)
    
    ax4.set_ylabel('Probability', fontsize=12, fontweight='bold')
    ax4.set_title(f'Distribution: {prob_results["predicted_class"]}', fontsize=12, fontweight='bold')
    ax4.set_xticks([0])
    ax4.set_xticklabels([prob_results['predicted_class']])
    ax4.grid(True, alpha=0.3, axis='y')
    
    mean_val = prob_results['confidence']
    std_val = std_probs[predicted_idx]
    ax4.axhline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.3f}')
    ax4.axhline(mean_val + std_val, color='orange', linestyle=':', linewidth=1.5)
    ax4.axhline(mean_val - std_val, color='orange', linestyle=':', linewidth=1.5)
    ax4.legend(fontsize=9)
    
    # 5. Histogram
    ax5 = fig.add_subplot(gs[2, 1])
    ax5.hist(predicted_samples, bins=20, color='lightgreen', edgecolor='black', alpha=0.7)
    ax5.axvline(mean_val, color='red', linestyle='--', linewidth=2, label='Mean')
    ax5.axvline(mean_val + std_val, color='orange', linestyle=':', linewidth=2, label='+1σ')
    ax5.axvline(mean_val - std_val, color='orange', linestyle=':', linewidth=2, label='-1σ')
    ax5.set_xlabel('Probability', fontsize=12, fontweight='bold')
    ax5.set_ylabel('Frequency', fontsize=12, fontweight='bold')
    ax5.set_title(f'Histogram: {prob_results["predicted_class"]}', fontsize=12, fontweight='bold')
    ax5.legend(fontsize=9)
    ax5.grid(True, alpha=0.3, axis='y')
    
    # 6. Info box
    ax6 = fig.add_subplot(gs[2, 2])
    ax6.axis('off')
    
    info_text = f"""
    BAYESIAN STATISTICS
    
    Predicted Class:
    {prob_results['predicted_class']}
    
    Confidence:
    {prob_results['confidence']:.4f} ({prob_results['confidence']*100:.2f}%)
    
    Standard Deviation:
    ±{std_probs[predicted_idx]:.4f}
    
    95% CI:
    [{prob_results['ci_95_lower'][predicted_idx]:.4f}, 
     {prob_results['ci_95_upper'][predicted_idx]:.4f}]
    
    CV: {prob_results['coefficient_variation_pct']:.2f}%
    
    Entropy: {prob_results['uncertainty_entropy']:.4f}
    
    MC Samples: {len(all_samples)}
    """
    
    ax6.text(0.1, 0.5, info_text, fontsize=11, family='monospace',
            verticalalignment='center', bbox=dict(boxstyle='round', 
            facecolor='wheat', alpha=0.5))
    
    plt.suptitle('Bayesian CNN - Probability Analysis', fontsize=16, fontweight='bold', y=0.98)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Saved: {save_path}")
    
    plt.close()


# ============================================================================
# CONTOH PENGGUNAAN: ANALISIS SATU IMAGE
# ============================================================================
print("\n" + "="*80)
print("EXAMPLE: ANALYZING SINGLE IMAGE")
print("="*80)

# Load sample image (ganti dengan path image Anda)
# Contoh: ambil image pertama dari setiap kelas
example_images = []

for class_name in CLASS_NAMES:
    class_dir = os.path.join(IMAGE_DIR, class_name)
    if os.path.exists(class_dir):
        files = [f for f in os.listdir(class_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if files:
            img_path = os.path.join(class_dir, files[0])
            example_images.append((class_name, img_path))

print(f"\nFound {len(example_images)} sample images")

# Analyze each sample
for idx, (true_class, img_path) in enumerate(example_images):
    print(f"\n{'='*80}")
    print(f"Analyzing image {idx+1}/{len(example_images)}: {true_class}")
    print(f"Path: {img_path}")
    print('='*80)
    
    # Load and preprocess image
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_original = img.copy()
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    img_normalized = img / 255.0
    
    # Get Bayesian probabilities
    prob_results = get_detailed_probabilities(model, img_normalized, n_samples=MC_SAMPLES)
    
    # Print report
    print_probability_report(prob_results)
    
    # Visualize
    save_path = f'{RESULTS_DIR}/probability_analysis_{true_class}_sample{idx+1}.png'
    visualize_single_prediction(prob_results, img, save_path=save_path)
    
    # Save detailed results to CSV
    prob_df = pd.DataFrame({
        'class': CLASS_NAMES,
        'mean_prob': prob_results['mean_probabilities'],
        'std_prob': prob_results['std_probabilities'],
        'min_prob': prob_results['min_probabilities'],
        'max_prob': prob_results['max_probabilities'],
        'ci_lower': prob_results['ci_95_lower'],
        'ci_upper': prob_results['ci_95_upper']
    })
    
    csv_path = f'{RESULTS_DIR}/probabilities_{true_class}_sample{idx+1}.csv'
    prob_df.to_csv(csv_path, index=False)
    print(f"✅ Saved probabilities to: {csv_path}")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("="*80)
print(" " * 25 + "ANALYSIS COMPLETE!")
print("="*80)
print("="*80)

print(f"\n📁 All results saved to: {RESULTS_DIR}/")
print("\nGenerated files:")
print(f"  - {len(example_images)} probability analysis plots")
print(f"  - {len(example_images)} probability CSV files")

print("\n" + "="*80)
print("🎉 DONE!")
print("="*80)