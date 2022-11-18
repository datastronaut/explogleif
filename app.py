######################
###   EXPLOGLEIF   ###
######################

import streamlit as st
from datetime import datetime
from explogleif import explogleif

# web page configuration
st.set_page_config(
    page_title="EXPLO GLEIF - exploration of GLEIF API", page_icon="🆑", layout="wide"
)

# sidebar
with st.sidebar:
    st.write(
        """
    # 🆑 Christian Lajouanie  
    ## 🧑‍💼 Follow me on [LinkedIn](https://www.linkedin.com/in/christianlajouanie)  
    ## 🧑‍💻 Check my [GitHub](https://github.com/ClearButton)  
    """
    )


now = datetime.now()
gleif_status = explogleif.latest_status()

lei_count = gleif_status["lei_count"]
latest_entity = gleif_status["latest_entity"]

f"""
# EXPLO GLEIF  
This app is meant to help identifying the relationships between companies.  
It is based on the incredible work of the [Global Legal Entity Identifier Foundation](https://www.gleif.org) (GLEIF).  
They maintain a huge database with millions of companies accross the world and the relationships between them.  
They also provide a [well documented API](https://www.gleif.org/en/lei-data/gleif-api) to allow developers to explore their data.      

###### Current status of the GLEIF database
- On the {now.strftime("%d of %B %Y at %H:%M")}, there are {lei_count:,} entities registered in the GLEIF database.  
- The latest entity registered is {latest_entity.legal_name}, located in {latest_entity.city}, {latest_entity.country}. Its LEI is {latest_entity.lei}.  
___
"""

"""
### Search for an Entity
"""

user_input = st.text_input("Search for a company here")

max_number_of_results = 100

if user_input:
    entities, total_number_of_results = explogleif.search_entities(
        user_input, page_size=max_number_of_results
    )

    if total_number_of_results == 0:
        st.error(f'"{user_input}" does not match any entity in GLEIF database.')
    else:
        if total_number_of_results > max_number_of_results:
            st.warning(
                f'"{user_input}" returns {total_number_of_results} results. Only the first {max_number_of_results} results are displayed here.'
            )
        else:
            st.success(f'"{user_input}" returns {total_number_of_results} results.')

        col1, col2 = st.columns([1, 4])

        with col1:

            for entity in entities:
                if st.button(f"{entity.legal_name}", key=f"start_button_{entity.lei}"):
                    with col2:
                        dot = explogleif.create_graph(entity)
                        st.graphviz_chart(dot)

                st.write(
                    f"""
                        *{entity.city}*, *{entity.country}*   
                        LEI : {entity.lei}
                    """
                )

                st.write("""___""")
