#SiS Custom smoothie order form Streamlit app
#Import python packages

import streamlit as st 
import pandas as pd
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f" :cup_with_straw: Customize your smoothie! :cup_with_straw: ")
st.write(
  """Choose the fruits you want in your Smoothie!
  """
)

title = st.text_input('Ordered by:','Dana')
st.write('This order is made by ', title)

cnx=st.connection("snowflake")
session= cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
ingredients_list = st.multiselect(
    'Choose up to 5 incredients'
    ,my_dataframe
    ,max_selections=5
)
#st.dataframe(data=my_dataframe, use_container_width=True)

pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)

ingredients_string=''

if ingredients_list:
  
  for fruit_chosen in ingredients_list:
    ingredients_string += fruit_chosen + ' '

    search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
    st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
    
    st.subheader(fruit_chosen+'Nutri()tion information')
    smoothiefroot_response = requests.get(f"https://www.smoothiefroot.com/api/fruit/{search_on}")
    sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

st.write(ingredients_string)

name_on_order = title
my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('""" + ingredients_string + """','""" + name_on_order + """')"""

st.write(my_insert_stmt)

time_to_insert =st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered, '+ name_on_order +'!', icon="✅")
