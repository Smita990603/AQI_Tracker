import streamlit as st
import os
import json

import request as r




dir = os.getcwd()
parent = os.path.dirname(dir)
file_path = "\\".join([parent, 'utils', 'form_data.json'])



with st.form("AQI Form"):
    st.header("AQI Form")
    district = st.text_input("Enter District*",placeholder="Enter District")
    state = st.text_input("Enter State*",placeholder="Enter State")
    country = st.text_input("Enter Country*",placeholder="Enter Country")
    bot_token = st.text_input("Enter bot token for telegram*",type="password",placeholder="Enter bot token for telegram")
    chat_id = st.text_input("Enter chat_id for telegram*",type="password",placeholder="Enter chat_id for telegram")
    st.write("Note : We respect your privacy, bot token and chat id are not getting stored")
    submit = st.form_submit_button("Submit")
    
    if "aqi" in st.session_state:
        r.main()
        

    if submit:
        if not district or not state or not country or not bot_token or not chat_id:
            st.warning("Please fill mandatory details")
        else:
            data = {
                "dis": district,
                "state": state,
                "country": country,
                "bot_token": bot_token,
                "chat_id": chat_id
            }
            with open(file_path, 'w') as f:
                json.dump(data, f)
            st.write("We are on request page")
            
            st.session_state["district"] = ""
            st.session_state["state"] = ""
            st.session_state["country"] = ""
            st.session_state["bot_token"] = ""
            st.session_state["chat_id"] = ""
            
            st.session_state["aqi"] = True
            


