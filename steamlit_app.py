# Import python packages
import streamlit as st

#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col



# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)


name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be: ", name_on_order)


#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections = 5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        #st.subheader(fruit_chosen + ' Nutrition Information')
  

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """',
            '""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response)
# returning response [502], no idea what that means but it's just error after error from this point onward!

#fv_df = st.dataframe(data=fruityvice_response.json(), use_conatiner_width=True)


