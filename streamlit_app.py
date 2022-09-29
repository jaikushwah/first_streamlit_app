import streamlit
import pandas
import requests;
import snowflake.connector
from urllib.error import URLError
streamlit.title('My Parents New Healthy Dinner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#streamlit.dataframe(my_fruit_list)
#changing the index to fruit column instead of numbers
my_fruit_list = my_fruit_list.set_index('Fruit')


# Let's put a pick list here so they can pick the fruit they want to include 
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

#Let's put a pick list here so they can pick the fruits they want to include
fruit_selected=streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruit_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#create function for printing the fruit data selected by user
def get_fruityvice_data(this_fruit_choice):
    #import requests;
    fruityvice_response=requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    # let the fruitvice data looking a little more nicer
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

#Adding fruityvice api header
streamlit.header("View Our Fruit List-Add Your Favorites")
try:
#taking input from the user
    fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
          streamlit.error("Please select a fruit to get information.")
    else:
          back_from_function=get_fruityvice_data(fruit_choice)
          streamlit.dataframe(back_from_function)
          
except URLError as e:
    streamlit.error()
    

#snowflake-related function
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()
    
    
#add a button to load a fruit
if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_row=get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_row)


#streamlit.write('The user entered ', fruit_choice)
#new section to display fruitvice api response

#streamlit.text(fruityvice_response)
#converting the response in json format
#streamlit.text(fruityvice_response.json())#just writes the data on the screen




#don't run anything past here while we troubleshoot
#streamlit.stop()

#import snowflake connector
#import snowflake.connector


#my_cur = my_cnx.cursor()
#my_cur.execute("select * from fruit_load_list")
#my_data_row=my_cur.fetchone()#will fetch only one row
#fetching all the rows
#my_data_rows=my_cur.fetchall()
#streamlit.text("The fruit load list contains:")
#streamlit.text(my_data_row)
#streamlit.header("The fruit load list contains:")
#streamlit.dataframe(my_data_rows)
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_row = my_cur.fetchone()
#streamlit.text("Hello from Snowflake:")
#streamlit.text(my_data_row)


#adding fruit function
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load_list values('" + new_fruit + "')")
         #displaying the selected fruit
         return "Thanks for adding " + new_fruit

        
        
#creating a text box to add fruit
add_my_fruit=streamlit.text_input('What fruit would you like to add?','jackfruit')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function=insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(back_from_function)
        
        
        
        
        
        

