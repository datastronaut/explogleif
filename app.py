######################
###   EXPLOGLEIF   ###
######################

import streamlit as st
from datetime import datetime
from explogleif import explogleif

# web page configuration
st.set_page_config(
    page_title="EXPLO GLEIF - exploration of GLEIF API",
    page_icon=":cl:", # Clear Button emoji
    # layout="wide",
    # initial_sidebar_state="auto"
    )


"""
# EXPLOGLEIF  
This app is meant to explore the API of the [Global Legal Entity Identifier Foundation](https://www.gleif.org).  
The API documentation [can be found here](https://documenter.getpostman.com/view/7679680/SVYrrxuU?version=latest#quick-start-guide).
## Check current status of the GLEIF database  
"""

now = datetime.now()

f"""
On {now.strftime("%Y-%m-%d %H:%M:%S")}, there are {explogleif.count_all_lei()} LEI in total.
"""

# if st.button('number of LEIs'):
#     st.write('there so many LEI, this is incredible !')
#     st.write(now.strftime("%Y-%m-%d %H:%M:%S"))
# else:
    
    
    
"""
:cl:
"""