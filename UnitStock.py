import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import math

class StockAnalyzer:
    def __init__(self, stock_name, start, end):
        self.stock_name = stock_name
        self.start = start
        self.end = end
        self.stock_df = self.fetch_data()
        self.ticker = self.fetch_ticker()

    def fetch_data(self):
        stock_data = yf.download(self.stock_name, start=self.start,end=self.end)
        return stock_data
    
    def fetch_ticker(self):
        return yf.Ticker(self.stock_name)

    def plot_stock_data(self,fig, ax): # wrapping plotter
        
        #fig, ax = plt.subplots(figsize=(10, 6))
        self.stock_df['Open'].plot(ax=ax, color='blue', label='Open')
        self.stock_df['Close'].plot(ax=ax, color='green', label='Close')
        self.stock_df['Adj Close'].plot(ax=ax, color='red', label='Adj Close')
        ax2 = ax.twinx()
        self.stock_df['Volume'].plot(ax=ax2, color='black', label='Volume')
        ax.legend(loc='upper left')
        ax2.legend(loc='upper right')
        ax.set_xlabel('Date',color='lightgray')
        ax.set_ylabel('Price',color='lightgray')
        ax2.set_ylabel('Volume',color='lightgray')

        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#333333')
        ax.grid(True, color='darkgray')
        ax2.set_facecolor('#333333')
        ax.tick_params(axis='x', colors='lightgray')
        ax.tick_params(axis='y', colors='lightgray')
        ax2.tick_params(axis='x', colors='lightgray')
        ax2.tick_params(axis='y', colors='lightgray')
        ax.spines['bottom'].set_color('lightgray')
        ax.spines['left'].set_color('lightgray')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax2.spines['bottom'].set_color('lightgray')
        ax2.spines['left'].set_color('lightgray')
        ax2.spines['right'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        plt.tight_layout()
       
        
        
        

    def map_volatility(self,fig, ax):
        self.stock_df['Volatility_shortterm'] = self.stock_df['Close'].pct_change().rolling(window=30).std()
        self.stock_df['Volatility_longterm'] = self.stock_df['Close'].pct_change().rolling(window=90).std()
        self.stock_df['Volatility_shortterm'].plot(ax=ax, color='orange')
        self.stock_df['Volatility_longterm'].plot(ax=ax, color='blue')
        filtered_list_longterm = [x for x in list(self.stock_df['Volatility_longterm']) if not math.isnan(x)]
        filtered_list_shortterm = [x for x in list(self.stock_df['Volatility_shortterm']) if not math.isnan(x)]
        avg_volatility_longterm = sum(filtered_list_longterm)/len(filtered_list_longterm)
        avg_volatility_shortterm = sum(filtered_list_shortterm)/len(filtered_list_shortterm)

        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#333333')
        ax.grid(True, color='darkgray')
        ax.tick_params(axis='x', colors='lightgray')
        ax.tick_params(axis='y', colors='lightgray')
        ax.spines['bottom'].set_color('lightgray')
        ax.spines['left'].set_color('lightgray')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.legend
        ax.set_xlabel('Date', color='lightgray')
        plt.tight_layout()

      

    def map_dividends(self,fig,ax):
        dividends = self.ticker.history(start=self.start, end=self.end)['Dividends']
        if not dividends.empty:
            dates = dividends.index.tolist()
            dates = [timestamp.strftime('%y-%-m-%-d') for timestamp in dates]
            dividends = dividends.tolist()
            ax.bar(dates, dividends,width=0.4)
            fig.patch.set_facecolor('#333333')
            ax.set_facecolor('#333333')
            ax.grid(True, color='darkgray')
            ax.tick_params(axis='x', colors='lightgray')
            ax.tick_params(axis='y', colors='lightgray')
            ax.spines['bottom'].set_color('lightgray')
            ax.spines['left'].set_color('lightgray')
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            plt.tight_layout()
            
           
           
        else:
            print(f'{self.stock_name} did not pay dividends in the specified duration.')


# Example usage:
if __name__ == "__main__":
    stock_name = "YTSL.NE"  # Example stock ticker
    start = "2016-01-01"
    end = "2024-04-16"
    analyzer = StockAnalyzer(stock_name, start=start,end=end)
    fig,ax = plt.subplots()
    #analyzer.plot_stock_data(ax)
    analyzer.map_volatility(fig,ax)
    #analyzer.map_dividends(ax)
    # analyzer.catch_event()