from pylibs.streamlit_lib import streamlit as st
from pylibs.base64_lib import base64

def set_background(color):
    pass#set_new_background(True)

def set_new_background(color):
    if color:
        st.markdown(f"""
            <style>
                .stApp {{
                    width=100%;
                    height=100%;
                    min_height=1500px!important;
                    background-color:{st.session_state.bg_color};
                    background-image: linear-gradient(45deg, {st.session_state.bg_color},{st.session_state.bg_color});
                }}
            </style>
        #""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <style>
                .stApp {{
                    width=100%;
                    height=1500px!important;
                    min_height=1500px!important;
                    background-color:{st.session_state.header_color};
                    background-image: linear-gradient(45deg, {st.session_state.header_color},{st.session_state.button_bg_color});
                }}
            </style>
        #""", unsafe_allow_html=True)

def set_background_image(image_path):
    #image_path=st.session_state.base_path+"/assets/logos/CAIR4_placeholder_logo.png"
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()

        st.markdown(f"""
        <style>
            .stApp {{
                background-color:{st.session_state.previous_use_case};
                background-image: url(data:image/png;base64,{encoded_string});
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                transition: unset!important;
            }}
        </style>
    #""", unsafe_allow_html=True)
    
    return True