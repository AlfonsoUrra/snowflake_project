# Import python packages
import streamlit as st
import snowflake.connector
from snowflake.connector import DictCursor

# Define title and description in Streamlit
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Get name on order from user input
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Function to create Snowflake connection
def create_snowflake_connection():
    # Load credentials securely from Streamlit's secrets
    sf_credentials = st.secrets["snowflake"]
    return snowflake.connector.connect(
        user=sf_credentials["user"],
        password=sf_credentials["password"],
        account=sf_credentials["account"],
        warehouse=sf_credentials["warehouse"],
        database=sf_credentials["database"],
        schema=sf_credentials["schema"],
        role=sf_credentials["role"],
        client_session_keep_alive=sf_credentials.get("client_session_keep_alive", False)
    )

# Initialize connection and cursor
conn = None
cur = None

try:
    conn = create_snowflake_connection()
    cur = conn.cursor(DictCursor)
    # Execute query to fetch fruit options
    cur.execute("SELECT FRUIT_NAME FROM SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    fruit_options = [row['FRUIT_NAME'] for row in cur.fetchall()]

    # Display multi-select widget for choosing ingredients
    ingredients_list = st.multiselect(
        'Choose up to 5 ingredients:', fruit_options, max_selections=5
    )

    if ingredients_list:
        ingredients_string = ', '.join(ingredients_list).strip()  # Join list into string and strip any extra spaces

        # Prepare SQL statement
        my_insert_stmt = "INSERT INTO smoothies.public.orders(ingredients, name_on_order) VALUES (%s, %s)"
        
        # Button to submit the order
        if st.button('Subir Orden', key='submit_order'):
            # Execute the insert statement
            cur.execute(my_insert_stmt, (ingredients_string, name_on_order))
            conn.commit()
            st.success('¡Tu Smoothie ha sido ordenado!', icon="✅")
except Exception as e:
    st.error(f"Failed to connect or execute the query: {str(e)}")
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()






