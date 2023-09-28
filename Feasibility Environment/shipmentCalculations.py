import math
import pandas as pd
from data import *
import numpy as np

class calculations(Data):
    #reviewed
    def __init__(self, data_instance):
        #assumptions of palet types, weights are here
        self.shipmentCosts = data_instance.shipmentcosts
        self.assumptions = data_instance.assumptions
        self.AverageShipmentCosts = data_instance.AverageShipmentCosts

        #palet dimensions, palet weight, max height according to shipment method, maximum weight of the palet
        self.paletTypes = {
            "US": [[100, 120], 30, {"Sea": 165, "Air": 140, "Ground": 235},900],
            "US - Main": [[100, 120], 30, {"Sea": 165, "Air": 140, "Ground": 235},650],
            "CA": [[100, 120], 30, {"Sea": 165, "Air": 140, "Ground": 235},900],
            "CA - Main": [[100, 120], 30, {"Sea": 165, "Air": 140, "Ground": 235},650],
            "EU": [[80, 120], 25, {"Sea": 165, "Air": 140, "Ground": 230},1000],
            "EU - Main": [[80, 120], 25, {"Sea": 165, "Air": 140, "Ground": 230},650],
            "UK": [[100, 120], 30, {"Sea": 165, "Air": 140, "Ground": 235},900],
            "UAE": [[80, 120], 25, {"Sea": 165, "Air": 140, "Ground": 230},650],
            "JAP": [[80, 120], 25, {"Sea": 165, "Air": 140, "Ground": 230},1000],
            "AU": [[80, 120], 25, {"Sea": 165, "Air": 140, "Ground": 230},1000],
            }
        #master carton weight assumption
        self.masterCartonGram = 300
        
        # Error margin for box filler
        self.error_margin_boxfiller = 0.001
        
        #raw pallet weight assumption
        self.rawPalletWeight = 30

        self.transport_map = {
            "CN": {
                "destinations": ["US - Main", "EU - Main", "CA - Main","US", "EU", "UK", "CA", "JAP", "UAE", "AU"],
                "Ground": [],
                "Sea": ["US - Main", "EU - Main", "CA - Main","US", "EU", "UK", "CA", "JAP", "UAE", "AU"],
                "Air": ["US - Main", "EU - Main", "CA - Main","US", "EU", "UK", "CA", "JAP", "UAE", "AU"]
            },
            "TR": {
                "destinations": ["US - Main", "EU - Main", "CA - Main","US", "EU", "CA", "UK", "JAP", "UAE", "AU"],
                "Ground": ["EU - Main", "EU", "UK"],
                "Sea": ["US - Main", "CA - Main","EU - Main", "US", "CA", "EU", "UK", "JAP", "UAE", "AU"],
                "Air":  ["US - Main", "EU - Main", "CA - Main","US", "EU", "CA", "UK", "JAP", "UAE", "AU"]
            },
        }
        
        self.wh_transport_map = {
            
            "US - Main": {
                "destinations": ["US", "CA"],
                "Ground": ["US","CA"],
                "Sea": [],
                "Air": ["US", "CA"]
            },
            
            "EU - Main": {
                "destinations": ["EU"],
                "Ground": ["EU"],
                "Sea": [],
                "Air": ["EU"]
            },
            
            "CA - Main": {
                "destinations": ["CA"],
                "Ground": ["CA"],
                "Sea": [],
                "Air": ["CA"]}
            
        }
            
    #reviewed
    def calculate_average_shipping_cost(self, shipmentCosts_df=None):
        if shipmentCosts_df is None:
            shipmentCosts_df = self.shipmentCosts
            
        if shipmentCosts_df is not None:
            # Columns to group by
            grouping_columns = ['Shipping Method', 'Origin', 'Destination', 'Loading Type']

            # Perform the groupby operation and aggregation
            self.AverageShipmentCosts = shipmentCosts_df.groupby(grouping_columns)['Shipping Cost/Pallet (USD)'].mean().reset_index()

            # Rename the aggregated column
            self.AverageShipmentCosts = self.AverageShipmentCosts.rename(columns={'Shipping Cost/Pallet (USD)': 'Average Shipping Cost/Pallet (USD)'})
        else:
            print("No shipment costs data provided.")
            
        print("All scenarios updated with average shipment costs.")
            
        return self.AverageShipmentCosts

        
    def _totalCost(self, row):
        if pd.isna(row["COGS"]): 
            total = (row["Landed Cost"] + row["Other Costs"])
            row["COGS"] = total
        
        return row

    def update_TotalCost(self, assumptions_df=None):
        if assumptions_df is None:
            assumptions_df = self.assumptions
        assumptions_df = assumptions_df.apply(self._totalCost, axis=1)
        
        print("Total costs updated.")
        return assumptions_df
    
    #reviewed
    def available_shipments(self, origin=None, dest=None):
    # Define the transportation options for each origin
    #according to origin and destination, check methods
        transport_map = self.transport_map
        available_methods = []
        # Check if the transport_maporigin exists within transport_map
        if origin in transport_map:
            for method, destinations in transport_map[origin].items():
                # Don't check "destinations" key as it's a special key for listing out all destinations
                if method != "destinations" and dest in destinations:
                    available_methods.append(method)
                    
        return available_methods
    
        #reviewed this with chat gpt, need to make sure if it works correctly        
    def populate_shipment_scenarios(self, shipmentScenarios=None, assumptions=None):
        if not isinstance(assumptions, pd.DataFrame) or assumptions.empty:
            print("Error: Invalid or empty assumptions DataFrame provided.")
            return

        loadingTypes = ["Pallet", "FTL - 20FT", "FTL - 40HC"]
        new_rows = []

        # Loop through each row in assumptions
        for index, row in assumptions.iterrows():
            try:
                currentProd = row['New Products']
                origin = row["Supplier"]

                # Check if all scenarios exist in shipmentScenarios dataframe for the current product
                if origin in self.transport_map:
                    for method in ["Ground", "Sea", "Air"]:
                        if method not in self.transport_map[origin]:
                            continue

                        for dest in self.transport_map[origin][method]:
                            loads = loadingTypes if method == "Sea" else ["Pallet"]
                            for loadtype in loads:
                                scenario_exists = shipmentScenarios[
                                    (shipmentScenarios['Product Name'] == currentProd) &
                                    (shipmentScenarios['Shipment Method'] == method) &
                                    (shipmentScenarios['Origin'] == origin) &
                                    (shipmentScenarios['Destination'] == dest) &
                                    (shipmentScenarios['Loading Type'] == loadtype)
                                ].shape[0] > 0

                                if not scenario_exists:
                                    new_rows.append({
                                        'ASIN': None,
                                        'Product Name': currentProd,
                                        'Shipment Method': method,
                                        'Origin': origin,
                                        'Destination': dest,
                                        'Loading Type': loadtype
                                    })

                # Similar check for warehouse scenarios
                for wh in self.wh_transport_map:
                    if wh in self.transport_map[origin]['destinations']:
                        for wh_method in ["Ground", "Sea", "Air"]:
                            if wh_method not in self.wh_transport_map[wh]:
                                continue

                            for final_dest in self.wh_transport_map[wh][wh_method]:
                                loads = loadingTypes if wh_method == "Sea" else ["Pallet"]
                                for loadtype in loads:
                                    scenario_exists = shipmentScenarios[
                                        (shipmentScenarios['Product Name'] == currentProd) &
                                        (shipmentScenarios['Shipment Method'] == wh_method) &
                                        (shipmentScenarios['Origin'] == wh) &
                                        (shipmentScenarios['Destination'] == final_dest) &
                                        (shipmentScenarios['Loading Type'] == loadtype)
                                    ].shape[0] > 0

                                    if not scenario_exists:
                                        new_rows.append({
                                            'ASIN': None,
                                            'Product Name': currentProd,
                                            'Shipment Method': wh_method,
                                            'Origin': wh,
                                            'Destination': final_dest,
                                            'Loading Type': loadtype
                                        })

            except KeyError as e:
                print(f"Error processing row {index}. Missing key: {e}")
            except Exception as e:
                print(f"Unexpected error processing row {index}: {e}")

        # Add new rows to shipmentScenarios
        try:
            shipmentScenarios = pd.concat([shipmentScenarios, pd.DataFrame(new_rows)], ignore_index=True)
        except Exception as e:
            print(f"Error appending new rows to shipmentScenarios: {e}")

        return shipmentScenarios



    #edited - reviewed, check later again
    def check_products_scenario(self, assumptions=None, shipmentScenarios=None):
        if not isinstance(assumptions, pd.DataFrame) or assumptions.empty:
            print("Error: Invalid or empty assumptions DataFrame provided.")
            return

        
        shipmentScenarios = self.populate_shipment_scenarios(shipmentScenarios, assumptions)  # Let this function handle the addition of rows
        missing_names = []
        # Loop through each product name in the assumptions table
        for idx, product in assumptions.iterrows():
            try:
                if product["New Products"] not in shipmentScenarios["Product Name"].values:
                    missing_names.append(product["New Products"])
            except KeyError as e:
                print(f"Error processing row {idx}. Missing key: {e}")
            except Exception as e:
                print(f"Unexpected error processing row {idx}: {e}")

        else:
            print("All product names in 'assumptions' are present in 'shipmentScenarios'.")

        print("All new products are now available with their scenario.")

        return shipmentScenarios

    #reviewed by chat gpt
    def get_suggestive_carton_dimensions(self, packageW, packageL, packageH, packageWeight, error_margin=0.20):
        # Check for invalid package dimensions or weight
        if any(dim <= 0 for dim in [packageW, packageL, packageH, packageWeight]):
            print("Error: Invalid package dimensions or weight provided.")
            return (0, 0, 0), 0

        # Assumptions (Constraints)
        error_factor = 1 - error_margin

        pallet_dimensions = [(100, 120), (80, 120)]
        master_carton_min_dims = (15, 10, 2.5)  # Width, Length, Height in cm
        master_carton_max_dim = 63.5  # Maximum allowable dimension for each side in cm
        master_carton_max_weight = 20  # in kilograms
        master_carton_weight = 0.3  # Weight of the master carton itself in kilograms
        max_products_per_carton = 50  # Maximum number of products per master carton

        best_dims = (0, 0, 0)
        best_count = 0

        # Determine the number of products that fit in each dimension outside the loop
        products_fit_by_dim_width = master_carton_max_dim // packageW
        products_fit_by_dim_length = master_carton_max_dim // packageL
        products_fit_by_dim_height = master_carton_max_dim // packageH

        max_products_by_weight = (master_carton_max_weight - master_carton_weight) // packageWeight

        for palletW, palletL in pallet_dimensions:
            # Adjust pallet dimensions to account for the carton's own dimension and the error margin
            adjusted_palletW = palletW * error_factor
            adjusted_palletL = palletL * error_factor

            # Determine the number of products that fit in each dimension
            products_fit_width = min(adjusted_palletW // packageW, products_fit_by_dim_width)
            products_fit_length = min(adjusted_palletL // packageL, products_fit_by_dim_length)

            # Calculate the maximum number of products that can be fit height-wise based on weight constraint
            max_height_by_weight = max_products_by_weight // (products_fit_width * products_fit_length)
            products_fit_height = min(adjusted_palletW // packageH, products_fit_by_dim_height, max_height_by_weight)

            # Apply the minimum constraints on dimensions
            products_fit_width = max(products_fit_width, master_carton_min_dims[0] // packageW)
            products_fit_length = max(products_fit_length, master_carton_min_dims[1] // packageL)
            products_fit_height = max(products_fit_height, master_carton_min_dims[2] // packageH)

            # Suggestive master carton dimensions
            suggestive_cartonW = packageW * products_fit_width
            suggestive_cartonL = packageL * products_fit_length
            suggestive_cartonH = packageH * products_fit_height

            # Number of products fit into 1 master carton
            products_per_carton = int(products_fit_width) * int(products_fit_length) * int(products_fit_height)
            

            products_per_carton = min(products_per_carton, max_products_per_carton)

            # Update best results
            current_count = products_per_carton * int(adjusted_palletW // suggestive_cartonW) * int(adjusted_palletL // suggestive_cartonL) * int(palletW // suggestive_cartonH)

            if current_count > best_count:
                best_count = current_count
                best_dims = (suggestive_cartonW, suggestive_cartonL, suggestive_cartonH)

        return best_dims, products_per_carton

    #reviewed by chat gpt
    def update_master_carton_dimensions(self, shipmentScenarios=None, assumptions=None):
        # Create a map for faster lookup of product information
        product_map = {row["New Products"]: {
            "width": float(row["Package Width (cm)"]),
            "length": float(row["Package Length (cm)"]),
            "height": float(row["Package Height (cm)"]),
            "weight": float(row["Weight (gr)"]) / 1000  # Convert to kilograms
        } for _, row in assumptions.iterrows()}
        
        for index, row in shipmentScenarios.iterrows():
            # Check if Master Carton Dimensions column or Items per Master Carton is empty or NaN
            if pd.isna(row["Master Carton Dimensions"]) or pd.isna(row["Items per Master Carton"]):
                currentProd = row["Product Name"]
            
                # Check if the product is in the product map
                if currentProd in product_map:
                    packageW = product_map[currentProd]["width"]
                    packageL = product_map[currentProd]["length"]
                    packageH = product_map[currentProd]["height"]
                    prodWeight = product_map[currentProd]["weight"]

                    # Get suggestive carton dimensions

                    masterCartonDims, products_per_carton = self.get_suggestive_carton_dimensions(packageW, packageL, packageH, prodWeight)

                    # Check for invalid carton dimensions
                    if masterCartonDims == (0, 0, 0):
                        print(f"Error: Invalid dimensions for product '{currentProd}'.")
                        continue

                    # Format the dimensions to the desired string format
                    formatted_dims = " ".join([str(dim) for dim in masterCartonDims])
                    
                    # Update the shipmentScenarios dataframe with the new dimensions and products per carton
                    if pd.isna(row["Master Carton Dimensions"]):
                        shipmentScenarios.at[index, "Master Carton Dimensions"] = formatted_dims
                    if pd.isna(row["Items per Master Carton"]):
                        shipmentScenarios.at[index, "Items per Master Carton"] = products_per_carton

        print("Master carton dimensions are entered for missing items.")
        return shipmentScenarios

    #reviewed bt chat gpt. moved error margin to __inni__
    def box_filler(self, masterCartonDims=None, product_dims=None):
        # Error margin for the master carton dimensions
        error_factor = 1 - self.error_margin_boxfiller
        # Ensure input validity
        if masterCartonDims is None or product_dims is None:
            print("Error: Master carton dimensions or product dimensions not provided.")
            return 0

        if len(product_dims) != 3:
            print("Error: Invalid product dimensions provided.")
            return 0

        if any(dim == 0 for dim in product_dims):
            print("Error: Product has a dimension of zero.")
            return 0


        # Unpack the dimensions of the master carton and product
        try:
            box_dim = list(map(float, masterCartonDims.split(" ")))
        except ValueError:
            print("Error: Invalid format for master carton dimensions.")
            return 0
        
        mcL, mcW, mcH = box_dim[0], box_dim[1], box_dim[2]
        pL, pW, pH = product_dims

        # Applying the error rate on the master carton dimensions
        mcL, mcW, mcH = mcL * error_factor, mcW * error_factor, mcH * error_factor

        possible_orientations_mc = [(mcL, mcW, mcH), (mcL, mcH, mcW), (mcW, mcL, mcH), (mcW, mcH, mcL), (mcH, mcL, mcW), (mcH, mcW, mcL)]
        possible_orientations_p = [(pL, pW, pH), (pL, pH, pW), (pW, pL, pH), (pW, pH, pL), (pH, pL, pW), (pH, pW, pL)]

        max_units = 0

        # Check each orientation of the master carton against each orientation of the product
        for mc_orientation in possible_orientations_mc:
            for p_orientation in possible_orientations_p:
                units_lengthwise = math.floor(mc_orientation[0] / p_orientation[0])
                units_widthwise = math.floor(mc_orientation[1] / p_orientation[1])
                units_heightwise = math.floor(mc_orientation[2] / p_orientation[2])

                total_units = units_lengthwise * units_widthwise * units_heightwise

                if total_units > max_units:
                    max_units = total_units

        return max_units

    #reviewed bt chat gpt. moved error margin to __inni__
    def palet_sorter(self, shipmentScenario=None, masterCartonDims=None, itemweight=None):

        shipmentMethod = shipmentScenario["Shipment Method"]
        dest = shipmentScenario["Destination"]
        paletTypes = self.paletTypes

        palet_dims, paletWeight, height_limits, max_weight = paletTypes[dest]
        maxH = height_limits[shipmentMethod]
        leftH = float(maxH)
    
        #print("masterCartonDims dims: ",masterCartonDims)
        
        
        box_dim = list(map(float, masterCartonDims.split(" ")))
        
        #print("box dims: ",box_dim)
        
        
        total_boxes = 0
        total_weight = 0

        while leftH > 0 and (total_weight <= max_weight):
            possible_heights = [dim for dim in box_dim if dim <= leftH]
            solutions = []

            for height in possible_heights:
                idx = box_dim.index(height)
                other_dims = [box_dim[(idx+1)%3], box_dim[(idx+2)%3]]
                boxbase_area = other_dims[0] * other_dims[1]
                boxes_by_dim = [
                    (palet_dims[0] // dim) * (palet_dims[1] // (boxbase_area / dim))
                    for dim in other_dims
                ]
                solutions.append(max(boxes_by_dim))

            boxes_this_layer = max(solutions) if solutions else 0
            potential_total_weight = total_weight + boxes_this_layer * (itemweight / 1000)

            if boxes_this_layer == 0:  # Add this condition to check if we can't fit more boxes
                break

            if potential_total_weight <= max_weight:
                total_boxes += boxes_this_layer
                total_weight = potential_total_weight
                
                if solutions:  # Check if solutions list is not empty
                    leftH -= box_dim[solutions.index(boxes_this_layer)]
            else:
                break

        return total_boxes


    def update_shipment_info(self, shipmentScenarios, assumptions):
        # Constants
        rawPalletWeight = self.rawPalletWeight
        masterCartonWeightAssumption = self.masterCartonGram

        # Pre-filter the DataFrame to only include rows that need to be updated
        missing_values_mask = shipmentScenarios['Master Carton per Pallet'].isnull()  # Adjust this to your needs

        def update_row(row):
            currentProd = row['Product Name']
            assumptionofitem = assumptions.loc[assumptions['New Products'] == currentProd]
            
            if assumptionofitem.empty:
                return row  # No changes

            currentW = assumptionofitem["Weight (gr)"].values[0]
            masterCartonDims = row['Master Carton Dimensions']
            product_dims = [assumptionofitem.iloc[0]['Package Width (cm)'], assumptionofitem.iloc[0]['Package Length (cm)'], assumptionofitem.iloc[0]['Package Height (cm)']]

            boxes_per_pallet = self.palet_sorter(row, masterCartonDims, currentW)
            items_per_box = self.box_filler(masterCartonDims, product_dims)
            
            totalCW = ((items_per_box * currentW) + masterCartonWeightAssumption) / 1000
            totalPaletW = totalCW * boxes_per_pallet + rawPalletWeight

            row['Master Carton per Pallet'] = boxes_per_pallet
            row['Items per Master Carton'] = items_per_box
            row['Bulk Shipment Quantity'] = boxes_per_pallet * items_per_box
            row['Master Carton Weight (kg)'] = totalCW
            row['Pallet Weight (kg)'] = totalPaletW

            return row

        updated_shipmentScenarios = shipmentScenarios.loc[missing_values_mask].apply(update_row, axis=1)
        shipmentScenarios.update(updated_shipmentScenarios)

        print("Shipment details are entered to shipment scenarios.")
        return shipmentScenarios

        
    def update_shipmentScenarios_with_avg_costs(self, shipmentScenarios=None):
        for index, row in shipmentScenarios.iterrows():
            match = self.AverageShipmentCosts[
                    (self.AverageShipmentCosts['Shipping Method'] == row['Shipment Method']) &
                    (self.AverageShipmentCosts['Origin'] == row['Origin']) &
                    (self.AverageShipmentCosts['Destination'] == row['Destination']) &
                    (self.AverageShipmentCosts['Loading Type'] == row['Loading Type'])
                    ]

            # Check if a match is found
            if not match.empty:
                avg_cost = match['Average Shipping Cost/Pallet (USD)'].values[0]
                shipmentScenarios.at[index, 'Average Shipping Cost/Pallet (USD)'] = avg_cost
                bulk_qty = shipmentScenarios.at[index, 'Bulk Shipment Quantity']
                
                if not pd.isna(avg_cost) and bulk_qty and bulk_qty != 0:
                    shipmentScenarios.at[index, 'Estimated Shipment Cost per unit (USD)'] = avg_cost / bulk_qty
                else:
                    shipmentScenarios.at[index, 'Estimated Shipment Cost per unit (USD)'] = np.nan
            else:
                shipmentScenarios.at[index, 'Average Shipping Cost/Pallet (USD)'] = np.nan
                shipmentScenarios.at[index, 'Estimated Shipment Cost per unit (USD)'] = np.nan

        print("Shipment costs per item information is updated.")

        return shipmentScenarios

    
    
    
    def get_cost_extremes(self, shipmentScenarios, product, market):

        #first step
        #the shipment to warehouse

        min_cost_1= "-"
        min_cost_2 = "-"
        max_cost_1 = "-"
        max_cost_2 = "-"
        
        if market == "US" or market == "CA" :
            filtered_scenarios_1 = shipmentScenarios[
                (shipmentScenarios['Product Name'] == product) &
                (shipmentScenarios['Destination'] == str(market+" - Main") )
            ]
            
            filtered_scenarios_2 = shipmentScenarios[
                (shipmentScenarios['Product Name'] == product) &
                (shipmentScenarios['Origin'] == str(market+" - Main")) &
                (shipmentScenarios['Destination'] == str(market))
            ]
            
            min_cost_1 = filtered_scenarios_1['Estimated Shipment Cost per unit (USD)'].min()
            min_cost_2 = filtered_scenarios_2['Estimated Shipment Cost per unit (USD)'].min()
        
            #to fba icin kırılım            
            min_cost = min_cost_1 + min_cost_2
            
            max_cost_1 = filtered_scenarios_1['Estimated Shipment Cost per unit (USD)'].max()
            max_cost_2 = filtered_scenarios_2['Estimated Shipment Cost per unit (USD)'].max()
            max_cost = max_cost_1+ max_cost_2
            
            #print("filtered_scenarios_1 ", filtered_scenarios_1)
            #print("min_cost_1: ", min_cost_1)
            #print("filtered_scenarios_2 ", filtered_scenarios_2)
            #print("min_cost_2: ", min_cost_2)
            
        elif (market == ['DE','FR','IT','ES','NL','SE','BE','PL']):
            
            destination = "EU"
            filtered_scenarios_1 = shipmentScenarios[
                (shipmentScenarios['Product Name'] == product) &
                (shipmentScenarios['Destination'] == str(destination+" - Main") )
            ]
            
            filtered_scenarios_2 = shipmentScenarios[
                (shipmentScenarios['Product Name'] == product) &
                (shipmentScenarios['Origin'] == str(market+" - Main")) &
                (shipmentScenarios['Destination'] == str(market))
            ]
            min_cost_1 = filtered_scenarios_1['Estimated Shipment Cost per unit (USD)'].min()
            min_cost_2 = filtered_scenarios_2['Estimated Shipment Cost per unit (USD)'].min()
            min_cost = min_cost_1 + min_cost_2
            max_cost_1 = filtered_scenarios_1['Estimated Shipment Cost per unit (USD)'].max()
            max_cost_2 = filtered_scenarios_2['Estimated Shipment Cost per unit (USD)'].max()
            max_cost = max_cost_1+ max_cost_2  
            
            
            
        else: #countries like Jap, UAE, UK
            filtered_scenarios_1 = shipmentScenarios[
                (shipmentScenarios['Product Name'] == product) &
                (shipmentScenarios['Destination'] == str(market) )
            ]
            min_cost_1 = filtered_scenarios_1['Estimated Shipment Cost per unit (USD)'].min()
            min_cost = min_cost_1
            max_cost_1 = filtered_scenarios_1['Estimated Shipment Cost per unit (USD)'].max()
            max_cost = max_cost_1

        best_scenario = min_cost
        worst_scenario = max_cost

        # Return both scenarios
        return best_scenario, min_cost_1, min_cost_2 , worst_scenario, max_cost_1, max_cost_2