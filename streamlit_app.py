import streamlit
import snowflake.connector
import pandas
import requests
from urllib.error import URLError

streamlit.title('My Parents New Health Diner');
streamlit.header('Breakfast Favorites');
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal');
streamlit.text('🥗 Kale Spinach & Rocket Smoothie');
streamlit.text('🐔 Hard Boiled Free-Range Egg');
streamlit.text('🥑🍞 Avocado Toast');

# ********1st SECTION******************************************************************
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇');

# --------PANDA----------
#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt");
my_fruit_list = my_fruit_list.set_index('Fruit');

# Let's put a pick list here so they can pick the fruit they want to include 
# Pre-populate the drop-down
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries']);
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show);

# ********2nd SECTION**********************************************************************
# --------JSON----------

#define function get_fruityvice_data
def get_fruityvice_data(this_fruit_choice):
    #gets the JSON file
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
    #normalizes the JSON file
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

# Import json file to streamlit
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  
  #if function
  if not fruit_choice:
    #outputs error for null entries
    streamlit.error('Please select a fruit to get information')
    
  else:
    back_from_function = get_fruityvice_data(this_fruit_choice)
    #tabulates the result
    streamlit.dataframe(back_from_function)

except URLerror as e:
  streamlit.error

# ********3rd SECTION**********************************************************************
#connect to snowflake yes
#import snowflake.connector
#load data from fruit_load_list
streamlit.header("the fruit load list contains:")

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select * from fruit_load_list")
         return my_cur.fetchall()
    
#add a button
if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

#stop
streamlit.stop()

#user add data to fruit_load_list
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
#my_cur.execute("insert into fruit_load_list values ('"+add_my_fruit+"')")
streamlit.write('Thank you for adding ', add_my_fruit)
my_cur.execute("insert into fruit_load_list values ('from streamlit')")

