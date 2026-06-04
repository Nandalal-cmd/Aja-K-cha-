import streamlit as st
import asyncio
from frontend.utils.api_client import get_feed
from frontend.components.post_card import show_post_card

PAGE_SIZE = 10


def show():
    lang = st.session_state.language

    feed_title = "📱 Friends' Feed" if lang == "en" else "📱 साथीहरूको फिड"
    feed_sub = "See what your friends are up to!" if lang == "en" else "तपाईंका साथीहरू के गर्दैछन् हेर्नुहोस्!"
    st.markdown(
        f"<h2 style='color:white;font-family:Baloo 2;'>{feed_title}</h2>"
        f"<p style='color:rgba(255,255,255,0.7);margin-bottom:20px;'>"
        f"{feed_sub}</p>",
        unsafe_allow_html=True,
    )

    if "feed_offset" not in st.session_state:
        st.session_state.feed_offset = 0
    if "feed_posts" not in st.session_state:
        st.session_state.feed_posts = []
    if "feed_has_more" not in st.session_state:
        st.session_state.feed_has_more = True

    if st.session_state.feed_offset == 0:
        try:
            resp = asyncio.run(get_feed(skip=0, limit=PAGE_SIZE))
            if resp.status_code == 200:
                st.session_state.feed_posts = resp.json()
                st.session_state.feed_has_more = len(resp.json()) == PAGE_SIZE
                st.session_state.feed_offset = PAGE_SIZE
        except Exception:
            st.session_state.feed_posts = []
            st.session_state.feed_has_more = False

    no_title = "No posts yet!" if lang == "en" else "कुनै पोस्ट छैन!"
    no_msg = "Add friends or complete today's challenge to see posts here." if lang == "en" else "यहाँ पोस्ट हेर्न साथीहरू थप्नुहोस् वा आजको च्यालेन्ज पूरा गर्नुहोस्।"

    if not st.session_state.feed_posts:
        st.markdown(
            f"<div style='text-align:center;padding:60px 20px;'>"
            f"<p style='font-size:3rem;margin-bottom:10px;'>📸</p>"
            f"<h3 style='color:white;font-family:Baloo 2;'>{no_title}</h3>"
            f"<p style='color:rgba(255,255,255,0.6);'>{no_msg}</p>"
            f"</div>",
            unsafe_allow_html=True,
        )
        return

    current_user_id = st.session_state.user.get("id") if st.session_state.get("user") else None
    for post in st.session_state.feed_posts:
        show_post_card(post, lang, current_user_id=current_user_id)

    if st.session_state.feed_has_more:
        load_more = "Load More" if lang == "en" else "थप लोड गर्नुहोस्"
        if st.button(load_more, use_container_width=True, key="feed_load_more"):
            try:
                resp = asyncio.run(
                    get_feed(skip=st.session_state.feed_offset, limit=PAGE_SIZE)
                )
                if resp.status_code == 200:
                    new_posts = resp.json()
                    st.session_state.feed_posts.extend(new_posts)
                    st.session_state.feed_offset += len(new_posts)
                    st.session_state.feed_has_more = len(new_posts) == PAGE_SIZE
                    st.rerun()
            except Exception:
                pass
