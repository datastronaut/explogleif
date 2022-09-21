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


"""
# EXPLO GLEIF  
This app is meant to explore the API of the [Global Legal Entity Identifier Foundation](https://www.gleif.org).  
The API documentation [can be found here](https://documenter.getpostman.com/view/7679680/SVYrrxuU?version=latest#quick-start-guide).  
"""


"""  
### Current status of the GLEIF database 
"""
now = datetime.now()
gleif_status = explogleif.latest_status()

lei_count = gleif_status["lei_count"]
latest_entity = gleif_status["latest_entity"]


f"""
On the {now.strftime("%d of %B %Y at %H:%M")}, there are {lei_count:,} LEIs in total in the GLEIF database.  
The latest entity registered is {latest_entity.legal_name}, located in {latest_entity.city}, {latest_entity.country}.  
Its LEI is {latest_entity.lei}.
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
