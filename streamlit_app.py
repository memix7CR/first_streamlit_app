import streamlit
import snowflake.connector
import pandas
import requests
from urllib.error import URLError

streamlit.title("My Mom's New Healthty Dinner")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥬 Kale, Spinach & Rocket Smoothie')
streamlit.text('🥚 Hard-Boiled Free-Range Egg')
streamlit.text('🥑 Avocado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie')




my_fruit_list = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

#Let's pick a list here so they can pick the fruit they want to include

fruits_selected = streamlit.multiselect('Pick some fruits', list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Display the table on the page
streamlit.dataframe(fruits_to_show)


#New section to display Fruityvice API response
streamlit.header("Fruityvice Fruit Advice")

try:
                                               
   fruit_choice = streamlit.text_input('What fruit would you like information about?')

   if not fruit_choice:
       streamlit.error("Please select a fruit to get information.")

   else:
       fruityvice_response =requests.get("https://fruityvice.com/api/fruit/" +fruit_choice)
       fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
       streamlit.dataframe(fruityvice_normalized)
    
except URLError as e:
  streamlit.error()

streamlit.stop() #to avoid running from here


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.text('THE FRUIT LIST CONTAINS:')
streamlit.dataframe(my_data_row)

add_my_fruit = streamlit.text_input('What fruit would you like to add?', 'jackfruit')
streamlit.write('Thanks for adding ' , add_my_fruit)
my_cur.execute("INSERT into fruit_load_list values ('from streamlit')")
