import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import tensorflow as tf
from PIL import Image, ImageOps, ImageTk, ImageDraw
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MNISTApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MNIST Handwritten Digit Recognition Studio")
        self.root.geometry("1100x750")
        self.root.configure(bg="#f4f5f7")

        self.model = None
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
        self.history = None

        self._build_ui()

    def _build_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#1e293b", height=60)
        header.pack(fill=tk.X)
        title_lbl = tk.Label(
            header,
            text="MNIST Neural Network Studio",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#1e293b",
            pady=12
        )
        title_lbl.pack()

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Tab 1: Train & Metrics
        self.tab_train = tk.Frame(self.notebook, bg="#ffffff")
        self.notebook.add(self.tab_train, text=" 1. Train & Evaluation ")

        # Tab 2: Upload & Recognize
        self.tab_predict = tk.Frame(self.notebook, bg="#ffffff")
        self.notebook.add(self.tab_predict, text=" 2. Upload & Recognize ")

        self._setup_train_tab()
        self._setup_predict_tab()

    # -------------------------------------------------------------
    # TAB 1: MODEL TRAINING & METRICS
    # -------------------------------------------------------------
    def _setup_train_tab(self):
        control_frame = tk.Frame(self.tab_train, bg="#ffffff", pady=10)
        control_frame.pack(fill=tk.X, padx=15)

        self.train_btn = tk.Button(
            control_frame,
            text="Train Model (5 Epochs)",
            command=self.start_training_thread,
            bg="#2563eb",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            padx=15,
            pady=6,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.train_btn.pack(side=tk.LEFT)

        self.status_lbl = tk.Label(
            control_frame,
            text="Status: Model not trained yet.",
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#4b5563",
            padx=15
        )
        self.status_lbl.pack(side=tk.LEFT)

        # Matplotlib Area
        self.fig, (self.ax_acc, self.ax_loss) = plt.subplots(1, 2, figsize=(9, 4), dpi=90)
        self.fig.tight_layout(pad=3.0)
        self.ax_acc.set_title("Model Accuracy")
        self.ax_loss.set_title("Model Loss")

        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=self.tab_train)
        self.canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

    def start_training_thread(self):
        self.train_btn.config(state=tk.DISABLED)
        self.status_lbl.config(text="Status: Loading dataset & training (Please wait)...", fg="#d97706")
        thread = threading.Thread(target=self.train_model, daemon=True)
        thread.start()

    def train_model(self):
        # 1. Load Data
        mnist = tf.keras.datasets.mnist
        (self.x_train, self.y_train), (self.x_test, self.y_test) = mnist.load_data()
        self.x_train, self.x_test = self.x_train / 255.0, self.x_test / 255.0

        # 2. Build Model
        self.model = tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(10, activation='softmax')
        ])

        self.model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )

        # 3. Fit
        self.history = self.model.fit(self.x_train, self.y_train, epochs=5, validation_split=0.2, verbose=0)
        _, test_acc = self.model.evaluate(self.x_test, self.y_test, verbose=0)

        # Update GUI on main thread
        self.root.after(0, lambda: self.on_training_complete(test_acc))

    def on_training_complete(self, test_acc):
        self.train_btn.config(state=tk.NORMAL)
        self.status_lbl.config(
            text=f"Status: Training Complete! Test Accuracy: {test_acc * 100:.2f}%",
            fg="#15803d"
        )

        # Plot metrics
        self.ax_acc.clear()
        self.ax_loss.clear()

        self.ax_acc.plot(self.history.history['accuracy'], label='Train Acc', color='#2563eb')
        self.ax_acc.plot(self.history.history['val_accuracy'], label='Val Acc', color='#059669')
        self.ax_acc.set_title("Accuracy over Epochs")
        self.ax_acc.set_xlabel("Epoch")
        self.ax_acc.set_ylabel("Accuracy")
        self.ax_acc.legend()

        self.ax_loss.plot(self.history.history['loss'], label='Train Loss', color='#dc2626')
        self.ax_loss.plot(self.history.history['val_loss'], label='Val Loss', color='#ea580c')
        self.ax_loss.set_title("Loss over Epochs")
        self.ax_loss.set_xlabel("Epoch")
        self.ax_loss.set_ylabel("Loss")
        self.ax_loss.legend()

        self.canvas_plot.draw()
        messagebox.showinfo("Success", f"Model trained successfully!\nTest Accuracy: {test_acc * 100:.2f}%")

    # -------------------------------------------------------------
    # TAB 2: UPLOAD IMAGE & RECOGNIZE
    # -------------------------------------------------------------
    def _setup_predict_tab(self):
        container = tk.Frame(self.tab_predict, bg="#ffffff", padx=20, pady=20)
        container.pack(fill=tk.BOTH, expand=True)

        # Left Column: Image / Drawing preview
        left_col = tk.Frame(container, bg="#f8fafc", relief=tk.RIDGE, bd=1, padx=15, pady=15)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        lbl_instructions = tk.Label(
            left_col,
            text="Upload an image (digit on white/light background):",
            font=("Segoe UI", 11, "bold"),
            bg="#f8fafc"
        )
        lbl_instructions.pack(anchor="w", pady=(0, 10))

        btn_bar = tk.Frame(left_col, bg="#f8fafc")
        btn_bar.pack(anchor="w", pady=(0, 15))

        upload_btn = tk.Button(
            btn_bar,
            text="Browse Image File...",
            command=self.upload_image,
            bg="#0284c7",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=6,
            relief=tk.FLAT,
            cursor="hand2"
        )
        upload_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Canvas for showing original image
        self.img_display = tk.Label(left_col, text="No image selected", bg="#e2e8f0", width=35, height=15)
        self.img_display.pack(fill=tk.BOTH, expand=True)

        # Right Column: Prediction Results
        right_col = tk.Frame(container, bg="#ffffff", padx=15, pady=15)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        res_header = tk.Label(right_col, text="Prediction Results", font=("Segoe UI", 13, "bold"), bg="#ffffff")
        res_header.pack(anchor="w")

        self.digit_display = tk.Label(
            right_col,
            text="-",
            font=("Segoe UI", 56, "bold"),
            fg="#2563eb",
            bg="#ffffff"
        )
        self.digit_display.pack(pady=10)

        self.confidence_display = tk.Label(
            right_col,
            text="Confidence: --",
            font=("Segoe UI", 12),
            bg="#ffffff",
            fg="#4b5563"
        )
        self.confidence_display.pack()

        # Probabilities breakdown
        self.fig_prob, self.ax_prob = plt.subplots(figsize=(4.5, 3), dpi=90)
        self.canvas_prob = FigureCanvasTkAgg(self.fig_prob, master=right_col)
        self.canvas_prob.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=10)
        self._draw_empty_probabilities()

    def _draw_empty_probabilities(self):
        self.ax_prob.clear()
        self.ax_prob.bar(range(10), [0]*10, color='#93c5fd')
        self.ax_prob.set_xticks(range(10))
        self.ax_prob.set_ylim(0, 100)
        self.ax_prob.set_ylabel("Confidence (%)")
        self.ax_prob.set_title("Probability Distribution (0-9)")
        self.fig_prob.tight_layout()
        self.canvas_prob.draw()

    def upload_image(self):
        if self.model is None:
            messagebox.showwarning("Model Not Ready", "Please train the model in Tab 1 first!")
            self.notebook.select(self.tab_train)
            return

        file_path = filedialog.askopenfilename(
            title="Select Handwritten Digit Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.webp")]
        )
        if not file_path:
            return

        # Open and display original image in preview
        raw_img = Image.open(file_path)
        preview_img = raw_img.copy()
        preview_img.thumbnail((260, 260))
        tk_img = ImageTk.PhotoImage(preview_img)
        self.img_display.config(image=tk_img, text="")
        self.img_display.image = tk_img

        # Preprocess to 28x28 grayscale
        processed_img = raw_img.convert('L')
        # Invert if the image background is light (mean brightness > 127)
        if np.mean(np.array(processed_img)) > 127:
            processed_img = ImageOps.invert(processed_img)

        processed_img = processed_img.resize((28, 28))
        img_array = np.array(processed_img) / 255.0
        img_array = img_array.reshape(1, 28, 28)

        # Run inference
        probabilities = self.model.predict(img_array)[0]
        predicted_digit = int(np.argmax(probabilities))
        top_confidence = probabilities[predicted_digit] * 100

        # Update Results UI
        self.digit_display.config(text=str(predicted_digit))
        self.confidence_display.config(text=f"Confidence: {top_confidence:.2f}%")

        # Update Probabilities Bar Chart
        self.ax_prob.clear()
        bars = self.ax_prob.bar(range(10), probabilities * 100, color='#93c5fd')
        bars[predicted_digit].set_color('#2563eb')
        self.ax_prob.set_xticks(range(10))
        self.ax_prob.set_ylim(0, 100)
        self.ax_prob.set_ylabel("Confidence (%)")
        self.ax_prob.set_title("Probability Distribution (0-9)")
        self.fig_prob.tight_layout()
        self.canvas_prob.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = MNISTApp(root)
    root.mainloop()