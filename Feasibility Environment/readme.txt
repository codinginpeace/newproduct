List of Functions in FBAus Class
__init__: Initializes the class with default values and data structures.

To Update: If you need to add more columns or change the default values, update this function.
convert_units: Converts units from grams and centimeters to pounds and inches.

To Update: If the unit conversion logic changes, update this function.
sizeTier_single: Determines the Amazon size tier for a single product based on its dimensions and weight.

To Update: If Amazon changes the size tier criteria, update this function.
lowPriceControl: Checks if the product's price is considered "low" based on a given threshold.

To Update: If the low price criteria change, update this function.
lowpriceFBACalculation_single: Calculates the FBA fee for a single product considered to have a "low" price.

To Update: If the fee structure for low-priced items changes, update this function.
highpriceFBACalculation_single: Calculates the FBA fee for a single product considered to have a "high" price.

To Update: If the fee structure for high-priced items changes, update this function.
US_fee: Calculates the FBA fees for all products in the U.S. and updates the fees DataFrame.

To Update: If you need to add more countries or change the fee calculation logic, update this function.
get_fee: Retrieves the FBA fee for a specific product.

To Update: If the way fees are retrieved changes, update this function.
How to Update the Class
Updating Fees:

The fees are stored in a separate Python dictionary (fee_config.py). Update the FBA_FEES dictionary in this file to reflect any changes in the fee structure.
Adding New Countries:

If you plan to add support for more countries, you might want to extend the US_fee function or create similar functions for other countries.
Changing Size Tiers or Price Criteria:

Update the sizeTier_single and lowPriceControl functions to reflect any changes in the size tier or price criteria.
Unit Conversion:

If the unit conversion logic changes, update the convert_units function.
Data Columns:

If you need to add or remove columns in the fees DataFrame, update the __init__ function.