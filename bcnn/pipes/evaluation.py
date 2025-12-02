import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix, classification_report, 
    accuracy_score, cohen_kappa_score,
    roc_curve, auc, roc_auc_score
)
from sklearn.preprocessing import label_binarize
import pandas as pd

CATEGORIES = ['No DR', 'Mild DR', 'Moderate DR', 'Severe DR', 'Proliferative DR']

class ModelEvaluator:
    def __init__(self, true_labels, predicted_labels, 
                 predicted_probs, uncertainties):
        self.true_labels = true_labels
        self.predicted_labels = predicted_labels
        self.predicted_probs = predicted_probs
        self.uncertainties = uncertainties
        self.num_classes = len(CATEGORIES)
    
    def plot_confusion_matrix(self, save_path='storage/evaluation/confusion_matrix.png'):
        """Plot confusion matrix"""
        cm = confusion_matrix(self.true_labels, self.predicted_labels)
        
        # Normalized confusion matrix
        cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        # Raw counts
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=CATEGORIES, yticklabels=CATEGORIES,
                   ax=axes[0])
        axes[0].set_title('Confusion Matrix (Counts)')
        axes[0].set_ylabel('True Label')
        axes[0].set_xlabel('Predicted Label')
        
        # Normalized
        sns.heatmap(cm_normalized, annot=True, fmt='.2f', cmap='Blues',
                   xticklabels=CATEGORIES, yticklabels=CATEGORIES,
                   ax=axes[1])
        axes[1].set_title('Confusion Matrix (Normalized)')
        axes[1].set_ylabel('True Label')
        axes[1].set_xlabel('Predicted Label')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return cm
    
    def print_classification_report(self):
        """Print detailed classification report"""
        print("\n" + "="*60)
        print("CLASSIFICATION REPORT")
        print("="*60)
        
        report = classification_report(
            self.true_labels, 
            self.predicted_labels,
            target_names=CATEGORIES,
            digits=4
        )
        print(report)
        
        # Additional metrics
        accuracy = accuracy_score(self.true_labels, self.predicted_labels)
        kappa = cohen_kappa_score(self.true_labels, self.predicted_labels)
        
        print(f"\nOverall Accuracy: {accuracy:.4f}")
        print(f"Cohen's Kappa: {kappa:.4f}")
        
        return report
    
    def plot_roc_curves(self, save_path='storage/evaluation/roc_curves.png'):
        """Plot ROC curves untuk setiap class"""
        # Binarize labels
        y_true_bin = label_binarize(self.true_labels, 
                                     classes=list(range(self.num_classes)))
        
        # Compute ROC curve dan AUC untuk setiap class
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        
        for i in range(self.num_classes):
            fpr[i], tpr[i], _ = roc_curve(y_true_bin[:, i], 
                                          self.predicted_probs[:, i])
            roc_auc[i] = auc(fpr[i], tpr[i])
        
        # Compute micro-average ROC curve
        fpr["micro"], tpr["micro"], _ = roc_curve(
            y_true_bin.ravel(), 
            self.predicted_probs.ravel()
        )
        roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
        
        # Plot
        plt.figure(figsize=(10, 8))
        
        # Plot ROC untuk setiap class
        colors = ['blue', 'red', 'green', 'orange', 'purple']
        for i, color in enumerate(colors):
            plt.plot(fpr[i], tpr[i], color=color, lw=2,
                    label=f'{CATEGORIES[i]} (AUC = {roc_auc[i]:.3f})')
        
        # Plot micro-average
        plt.plot(fpr["micro"], tpr["micro"],
                color='deeppink', linestyle='--', lw=2,
                label=f'Micro-average (AUC = {roc_auc["micro"]:.3f})')
        
        plt.plot([0, 1], [0, 1], 'k--', lw=1)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curves - Multi-class Classification')
        plt.legend(loc="lower right")
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        return roc_auc
    
    def analyze_uncertainty(self, save_path='storage/evaluation/uncertainty_analysis.png'):
        """Analyze prediction uncertainty"""
        
        # Mean uncertainty per class
        mean_uncertainty = np.mean(self.uncertainties, axis=1)
        
        # Separate correct vs incorrect predictions
        correct_mask = self.true_labels == self.predicted_labels
        incorrect_mask = ~correct_mask
        
        correct_uncertainty = mean_uncertainty[correct_mask]
        incorrect_uncertainty = mean_uncertainty[incorrect_mask]
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Uncertainty distribution (correct vs incorrect)
        axes[0, 0].hist(correct_uncertainty, bins=50, alpha=0.6, 
                       label='Correct', color='green')
        axes[0, 0].hist(incorrect_uncertainty, bins=50, alpha=0.6, 
                       label='Incorrect', color='red')
        axes[0, 0].set_xlabel('Mean Uncertainty')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].set_title('Uncertainty Distribution')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Uncertainty per true class
        uncertainty_by_class = []
        for i in range(self.num_classes):
            mask = self.true_labels == i
            uncertainty_by_class.append(mean_uncertainty[mask])
        
        axes[0, 1].boxplot(uncertainty_by_class, labels=CATEGORIES)
        axes[0, 1].set_xlabel('True Class')
        axes[0, 1].set_ylabel('Mean Uncertainty')
        axes[0, 1].set_title('Uncertainty by True Class')
        axes[0, 1].tick_params(axis='x', rotation=45)
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Confidence vs Accuracy
        confidences = np.max(self.predicted_probs, axis=1)
        
        # Bin predictions by confidence
        bins = np.linspace(0, 1, 11)
        bin_indices = np.digitize(confidences, bins)
        
        bin_accuracy = []
        bin_confidence = []
        
        for i in range(1, len(bins)):
            mask = bin_indices == i
            if mask.sum() > 0:
                bin_acc = (self.true_labels[mask] == 
                          self.predicted_labels[mask]).mean()
                bin_conf = confidences[mask].mean()
                bin_accuracy.append(bin_acc)
                bin_confidence.append(bin_conf)
        
        axes[1, 0].plot(bin_confidence, bin_accuracy, 'o-', linewidth=2)
        axes[1, 0].plot([0, 1], [0, 1], 'k--', label='Perfect Calibration')
        axes[1, 0].set_xlabel('Confidence')
        axes[1, 0].set_ylabel('Accuracy')
        axes[1, 0].set_title('Reliability Diagram')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. Uncertainty vs Confidence
        axes[1, 1].scatter(confidences, mean_uncertainty, alpha=0.5,
                          c=correct_mask, cmap='RdYlGn')
        axes[1, 1].set_xlabel('Confidence (Max Probability)')
        axes[1, 1].set_ylabel('Mean Uncertainty')
        axes[1, 1].set_title('Uncertainty vs Confidence')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        # Print statistics
        print("\n" + "="*60)
        print("UNCERTAINTY ANALYSIS")
        print("="*60)
        print(f"Mean uncertainty (correct): {correct_uncertainty.mean():.4f}")
        print(f"Mean uncertainty (incorrect): {incorrect_uncertainty.mean():.4f}")
        print(f"Std uncertainty (correct): {correct_uncertainty.std():.4f}")
        print(f"Std uncertainty (incorrect): {incorrect_uncertainty.std():.4f}")
    
    def identify_high_uncertainty_samples(self, threshold_percentile=90):
        """Identify samples dengan uncertainty tinggi"""
        mean_uncertainty = np.mean(self.uncertainties, axis=1)
        threshold = np.percentile(mean_uncertainty, threshold_percentile)
        
        high_uncertainty_indices = np.where(mean_uncertainty > threshold)[0]
        
        print(f"\n" + "="*60)
        print(f"HIGH UNCERTAINTY SAMPLES (>{threshold_percentile}th percentile)")
        print("="*60)
        print(f"Threshold: {threshold:.4f}")
        print(f"Number of samples: {len(high_uncertainty_indices)}")
        
        results = []
        for idx in high_uncertainty_indices:
            results.append({
                'index': idx,
                'true_label': CATEGORIES[self.true_labels[idx]],
                'predicted_label': CATEGORIES[self.predicted_labels[idx]],
                'uncertainty': mean_uncertainty[idx],
                'confidence': np.max(self.predicted_probs[idx])
            })
        
        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values('uncertainty', ascending=False)
        
        print("\nTop 10 highest uncertainty samples:")
        print(results_df.head(10).to_string(index=False))
        
        return results_df
    
    def generate_full_report(self, output_dir='storage/evaluation'):
        """Generate complete evaluation report"""
        from pathlib import Path
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)
        
        print("\n" + "="*60)
        print("GENERATING FULL EVALUATION REPORT")
        print("="*60)
        
        # 1. Confusion Matrix
        cm = self.plot_confusion_matrix(
            save_path=output_dir / 'confusion_matrix.png'
        )
        
        # 2. Classification Report
        report = self.print_classification_report()
        
        # 3. ROC Curves
        roc_auc = self.plot_roc_curves(
            save_path=output_dir / 'roc_curves.png'
        )
        
        # 4. Uncertainty Analysis
        self.analyze_uncertainty(
            save_path=output_dir / 'uncertainty_analysis.png'
        )
        
        # 5. High Uncertainty Samples
        high_unc_df = self.identify_high_uncertainty_samples()
        high_unc_df.to_csv(
            output_dir / 'high_uncertainty_samples.csv', 
            index=False
        )
        
        print(f"\nAll evaluation results saved to {output_dir}/")

# Usage example
if __name__ == "__main__":
    # Contoh penggunaan dengan dummy data
    np.random.seed(42)
    
    n_samples = 366
    n_classes = 5
    
    # Simulate predictions
    true_labels = np.random.randint(0, n_classes, n_samples)
    predicted_probs = np.random.dirichlet(np.ones(n_classes), n_samples)
    predicted_labels = np.argmax(predicted_probs, axis=1)
    uncertainties = np.random.rand(n_samples, n_classes) * 0.3
    
    # Create evaluator
    evaluator = ModelEvaluator(
        true_labels, predicted_labels, 
        predicted_probs, uncertainties
    )
    
    # Generate full report
    evaluator.generate_full_report()