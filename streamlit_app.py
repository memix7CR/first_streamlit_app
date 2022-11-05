import streamlit

streamlit.title("My Mom's New Healthty Dinner")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥬 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥚 Hard-Boiled Free-Range Egg')
streamlit.text('🥑 Avocado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie')


import pandas

my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

#Let's pick a list here so they can pick the fruit they want to include

fruits_selected = streamlit.multiselect('Pick some fruits', list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Display the table on the page
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice")
                                               
import requests
fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
streamlit.write('The user entered', fruit_choice)

fruityvice_response =requests.get("https://fruityvice.com/api/fruit/" +fruit_choice)

#take the json version of the response and normalize it
#it uses pandas to convert the json response data in a tabular format

fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

#output in the screen as a table
#it allow us to display the data in a table

streamlit.dataframe(fruityvice_normalized)

import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text('THE FRUIT LIST CONTAINS:')
streamlit.text(my_data_row)
