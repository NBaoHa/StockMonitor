import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

class MatplotlibGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Matplotlib Graphs")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.plot_button = QPushButton("Plot Graph")
        self.plot_button.clicked.connect(self.plot_graph)
        layout.addWidget(self.plot_button)

        self.canvas = FigureCanvas(plt.Figure())
        layout.addWidget(self.canvas)

        self.central_widget.setLayout(layout)

    def plot_graph(self):
        # Generate some data
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        # Clear the previous plot
        self.canvas.figure.clear()

        # Plot the new data
        ax = self.canvas.figure.add_subplot(111)
        ax.plot(x, y)

        # Refresh the canvas
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MatplotlibGUI()
    gui.show()
    sys.exit(app.exec_())
