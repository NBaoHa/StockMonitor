import sys
from UnitStock import StockAnalyzer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np


class MainStockGUI(QWidget):
    def __init__(self):
        super().__init__()

        # Features
        self.title_label = QLabel("Stock Ticker Search")
        self.search_bar = QLineEdit()
        self.search_button = QPushButton("Search")
        self.start_date_label = QLabel("Start Date")
        self.calendar_input_start = QDateEdit()
        self.end_date_label = QLabel("End Date")
        self.calendar_input_end = QDateEdit()

        # layout
        self.setWindowTitle("Stock Analyzer")
        self.setGeometry(100, 100, 400, 200)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.search_button)

        # calender layout
        self.calendar_layout = QHBoxLayout()
        self.start_layout = QVBoxLayout()
        self.end_layout = QVBoxLayout()
        self.start_layout.addWidget(self.start_date_label)
        self.start_layout.addWidget(self.calendar_input_start)
        self.end_layout.addWidget(self.end_date_label)
        self.end_layout.addWidget(self.calendar_input_end)
        self.calendar_layout.addLayout(self.start_layout)
        self.calendar_layout.addLayout(self.end_layout)
        self.layout.addLayout(self.calendar_layout)

        self.setLayout(self.layout)

        # Actions
        self.search_button.clicked.connect(self.search_stock)

        # User Variables
        self.stock = None
        self.start_date = None
        self.end_date = None

        # User Sessions
        self.Stock_Monitor_session = None
        self.finance_projection_session = None
        

    def search_stock(self):
        stock_ticker = self.search_bar.text()
        self.start_date = self.calendar_input_start.date().toString("yyyy-MM-dd")
        self.end_date = self.calendar_input_end.date().toString("yyyy-MM-dd")
        
        self.stock = StockAnalyzer(stock_name=stock_ticker,start=self.start_date,end=self.end_date)

        #spawn Stock Monitor GUI
        self.Stock_Monitor_session = GraphDashboard(self.stock)
        self.Stock_Monitor_session.show()

class GraphDashboard(QWidget):
    def __init__(self, stock: StockAnalyzer):
        super().__init__()
        
        # user input params
        self.stockObject = stock

        # Features
        self.setWindowTitle("Stock Graphs")
        self.setGeometry(100, 100, 1000, 900)
        self.general_graph_canvas = FigureCanvas(plt.Figure())
        self.volatility_graph_canvas = FigureCanvas(plt.Figure())
        self.dividend_graph_canvas = FigureCanvas(plt.Figure())
        self.general_label = QLabel("Stock Data")
        self.volatility_label = QLabel("Volatility")
        self.dividends_label = QLabel('Dividends')
        #PLACEHOLDER for controls
        self.placeholder_label = QLabel('placeholder for controls here')

        # Layout
        self.layout = QHBoxLayout()
        self.general_stock_layout = QVBoxLayout()
        self.support_stock_layout = QVBoxLayout()  # right side of the monitor
        self.controls_layout = QHBoxLayout()
        self.volatility_layout = QVBoxLayout()
        self.dividend_layout = QVBoxLayout()

        self.general_stock_layout.addWidget(self.general_label,1)
        self.general_stock_layout.addWidget(self.general_graph_canvas,9)

        self.volatility_layout.addWidget(self.volatility_label,1)
        self.volatility_layout.addWidget(self.volatility_graph_canvas,1)

        self.dividend_layout.addWidget(self.dividends_label)
        self.dividend_layout.addWidget(self.dividend_graph_canvas)

        self.layout.addLayout(self.general_stock_layout)
        self.support_stock_layout.addLayout(self.volatility_layout)
        self.support_stock_layout.addLayout(self.dividend_layout)
        self.support_stock_layout.addLayout(self.controls_layout)
        self.layout.addLayout(self.support_stock_layout)
        self.setLayout(self.layout)

        # initiative
        self.plot_all_graphs()
        
    def plot_all_graphs(self):
        self.plot_general_graph()
        self.plot_volatility_graph()
        self.plot_dividend_graph()
        
    def plot_general_graph(self):
        self.general_graph_canvas.figure.clear()
        ax = self.general_graph_canvas.figure.add_subplot(111)
        self.stockObject.plot_stock_data(ax)
        self.general_graph_canvas.draw()
    
    def plot_volatility_graph(self):
        self.volatility_graph_canvas.figure.clear()
        ax = self.volatility_graph_canvas.figure.add_subplot(111)
        self.stockObject.map_volatility(ax)
        self.volatility_graph_canvas.draw()
    
    def plot_dividend_graph(self):
        self.dividend_graph_canvas.figure.clear()
        ax = self.dividend_graph_canvas.figure.add_subplot(111)
        self.stockObject.map_dividends(ax)
        self.dividend_graph_canvas.draw()
        
        
    





if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MainStockGUI()
    gui.show()
    sys.exit(app.exec_())