import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 🔧 CONFIGURATION
# Paste your Tailscale Funnel URL here!
# Example: "https://my-laptop.tailnet-name.ts.net"
# ==========================================
NEW_APP_URL = "https://archlinux.tail378a15.ts.net/"

st.set_page_config(page_title="Redirecting...", page_icon="🚀")

# --- UI Layout ---
st.title("Upgraded to local host!")

st.info(
    "The **Encrypted Image Decoder** has moved to a dedicated server for faster performance and better stability."
)

st.write("You should be redirected automatically in a moment...")

# --- 1. The Manual Fallback Button ---
# This is crucial in case the browser blocks the automatic script
st.link_button(
    "Click here to go to the App",
    NEW_APP_URL,
    type="primary",
    use_container_width=True,
)

# --- 2. The Automatic Redirect ---
# This uses a meta-refresh tag AND a JavaScript redirect to ensure
# the user is moved as quickly as possible.
redirect_code = f"""
<meta http-equiv="refresh" content="0; url={NEW_APP_URL}">
<script>
    window.top.location.href = "{NEW_APP_URL}";
</script>
"""

# We render this as HTML. The height=0 makes it invisible.
components.html(redirect_code, height=0)

# Optional: Footer
st.divider()
st.caption("Hosted via Tailscale Funnel • 2024")
