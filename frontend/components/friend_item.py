import streamlit as st


def show_friend_item(display_name, username, streak=0, lang="en"):
    st.markdown(
        f"<div class='friend-item'>"
        f"<div>"
        f"<strong>{display_name}</strong><br>"
        f"<small style='opacity:0.7;'>@{username}</small>"
        f"</div>"
        + (
            f"<span class='streak-badge' style='font-size:0.8rem;padding:4px 12px;'>"
            f"🔥 {streak}</span>"
            if streak
            else ""
        )
        + f"</div>",
        unsafe_allow_html=True,
    )
