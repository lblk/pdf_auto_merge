import sys
from PyQt5.QtWidgets import QApplication
from ui_main import PDFMergeUI

def main():
    app = QApplication(sys.argv)
    window = PDFMergeUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    # Ensure to add 'pyqt5' to your requirements.txt or install it via pip
    main()
