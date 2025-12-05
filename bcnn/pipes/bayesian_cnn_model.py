import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow.keras import layers, models
import numpy as np
import ssl
import certifi

# Fix SSL certificate verification untuk macOS
ssl._create_default_https_context = ssl._create_unverified_context

tfd = tfp.distributions
tfpl = tfp.layers

class BayesianCNN:
    """Bayesian CNN menggunakan Monte Carlo Dropout"""
    
    def __init__(self, input_shape=(224, 224, 3), num_classes=5, 
                 dropout_rate=0.3, backbone='efficientnet'):
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.dropout_rate = dropout_rate
        self.backbone = backbone
    
    def build_model(self):
        """Build Bayesian CNN model"""
        
        inputs = layers.Input(shape=self.input_shape)
        
        # Feature extractor (backbone)
        if self.backbone == 'efficientnet':
            backbone = tf.keras.applications.EfficientNetB3(
                include_top=False,
                weights='imagenet',
                input_tensor=inputs,
                pooling='avg'
            )
        elif self.backbone == 'resnet':
            backbone = tf.keras.applications.ResNet50V2(
                include_top=False,
                weights='imagenet',
                input_tensor=inputs,
                pooling='avg'
            )
        else:
            raise ValueError(f"Unknown backbone: {self.backbone}")
        
        # Unfreeze beberapa layer terakhir untuk fine-tuning
        for layer in backbone.layers[:-30]:
            layer.trainable = False
        
        x = backbone.output
        
        # Bayesian layers dengan MC Dropout
        x = layers.Dense(512, activation='relu')(x)
        x = layers.Dropout(self.dropout_rate)(x, training=True)  # Always active
        
        x = layers.Dense(256, activation='relu')(x)
        x = layers.Dropout(self.dropout_rate)(x, training=True)  # Always active
        
        x = layers.Dense(128, activation='relu')(x)
        x = layers.Dropout(self.dropout_rate)(x, training=True)  # Always active
        
        # Output layer
        outputs = layers.Dense(self.num_classes, activation='softmax')(x)
        
        model = models.Model(inputs=inputs, outputs=outputs, name='Bayesian_CNN')
        
        return model
    
    def predict_with_uncertainty(self, model, x, n_iter=50):
        """
        Prediksi dengan uncertainty estimation menggunakan MC Dropout
        
        Args:
            model: Trained model
            x: Input data
            n_iter: Jumlah forward passes (sampling)
        
        Returns:
            mean_predictions: Mean predictions
            uncertainty: Uncertainty (standard deviation)
        """
        predictions = []
        
        for _ in range(n_iter):
            pred = model(x, training=True)  # Dropout active
            predictions.append(pred)
        
        predictions = tf.stack(predictions)
        
        # Mean prediction
        mean_predictions = tf.reduce_mean(predictions, axis=0)
        
        # Uncertainty (variance atau std)
        uncertainty = tf.math.reduce_std(predictions, axis=0)
        
        return mean_predictions, uncertainty

class AdvancedBayesianCNN:
    """Advanced Bayesian CNN menggunakan Variational Inference"""
    
    def __init__(self, input_shape=(224, 224, 3), num_classes=5):
        self.input_shape = input_shape
        self.num_classes = num_classes
    
    def prior(self, kernel_size, bias_size, dtype=None):
        """Prior distribution untuk weights"""
        n = kernel_size + bias_size
        prior_model = tf.keras.Sequential([
            tfpl.DistributionLambda(
                lambda t: tfd.MultivariateNormalDiag(
                    loc=tf.zeros(n), 
                    scale_diag=tf.ones(n)
                )
            )
        ])
        return prior_model
    
    def posterior(self, kernel_size, bias_size, dtype=None):
        """Posterior distribution untuk weights"""
        n = kernel_size + bias_size
        posterior_model = tf.keras.Sequential([
            tfpl.VariableLayer(
                tfpl.MultivariateNormalTriL.params_size(n), 
                dtype=dtype
            ),
            tfpl.MultivariateNormalTriL(n)
        ])
        return posterior_model
    
    def build_model(self):
        """Build Bayesian CNN dengan Variational Inference"""
        
        inputs = layers.Input(shape=self.input_shape)
        
        # Backbone
        backbone = tf.keras.applications.EfficientNetB0(
            include_top=False,
            weights='imagenet',
            input_tensor=inputs,
            pooling='avg'
        )
        
        for layer in backbone.layers[:-20]:
            layer.trainable = False
        
        x = backbone.output
        
        # Bayesian Dense layers
        x = tfpl.DenseVariational(
            units=256,
            make_prior_fn=self.prior,
            make_posterior_fn=self.posterior,
            kl_weight=1/2930,  # 1/num_training_samples
            activation='relu'
        )(x)
        
        x = tfpl.DenseVariational(
            units=128,
            make_prior_fn=self.prior,
            make_posterior_fn=self.posterior,
            kl_weight=1/2930,
            activation='relu'
        )(x)
        
        # Output layer
        outputs = tfpl.DenseVariational(
            units=self.num_classes,
            make_prior_fn=self.prior,
            make_posterior_fn=self.posterior,
            kl_weight=1/2930,
            activation='softmax'
        )(x)
        
        model = models.Model(inputs=inputs, outputs=outputs, 
                            name='Advanced_Bayesian_CNN')
        
        return model

def create_callbacks(model_name='bayesian_cnn'):
    """Create training callbacks"""
    
    callbacks = [
        # Model checkpoint
        tf.keras.callbacks.ModelCheckpoint(
            f'models/{model_name}_best.keras',
            monitor='val_accuracy',
            save_best_only=True,
            mode='max',
            verbose=1
        ),
        
        # Early stopping
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=15,
            restore_best_weights=True,
            verbose=1
        ),
        
        # Reduce learning rate
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        ),
        
        # TensorBoard
        tf.keras.callbacks.TensorBoard(
            log_dir=f'logs/{model_name}',
            histogram_freq=1
        ),
        
        # CSV Logger
        tf.keras.callbacks.CSVLogger(
            f'logs/{model_name}_training.csv'
        )
    ]
    
    return callbacks

# Test model building
if __name__ == "__main__":
    import os
    os.makedirs('models', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    print("="*60)
    print("Testing Bayesian CNN Model")
    print("="*60)
    
    # Build model dengan MC Dropout
    print("\n1. Building MC Dropout Bayesian CNN...")
    bayesian_cnn = BayesianCNN(
        input_shape=(224, 224, 3),
        num_classes=5,
        dropout_rate=0.3,
        backbone='efficientnet'
    )
    
    model = bayesian_cnn.build_model()
    print(f"Total parameters: {model.count_params():,}")
    print(f"Trainable parameters: {sum([tf.size(w).numpy() for w in model.trainable_weights]):,}")
    
    model.summary()
    
    # Test prediction dengan uncertainty
    print("\n2. Testing uncertainty prediction...")
    dummy_input = tf.random.normal((1, 224, 224, 3))
    mean_pred, uncertainty = bayesian_cnn.predict_with_uncertainty(
        model, dummy_input, n_iter=10
    )
    
    print(f"Mean prediction shape: {mean_pred.shape}")
    print(f"Uncertainty shape: {uncertainty.shape}")
    print(f"Mean prediction: {mean_pred.numpy()[0]}")
    print(f"Uncertainty: {uncertainty.numpy()[0]}")
    
    print("\n" + "="*60)
    print("Model testing completed!")
    print("="*60)