from fba_fee_config import *
def calculate_fba_fee(product, region='US'):
    # Get the appropriate fee dictionary based on the region
    fba_sizes = globals().get(f'FBA_SIZES_{region}')
    fba_fees = globals().get(f'FBA_FEES_{region}')
    
    if not fba_sizes or not fba_fees:
        return "Invalid region"
    
    # Identify the size tier based on product dimensions and weight
    size_tier = None
    for tier, specs in fba_sizes['size_tiers'].items():
        if (product['weight'] <= specs['unit_weight'] and
            product['longest_side'] <= specs['longest_side'] and
            product['median_side'] <= specs.get('median_side', float('inf')) and
            product['shortest_side'] <= specs.get('shortest_side', float('inf'))):
            size_tier = tier
            break
    
    if not size_tier:
        return "Product dimensions do not fit any size tier"
    
    # Calculate the fee based on the weight of the product
    for fee_bracket in fba_fees[size_tier]:

        if product['weight'] >= fee_bracket['min_weight'] and (fee_bracket['max_weight'] is None or product['weight'] <= fee_bracket['max_weight']):
            return fee_bracket['fee']
    
    return "Could not determine fee"

# Example usage
product = {
    'weight': 10,  # in oz
    'longest_side': 10,  # in inches
    'median_side': 8,  # in inches
    'shortest_side': 2  # in inches
}

def get_fba_size_tier(country, dimensions, weight):
    # Define the size tier dictionaries for different countries
    FBA_SIZES_US = {...}  # Existing dictionary
    FBA_SIZES_CA = {...}  # Existing dictionary
    FBA_SIZES_EU = {...}  # Existing dictionary for all EU countries
    FBA_SIZES_JP = {...}  # Existing dictionary

    # Choose the appropriate size tier dictionary based on the country
    if country == 'US':
        size_tiers = FBA_SIZES_US['size_tiers']
    elif country == 'CA':
        size_tiers = FBA_SIZES_CA['size_tiers']
    elif country in ['UK', 'DE', 'FR', 'IT', 'ES']:  # Add more EU countries as needed
        size_tiers = FBA_SIZES_EU['size_tiers']
    elif country == 'JP':
        size_tiers = FBA_SIZES_JP['size_tiers']
    else:
        return "Country not supported"





















"""
class FBAus(Data):
    def __init__(self):
        self.fee_lookup = FBA_FEES
        self.sizes = ["smallStd", "largeStd", "smallOs", "mediumOs", "largeOs", "specialOs"]
        self.newproducts = list(Data.assumptions["New Products"])
        self.assumptions = Data.assumptions

        columns = {"Product": [], "Dimensions (inch)": [], "Weight (lb)": [], "Dimensional Weight": [], "Low Price": [], "Size Tier": [], "US FBA Fee": []}
        self.fees = pd.DataFrame(data=columns)            
        self.fee_lookup = {
                "smallStd": {
                    (0, 0.25): 3.42,
                    (0.25, 0.5): 3.71,
                    (0.5, 0.75): 3.87,
                    (0.75, 16): 3.60,
                },
                "largeStd": {
                    (0, 0.25): 3.09,
                    (0.25, 0.5): 3.31,
                    (0.5, 0.75): 3.47,
                    (0.75, 1): 3.98,
                    (1, 1.5): 4.63,
                    (1.5, 2): 4.92,
                    (2, 2.5): 5.33,
                    (2.5, 3): 5.62,
                    (3, float('inf')): 6.40,  # You can adjust this for the additional 0.16 * ((weight-3)/2)
                },
                "smallOs": {
                    (1, 70): 8.96,  # You can adjust this for the additional 0.42 * (weight-1)
                },
                "mediumOs": {
                    (1, 150): 18.28,  # You can adjust this for the additional 0.42 * (weight-1)
                },
                "largeOs": {
                    (90, 150): 89.21,  # You can adjust this for the additional 0.83 * (weight-90)
                },
                "specialOs": {
                    (90, float('inf')): 157.72,  # You can adjust this for the additional 0.83 * (weight-90)
                }
            }

    def convert_units(self, itemassumption):
      
        Convert units from grams to pounds and centimeters to inches.
        
        Parameters:
            itemassumption (dict): Dictionary containing item assumptions.
            
        Returns:
            tuple: Converted units for weight in pounds, length, width, and height in inches.
    
        weight_lb = itemassumption["Weight (gr)"] * LB_TO_GR
        length_inch = itemassumption["Package Length (cm)"] * CM_TO_INCH
        width_inch = itemassumption["Package Width (cm)"] * CM_TO_INCH
        height_inch = itemassumption["Package Height (cm)"] * CM_TO_INCH

        return weight_lb, length_inch, width_inch, height_inch
    
    def lowpriceFBACalculation_single(self, itemassumption, size):
        weight_lb, length_inch, width_inch, height_inch = self.convert_units(itemassumption)
        dimensional_weight = (length_inch * width_inch * height_inch) / DIMENSIONAL_WEIGHT_DIVISOR
        weight = max(weight_lb, dimensional_weight)

        for fee_range in self.fee_lookup[size]:
            min_weight = fee_range["min_weight"]
            max_weight = fee_range["max_weight"]
            fee_formula = fee_range["fee"]

            if min_weight < weight <= max_weight:
                if isinstance(fee_formula, str):
                    # Handle the formula case, e.g., "7.17 + 0.16/half-lb above first 3 lb"
                    base_fee, variable_fee = fee_formula.split(" + ")
                    base_fee = float(base_fee)
                    variable_fee = float(variable_fee.split("/")[0])
                    extra_weight = weight - 3  # 3 lb is the first weight limit for this fee range
                    fee = base_fee + variable_fee * (extra_weight / 0.5)  # 0.5 lb is the increment for the variable fee
                else:
                    # Direct fee value
                    fee = fee_formula

                return fee, dimensional_weight

        # Handle special cases or raise an exception
        print(f"Product size might be wrong!! Weight: {weight}, Size: {size}")
        return None, dimensional_weight

    def sizeTier_single(self, itemassumption):
        #weight constraints are in pound (lb)
        #measures in inches
        amazon_sizes = self.sizes

        sides =[]
        sizeclass= "NA"
        
        weight_lb = (itemassumption["Weight (gr)"])*0.00220462262
        length_inch = (itemassumption["Package Length (cm)"])*0.393791
        height_inch = itemassumption["Package Height (cm)"]*0.393791
        width_inch = itemassumption["Package Width (cm)"]*0.393791
        
        sides.append(length_inch)
        sides.append(height_inch)
        sides.append(width_inch)
        sides.sort() #sorts from shortest to longest
        
        longestside = sides[2]#last item of the list is the longest side
        medianside = sides[1]
        shortestside = sides[0]
        lengthgirth = ((medianside + shortestside) *2) + longestside

        if (weight_lb <=1 and longestside <= 15 and medianside <= 12 and shortestside <= 0.75):
            sizeclass = amazon_sizes[0]
        elif (weight_lb <=20 and longestside <= 18 and medianside <= 14 and shortestside <= 8):
            sizeclass = amazon_sizes[1]
        elif (weight_lb <=70 and longestside <= 60 and medianside <= 30 and lengthgirth <= 130):
            sizeclass = amazon_sizes[2]
        elif (weight_lb <=150 and longestside <= 108 and lengthgirth <= 130):
            sizeclass = amazon_sizes[3]
        elif (weight_lb <=150 and longestside <= 108 and lengthgirth <= 165):
            sizeclass = amazon_sizes[4]
        elif (weight_lb >=150 and longestside >= 108 and lengthgirth >= 165):
            sizeclass = amazon_sizes[5]

        returning = [sizeclass,sides,weight_lb]
        return returning
    
    def lowPriceControl(self,itemassumption, price):
        if price != "-":
            price = float(price)
            lowpricecheck = ""       
                    
            priceassigned ="YES"
            if pd.isna(price):
                priceassigned = "NONE"
            
            
            if(price < 10) and priceassigned =="YES":
                lowpricecheck ="TRUE"
            else:
                lowpricecheck ="FALSE"
        
            return lowpricecheck
        else:
            this = "-"
            return this
        
    def highpriceFBACalculation_single(self,itemassumption,size):
        
        #for index, itemassumption in itemassumptions.iterrows():
        side1 =itemassumption["Package Length (cm)"]*0.393700787
        side2 =itemassumption["Package Width (cm)"]*0.393700787
        side3 =itemassumption["Package Height (cm)"]*0.393700787
        
        dimensionalweight = (side1 * side2 * side3) / 139
        fbaFee = 0
        unit_weight =itemassumption["Weight (gr)"] *0.00220462262
        name = itemassumption["New Products"]
        weight = unit_weight
      
        #for not appearal and dangerous goods
        if size == self.sizes[0]:
        #small standart
            weight = unit_weight
            if (weight <= 0.25):
                fbaFee = 3.22
            elif (0.25 < weight <= 0.5):
                fbaFee = 3.40
            elif (0.5 < weight <= 0.75):
                fbaFee = 3.58
            elif (0.75 < weight <= 16):
                fbaFee = 3.77

        elif size == self.sizes[1]:
        #large standart
            if (unit_weight >= dimensionalweight):
                weight = unit_weight
            else:
                weight = dimensionalweight
                
            if (0<weight <=0.25):
                fbaFee = 3.86
            elif (0.25<weight <=0.5):
                fbaFee = 4.08
            elif (0.5<weight <=0.75):
                fbaFee = 4.24
            elif (0.75<weight <=1):
                fbaFee = 4.75
            elif (1<weight <=1.5):
                fbaFee = 5.40
            elif (1.5<weight <=2):
                fbaFee = 5.69
            elif (2 < weight <=2.5):
                fbaFee = 6.10
            elif (2.5 < weight <=3):
                fbaFee = 6.39
            elif(3 < weight <=20):
                fbaFee = 7.17 + (0.16) * ((weight-3)/2)
            else:
                print(name,weight,"exceeding 20 lbs")

        elif size == self.sizes[2]:            
        #small oversize
            if (unit_weight >= dimensionalweight):
                weight = unit_weight
            else:
                weight = dimensionalweight
                
            if weight <= 70:
                fbaFee = 9.73 + (0.42) * (weight-1)
            else:
                print("product size might be wrong!!")


        elif size == self.sizes[3]:
        #med oversize
            if (unit_weight >= dimensionalweight):
                weight = unit_weight
            else:
                weight = dimensionalweight
            
            if weight <= 150:
                fbaFee = 19.05  + (0.42) * (weight-1)
            else:
                print("product size might be wrong!!")

        elif size == self.sizes[4]:
            #large oversize
            if (unit_weight >= dimensionalweight):
                weight = unit_weight
            else:
                weight = dimensionalweight
            

            if weight <= 150:
                fbaFee = 89.98  + (0.83) * (weight-90)
            else:
                print("product size might be wrong!!")

        elif size == self.sizes[5]:
            #special oversize
            weight = unit_weight
            if weight >= 150:
                fbaFee = 158.49  + (0.83) * (weight-90)
            else:
                print("product size might be wrong!!")

        return fbaFee, dimensionalweight
    
    def US_fee(self, assumptions):
        for index, itemassumption in assumptions.iterrows():
            product = itemassumption["New Products"]
            returning = self.sizeTier_single(itemassumption)
            sizetier = returning[0]
            sides = returning[1]
            weight_lb = returning[2]
            country = "US"
            prices = Data.salesprices

            unitprice = prices[prices['Pricing (in market currency)'] == product][country].iloc[0]
            lowprice = self.lowPriceControl(itemassumption, unitprice)

            if lowprice == "TRUE":
                fee, dimensionalweight = self.lowpriceFBACalculation_single(itemassumption, sizetier)
            elif lowprice == "FALSE":
                fee, dimensionalweight = self.highpriceFBACalculation_single(itemassumption, sizetier)

            assign = {"Product": product, "Low Price": lowprice, "Dimensions (inch)": sides, "Weight (lb)": weight_lb, "Dimensional Weight": dimensionalweight, "Size Tier": sizetier, "US FBA Fee": fee}
            self.fees = pd.concat([self.fees, pd.DataFrame([assign])], ignore_index=True)

        return self.fees

    def get_fee(self, product):
        self.fees = self.US_fee(Data.assumptions)
        df = self.fees
        fee = df[df["Product"] == product]["US FBA Fee"]
        return fee

"""