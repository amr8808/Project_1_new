import panel as pn
import hvplot.pandas
import pandas as pd
from panel.interact import interact
from panel import widgets


class nba:
    def __init__ (self, csv):
        self.csv = csv #assign csv to the class
        self.clean_csv() #run data cleaning
        self.get_attributes() #run get_attributes
        self.value_plot()
        self.player_pricing()
        self.serial_price()
        self.player_txn_count()
        self.dash()
        self.ptc_plot()
        
        
    def clean_csv(self):
        df = pd.read_csv(self.csv,infer_datetime_format=True,parse_dates=True, index_col='Transaction Date')
        df.index = df.index.date
        df.sort_index(inplace=True)
        self.df = df
        
    def player_txn_count(self):
        number_of_transactions_df = self.df.groupby('Player Name').count().filter(['Player Name','Set'])
        number_of_transactions_df.columns = ['Transaction Count']
        number_of_transactions_df.sort_values('Transaction Count',inplace=True,ascending=False)
        self.player_txn_count = number_of_transactions_df
        
    def ptc_plot(self):
        return self.player_txn_count.hvplot.bar(rot=90,color='green')
        
    
    def get_attributes(self):
        self.price_avg = self.df['Purchase Price'].mean
        self.buyer = self.df.groupby('Buyer').size

    def value_plot(self):
        return self.df.hvplot.line()
    
    def serial_price(self):
        return self.df.hvplot.scatter(x='Serial', y='Purchase Price', groupby = 'Player Name')
    
    def player_pricing(self):
        return self.df.hvplot.line(y='Purchase Price',groupby='Player Name')
    
    def dash(self):
        dashboard_title = "NBA TopShot Evaluator"
        welcome_message = "This is our NBA TopShot Evaluator.  Our mission is to help collectors value their NFT portfolios and identify opportunities."
        serial_findings = "We observe a correlation between low serial number and higher prices. With the current portfolio eval tools, an investors portfolio will not be accurately represented if they own low serials. Evaluation tools simply take the floor price of moments, and use that to determine portfolio value, leading to "
        all_star_icon = pn.pane.PNG('2021allstar.png', height=100, width=100)

        welcome_column = pn.Column(
            dashboard_title,
            welcome_message,
            all_star_icon
#             '2021 All Star Set Value',set_value()            
        )

#         floor_column = pn.Column(
#             all_star_icon,
#             'Player Floor',player_floor(),
#             'Historal Prices by Player', player_pricing()
# )

        serial_column = self.serial_price
    
        tabs = pn.Tabs(
            ("Welcome",welcome_column),
#             ("2021 All Star Pricing",floor_column),
            ("Serial Number/Price",serial_column)
        
        )
        
        return tabs