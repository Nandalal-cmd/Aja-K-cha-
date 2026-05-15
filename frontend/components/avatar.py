import streamlit as st
import os


def show_avatar(display_name, avatar_url=None, size=45, font_size=None):
    if font_size is None:
        font_size = "1.2rem" if size <= 45 else "3rem"
    if avatar_url:
        st.image(
            f"http://localhost:8000/uploads/{avatar_url.replace(os.sep, '/')}",
            width=size,
            output_format="auto",
        )
    else:
        initial = (display_name or "U")[0].upper()
        st.markdown(
            f"<div style='width:{size}px;height:{size}px;border-radius:50%;"
            f"background:linear-gradient(135deg,#f093fb,#f5576c);"
            f"display:flex;align-items:center;justify-content:center;"
            f"color:white;font-weight:bold;font-size:{font_size};margin:0 auto;'>{initial}</div>",
            unsafe_allow_html=True,
        )
