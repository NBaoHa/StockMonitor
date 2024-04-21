import sys
from UnitStock import StockAnalyzer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import style


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

        # styling
        self.title_label.setStyleSheet(style.label)

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

        self.setWindowTitle("Stock Graphs")
        self.setGeometry(100, 100, 1000, 1200)

        # Features
        self.general_graph_canvas = FigureCanvas(plt.Figure())
        self.volatility_graph_canvas = FigureCanvas(plt.Figure())
        self.dividend_graph_canvas = FigureCanvas(plt.Figure())
        self.general_label = QLabel("Stock Data")
        self.volatility_label = QLabel("Volatility")
        self.dividends_label = QLabel('Dividends')
        self.controls_label = QLabel('Controls')

        # Layout
        self.layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.general_label)
        self.left_layout.addWidget(self.general_graph_canvas,8)
        self.left_layout.addWidget(self.controls_label,4)
        self.layout.addLayout(self.left_layout, 6)  
        self.right_layout = QVBoxLayout()
        # Volatility
        self.volatility_layout = QVBoxLayout()
        self.volatility_layout.addWidget(self.volatility_label)
        self.volatility_layout.addWidget(self.volatility_graph_canvas)
        self.right_layout.addLayout(self.volatility_layout)
        # Dividends
        self.dividend_layout = QVBoxLayout()
        self.dividend_layout.addWidget(self.dividends_label)
        self.dividend_layout.addWidget(self.dividend_graph_canvas)
        self.right_layout.addLayout(self.dividend_layout)

        self.layout.addLayout(self.right_layout, 4)  
        self.setLayout(self.layout)

        #styling
        self.general_label.setFixedSize(400,45) # width=100, height=30
        self.volatility_label.setFixedSize(400,45)
        self.dividends_label.setFixedSize(400,45)
        self.general_label.setStyleSheet(style.label)
        self.volatility_label.setStyleSheet(style.label)
        self.dividends_label.setStyleSheet(style.label)
        self.setStyleSheet("background-color: #333333;")

        # initiative
        self.plot_all_graphs()
    
    
    def plot_all_graphs(self):
        self.plot_general_graph()
        self.plot_volatility_graph()
        self.plot_dividend_graph()
        
    def plot_general_graph(self):
        self.general_graph_canvas.figure.clear()
        ax = self.general_graph_canvas.figure.add_subplot(111)
        fig = self.general_graph_canvas.figure
        self.stockObject.plot_stock_data(fig, ax)
        self.general_graph_canvas.draw()
    
    def plot_volatility_graph(self):
        self.volatility_graph_canvas.figure.clear()
        ax = self.volatility_graph_canvas.figure.add_subplot(111)
        fig = self.volatility_graph_canvas.figure
        self.stockObject.map_volatility(fig,ax)
        self.volatility_graph_canvas.draw()
    
    def plot_dividend_graph(self):
        self.dividend_graph_canvas.figure.clear()
        ax = self.dividend_graph_canvas.figure.add_subplot(111)
        fig = self.dividend_graph_canvas.figure
        self.stockObject.map_dividends(fig,ax)
        self.dividend_graph_canvas.draw()
        
class CompareStockMonitor(QWidget):
    """
    - compare different stocks over time on the same graph
    - tools to zoom and analyze
    - add max 10 sessions (time series graphs for stocks) to compare

    """
    pass 

    





if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MainStockGUI()
    gui.show()
    sys.exit(app.exec_())