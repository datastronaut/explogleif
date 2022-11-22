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
### Graph of an entity
"""

user_input = st.text_input("Search below the entity below to graph")

# constant to limit the number of results to display
RESULTS_MAX_LIMIT = 100

if user_input:
    entities, total_number_of_results = explogleif.search_entities(
        user_input, page_size=RESULTS_MAX_LIMIT
    )

    if total_number_of_results == 0:
        st.error(
            f'😩 Oh no! "{user_input}" does not match any entity in GLEIF database.'
        )
    else:
        if total_number_of_results > RESULTS_MAX_LIMIT:
            st.warning(
                f'⚠️ "{user_input}" returns too many results ({total_number_of_results}). Only the first {RESULTS_MAX_LIMIT} results can be selected in the list below.'
            )
        else:
            st.info(f'✅ "{user_input}" returns {total_number_of_results} results.')

        default_selection = ["Select an entity"]

        selected_entity = st.selectbox(
            "Select below the entity you would like to graph",
            default_selection
            + [
                f"{entity.legal_name.upper()}, {entity.city.title()}, {entity.country}. LEI: {entity.lei}"
                for entity in entities
            ],
            label_visibility="visible",
        )

        if selected_entity != default_selection:
            selected_lei = selected_entity[-20:]
            for entity in entities:
                if entity.lei == selected_lei:
                    with st.spinner("Graph under construction"):
                        dot = explogleif.create_graph(entity)
                    st.write("See below the graph of " + f"{entity.legal_name}".title())
                    st.graphviz_chart(dot, True)
