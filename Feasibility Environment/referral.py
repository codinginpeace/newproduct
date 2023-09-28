from data import *
class Referral(Data):
    def __init__(self, data):
        self.refferaltable = data.referral
    
    def get_refferal(self,market, categotry, salesprice):
        df = self.refferaltable

        line = df[(df["Marketplace"] == market) & (df["Category"] == categotry) & (df["Marketplace"] == market)]
        treshhold = float(line["Threshold (orginal currency)"].iloc[0])
  
        treshhold = line["Threshold (orginal currency)"].iloc[0]
        
        if salesprice != "-":
            salesprice = float(salesprice)
            if (salesprice >= treshhold):
                rate = line["Above Threshold"]
                
            else:
                rate = line["Below Threshold"]
            cost = rate * salesprice
        
            return cost
        else:
            return ["-"]
        
        
                
