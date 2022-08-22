######################
###   EXPLOGLEIF   ###
######################

import streamlit as st
from datetime import datetime
from explogleif import explogleif

# web page configuration
st.set_page_config(
    page_title="EXPLO GLEIF - exploration of GLEIF API",
    page_icon=":cl:" # Clear Button emoji
    )

# sidebar
st.sidebar.markdown(
    """
    App developped by Christian Lajouanie.  
    :necktie: Follow me on [LinkedIn](https://www.linkedin.com/in/christianlajouanie)  
    :octopus: Check my [GitHub profile](https://github.com/ClearButton)  
    :cl:
    """
)


"""
# EXPLOGLEIF  
This app is meant to explore the API of the [Global Legal Entity Identifier Foundation](https://www.gleif.org).  
The API documentation [can be found here](https://documenter.getpostman.com/view/7679680/SVYrrxuU?version=latest#quick-start-guide).  
  
  
### Total number of LEIs in GLEIF database  
"""

now = datetime.now()
gleif_status = explogleif.latest_status()

lei_count = gleif_status['lei_count']
latest_entity = gleif_status["latest_entity"]


f"""
On {now.strftime("%Y-%m-%d %H:%M:%S")}, there are {lei_count} LEIs in total in the GLEIF database.  
"""


f"""  
### Latest entity registered
The latest entity registered is {latest_entity.name}.  
It is located in {latest_entity.city}, {latest_entity.country}.  
Its LEI is {latest_entity.lei}.
"""
