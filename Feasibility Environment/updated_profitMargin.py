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
        # Class constants for static data
    PALET_TYPE = {
        "DE": "palet-eu", "UK": "palet-eu", "UAE": "palet-eu", "FR": "palet-eu",
        "IT": "palet-eu", "ES": "palet-eu", "NL": "palet-eu", "SE": "palet-eu",
        "PL": "palet-eu", "AU": "palet-eu", "BE": "palet-eu", "JAP": "palet-eu",
        "US": "palet-us", "CA": "palet-us", "MX": "palet-us"
    }
    COUNTRIES_WITH_VAT = ['UK', 'DE', 'FR', 'IT', 'ES', 'NL', 'SE', 'BE', 'PL']
    COUNTRIES_WITH_DUTY = ['US', 'CA', 'MX', 'AU', "UAE", "JAP"]
    SALESTAX_ASSUMPTIONS = {'MX': 0.06}

    # Using __slots__ to optimize memory usage
    __slots__ = ['product_details', 'shipments', 'vats', 'dutys']
    def __init__(self, data):
        # Grouping related attributes
        self.product_details = {
            'market': None, 'currency': None, 'product': None, 'category': None,
            'sizetier': None, 'shipmentscenario': None, 'bestshipment': None,
            'worstshipment': None, 'salesprice': None, 'nonvatprice': None,
            'cogs': None, 'duty': None, 'vat': "-", 'shipment': None,
            'grossprofit': None, 'fbafee': "-", 'referralfee': None,
            'storageamazon': None, 'storage3pl': None, 'storagetotal': None,
            'salestax_assumptions': None, 'operatingprofit': None, 'profitmargin': None
        }

        # Fetching data using methods (assuming these methods exist in the Data class)
        self.shipments = self.get_scenarios(data)
        self.vats = self.get_vat(data)
        self.dutys = self.get_duty(data)
        self.sizetier = None
        self.currency = None  # or some default value
        # Sample methods to fetch data (you can implement the actual logic)

        self.currency_instance = Currency()


    def get_palet_type(self, country):
        return self.PALET_TYPE.get(country, None)
    
    def get_scenarios(self, data):
        return data.scenarios

    def get_vat(self, data):
        return data.vat

    def get_duty(self, data):
        return data.duty

    def bulkshipment(self, product, country):
        df = self.shipments
        palet = self.get_palet_type(country)
        
        if palet == "palet-eu":
            bulkq = df[(df["Product Name"] == product) & (df["Destination"] == "EU - Main") & (df["Shipment Method"] != "Air")]["Bulk Shipment Quantity"]
        elif palet == "palet-us":
            bulkq = df[(df["Product Name"] == product) & (df["Destination"] == "US - Main") & (df["Shipment Method"] != "Air")]["Bulk Shipment Quantity"]
        else:
            return None  # or some default value or raise an exception
        
        # Return the first value of the filtered dataframe
        return bulkq.iloc[0] if not bulkq.empty else None

        
    def assign_currency(self, country):
        """Assign currency based on the country using the Currency class."""
        self.currency = self.currency_instance.get_market_currencies(country)
        if not self.currency:
            raise ValueError(f"Currency not found for country: {country}")
        
    def calling(self, data, product, country, performing_scenario="Performing Scenerio", shipment_scenario="Best", input_salesprice=None):
        # Calculate sales price
        
        salesprice = self.calculate_salesprice(data, product, country, input_salesprice)
        # Fetch product details
        product_details = self.get_product_details(product, data)
        # Calculate FBA fee
        fbafee, sizetier, short_sizetier = self.calculate_fba_fee(product_details, country, salesprice, data)

        # Calculate currency conversion
        cogs = self.calculate_cogs(product_details, country)
        
        # Calculate shipment costs
        shipment_costs = self.calculate_shipment_costs(product, country, shipment_scenario,data)

        # Calculate storage fees
        storage_fees = self.calculate_storage_fees(product, country, performing_scenario, product_details, short_sizetier,data)
        
        # Calculate VAT and Duty
        vat, duty = self.calculate_vat_and_duty(product, country, salesprice, cogs)
        
        # Calculate referral fee
        referral_fee = self.calculate_referral_fee(country, product_details['category'], salesprice,data)
        
        # Calculate profit margins
        profit_margins = self.calculate_profit_margins(salesprice, cogs, shipment_costs, vat, duty, fbafee, referral_fee, storage_fees)
        
        instance = Currency()
        currency = instance.get_market_currencies(country)
        # Construct the result dataframe
        df = self.construct_dataframe(country,  product, product_details, sizetier, salesprice, cogs, vat, duty, shipment_costs, fbafee, referral_fee, storage_fees, profit_margins)
        
        return df

    def get_product_details(self, product, data):
    # Fetch product details from Data.assumptions
        df = data.assumptions
        product_line = df[df['New Products'] == product]
        
        details = {
            'category': product_line['Category'].iloc[0],
            'packageL': product_line['Package Length (cm)'].iloc[0],
            'packageW': product_line['Package Width (cm)'].iloc[0],
            'packageH': product_line['Package Height (cm)'].iloc[0],
            'weight': product_line['Weight (gr)'].iloc[0],
            'cogs_usd': product_line["COGS"].iloc[0]
        }
        
        return details

    def calculate_cogs(self, product_details, country,):
        # Calculate COGS based on product details and currency conversion
        currency_instance = Currency()
        to_market = currency_instance.get_market_currencies(country)
        cogs_local = currency_instance.convert_currency(amount=product_details['cogs_usd'], from_currency="USD", to_currency=to_market)
        
        return cogs_local

    def calculate_storage_fees(self, product, country, performing_scenario, product_details, short_sizetier,data):
        # Calculate storage fees based on country, scenario, and product details
        storage_instance = Storage(data)
        data.storage = storage_instance.averagefee()
        
        bulk = self.bulkshipment(product, country)
        instance = newProduct(data)
        volume_ft3 = instance.productcubicfeet(product_details)

        storage_amazon = ((storage_instance.amazon_fee(country, short_sizetier, performing_scenario)) * volume_ft3).item()
        
        storage_3pl = (storage_instance.thirdparty(country, performing_scenario)) / bulk
        currencyInstence = Currency()
        to_currency1 = currencyInstence.get_market_currencies(country)
        storage_3pl = self.currency_instance.convert_currency(amount=storage_3pl, from_currency="USD", to_currency=to_currency1)
        
        total_storage_fee = storage_amazon + storage_3pl
        
        return total_storage_fee

    def calculate_shipment_costs(self, product, country, shipment_scenario, data):
        # Calculate shipment costs based on product, country, and scenario
        shipment = calculations(data)
        bestshipment, best_towh, best_tofba, worstshipment, worst_towh, worst_tofba = shipment.get_cost_extremes(self.shipments, product, country)

        if shipment_scenario == "Best":
            shipment_cost = bestshipment
        else:
            shipment_cost = worstshipment

        curr = Currency()
        tomarket = curr.get_market_currencies(country)
        shipment_cost = self.currency_instance.convert_currency(amount=shipment_cost, from_currency="USD", to_currency=tomarket)

        return shipment_cost

    def calculate_salesprice(self, data, product, country, input_salesprice):
        # Calculate sales price based on product, country, and input_salesprice
      
        if input_salesprice is None:
            prices = data.salesprices
            salesprice = prices[prices['Pricing (in market currency)'] == product][country].iloc[0]
        else:
            salesprice = input_salesprice

        return salesprice

    def calculate_vat_and_duty(self, product, country, salesprice, cogs):
        # Calculate VAT and Duty based on country, salesprice, and cogs
        vat = 0
        duty = 0

        if country in self.COUNTRIES_WITH_VAT:
            vatrate = self.vats[self.vats['Product Name'] == product][country].iloc[0]
            if vatrate != "-" and salesprice != "-":
                salesprice = float(salesprice)
                vat = vatrate * salesprice

        if country in self.COUNTRIES_WITH_DUTY:
            line = self.dutys[self.dutys['Product Name'] == product]
            if country == "US":
                duty1 = line["US-DUTY"].iloc[0]
                mpf = line["US-MPF"].iloc[0]
                if duty1 != "-" and mpf != "-":
                    duty = (float(duty1) + float(mpf)) * cogs

        return vat, duty

    def calculate_fba_fee(self, product_details, country, salesprice,data):
        # Calculate FBA fee based on product details, country, and salesprice
        dimensions = sorted([product_details['packageL'], product_details['packageW'], product_details['packageH']], reverse=True)
        weight = product_details['weight']

        fee_calculator = GetFBAFee()
        fba_fee, _ = fee_calculator.get_fee(weight, dimensions, country, salesprice)

        new_prod = newProduct(data)
        sizetier, short_sizetier = new_prod.get_sizeTier(product_details, country)

        return fba_fee, sizetier, short_sizetier

    def calculate_referral_fee(self, country, category, salesprice,data):
        # Calculate referral fee based on country, category, and salesprice
        referral_instance = Referral(data)
        if salesprice != "-":
            referral_fee = referral_instance.get_refferal(country, category, salesprice).iloc[0]
            return referral_fee
        else:
            return "-"

    def calculate_profit_margins(self, salesprice, cogs, shipment_costs, vat, duty, fbafee, referral_fee, storage_fees):
        if salesprice != "-":
            salesprice = float(salesprice)
        # Calculate profit margins based on various inputs
            gross_profit = salesprice - (cogs + shipment_costs + vat + duty)
            operating_profit = gross_profit - (fbafee + referral_fee + storage_fees)
            
            if salesprice != 0:
                profit_margin_percentage = (operating_profit / salesprice) * 100
            else:
                profit_margin_percentage = 0  # or handle this case differently if needed
            
            return profit_margin_percentage
        else:
            return "-"



    def construct_dataframe(self, country, product, product_details, sizetier, salesprice, cogs, vat, duty, shipment_costs, fbafee, referral_fee, storage_fees, profit_margins):
        # Construct the result dataframe based on various inputs
        
        # Formatting the float values
        salesprice = "{:.2f}".format(salesprice)
        cogs = "{:.2f}".format(cogs)
        vat = "{:.2f}".format(vat)
        duty = "{:.2f}".format(duty)
        shipment_costs = "{:.2f}".format(shipment_costs)
        fbafee = "{:.2f}".format(fbafee)
        referral_fee = "{:.2f}".format(referral_fee)
        storage_fees = "{:.2f}".format(storage_fees)
        
        # Formatting profit margins as a percentage
        profit_margins = "{:.2f}%".format(profit_margins)

        variables = [
            ["Market", country],
            ["Product", product],
            ["Category", product_details['category']],
            ["Size Tier", sizetier],
            ["Sales Price", salesprice],
            ["COGS", cogs],
            ["VAT", vat],
            ["Duty", duty],
            ["Shipment Costs", shipment_costs],
            ["FBA Fee", fbafee],
            ["Referral Fee", referral_fee],
            ["Storage Fees", storage_fees],
            ["Profit Margin", profit_margins]
        ]

        # Create the DataFrame
        df = pd.DataFrame(variables, columns=['Variable', 'Value'])
        return df


    def get_profit_margin(self, df):
        """
        Retrieve and format the profit margin from the dataframe.
        """
        profit_margin_value = df.loc[df['Variable'] == 'Profit Margin', 'Value'].values[0]
        
        # Check if the profit margin value is numeric (either int or float)
        if isinstance(profit_margin_value, (int, float)):
            formatted_profit_margin = f"{profit_margin_value:.2f}%"
        else:
            formatted_profit_margin = "-"
        
        return formatted_profit_margin

    def get_profitmargin(self,data, product, country, performing_scenario="Performing Scenerio", shipment_scenario="Best", input_salesprice=None):
        """
        Call the main function to get the dataframe and retrieve the profit margin.
        """
        df = self.calling(data, product, country, performing_scenario, shipment_scenario, input_salesprice)
        profitmargin = self.get_profit_margin(df)
        
        return profitmargin

