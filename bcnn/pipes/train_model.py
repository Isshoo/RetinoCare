import tensorflow as tf
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json

# Import dari file sebelumnya
from data_preprocessing import prepare_datasets, DataPreprocessor
from bayesian_cnn_model import BayesianCNN, create_callbacks

# Konfigurasi
DATASET_PATH = Path("APTOS-2019")
TRAIN_PATH = DATASET_PATH / "train_images/train_images"
VAL_PATH = DATASET_PATH / "validation_images/validation_images"
TEST_PATH = DATASET_PATH / "test_images/test_images"

IMG_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 50
LEARNING_RATE = 1e-4
NUM_CLASSES = 5

class TrainingPipeline:
    def __init__(self, config):
        self.config = config
        self.history = None
        self.model = None
        
    def load_data(self):
        """Load dan prepare datasets"""
        print("Loading datasets...")
        
        # Load labels
        train_df = pd.read_csv(self.config['train_csv'])
        val_df = pd.read_csv(self.config['val_csv'])
        test_df = pd.read_csv(self.config['test_csv'])
        
        print(f"Train samples: {len(train_df)}")
        print(f"Validation samples: {len(val_df)}")
        print(f"Test samples: {len(test_df)}")
        
        # Prepare datasets
        train_ds, val_ds, test_ds, class_weights = prepare_datasets(
            train_df, val_df, test_df,
            self.config['train_path'],
            self.config['val_path'],
            self.config['test_path'],
            img_size=self.config['img_size']
        )
        
        self.train_ds = train_ds
        self.val_ds = val_ds
        self.test_ds = test_ds
        self.class_weights = class_weights
        
        return train_ds, val_ds, test_ds, class_weights
    
    def build_and_compile_model(self):
        """Build dan compile model"""
        print("\nBuilding Bayesian CNN model...")
        
        bayesian_cnn = BayesianCNN(
            input_shape=(self.config['img_size'], self.config['img_size'], 3),
            num_classes=self.config['num_classes'],
            dropout_rate=0.3,
            backbone='efficientnet'
        )
        
        model = bayesian_cnn.build_model()
        
        # Compile model
        optimizer = tf.keras.optimizers.Adam(
            learning_rate=self.config['learning_rate']
        )
        
        model.compile(
            optimizer=optimizer,
            loss='sparse_categorical_crossentropy',
            metrics=[
                'accuracy',
                tf.keras.metrics.SparseCategoricalAccuracy(name='acc'),
                tf.keras.metrics.SparseTopKCategoricalAccuracy(k=2, name='top_2_acc')
            ]
        )
        
        self.model = model
        self.bayesian_cnn = bayesian_cnn
        
        print(f"\nModel compiled successfully!")
        print(f"Total parameters: {model.count_params():,}")
        
        return model
    
    def train(self):
        """Train model"""
        print("\n" + "="*60)
        print("STARTING TRAINING")
        print("="*60)
        
        # Create callbacks
        callbacks = create_callbacks(model_name='bayesian_cnn_dr')
        
        # Train
        history = self.model.fit(
            self.train_ds,
            validation_data=self.val_ds,
            epochs=self.config['epochs'],
            class_weight=self.class_weights,
            callbacks=callbacks,
            verbose=1
        )
        
        self.history = history
        
        return history
    
    def plot_training_history(self, save_path='storage/training/training_history.png'):
        """Plot training history"""
        if self.history is None:
            print("No training history available!")
            return
        
        history = self.history.history
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Loss
        axes[0, 0].plot(history['loss'], label='Train Loss')
        axes[0, 0].plot(history['val_loss'], label='Val Loss')
        axes[0, 0].set_title('Loss')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Loss')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Accuracy
        axes[0, 1].plot(history['accuracy'], label='Train Acc')
        axes[0, 1].plot(history['val_accuracy'], label='Val Acc')
        axes[0, 1].set_title('Accuracy')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('Accuracy')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # Top-2 Accuracy
        axes[1, 0].plot(history['top_2_acc'], label='Train Top-2 Acc')
        axes[1, 0].plot(history['val_top_2_acc'], label='Val Top-2 Acc')
        axes[1, 0].set_title('Top-2 Accuracy')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].set_ylabel('Accuracy')
        axes[1, 0].legend()
        axes[1, 0].grid(True)
        
        # Learning Rate (jika ada)
        if 'lr' in history:
            axes[1, 1].plot(history['lr'])
            axes[1, 1].set_title('Learning Rate')
            axes[1, 1].set_xlabel('Epoch')
            axes[1, 1].set_ylabel('LR')
            axes[1, 1].set_yscale('log')
            axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"\nTraining history plot saved to {save_path}")
    
    def evaluate(self):
        """Evaluate model on test set"""
        print("\n" + "="*60)
        print("EVALUATING ON TEST SET")
        print("="*60)
        
        test_results = self.model.evaluate(self.test_ds, verbose=1)
        
        print("\nTest Results:")
        for metric_name, value in zip(self.model.metrics_names, test_results):
            print(f"{metric_name}: {value:.4f}")
        
        return test_results
    
    def predict_with_uncertainty(self, dataset, n_iter=50):
        """Predict dengan uncertainty estimation"""
        print(f"\nPredicting with uncertainty (n_iter={n_iter})...")
        
        all_mean_preds = []
        all_uncertainties = []
        all_true_labels = []
        
        for images, labels in dataset:
            mean_pred, uncertainty = self.bayesian_cnn.predict_with_uncertainty(
                self.model, images, n_iter=n_iter
            )
            
            all_mean_preds.append(mean_pred.numpy())
            all_uncertainties.append(uncertainty.numpy())
            all_true_labels.append(labels.numpy())
        
        mean_preds = np.concatenate(all_mean_preds, axis=0)
        uncertainties = np.concatenate(all_uncertainties, axis=0)
        true_labels = np.concatenate(all_true_labels, axis=0)
        
        predicted_labels = np.argmax(mean_preds, axis=1)
        
        return mean_preds, uncertainties, predicted_labels, true_labels
    
    def save_results(self, output_dir='storage/training'):
        """Save training results"""
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        # Save config
        with open(output_dir / 'config.json', 'w') as f:
            json.dump(self.config, f, indent=4, default=str)
        
        # Save history
        if self.history:
            history_df = pd.DataFrame(self.history.history)
            history_df.to_csv(output_dir / 'training_history.csv', index=False)
        
        print(f"\nResults saved to {output_dir}")

def main():
    # Set random seeds
    tf.random.set_seed(42)
    np.random.seed(42)
    
    # Configuration
    config = {
        'dataset_path': DATASET_PATH,
        'train_path': TRAIN_PATH,
        'val_path': VAL_PATH,
        'test_path': TEST_PATH,
        'train_csv': DATASET_PATH / 'train.csv',
        'val_csv': DATASET_PATH / 'validation.csv',
        'test_csv': DATASET_PATH / 'test.csv',
        'img_size': IMG_SIZE,
        'batch_size': BATCH_SIZE,
        'epochs': EPOCHS,
        'learning_rate': LEARNING_RATE,
        'num_classes': NUM_CLASSES,
        'timestamp': datetime.now().strftime('%Y%m%d_%H%M%S')
    }
    
    # Create pipeline
    pipeline = TrainingPipeline(config)
    
    # Load data
    train_ds, val_ds, test_ds, class_weights = pipeline.load_data()
    
    # Build model
    model = pipeline.build_and_compile_model()
    
    # Train
    history = pipeline.train()
    
    # Plot history
    pipeline.plot_training_history()
    
    # Evaluate
    test_results = pipeline.evaluate()
    
    # Predict dengan uncertainty
    mean_preds, uncertainties, pred_labels, true_labels = \
        pipeline.predict_with_uncertainty(test_ds, n_iter=50)
    
    # Save results
    pipeline.save_results()
    
    print("\n" + "="*60)
    print("TRAINING COMPLETED!")
    print("="*60)
    
    return pipeline, mean_preds, uncertainties, pred_labels, true_labels

if __name__ == "__main__":
    pipeline, mean_preds, uncertainties, pred_labels, true_labels = main()