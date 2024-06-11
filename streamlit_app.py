# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom
 Smoothie!
    """
)
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)


session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for index, x in enumerate(ingredients_list):
        ingredients_string += x + ' , '

    ingredients_string = ingredients_string.strip()  # Remueve el espacio extra al final

    # Corregir la sentencia SQL para incluir correctamente ambas columnas 'ingredients' y 'name_order'.
    # La variable 'name_on_order' debe ser definida en alguna parte de tu código anteriormente.
    my_insert_stmt = f"INSERT INTO smoothies.public.orders(ingredients, name_on_order) VALUES ('{ingredients_string}', '{name_on_order}')"

    # Botón para enviar la orden con una clave única para evitar el error DuplicateWidgetID.
    if st.button('Subir Orden', key='submit_order'):
        # Ejecuta la sentencia SQL y maneja cualquier excepción que pueda ocurrir.
        try:
            session.sql(my_insert_stmt).collect()
            st.success('¡Tu Smoothie ha sido ordenado!', icon="✅")
        except Exception as e:
            st.error(f'Ocurrió un error al realizar la orden: {e}')








