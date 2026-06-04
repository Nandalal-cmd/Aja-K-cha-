import streamlit as st
import asyncio
import os
from pathlib import Path

from frontend.components.avatar import show_avatar
from frontend.utils.api_client import react_to_post, delete_post

VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}


def get_image_url(path):
    return f"http://localhost:8000/{path.replace(os.sep, '/')}"


def _is_video(path):
    return Path(path).suffix.lower() in VIDEO_EXTENSIONS


def show_post_card(post, lang="en", current_user_id=None):
    user_data = post.get("user", {})
    challenge_data = post.get("challenge", {})
    reactions = post.get("reactions", [])

    unknown_user = "Unknown" if lang == "en" else "अज्ञात"
    challenge_fallback = "Challenge" if lang == "en" else "च्यालेन्ज"
    display_name = user_data.get("display_name", unknown_user)
    username = user_data.get("username", "")
    challenge_title = challenge_data.get(
        f"title_{lang}", challenge_data.get("title_en", challenge_fallback)
    )
    caption = post.get("caption", "")
    image_path = post.get("image_path", "")

    st.markdown("<div class='post-card'>", unsafe_allow_html=True)

    col_av, col_name, col_del = st.columns([0.1, 0.7, 0.2])
    with col_av:
        show_avatar(display_name, user_data.get("avatar_url"), size=40)
    with col_name:
        st.markdown(
            f"<p style='font-weight:700;margin:0;'>{display_name}</p>"
            f"<p style='font-size:0.8rem;color:rgba(0,0,0,0.4);margin:0;'>@{username}</p>",
            unsafe_allow_html=True,
        )
    with col_del:
        if current_user_id and post.get("user_id") == current_user_id:
            delete_label = "🗑️" if lang == "en" else "🗑️"
            if st.button(delete_label, key=f"del_{post['id']}", help="Delete post"):
                try:
                    r = asyncio.run(delete_post(post["id"]))
                    if r.status_code == 200:
                        st.rerun()
                except Exception:
                    pass

    if image_path:
        media_url = get_image_url(image_path)
        if _is_video(image_path):
            st.video(media_url)
        else:
            st.image(media_url, use_column_width=True)

    st.markdown(
        f"<div class='post-footer'>"
        f"<p style='font-size:0.85rem;color:#764ba2;font-weight:600;margin:0;'>"
        f"📌 {challenge_title}</p>",
        unsafe_allow_html=True,
    )

    if caption:
        st.markdown(f"<p style='margin-top:5px;'>{caption}</p>", unsafe_allow_html=True)

    reaction_emojis = ["🔥", "💜", "😂", "😱", "🙌", "❤️"]
    cols = st.columns(len(reaction_emojis))
    for i, emoji in enumerate(reaction_emojis):
        with cols[i]:
            if st.button(emoji, key=f"react_{post['id']}_{emoji}"):
                try:
                    r = asyncio.run(react_to_post(post["id"], emoji))
                    if r.status_code == 200:
                        st.rerun()
                except Exception:
                    pass

    if reactions:
        emoji_counts = {}
        for r in reactions:
            e = r.get("emoji", "")
            emoji_counts[e] = emoji_counts.get(e, 0) + 1
        counts_str = " ".join(
            [f"{e} {c}" for e, c in sorted(emoji_counts.items(), key=lambda x: -x[1])]
        )
        st.markdown(
            f"<p style='font-size:0.85rem;color:rgba(0,0,0,0.5);margin-top:5px;'>{counts_str}</p>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
