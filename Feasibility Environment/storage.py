
import pandas as pd
from data import *
import numpy as np
from currency_converter import *
from shipmentCalculations import *

class Storage(Data):
    def __init__(self, data_instance):
        self.fees = data_instance.storage
        self.fees["Average"] = np.nan
        
        self.durations = {
            "Performing Scenerio": {
                "3PL Storage Duration": 3,
                "Amazon Duration": 2
            },
            "Non-Performing Scenerio": {
                "3PL Storage Duration": 6,
                "Amazon Duration": 6
            }
        }
        
        self.costincurrency = None
        
        self.marketsfedfromwh = {"WOW": ["US", "CA", "MX"], "BORSAN":["UK", "DE", "FR", "IT", "ES", "NL", "SE", "PL", "AU", "BE"]}
        #this cost is per palet per month, need to divide
        self.whcosts = {"WOW":[6.77,"USD"], "BORSAN":[4,"EUR"]}

    def get_costincurrency(self, cost, warehouse, market):
        currency = Currency.get_cost_in_market_currency(warehouse,market)
        self.costincurrency = Currency.convert_currency(cost, "USD",currency)
        return self.costincurrency

        
    def averagefee(self):
    #this method should only ran when data is updated
        for index, entry in self.fees.iterrows():
            
            #print(entry)
            #print((9*(entry["JAN-SEP"]) + 3*(entry["OCT-DEC"]))/12)
            average = (9*(entry["JAN-SEP"]) + 3*(entry["OCT-DEC"]))/12
            self.fees.loc[index,"Average"] = average
            #print(self.fees)
        return self.fees
        
            
    def amazon_fee(self, country, size, scenario):
        fee_row = self.fees[(self.fees['Country'] == country) & (self.fees['Size'] == size)]
        
        cost = fee_row['Average']
        cost *= self.durations[scenario]["Amazon Duration"]


        return cost
        
    def thirdparty(self, country,scenario):
        # Loop through the warehouses to find which one serves the given country
        for wh, countries_served in self.marketsfedfromwh.items():
            if country in countries_served:
                # Return the cost for the warehouse that serves the country
                costinsusd = self.whcosts[wh]
                currency_instance = Currency()
                cost = currency_instance.convert_currency(costinsusd[0],"USD",costinsusd[1])
                
                # Multiply the cost with 3PL Storage Duration for the Performing Scenario
                cost *= self.durations[scenario]["3PL Storage Duration"]
                
                return cost
        
        
    