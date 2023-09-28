# Import the Streamlit library
import streamlit as st
from main import *
from data import *
import io
import os
from datetime import datetime
from datetime import date
import pydeck as pdk
from streamlit_folium import folium_static
import folium
data,profitmargin_instance = initialize()
def highlight_rows(row, list_to_highlight):
    return ['background-color: #8a4c4c; color: yellow' if row.name in list_to_highlight else '' for _ in row]

def highlight_rows_with_rounding(row, list):
    # Check if the row should be highlighted
    styles = ['background-color: #8a4c4c; color: yellow' if row.name in list else '' for _ in row]
    
    # Round numeric values to 2 decimal places and format them
    formatted_row = []
    for value in row:
        if isinstance(value, (float, int)):
            formatted_value = f"{value:.2f}"
        else:
            formatted_value = value
        formatted_row.append(formatted_value)
    
    # Combine the styles and the formatted values
    styled_row = [f"{style}; {value}" for style, value in zip(styles, formatted_row)]
    
    return styled_row
productlist = data.assumptions["New Products"]

st.set_page_config(layout="wide", 
                   page_title="Feasibility",
                   page_icon="🥳",
                   menu_items={"About":None})
# Title of the app
st.title("New Era of Feasibility")

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Home", "Summary","Trials","Try Price","About", "Updates", "Data"])

datamap = [
    {"latitude": 37.0902, "longitude": -95.7129, "label": "US"},
    {"latitude": 56.1304, "longitude": -106.3468, "label": "CA"},
    {"latitude": 51.1657, "longitude": 10.4515, "label": "DE"},
    {"latitude": 55.3781, "longitude": -3.4359, "label": "UK"},
]

view_state = pdk.ViewState(
    latitude=45,  # Roughly centered
    longitude=-40,
    zoom=0,  # Zoom level (1 is quite zoomed out)
    pitch=0,
    bearing=0,
)
# Create the deck object
deck = pdk.Deck(
    map_style="mapbox://styles/mapbox/dark-v9",  # Dark map style
    initial_view_state=view_state,
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=datamap,
            get_position=["longitude", "latitude"],
            get_radius=100000,  # Adjust the size of the dots here
            get_fill_color=[255, 0, 0],  # Red color
            pickable=True,
            opacity=0.6,
        ),
        pdk.Layer(
            "TextLayer",
            data=datamap,
            get_position=["longitude", "latitude"],
            get_text="label",
            get_color=[255, 255, 255],  # White color
            get_size=16,
            get_angle=0,
            get_text_anchor="middle",
            get_alignment_baseline="center",
        ),
    ],
)

# Render the map in Streamlit

# Home Page
if selection == "Home":
    def main():
        st.subheader("Welcome!")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.text("Active Countries")
            st.pydeck_chart(deck)
        with col2:
            st.text("Active Products in the Database")
            st.table(data.assumptions["New Products"])


        with col3:
            current_date = date.today()
            formatted_date = current_date.strftime('%A-%d-%B')  # This will format the date as Day-DayNumber-Month
            # Display the date in a box using Streamlit
            st.markdown(f"""
                <div style="border:1px white; padding:10px; border-radius:5px; text-align:center; background:green">
                    <strong>{formatted_date}</strong>
                </div>
            """, unsafe_allow_html=True)

            # Check if the month is within peak season
            if current_date.month in [9, 10, 11, 12]:  # 9=September, 10=October, 11=November, 12=December
                season = "peak season"
            else:
                season = "nonpeak season"

            st.markdown(f"""
                <div style="border:1px white; padding:10px; border-radius:5px; text-align:center; background:red">
                    <strong>{season}</strong>
                </div>
            """, unsafe_allow_html=True)


                



    # Run the Streamlit app
    if __name__ == "__main__":
        main()

# Try Price Page
elif selection == "Trials":
    st.title("Trials")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        salesprices = data.salesprices
        
        product_name = st.selectbox("Product Name:", productlist)
        #cogs
        cogs = st.text_input("COGS (USD):", "1.2")
        country = st.selectbox("Marketplace", ["US", "CA", "UK", "DE"])
        scenario = st.selectbox("Scenario of Performance", ["Performing Scenerio", "Non-Performing Scenerio"])
        performance = st.selectbox("Scenario of Shipment:", ["Best","Worst"])
        #shipmentcost
        shipmentcost = st.text_input("Shipment Cost (USD):", "0.05")
        #fba
        fba = st.text_input("FBA Fee:", "")
        #season
        season = st.selectbox("Season", ["Peak", "Non-peak"])

        run_button = st.button("Get Product")
        
        

    with col2:
        currentprice = salesprices[salesprices['Pricing (in market currency)'] == product_name][country].iloc[0]
        result_df = profitmargin_instance.calling(product_name, country, scenario, performance, currentprice)
        original = profitmargin_instance.get_profit_margin(self=profitmargin_instance ,df=result_df)
        
        st.write("Current Price", currentprice)        
        tryprice = st.slider("Select a price", min_value=currentprice-10, max_value=currentprice+10, value=currentprice, step=0.1)
        
        result_df2 = profitmargin_instance.calling(product_name, country, scenario, performance, tryprice)
        st.table(result_df2)
        """
        vat_row = result_df2[result_df2['Variable'] == 'VAT']
        duty_row = result_df2[result_df2['Variable'] == 'DUTY']

        if not vat_row.empty and vat_row['Value'].iloc[0] != "-" and vat_row['Value'].iloc[0] != 0:
            thisrow = vat_row
        else:
            thisrow = duty_row
        rows_to_concat = [result_df2.iloc[[3]],result_df2.iloc[[17]],   thisrow,  result_df2.iloc[[15]],   result_df2.iloc[[16]],    result_df2.iloc[18:19], result_df2.iloc[[22]],result_df2.iloc[24:25]]
        selected_rows = pd.concat(rows_to_concat, axis=0)
        selected_rows = selected_rows.reset_index(drop=True)
        # Round and format the numeric values in the DataFrame
        for col in selected_rows.columns:
            if selected_rows[col].dtype in ['float64', 'int64']:
                selected_rows[col] = selected_rows[col].apply(lambda x: f"{x:.2f}")

        # Apply the styling
        rows_to_highlight = [3, 6]
        styled_df = selected_rows.style.apply(lambda row: highlight_rows(row, rows_to_highlight), axis=1)
        st.table(styled_df)
        """


    with col3:
        """       
        st.table(selected_rows)
        edited = profitmargin.get_profit_margin(self=prof, df=result_df2)

        data1 = {'Original Profit Margin': original,
         'Re-priced Profit Margin': edited}
        
        st.table(data1)
        """
    
    with col4:
        st.write("Profit Margin Table:")

elif selection == "Try Price":
    st.title("Try Price")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        salesprices = data.salesprices
        product_name = st.selectbox("Product Name:", productlist)
        country = st.selectbox("Marketplace", ["US", "CA", "DE", "UK"])
        scenario = st.selectbox("Scenario of Performance", ["Performing Scenerio", "Non-Performing Scenerio"])
        performance = st.selectbox("Scenario of Shipment:", ["Best","Worst"])
        run_button = st.button("Get Product")
        currentprice = salesprices[salesprices['Pricing (in market currency)'] == product_name][country].iloc[0]
       
    with col2:
        st.write("Current Price", currentprice)        
        tryprice = st.slider("Select a price", min_value=currentprice-10, max_value=currentprice+10, value=currentprice, step=0.1)

        result_df=profitmargin_instance.calling(data, product_name, country, scenario, performance, currentprice)
        original = profitmargin_instance.get_profitmargin(data, product_name, country, scenario , performance, currentprice)
         
        result_df2 = profitmargin_instance.calling(data, product_name, country, scenario, performance, tryprice)
        
        result_df2 = result_df2.applymap(lambda x: round(x, 2) if isinstance(x, (float, int)) else x)

      
        edited = profitmargin_instance.get_profitmargin(data, product_name, country, scenario , performance, tryprice)
        
        data1 = {'Original Profit Margin': original,
        'Re-priced Profit Margin': edited}
        
        st.table(data1)
    
    with col3:
        st.write("Original Table")
        st.table(result_df)
    with col4:
        st.write("Re-priced Table")
        st.table(result_df2)

                    
        # Round numeric columns to 2 decimal places

elif selection == "About":
    st.title("About This App")
    
    st.header("Purpose")
    st.write("""
    The purpose of this app is to provide a robust and efficient way to analyze various aspects of product feasibility.
    It aims to simplify complex calculations related to shipping, storage, and profit margins.
    """)

    st.header("Who Created This App?")
    st.write("""
    This app was created by the one and only Supply Chain and New Product Development department, a team dedicated to providing data-driven solutions for our businesses.
    """)

    st.header("How to Use This App")
    st.write("""
    1. **Data Input**: Upload your data using the upload button.
    2. **Analysis**: Choose the type of analysis you want to perform.
    3. **Results**: View the results in table or chart format.
    4. **Download**: You can also download the results for further analysis.
    """)

    st.header("Contact Us")
    st.write("""
    Feel free to contact me at [elifnurozturk@robustventures.com](mailto:elifnurozturk@robustventures.com) for any questions or feedback. (Or, you know, just message me on teams :)
    """)

    st.header("Version")
    st.write("1.0.0")


elif selection == "Updates":
    st.header("Updates & LOGS")
    st.write("""
    24.09.2023 - Base Model implemented. 
    """)

# Data Page
elif selection == "Data":
    # Function to display DataFrames
    def display_data():
        st.table(newproducts)
        st.table(scenarios)

    # Function to get selected DataFrame
    def get_selected_df(selected_df):
        if selected_df == "New Product Assumptions":
            return newproducts
        elif selected_df == "Shipment Scnearios":
            return scenarios
        

    st.header("Database")
    st.write("Last Updated: 24.04.2023")

    # Get DataFrames
    newproducts = data.assumptions
    scenarios = data.scenarios

    # Dropdown to select DataFrame
    selected_df = st.selectbox("Select a dataset to export", ["New Product Assumptions", "Shipment Scnearios"])

    # Get the selected DataFrame
    df_to_download = get_selected_df(selected_df)

    # Temporary Excel file
    temp_file = "temp.xlsx"

    # Save DataFrame to Excel on server side
    df_to_download.to_excel(temp_file, index=False)

    # Create a download button
    with open(temp_file, "rb") as f:
        bytes_data = f.read()
        st.download_button(
            label="Download Excel File",
            data=io.BytesIO(bytes_data),
            file_name=f"{selected_df}_{datetime.now().strftime('%Y-%m-%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # Remove the temporary file
    os.remove(temp_file)

elif selection == "Summary":
    
    st.header("Profit Margin Summary")

    # Define the list of countries
    #countries =  ["US", "CA", "DE", "UK", "FR", "IT", "ES", "NL", "SE", "PL" ]
    countries =["US", "CA", "DE", "UK"]
    # Get the list of products from Data.assumptions
    products = data.assumptions['New Products'].tolist()
    st.write(products)

    # Initialize an empty DataFrame to store the matrix
    profit_margin_matrix = pd.DataFrame(index=products, columns=countries)

    # Initialize the object for the profitmargin class


    # Populate the matrix
    for product in products:
        for country in countries:
            try:
                profit_margin = profitmargin_instance.get_profitmargin(data,product, country)
                profit_margin_matrix.loc[product, country] = profit_margin
            except Exception as e:
                profit_margin_matrix.loc[product, country] = "-"

    # Display the matrix in Streamlit
    st.table(profit_margin_matrix)    
    
