import pandas as pd
from data import *
from currency_converter import *
from newProduct import *
from fulfillment import *
from storage import *
from shipmentCalculations import *
from referral import *
from get_fba_fee import *
from FBAsizes import *

class profitmargin(Data):
    def __init__(self):
        self.market = None
        self.currency = None
        self.product = None
        self.category = None
        self.sizetier = None
        self.shipmentscenario = None
        self.bestshipment = None
        self.worstshipment = None
        self.salesprice = None
        self.nonvatprice = None
        self.cogs = None
        self.duty = None
        self.vat = "-"
        self.shipment = None
        self.grossprofit = None
        self.fbafee = "-"
        self.referralfee = None
        self.storageamazon = None
        self.storage3pl = None
        self.storagetotal = None
        self.salestax_assumptions = None
        self.operatingprofit = None
        self.profitmargin = None
        
        self.shipments = Data.scenarios
        self.vats = Data.vat
        self.dutys = Data.duty
        self.paletType = {
            "DE": "palet-eu",
            "UK": "palet-eu",
            "UAE": "palet-eu",
            "FR": "palet-eu",
            "IT": "palet-eu",
            "ES": "palet-eu",
            "NL": "palet-eu",
            "SE": "palet-eu",
            "PL": "palet-eu",
            "AU": "palet-eu",
            "BE": "palet-eu",
            "JAP": "palet-eu",
            "US": "palet-us",
            "CA": "palet-us",
            "MX": "palet-us"
        }
        self.salestax_assumptions = {'MX': 0.06}

        self.vatcounties = ['UK','DE','FR','IT','ES','NL','SE','BE','PL']
        
        self.dutycountries = ['US','CA', 'MX', 'AU', "UAE", "JAP"]
        
    
    def bulkshipment(self,product,country):
        df = self.shipments
        
        palet = self.paletType[country]
        if palet == "palet-eu":
            bulkq = df[(df["Product Name"] == product) & (df["Destination"] == "EU - Main") & (df["Shipment Method"] != "Air")]["Bulk Shipment Quantity"]
        elif palet == "palet-us":
            bulkq = df[(df["Product Name"] == product) & (df["Destination"] == "US - Main") & (df["Shipment Method"] != "Air")]["Bulk Shipment Quantity"]
          
            
        #note: this returns more than one value since there are multiple alternatives for that product but lets suppose i take the first one out
        return bulkq.iloc[0]
        
    def calling(self,product,country,performingscenario,shipment_scenario, input_salesprice):
        
        cogs = self.cogs
        duty = self.duty
        vat = self.vat
        grossprofit = self.grossprofit
        storageamazon = self.storageamazon
        storage3pl =self.storage3pl
        storagetotal = self.storagetotal
        salestax_assumptions = self.salestax_assumptions
        operatingprofit = self.operatingprofit
        profitmargin = self.profitmargin  
        fbafee = self.fbafee
        nonvatprice = self.nonvatprice
        vat = 0  
        sizetier2 = None
        self.market = country  
        currency_instance = Currency()
        currency = currency_instance.get_market_currencies(country)
        product = product
        df = Data.assumptions
        category = df[df['New Products'] == product]['Category'].iloc[0]
        packageL = df[df['New Products'] == product]['Package Length (cm)'].iloc[0]
        packageW = df[df['New Products'] == product]['Package Width (cm)'].iloc[0]
        packageH = df[df['New Products'] == product]['Package Height (cm)'].iloc[0]
        weight = df[df['New Products'] == product]['Weight (gr)'].iloc[0]
        dimensions = sorted([packageL, packageW, packageH],reverse=True)
        line = df[df['New Products'] == product]
        sizetier = newProduct.get_sizeTier(itemassumption=line,country=country)      
        if input_salesprice ==None:
            prices = Data.salesprices
            salesprice = prices[prices['Pricing (in market currency)'] == product][country].iloc[0]
        else:
            salesprice = input_salesprice
        cogs = line["COGS"].iloc[0]
        cogs = currency_instance.convert_currency(amount=cogs, from_currency="USD", to_currency=currency)
        storage_instance = Storage()
        Data.storage = storage_instance.averagefee()
              
        bulk = (self.bulkshipment(product, country))
        instance = newProduct()
        volume_ft3 = instance.productcubicfeet(line)

        storageamazon = ((storage_instance.amazon_fee(country, sizetier,performingscenario))*volume_ft3).item()
        
        storage3pl = (storage_instance.thirdparty(country,performingscenario))/bulk
        storage3pl = currency_instance.convert_currency(amount=storage3pl, from_currency="USD",to_currency=currency)
        storagetotal = (storageamazon + storage3pl)
        shipmentscenario = shipment_scenario
        vats = self.vats
        dutys = self.dutys
        
        #feasibility'de shipment kırılımları gelecek fba vs aradepo
        #duty hesaplarken cogs olacak
        #vat salesprice tan
        #fizibilite güncellenecek
        #refferal fee kontrol
        #storage + 3pl kontrolü
        #baby food freezer tray
        #pomogranade 
        #chickpee ler
        #silver cup - sadece air olacak
        
        if (salesprice != "-"):
            salesprice = float(salesprice)
            if country in self.vatcounties:
                dutyrate = 0
                vatrate = vats[(vats['Product Name'] == product)][country].iloc[0]
                if vatrate != "-":
                    vat = vatrate * salesprice
                else:
                    vat = "-"
                nonvatprice = salesprice/(1+vatrate)
            
            elif country in self.dutycountries:
                vatrate = 0
                nonvatprice = "-"
                line = dutys[(dutys['Product Name'] == product)]
                if country == "US":
                    duty1= line["US-DUTY"].iloc[0]
                    mpf = line["US-MPF"].iloc[0]
                    if (duty1 != "-" and mpf != "-"):
                        dutyrate = float(duty1)+float(mpf)
                        duty = dutyrate*cogs
                    else:
                        duty = "-"
                        
                    
                elif country == "CA":
                    nonvatprice = "-"
                    duty1 = line["CA-DUTY"].iloc[0]
                    gst = line["CA-GST"].iloc[0]
                    if (duty1 != "-" and gst != "-"):
                        dutyrate = float(duty1)+float(gst)
                        duty = dutyrate * cogs
                    else:
                        duty = "-" 
                
            fee_calculator = GetFBAFee()
            
            fbafee, sizetier2 = fee_calculator.get_fee(weight, dimensions, country, salesprice)
            
            
            referralinstacne = Referral()
            self.referralfee = referralinstacne.get_refferal(country, category, salesprice).iloc[0]
        else:
            vat = "-"

        if (country in self.salestax_assumptions.keys()):
            salestaxrate = self.salestax_assumptions[country][0]
        else:
            salestaxrate = 0
            
        salestax = salesprice*salestaxrate
        


        shipment = calculations()
        bestshipment, best_towh, best_tofba, worstshipment, worst_towh, worst_tofba = shipment.get_cost_extremes(self.shipments ,product, country)

        if shipmentscenario == "Best":
            shipment = bestshipment
            shiptoWH = best_towh
            shiptoFBA = best_tofba
        else:
            shipment = worstshipment
            shiptoWH = worst_towh
            shiptoFBA = worst_tofba
         
        shipment = currency_instance.convert_currency(amount=shipment, from_currency="USD", to_currency=currency)
        shiptoWH = currency_instance.convert_currency( amount=shiptoWH, from_currency="USD", to_currency= currency)
        shiptoFBA = currency_instance.convert_currency(amount=shiptoFBA, from_currency="USD", to_currency=currency)

        if vat == 0:
            grossprofit = salesprice - (cogs + duty + shipment)
        elif vat == "-":
            grossprofit = "-"
        else:
            if vat != "-" or vat != None:
                grossprofit = nonvatprice - (cogs+shipment)
            elif duty != "-" or duty != None:
                grossprofit = nonvatprice - (cogs+shipment)

        if (grossprofit != "-" and fbafee!= "-" and self.referralfee != "-" and storagetotal != "-" and salestax != "-"):
            operatingprofit = grossprofit - (float(fbafee) + self.referralfee.item() + storagetotal + salestax )
        else:
            operatingprofit = "-"
                
        if ((category != "-") and (sizetier != "-") and (shipmentscenario != "-") and (bestshipment != "-") and (worstshipment != "-") and (salesprice != "-") and 
            ((self.vat != "-") or (duty != "-")) and (cogs != "-") and (shipment != "-") and (fbafee != "-") and (self.referralfee != "-") and (storagetotal != "-") and operatingprofit != "-"):
            
            profitmargin = (((operatingprofit/salesprice)*100))
            
        else:
            profitmargin = "-"
                
        variables = [
            ["Market", country],
            ["Currency", currency],
            ["Product", product],
            ["Category", category],
            ["Size Tier", sizetier],
            ["Shipment Scenario", shipmentscenario],
            ["Best Shipment", bestshipment],
            ["Worst Shipment", worstshipment],
            ["Sales Price", salesprice],
            ["Non-VAT Price", nonvatprice],
            ["COGS", cogs],
            ["Duty", duty],
            ["VAT", vat],
            ["Shipment (to Warehouse)", shiptoWH],
            ["Shipment (to FBA)", shiptoFBA],
            ["Shipment", shipment],
            ["Gross Profit", grossprofit],
            ["Calculated Size Tier", sizetier2],
            ["FBA Fee", fbafee],
            ["Referral Fee", self.referralfee],  # Use 'self.referralfee' in your actual code
            ["Storage (Amazon)", storageamazon],
            ["Storage (3PL)", storage3pl],
            ["Storage", storagetotal],
            ["Sales Tax", salestax],
            ["Operating Profit", operatingprofit],
            ["Profit Margin", profitmargin]
        ]

        # Create the DataFrame
        df = pd.DataFrame(variables, columns=['Variable', 'Value'])

        
        return df
        
        
        
    def get_profit_margin(self,df):
        profit_margin_row = df[df['Variable'] == 'Profit Margin']
        profit_margin_value = profit_margin_row['Value'].iloc[0]
        if profit_margin_value != "-":
            formatted_profit_margin = f"{profit_margin_value :.2f}%"
        else:
            formatted_profit_margin = "-"
        return formatted_profit_margin

    def get_profitmargin(self,product,country):
        df = self.calling(product,country,performingscenario="Performing Scenerio",shipment_scenario="Best",input_salesprice=None)
        profitmargin = self.get_profit_margin(df)
        return profitmargin