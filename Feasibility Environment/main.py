from shipmentCalculations import *
from data import *
from newProduct import *
import pandas as pd
from storage import *
from currency_converter import *
from fullfillment2 import *
from FBAsizes import *
from get_fba_fee import *
from updated_profitMargin import *
from multiprocessing import Pool

def initialize():
    global data, currency, product_instance, calculator, storage, profitmargin_instance

    data = Data()
    
    data.handle_file_upload()
    
    currency = Currency()
    calculator = calculations(data)
    product_instance = newProduct(data)
    data.assumptions = product_instance.alternativesCheck(data.assumptions)    
    data.assumptions = calculator.update_TotalCost()
    data.scenarios = calculator.check_products_scenario(data.assumptions, data.scenarios)
    data.scenarios = calculator.update_master_carton_dimensions(data.scenarios, data.assumptions)
    data.scenarios = calculator.update_shipment_info(data.scenarios, data.assumptions)
    data.scenarios = calculator.update_shipmentScenarios_with_avg_costs(data.scenarios)
    
    storage = Storage(data)
    data.storage = storage.averagefee()
    profitmargin_instance = profitmargin(data)

    print("Initialization Complete.")
    return data, profitmargin_instance


def get_margin(args):
    product, country, profitmargin_instance , data_instance = args
    
    return product, country, profitmargin_instance.get_profitmargin(data_instance, product, country)

if __name__ == "__main__":
    # Run initialization once
    initialize()
    countries = ["US", "CA", "DE", "UK"]
    products = data.assumptions['New Products'].tolist()
    profit_margin_matrix = pd.DataFrame(index=products, columns=countries)

    print(profitmargin_instance.get_profitmargin(data, "Fruit Leather 50", "US", "Performing Scenerio", "Best"))

    results = []
    for product in products:
        for country in countries:
            result = get_margin((product, country, profitmargin_instance, data))
            results.append(result)

    for product, country, margin in results:
        profit_margin_matrix.loc[product, country] = margin

    print(profit_margin_matrix)
