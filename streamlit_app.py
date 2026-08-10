# Custom smoothie order form Streamlit app
# Co-authored with CoCo
#Import python packages

import streamlit as st 
import pandas as pd
import requests

#SiS
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
#import os

# Write directly to the app
st.title(f" :cup_with_straw: Customize your smoothie! :cup_with_straw: ")
st.write(
  """Choose the fruits you want in your Smoothie!
  """
)

#select box
# option = st.selectbox(
#     "What is your favourite fruit?",
#     ("Strawberry", "Banana", "Peaches")
# )

# st.write("You selected:", option)

title = st.text_input('Movie Title','Dana')
st.write('The current movie title is', title)

#table

#session = get_active_session()
cnx=st.connection("snowflake")
session= cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()


ingredients_list = st.multiselect(
    'Choose up to 5 incredients'
    ,my_dataframe
    ,max_selections=5
)

# if ingredients_list:
#     st.write(ingredients_list)
#     st.text(ingredients_list)

if ingredients_list:
  ingredients_string=''
  
  for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen + ' '
    st.subheader(fruit_chosen+'Nutrition information')
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
    sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

#st.write(ingredients_string)
name_on_order = title
my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""

st.write(my_insert_stmt)

time_to_insert =st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered, '+ name_on_order +'!', icon="✅")

# import requests
# smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
#st.text(smoothiefroot_response.json())
# sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)




