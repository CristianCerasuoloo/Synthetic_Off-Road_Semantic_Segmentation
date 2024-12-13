import sys
import cv2
import numpy as np
import torch
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from model import TwinLite as net
from inference_utils import Run_rgb

class ImageProcessingGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Image Processing GUI')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2C3E50;
            }
            QLabel {
                color: #ECF0F1;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                padding: 5px 10px;
                font-size: 14px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Controls
        controls_layout = QHBoxLayout()

        # Select image button
        self.select_image_button = QPushButton('Select Image')
        self.select_image_button.clicked.connect(self.select_image)
        controls_layout.addWidget(self.select_image_button)

        # Select model button
        self.select_model_button = QPushButton('Select Model')
        self.select_model_button.clicked.connect(self.select_model)
        controls_layout.addWidget(self.select_model_button)

        # Process button
        self.process_button = QPushButton('Process Image')
        self.process_button.clicked.connect(self.process_image)
        self.process_button.setEnabled(False)
        controls_layout.addWidget(self.process_button)

        main_layout.addLayout(controls_layout)

        # Image display
        self.original_image_label = QLabel("Original Image")
        self.original_image_label.setStyleSheet("border: 2px solid #7F8C8D; background-color: #34495E;")
        self.original_image_label.setAlignment(Qt.AlignCenter)

        self.processed_image_label = QLabel("Processed Image")
        self.processed_image_label.setStyleSheet("border: 2px solid #7F8C8D; background-color: #34495E;")
        self.processed_image_label.setAlignment(Qt.AlignCenter)

        images_layout = QHBoxLayout()
        images_layout.addWidget(self.original_image_label)
        images_layout.addWidget(self.processed_image_label)
        main_layout.addLayout(images_layout)

        # Internal variables
        self.image_path = ''
        self.model_path = ''
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def select_image(self):
        self.image_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Image Files (*.jpg *.png *.bmp)")
        if self.image_path:
            self.display_image(self.image_path, self.original_image_label)
            self.process_button.setEnabled(bool(self.model_path))

    def select_model(self):
        self.model_path, _ = QFileDialog.getOpenFileName(self, "Select Model", "", "Model Files (*.pth *.pt)")
        if self.model_path:
            self.load_model()
            self.process_button.setEnabled(bool(self.image_path))

    def load_model(self):
        # check if the model is a jit model
        if self.model_path.endswith('.pt'):
            self.model = torch.jit.load(self.model_path, map_location=self.device)
            self.model.eval()
            return
        self.model = net.TwinLiteNet().to(self.device)
        self.model.load_state_dict(torch.load(self.model_path, map_location=self.device))
        self.model.eval()

    def process_image(self):
        if not self.image_path or not self.model:
            return

        # Load the image
        image = cv2.imread(self.image_path)
        processed_image = Run_rgb(self.model, image, self.device)

        # Display the processed image
        self.display_image(processed_image, self.processed_image_label)

    def display_image(self, image, label):
        if isinstance(image, str):
            image = cv2.imread(image)
        
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(qt_image).scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ImageProcessingGUI()
    gui.show()
    sys.exit(app.exec_())
