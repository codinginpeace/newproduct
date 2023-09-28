from fba_fee_config import *
from FBAsizes import *

class GetFBAFee:
    def __init__(self):
        self.calculator = FBASizeCalculator()
        



    def get_fee(self, weight, dimensions, country, salesprice):
        # Determine the size tier using the FBASizeCalculator class
        size_tier,weight = self.calculator.determine_size_tier(weight, dimensions, country)

        #calculate dimensional weight or other weight to understand the corresponding weight
        
        # Choose the appropriate FBA fee dictionary based on the country
        fee_dict = {
            'US': FBA_FEES_US,
            'CA': FBA_FEES_CA,
            # 'JP': FBA_FEES_JP,
            'UK': FBA_FEES_UK,
            'DE': FBA_FEES_DE,
            'FR': FBA_FEES_FR,
            'IT': FBA_FEES_IT,
            'ES': FBA_FEES_ES,
            'NL': FBA_FEES_NL,
            'SE': FBA_FEES_SE,
            'PL': FBA_FEES_PL,
        }.get(country, None)
        
        if country == "US" and salesprice < 10:
            fee_dict = FBA_FEES_US_LOWPRICE

        if fee_dict is None:
            return "Country not supported","Error"
        
        # Get the fee for the determined size tier

        fee_list = fee_dict.get(size_tier, [])

        if not fee_list:
            return "Size tier not found in fee dictionary","Error"
        
        # Initialize total_fee to 0
        total_fee = 0
        
        # Function to calculate fee based on unit
        def calculate_fee_based_on_unit(additional_fee, additional_unit, weight,limitweight):
            additional_weight = limitweight - weight
            if additional_unit == "per-lb":
                return additional_fee * additional_weight
            elif additional_unit == "per-halflb":
                return additional_fee * (additional_weight * 2)
            elif additional_unit == "per-100g":
                return additional_fee * (additional_weight / 0.1)
            else:
                return 0  # Default case, assumes fee is a flat rate
        
        # Loop through the fee_list to find the appropriate fee based on weight
        for fee_item in fee_list:
            min_weight = fee_item.get('min_weight', 0)
            max_weight = fee_item.get('max_weight', float('inf'))  # Use infinity if max_weight is not defined

            if min_weight <= weight <= max_weight:
                total_fee += fee_item.get('fee', 0)
                

                # Check for additional fees
                additional_fee = fee_item.get('additional_fee', 0)
                additional_unit = fee_item.get('additional_unit', None)
                if additional_fee and additional_unit:
                    additions = calculate_fee_based_on_unit(additional_fee, additional_unit, weight,min_weight)
                
                break            
        
        total_fee = total_fee + additional_fee
        if total_fee == 0:
            return "Weight not within any range for the size tier","Error"
        
        #print("\n","\n","\n",total_fee,size_tier, "\n""\n","\n")
        return total_fee, size_tier