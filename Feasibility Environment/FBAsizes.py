from fba_fee_config import *

class FBASizeCalculator:
    def __init__(self):
        # Use the imported size tier dictionaries
        self.FBA_SIZES_US = FBA_SIZES_US
        self.FBA_SIZES_CA = FBA_SIZES_CA
        self.FBA_SIZES_EU = FBA_SIZES_EU
        self.FBA_SIZES_JP = FBA_SIZES_JAP
    # Function to convert grams to ounces

    # Logic to determine the size tier based on dimensions and weight
    def determine_size_tier(self, weight, dimensions, country):
        def get_size_tiers(country):
            if country == "US":
                size_tiers = self.FBA_SIZES_US
            elif country == "CA":
                size_tiers = self.FBA_SIZES_CA
            elif country == "JP":
                size_tiers = self.FBA_SIZES_JAP
            elif country in ['UK', 'DE', 'FR', 'IT', 'ES', 'NL', 'SE', 'PL']:
                size_tiers = self.FBA_SIZES_EU
            return size_tiers
    
        def determine_shipping_weight(dimensions, unit_weight):
            dimensional_weight = (dimensions[0] *dimensions[1] * dimensions[2])/139
            if dimensional_weight > unit_weight:
                shipment_weight = dimensional_weight
            else:
                shipment_weight = unit_weight
            
            return shipment_weight

        def grams_to_ounces(grams):
            return grams * 0.03527396
        # Function to convert grams to pounds
        def grams_to_pounds(grams):
                return grams * 0.00220462
        # Function to convert centimeters to inches
        def cm_to_inches(cm):
            return cm * 0.393701
        
        size_tiers = get_size_tiers(country)

        if country == 'US':
            weight = grams_to_pounds(weight)
            dimensions = [cm_to_inches(dim) for dim in dimensions]
        elif country in ['CA', 'JP', 'UK', 'DE', 'FR', 'IT', 'ES', 'NL', 'SE', 'PL']:
            # Assuming these countries uses grams and cm, so no conversion needed
            pass

        
        for tier, criteria in size_tiers.items():
            shipping_weight = weight
            for sub_tier, sub_criteria in criteria.items():                
                unit_weight = sub_criteria.get('unit_weight', None)
                longest_side = sub_criteria.get('longest_side', None)
                median_side = sub_criteria.get('median_side', None)
                shortest_side = sub_criteria.get('shortest_side', None)

                if unit_weight:
                    if isinstance(unit_weight, str):
                        if 'Over' in unit_weight:
                            continue  # Skip this tier if weight is over some limit
                    elif weight <= unit_weight:
                        # Check dimensions
                        dims_criteria = [longest_side, median_side, shortest_side]
                        dims_criteria = [x for x in dims_criteria if x is not None]  # Remove None values
                        
                        if all(dim <= max_dim for dim, max_dim in zip(sorted(dimensions), sorted(dims_criteria))):
                            if (sub_tier == "Large standard") or (("oversize" in sub_tier) and sub_tier != "Special oversize"):
                                shipping_weight = determine_shipping_weight(dimensions, weight)
                            return sub_tier, shipping_weight

        return "No suitable size tier found",weight