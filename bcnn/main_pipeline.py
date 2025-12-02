"""
MAIN PIPELINE - Bayesian CNN untuk Deteksi Retinopati Diabetik
Jalankan script ini untuk training lengkap dari awal hingga evaluasi
"""

import tensorflow as tf
import numpy as np
import pandas as pd
from pathlib import Path
import argparse
import json
from datetime import datetime

# Import modules
from pipes.data_exploration import main as explore_data
from pipes.data_preprocessing import prepare_datasets
from pipes.bayesian_cnn_model import BayesianCNN, create_callbacks
from pipes.train_model import TrainingPipeline
from pipes.evaluation import ModelEvaluator

# Set random seeds untuk reproducibility
def set_seeds(seed=42):
    np.random.seed(seed)
    tf.random.set_seed(seed)

def create_directory_structure():
    """Create necessary directories"""
    directories = [
        'models',
        'logs',
        'results',
        'evaluation_results',
        'visualizations'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✓ Directory structure created")

def check_dataset_structure():
    """Verify dataset structure"""
    dataset_path = Path("APTOS-2019")
    
    required_paths = {
        'train_images': dataset_path / "train_images/train_images",
        'test_images': dataset_path / "test_images/test_images",
        'validation_images': dataset_path / "validation_images/validation_images",
        'train_csv': dataset_path / "train.csv"
    }
    
    print("\nChecking dataset structure...")
    all_exist = True
    
    for name, path in required_paths.items():
        exists = path.exists()
        status = "✓" if exists else "✗"
        print(f"{status} {name}: {path}")
        all_exist = all_exist and exists
    
    if not all_exist:
        print("\n⚠ Warning: Some required files/folders are missing!")
        print("Please ensure your dataset structure matches the required format.")
        return False
    
    return True

def run_full_pipeline(args):
    """Run complete training pipeline"""
    
    print("="*70)
    print("BAYESIAN CNN - DETEKSI RETINOPATI DIABETIK")
    print("="*70)
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Set seeds
    set_seeds(args.seed)
    
    # Create directories
    create_directory_structure()
    
    # Check dataset
    if not check_dataset_structure():
        print("\nPlease fix dataset structure before continuing.")
        return
    
    # Step 1: Data Exploration (optional)
    if args.explore:
        print("\n" + "="*70)
        print("STEP 1: DATA EXPLORATION")
        print("="*70)
        explore_data()
    
    # Step 2: Prepare configuration
    print("\n" + "="*70)
    print("STEP 2: CONFIGURATION")
    print("="*70)
    
    config = {
        'dataset_path': Path("APTOS-2019"),
        'train_path': Path("APTOS-2019/train_images/train_images"),
        'val_path': Path("APTOS-2019/validation_images/validation_images"),
        'test_path': Path("APTOS-2019/test_images/test_images"),
        'train_csv': Path("APTOS-2019/train.csv"),
        'val_csv': Path("APTOS-2019/validation.csv"),
        'test_csv': Path("APTOS-2019/test.csv"),
        'img_size': args.img_size,
        'batch_size': args.batch_size,
        'epochs': args.epochs,
        'learning_rate': args.learning_rate,
        'num_classes': 5,
        'dropout_rate': args.dropout_rate,
        'backbone': args.backbone,
        'seed': args.seed,
        'timestamp': datetime.now().strftime('%Y%m%d_%H%M%S')
    }
    
    print(json.dumps({k: str(v) for k, v in config.items()}, indent=2))
    
    # Step 3: Training
    print("\n" + "="*70)
    print("STEP 3: MODEL TRAINING")
    print("="*70)
    
    pipeline = TrainingPipeline(config)
    
    # Load data
    train_ds, val_ds, test_ds, class_weights = pipeline.load_data()
    
    # Build model
    model = pipeline.build_and_compile_model()
    
    # Train
    history = pipeline.train()
    
    # Plot training history
    pipeline.plot_training_history(
        save_path='storage/visualizations/training_history.png'
    )
    
    # Step 4: Evaluation
    print("\n" + "="*70)
    print("STEP 4: MODEL EVALUATION")
    print("="*70)
    
    # Evaluate on test set
    test_results = pipeline.evaluate()
    
    # Predict dengan uncertainty
    print("\nGenerating predictions with uncertainty estimation...")
    mean_preds, uncertainties, pred_labels, true_labels = \
        pipeline.predict_with_uncertainty(test_ds, n_iter=args.mc_iterations)
    
    # Create evaluator
    evaluator = ModelEvaluator(
        true_labels, pred_labels,
        mean_preds, uncertainties
    )
    
    # Generate full evaluation report
    evaluator.generate_full_report(output_dir='storage/evaluation/evaluation_results')
    
    # Step 5: Save final results
    print("\n" + "="*70)
    print("STEP 5: SAVING RESULTS")
    print("="*70)
    
    pipeline.save_results(output_dir='results')
    
    # Save model
    model.save('models/bayesian_cnn_final.keras')
    print("✓ Model saved to models/bayesian_cnn_final.keras")
    
    # Save predictions
    predictions_df = pd.DataFrame({
        'true_label': true_labels,
        'predicted_label': pred_labels,
        'confidence': np.max(mean_preds, axis=1),
        'mean_uncertainty': np.mean(uncertainties, axis=1)
    })
    predictions_df.to_csv('storage/results/predictions.csv', index=False)
    print("✓ Predictions saved to results/predictions.csv")
    
    # Final summary
    print("\n" + "="*70)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("="*70)
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\nTest Accuracy: {test_results[1]:.4f}")
    print(f"Test Loss: {test_results[0]:.4f}")
    print("\nAll results saved to:")
    print("  - models/bayesian_cnn_final.keras")
    print("  - results/")
    print("  - evaluation_results/")
    print("  - visualizations/")
    print("="*70)

def main():
    parser = argparse.ArgumentParser(
        description='Train Bayesian CNN for Diabetic Retinopathy Detection'
    )
    
    # Dataset parameters
    parser.add_argument('--explore', action='store_true',
                       help='Run data exploration before training')
    
    # Model parameters
    parser.add_argument('--img-size', type=int, default=224,
                       help='Input image size (default: 224)')
    parser.add_argument('--backbone', type=str, default='efficientnet',
                       choices=['efficientnet', 'resnet'],
                       help='Backbone architecture (default: efficientnet)')
    parser.add_argument('--dropout-rate', type=float, default=0.3,
                       help='Dropout rate (default: 0.3)')
    
    # Training parameters
    parser.add_argument('--batch-size', type=int, default=16,
                       help='Batch size (default: 16)')
    parser.add_argument('--epochs', type=int, default=50,
                       help='Number of epochs (default: 50)')
    parser.add_argument('--learning-rate', type=float, default=1e-4,
                       help='Learning rate (default: 1e-4)')
    
    # Bayesian parameters
    parser.add_argument('--mc-iterations', type=int, default=50,
                       help='Monte Carlo iterations for uncertainty (default: 50)')
    
    # Other parameters
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed (default: 42)')
    
    args = parser.parse_args()
    
    # Run pipeline
    run_full_pipeline(args)

if __name__ == "__main__":
    main()