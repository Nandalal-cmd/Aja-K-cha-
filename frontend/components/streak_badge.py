import streamlit as st


def show_streak_badge(current, lang="en"):
    label = "day streak" if lang == "en" else "दिनको स्ट्रीक"
    st.markdown(
        f"<div class='streak-badge' style='margin:15px auto;display:table;'>"
        f"🔥 {current} {label}</div>",
        unsafe_allow_html=True,
    )
