import pandas as pd
from data import *
from FBAsizes import *

class newProduct():
    def __init__(self, data_instance):
        self.assumptions = data_instance.assumptions
        
    def alternativesCheck(self,df):
        """
        Function to check and update the 'Alternative' column in the dataframe.
        """
        product_counts = df['New Products'].value_counts().to_dict()

        for product, count in product_counts.items():
            if count == 1:
                df.loc[df['New Products'] == product, 'Alternative'] = 1
            else:
                df.loc[df['New Products'] == product, 'Alternative'] = df[df['New Products'] == product].groupby('New Products').cumcount() + 1

        return df

    def get_sizeTier(self, product_details, country):
        fbasize_calculator = FBASizeCalculator()
        
        weight = product_details["weight"]
        length = product_details["packageL"]
        height = product_details["packageH"]
        width = product_details["packageW"]
        
        dimensions = sorted([length, width, height])
        sizetier, weight_in_unit = fbasize_calculator.determine_size_tier(weight, dimensions, country)

        if "standard" in sizetier.lower():
            short_size = "Standard-size"
        else:
            short_size = "Oversize"
        return sizetier, short_size
    """
    def sizeTier(itemassumption, country):
        if country == "US":
            amazon_sizes = ["Standard Size", "Over Size"]
            sides = []
            sizeclass = "NA"

            weight_lb = (itemassumption["Weight (gr)"].iloc[0]) * 0.00220462262
            length_inch = (itemassumption["Package Length (cm)"].iloc[0]) * 0.393791
            height_inch = (itemassumption["Package Height (cm)"].iloc[0]) * 0.393791
            width_inch = (itemassumption["Package Width (cm)"].iloc[0]) * 0.393791

            sides.extend([length_inch, height_inch, width_inch])
            sides.sort()  # sorts from shortest to longest

            longestside = sides[2]
            medianside = sides[1]
            shortestside = sides[0]
            lengthgirth = ((medianside + shortestside) * 2) + longestside

            if (weight_lb <= 1 and longestside <= 15 and medianside <= 12 and shortestside <= 0.75):
                sizeclass = amazon_sizes[0]
            elif (weight_lb <= 20 and longestside <= 18 and medianside <= 14 and shortestside <= 8):
                sizeclass = amazon_sizes[0]
            elif (weight_lb <= 150 and 
                ( 
                    (weight_lb <= 70 and longestside <= 60 and medianside <= 30 and lengthgirth <= 130) or
                    (longestside <= 108 and lengthgirth <= 165)
                )
                ):
                sizeclass = amazon_sizes[1]
            else:
                sizeclass = "Unknown Size"

            return sizeclass
"""
    def productcubicfeet(self, itemassumption):
        volume_cm3 = itemassumption['packageL'] * itemassumption['packageW'] * itemassumption['packageH']
        # Convert the volume to cubic feet
        volume_ft3 = (volume_cm3 / 1000000) * 35.315

        return volume_ft3
