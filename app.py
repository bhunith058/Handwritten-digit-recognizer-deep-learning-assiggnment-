import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image, ImageOps, ImageDraw
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="MNIST Digit Classifier",
    page_icon="🔢",
    layout="wide"
)

st.title("🔢 MNIST Handwritten Digit Classifier")
st.write("TensorFlow/Keras neural network for classifying handwritten digits from 0–9.")

@st.cache_resource
def load_model():
    model = keras.Sequential([
        keras.layers.Input(shape=(28, 28)),
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation="relu"),
        keras.layers.Dense(64, activation="relu"),
        keras.layers.Dense(10, activation="softmax")
    ])
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model

@st.cache_data
def load_mnist():
    return keras.datasets.mnist.load_data()

(x_train, y_train), (x_test, y_test) = load_mnist()

x_train_norm = x_train.astype("float32") / 255.0
x_test_norm = x_test.astype("float32") / 255.0

# Train only when the user asks, and cache the result.
@st.cache_resource
def train_model():
    model = load_model()
    history = model.fit(
        x_train_norm, y_train,
        validation_split=0.1,
        epochs=10,
        batch_size=128,
        verbose=0
    )
    return model, history

st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Choose section",
    ["🏠 Overview", "🖼️ Dataset Samples", "🧠 Train & Evaluate",
     "✍️ Test 5 Images", "🧪 Dropout Experiment"]
)

if page == "🏠 Overview":
    st.subheader("Project Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Training Images", "60,000")
    c2.metric("Test Images", "10,000")
    c3.metric("Image Size", "28 × 28")

    st.markdown("""
    ### Model Architecture
    1. Flatten: 28×28 → 784
    2. Dense: 128 neurons, ReLU
    3. Dense: 64 neurons, ReLU
    4. Dense: 10 neurons, Softmax

    ### Experiment
    A second model adds **Dropout(0.20)** after both hidden layers.
    """)

    st.info("Use the sidebar to explore the dataset, train the model, test five images, and compare the Dropout experiment.")

elif page == "🖼️ Dataset Samples":
    st.subheader("MNIST Sample Images")
    n = st.slider("Number of images", 5, 20, 10)
    cols = st.columns(5)
    for i in range(n):
        with cols[i % 5]:
            st.image(x_train[i], caption=f"Label: {y_train[i]}", width=120)

    st.write("### Dataset Information")
    st.write("Training shape:", x_train.shape)
    st.write("Test shape:", x_test.shape)
    st.write("Pixel range:", int(x_train.min()), "to", int(x_train.max()))
    st.write("Classes:", np.unique(y_train))

elif page == "🧠 Train & Evaluate":
    st.subheader("Train and Evaluate Baseline Model")

    if st.button("🚀 Train Model", type="primary"):
        with st.spinner("Training for 10 epochs..."):
            model, history = train_model()

        test_loss, test_accuracy = model.evaluate(x_test_norm, y_test, verbose=0)

        c1, c2 = st.columns(2)
        c1.metric("Test Accuracy", f"{test_accuracy*100:.2f}%")
        c2.metric("Test Loss", f"{test_loss:.4f}")

        hist = history.history

        fig1, ax1 = plt.subplots()
        ax1.plot(hist["accuracy"], label="Training Accuracy")
        ax1.plot(hist["val_accuracy"], label="Validation Accuracy")
        ax1.set_xlabel("Epoch")
        ax1.set_ylabel("Accuracy")
        ax1.set_title("Training vs Validation Accuracy")
        ax1.legend()
        ax1.grid(True)
        st.pyplot(fig1)

        fig2, ax2 = plt.subplots()
        ax2.plot(hist["loss"], label="Training Loss")
        ax2.plot(hist["val_loss"], label="Validation Loss")
        ax2.set_xlabel("Epoch")
        ax2.set_ylabel("Loss")
        ax2.set_title("Training vs Validation Loss")
        ax2.legend()
        ax2.grid(True)
        st.pyplot(fig2)
    else:
        st.info("Click **Train Model** to train the neural network.")

elif page == "✍️ Test 5 Images":
    st.subheader("Actual vs Predicted — 5 Handwritten Images")

    model, history = train_model()

    indices = [0, 1, 2, 3, 4]
    images = x_test_norm[indices]
    actual = y_test[indices]
    probs = model.predict(images, verbose=0)
    predicted = np.argmax(probs, axis=1)

    cols = st.columns(5)
    for i, idx in enumerate(indices):
        with cols[i]:
            st.image(x_test[idx], caption=f"Actual: {actual[i]}", width=130)
            st.write(f"**Predicted: {predicted[i]}**")
            if actual[i] == predicted[i]:
                st.success("Correct")
            else:
                st.error("Wrong")
            st.write(f"Confidence: {probs[i][predicted[i]]*100:.2f}%")

    st.markdown("### Comparison Table")
    import pandas as pd
    df = pd.DataFrame({
        "Image": [1,2,3,4,5],
        "Actual Label": actual,
        "Predicted Label": predicted,
        "Correct": actual == predicted
    })
    st.dataframe(df, use_container_width=True)

elif page == "🧪 Dropout Experiment":
    st.subheader("Experiment: Adding Dropout")

    @st.cache_resource
    def train_dropout_model():
        model = keras.Sequential([
            keras.layers.Input(shape=(28, 28)),
            keras.layers.Flatten(),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dropout(0.20),
            keras.layers.Dense(64, activation="relu"),
            keras.layers.Dropout(0.20),
            keras.layers.Dense(10, activation="softmax")
        ])
        model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"]
        )
        history = model.fit(
            x_train_norm, y_train,
            validation_split=0.1,
            epochs=10,
            batch_size=128,
            verbose=0
        )
        return model, history

    if st.button("🧪 Run Dropout Experiment", type="primary"):
        with st.spinner("Training Dropout model..."):
            baseline, base_history = train_model()
            dropout, dropout_history = train_dropout_model()

        base_loss, base_acc = baseline.evaluate(x_test_norm, y_test, verbose=0)
        drop_loss, drop_acc = dropout.evaluate(x_test_norm, y_test, verbose=0)

        c1, c2 = st.columns(2)
        c1.metric("Baseline Accuracy", f"{base_acc*100:.2f}%")
        c2.metric("Dropout Accuracy", f"{drop_acc*100:.2f}%")

        import pandas as pd
        comparison = pd.DataFrame({
            "Model": ["Baseline", "With Dropout"],
            "Test Accuracy": [base_acc, drop_acc],
            "Test Loss": [base_loss, drop_loss]
        })
        st.dataframe(comparison, use_container_width=True)

        fig, ax = plt.subplots()
        ax.bar(comparison["Model"], comparison["Test Accuracy"])
        ax.set_ylim(0, 1)
        ax.set_ylabel("Test Accuracy")
        ax.set_title("Baseline vs Dropout")
        st.pyplot(fig)

        st.write("The exact result can vary slightly between runs and TensorFlow versions.")
