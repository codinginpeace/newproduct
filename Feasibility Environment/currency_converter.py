import requests
from datetime import datetime, timedelta
from data import *
class Currency(Data):
    def __init__(self):
        
        self.conversion_rates = {}
        self.last_updated = datetime.now() - timedelta(days=31)
        self.update_conversion_rates()


    def get_market_currencies(self,market):
        if market == "US":
            currency = "USD"
        elif market == "CA":
            currency = "CAD"
        elif market == "MX":
            currency = "MXN"
        elif market == "UK":
            currency = "GBP"
        elif market == "DE":
            currency = "EUR"
        elif market == "FR":
            currency = "EUR"
        elif market == "IT":
            currency = "EUR"
        elif market == "ES":
            currency = "EUR"
        elif market == "NL":
            currency = "EUR"
        elif market == "SE":
            currency = "SEK"
        elif market == "PL":
            currency = "PLN"
        elif market == "AU":
            currency = "AUD"
        elif market == "BE":
            currency = "EUR"
        else:
            currency = None

        return currency

    def fetch_conversion_rates_from_api(self):
        API_KEY = 'acf63c43310b7c9b011f8c47'
        BASE_URL = f'https://open.er-api.com/v6/latest/USD'
        
        try:
            response = requests.get(BASE_URL)
            response.raise_for_status()
            
            data = response.json()
           # print(f"API Response: {data}")  # Debugging line
            
            rates = data.get('rates', {})
            for currency, rate in rates.items():
                self.conversion_rates[('USD', currency)] = rate
        except requests.RequestException as e:
            print(f"Error during the API request: {e}")
        except ValueError:
            print("Error decoding the API response")

    def update_conversion_rates(self):
        current_date = datetime.now()
        if (current_date - self.last_updated).days >= 30:
            self.fetch_conversion_rates_from_api()
            self.last_updated = datetime.now()

    def convert_currency(self, amount, from_currency, to_currency):
        if amount == "-":
            return "-"
        
        else:

            if from_currency == to_currency:
                return amount
            
            if from_currency == 'USD':
                rate = self.conversion_rates.get((from_currency, to_currency))
            else:
                # Handle conversions that are not from USD
                rate_to_usd = self.conversion_rates.get(('USD', from_currency))
                rate_from_usd = self.conversion_rates.get(('USD', to_currency))
                if rate_to_usd and rate_from_usd:
                    rate = rate_from_usd / rate_to_usd
            
            if rate:
                return amount * rate
        return None

    def get_cost_in_market_currency(self, warehouse, market):
        cost, currency = self.whcosts[warehouse]
        target_currency = self.market_currencies[market]
        return self.convert_currency(cost, currency, target_currency)