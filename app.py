######################
###   EXPLOGLEIF   ###
######################

import streamlit as st
from datetime import datetime
from explogleif import explogleif

# web page configuration
st.set_page_config(
    page_title="EXPLO GLEIF - exploration of GLEIF API",
    page_icon="🆑",  # Clear Button emoji
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

        for idx, entity in enumerate(entities):
            with st.expander(entity.legal_name):
                st.write(
                    f"""
                         LEI : {entity.lei}  
                         Location: {entity.city}, {entity.country}
                         """
                )

                # display a button "Parents" to display the parents of the entity
                if st.button("Parents", key=f"parents_button_{idx}"):
                    parents = entity.get_direct_parents()
                    total_number_of_parents = len(parents)
                    if total_number_of_parents == 0:
                        st.write(
                            f"{entity.legal_name} does not have any parent registered in the GLEIF database"
                        )
                    else:
                        if total_number_of_parents == 1:
                            st.write(
                                f"The parent of {entity.legal_name} in the GLEIF database is"
                            )
                        else:
                            st.write(
                                f"The parents of {entity.legal_name} in the GLEIF database are"
                            )

                        for parent in parents:
                            st.write(
                                f"""
                                     >**{parent.legal_name}**  
                                     > LEI: {parent.lei}  
                                     > City:  {parent.city}  
                                     > Country: {parent.country}  
                                       
                                     """
                            )

                # display a button "Children" to display the children of the entity
                if st.button("Children", key=f"children_button_{idx}"):
                    children = entity.get_direct_children()
                    total_number_of_children = len(children)
                    if total_number_of_children == 0:
                        st.write(
                            f"{entity.legal_name} does not have any child registered in the GLEIF database"
                        )
                    else:
                        if total_number_of_children == 1:
                            st.write(
                                f"There is only one child of {entity.legal_name} registered in the GLEIF database."
                            )
                        else:
                            st.write(
                                f"There are {total_number_of_children} children of {entity.legal_name} registered in the GLEIF database."
                            )

                        for child in children:
                            st.write(
                                f"""
                                     > **{child.legal_name}**  
                                     > LEI: {child.lei}  
                                     > City:  {child.city}  
                                     > Country: {child.country}  
                                     """
                            )
