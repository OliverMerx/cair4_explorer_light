"""
===========================
CAIR4 PDF-Viewer (iframe)
===========================

Einfaches Modul zur Abfrage des Browsers

"""
from streamlit_javascript import st_javascript

def render_browser_check():

    user_agent = st_javascript("navigator.userAgent")

    browser = "Unbekannt"
    if user_agent:
        ua = user_agent.lower()
        if "chrome" in ua and "safari" in ua and "edg" not in ua:
            browser = "Chrome"
        elif "safari" in ua and "chrome" not in ua:
            browser = "Safari"
        elif "firefox" in ua:
            browser = "Firefox"
        elif "edg" in ua:
            browser = "Edge"
        else:
            browser = "Unbekannt"

    return browser
