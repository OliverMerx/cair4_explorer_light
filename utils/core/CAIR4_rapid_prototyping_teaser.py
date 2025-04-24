import streamlit as st

def render_api_item():
     # 🔹 **CSS für den Container & Pills**
    st.markdown("""
        <style>
            /* ✅ Haupt-Container */
            .api-container {
                width: 100%;
                display: flex;
                flex-wrap: wrap;
                gap: 15px;
                padding: 20px;
                background-color: #fff;
                border-radius: 15px;
                box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.1);
                justify-content: center;
                align-items: center;
            }
        </style>
    """, unsafe_allow_html=True)
    html = '<div class="api-container">'
    target_url=""
    # 🔹 **Jedes Kapitel als klickbare Pille rendern**
    html += f"""<p style="background-color: #fff;">🔑 CAIR4 API-Key Management"
        Anmelden mit dem eigenen API Schlüssel für viele verschiedene KI-Modelle. 
     </p></br><a href="{target_url}" target="_self">weiter</a> """

    html += '</div>'

    st.markdown(html, unsafe_allow_html=True)