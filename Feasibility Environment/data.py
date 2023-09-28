import pandas as pd

class Data:
    
    def __init__(self, file_path="C:\\Users\\ElifnurÖztürk\\Desktop\\Feasibility Environment\\Database\\Main Database.xlsx"):    
          
        self.file_path = file_path
        self.scenarios = None
        self.shipmentcosts = None
        self.assumptions = None
        self.masterdata = None
        self.vat = None
        self.duty = None
        self.storage = None
        self.referral = None     
        self.salesprices = None   
        self.AverageShipmentCosts= None
        self.shipmentCosts= None

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
    
    def handle_file_upload(self, file_path=None):
        print(f"Attempting to load data from {self.file_path}...")

        if file_path is not None:
            self.file_path = file_path

        # Ensure the given path exists
        try:
            # Read data from each sheet
            self.scenarios = pd.read_excel(self.file_path, sheet_name='Shipment Scenarios')
            self.shipmentcosts = pd.read_excel(self.file_path, sheet_name='Shipment Costs Info')                
            self.assumptions = pd.read_excel(self.file_path, sheet_name='New Product Assumptions')
            self.vat = pd.read_excel(self.file_path, sheet_name='VAT Rates')      
            self.duty = pd.read_excel(self.file_path, sheet_name='DUTY Rates')       
            self.storage = pd.read_excel(self.file_path, sheet_name='Amazon Storage Fees')          
            self.referral = pd.read_excel(self.file_path, sheet_name='Amazon Referral Fees')      
            self.masterdata = pd.read_excel(self.file_path, sheet_name='Master Data')    
            self.salesprices = pd.read_excel(self.file_path, sheet_name='Sales Prices')  
            self.AverageShipmentCosts = self.calculate_average_shipping_cost(self.shipmentcosts)
            
            # Display a message indicating that the data has been loaded
            print("Data from all sheets loaded successfully.")
        except FileNotFoundError:
            print(f"The file {self.file_path} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

# Main function
if __name__ == "__main__":
    data_instance = Data()
    data_instance.handle_file_upload()
