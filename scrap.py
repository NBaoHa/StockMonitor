# main.py

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
import style

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Styled Widgets")
        self.setGeometry(100, 100, 400, 200)
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Create and configure widgets
        self.label = QLabel("Hello, PyQt!")
        self.label.setStyleSheet(style.label)

        self.button = QPushButton("Click me")
        self.button.setStyleSheet(style.button_style)
        
        # Add widgets to layout
        layout.addWidget(self.label)
        layout.addWidget(self.button)

def main():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
