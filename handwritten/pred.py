import tensorflow as tf
from tensorflow.keras import models
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps # ImageOps helps with inverting colors if needed

# --- CONFIGURATION ---
# Assumes you have already trained and saved your model.
# If your model is in memory as `base_model`, use that.
# Otherwise, load it here:
# base_model = models.load_model('my_mnist_model.h5')

# Define the names of your 5 handwritten files
image_files = ['digit_0.png', 'digit_1.png', 'digit_2.png', 'digit_3.png', 'digit_4.png']


def predict_custom_image(model, img_path):
    """
    Loads, preprocesses, and predicts a single custom handwritten image.
    """
    try:
        # 1. Load the image and convert to grayscale ('L')
        # This standardizes different input formats (RGBA, RGB, CMYK).
        img = Image.open(img_path).convert('L')

        # === CRITICAL PREPROCESSING ===
        # Standard MNIST is WHITE digit on BLACK background.
        # Check if the drawing needs to be inverted (black ink on white paper).
        # We check the pixel value of the center (14,14). If it's light, we invert.
        # This is a robust way to handle any input background color.
        img_array_check = np.array(img)
        if img_array_check[14, 14] > 128: # If the center is relatively bright
            img = ImageOps.invert(img)
            # print(f"Note: Inverting colors for '{img_path}' (black on white detected).")

        # 2. Resize to exactly 28x28 pixels
        img = img.resize((28, 28))

        # 3. Convert to NumPy array
        img_array = np.array(img)

        # 4. Normalize pixel values from 0-255 to 0.0-1.0
        # (Must match the training input)
        img_array = img_array / 255.0

        # 5. Reshape for the model
        # Our model expects (batch_size, 28, 28). We have (28, 28).
        # We add the batch dimension of 1.
        img_array = np.expand_dims(img_array, axis=0)

        # === INFERENCE ===
        # Make the prediction
        predictions = model.predict(img_array, verbose=0)
        
        # Determine the class (0-9) with the highest probability score
        predicted_class = np.argmax(predictions)
        confidence_score = predictions[0][predicted_class]

        return predicted_class, confidence_score, np.squeeze(img_array)

    except FileNotFoundError:
        print(f"Error: Could not find the file '{img_path}'. Ensure it's in the correct directory.")
        return None, None, None
    except Exception as e:
        print(f"An unexpected error occurred processing '{img_path}': {e}")
        return None, None, None


# --- Run the experiment on the list of files ---
plt.figure(figsize=(15, 5))

# Use the base model trained in the previous step
current_model = base_model # Or use exp_model if you prefer

for i, file_name in enumerate(image_files):
    predicted, confidence, formatted_img = predict_custom_image(current_model, file_name)
    
    # If the file was successfully processed
    if predicted is not None:
        plt.subplot(1, 5, i + 1)
        
        # Display the *preprocessed* image (what the model actually sees)
        plt.imshow(formatted_img, cmap='gray')
        plt.title(f"File: {file_name}\nPred: {predicted} ({confidence:.1%})")
        plt.axis('off')

plt.suptitle("Model Predictions on Custom Handwritten Images", fontsize=16)
plt.show()