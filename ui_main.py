import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit, QWidget, QMessageBox
from generate_merge import merge_pdfs

class PDFMergeUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Auto Merge")
        self.setGeometry(100, 100, 400, 200)

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Input directory selection
        self.input_label = QLabel("Input Directory:")
        self.layout.addWidget(self.input_label)
        self.input_path = QLineEdit()
        self.layout.addWidget(self.input_path)
        self.input_button = QPushButton("Select Input Directory")
        self.input_button.clicked.connect(self.select_input_directory)
        self.layout.addWidget(self.input_button)

        # Output file selection
        self.output_label = QLabel("Output File:")
        self.layout.addWidget(self.output_label)
        self.output_path = QLineEdit()
        self.layout.addWidget(self.output_path)
        self.output_button = QPushButton("Select Output File")
        self.output_button.clicked.connect(self.select_output_file)
        self.layout.addWidget(self.output_button)

        # Run button
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.run_merge)
        self.layout.addWidget(self.run_button)

    def select_input_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Input Directory")
        if directory:
            self.input_path.setText(directory)

    def select_output_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Select Output File", filter="PDF Files (*.pdf)")
        if file_path:
            self.output_path.setText(file_path)

    def run_merge(self):
        input_dir = self.input_path.text()
        output_file = self.output_path.text()
        if not input_dir or not output_file:
            QMessageBox.warning(self, "Warning", "Please select both input directory and output file.")
            return

        try:
            QMessageBox.information(self, "Success", f"Running start")
            merge_pdfs(input_dir, output_file)
            QMessageBox.information(self, "Success", f"PDF files merged successfully!\nOutput: {output_file}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")
