import streamlit as st

st.set_page_config(
    page_title="Aaj K Garne?",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="auto",
)


def get_custom_css(dark_mode=False):
    bg = ("background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);"
          if dark_mode else
          "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);")
    sidebar_bg = ("background: linear-gradient(180deg, #0d0d1a 0%, #1a1a3e 100%);"
                  if dark_mode else
                  "background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);")
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600;700;800&family=Poppins:wght@400;500;600;700&display=swap');

* {{
    font-family: 'Poppins', sans-serif;
}}

.stApp {{
    {bg}
}}

h1, h2, h3, .big-title {
    font-family: 'Baloo 2', sans-serif !important;
    font-weight: 800 !important;
}

.big-title {
    font-size: 3rem !important;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    color: white;
    opacity: 0.9;
    font-size: 1.1rem;
    margin-top: -10px;
    margin-bottom: 30px;
}

.challenge-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    padding: 25px;
    color: white;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
    border: 1px solid rgba(255,255,255,0.1);
}

.challenge-emoji {
    font-size: 3rem;
    text-align: center;
    margin-bottom: 10px;
}

.post-card {
    background: white;
    border-radius: 16px;
    padding: 0;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    overflow: hidden;
    border: none;
}

.post-card img {
    width: 100%;
    object-fit: cover;
    max-height: 500px;
}

.post-header {
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.post-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
}

.post-footer {
    padding: 12px 16px;
    border-top: 1px solid #f0f0f0;
}

.streak-badge {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    padding: 8px 16px;
    border-radius: 50px;
    font-weight: 700;
    font-size: 0.9rem;
    display: inline-flex;
    align-items: center;
    gap: 5px;
}

.nav-btn {
    background: rgba(255,255,255,0.15);
    color: white;
    border: 1px solid rgba(255,255,255,0.2);
    padding: 10px 20px;
    border-radius: 12px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s;
    margin-bottom: 5px;
    font-weight: 600;
}

.nav-btn:hover {
    background: rgba(255,255,255,0.25);
    transform: translateX(5px);
}

.nav-btn.active {
    background: rgba(255,255,255,0.3);
    border-color: rgba(255,255,255,0.5);
}

.upload-area {
    border: 2px dashed rgba(255,255,255,0.4);
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    background: rgba(255,255,255,0.05);
}

.friend-item {
    background: rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 8px;
    color: white;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.reaction-btn {
    font-size: 1.5rem;
    cursor: pointer;
    transition: transform 0.2s;
    background: none;
    border: none;
    padding: 5px 10px;
}

.reaction-btn:hover {
    transform: scale(1.3);
}

div[data-testid="stSidebarNav"] {display: none;}
section[data-testid="stSidebar"] {{
    {sidebar_bg}
}}

/* Fix form inputs */
.stTextInput input, .stTextInput div, .stTextInput {
    background: rgba(255,255,255,0.95) !important;
    border-radius: 12px !important;
    border: none !important;
    color: #333 !important;
}

.stTextInput label {
    color: white !important;
}

.stButton button {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 30px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    width: 100%;
    transition: transform 0.2s;
}

.stButton button:hover {
    transform: scale(1.02);
}

.stFileUploader div {
    background: rgba(255,255,255,0.1) !important;
    border: 2px dashed rgba(255,255,255,0.3) !important;
    border-radius: 16px !important;
    color: white !important;
}

.stAlert {
    border-radius: 12px !important;
}

.reaction-bar {{
    display: flex;
    gap: 8px;
    padding: 8px 0;
    flex-wrap: wrap;
}}
</style>
"""


def init_session_state():
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "token" not in st.session_state:
        st.session_state.token = None
    if "user" not in st.session_state:
        st.session_state.user = None
    if "language" not in st.session_state:
        st.session_state.language = "ne"
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False


def sidebar_nav():
    with st.sidebar:
        lang = st.session_state.get("language", "ne")
        title_text = "🔥 आज के गर्ने?" if lang == "ne" else "🔥 Aaj K Garne?"
        sub_text = "Aaj K Garne?" if lang == "ne" else "What to do today?"
        st.markdown(
            f"<p style='font-family: Baloo 2; font-size: 2rem; font-weight: 800; "
            f"color: white; text-align: center; margin-bottom: 5px;'>{title_text}</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p style='text-align: center; color: rgba(255,255,255,0.6); font-size: 0.8rem; "
            f"margin-bottom: 30px;'>{sub_text}</p>",
            unsafe_allow_html=True,
        )

        if st.session_state.user:
            user = st.session_state.user
            from frontend.components.avatar import show_avatar
            from frontend.components.streak_badge import show_streak_badge
            col1, col2 = st.columns([1, 3])
            with col1:
                show_avatar(
                    user.get("display_name", ""),
                    user.get("avatar_url"),
                    size=45,
                    font_size="1.2rem",
                )
            with col2:
                st.markdown(
                    f"<p style='color:white;font-weight:700;margin:0;'>{user.get('display_name','')}</p>"
                    f"<p style='color:rgba(255,255,255,0.6);font-size:0.8rem;margin:0;'>"
                    f"@{user.get('username','')}</p>",
                    unsafe_allow_html=True,
                )

            streak = user.get("streak") or {}
            current = streak.get("current_streak", 0)
            show_streak_badge(current, lang)

            st.markdown("<hr style='opacity:0.2;margin:20px 0;'>", unsafe_allow_html=True)

            st.markdown(
                "<p style='color:rgba(255,255,255,0.6);font-size:0.8rem;margin-bottom:5px;'>"
                "Language / भाषा</p>",
                unsafe_allow_html=True,
            )
            lang = st.session_state.language
            col_np, col_en = st.columns(2)
            with col_np:
                if st.button(
                    "🇳🇵 नेपाली",
                    key="lang_ne",
                    use_container_width=True,
                    disabled=(lang == "ne"),
                ):
                    st.session_state.language = "ne"
                    st.rerun()
            with col_en:
                if st.button(
                    "🇬🇧 English",
                    key="lang_en",
                    use_container_width=True,
                    disabled=(lang == "en"),
                ):
                    st.session_state.language = "en"
                    st.rerun()

            st.markdown("<hr style='opacity:0.2;margin:20px 0;'>", unsafe_allow_html=True)

            dark_label = "🌙 Dark Mode" if lang == "en" else "🌙 डार्क मोड"
            light_label = "☀️ Light Mode" if lang == "en" else "☀️ लाइट मोड"
            toggle_label = dark_label if not st.session_state.dark_mode else light_label
            if st.button(toggle_label, use_container_width=True):
                st.session_state.dark_mode = not st.session_state.dark_mode
                st.rerun()

            st.markdown("<hr style='opacity:0.2;margin:20px 0;'>", unsafe_allow_html=True)

            notif_icon = "🔔" if lang == "en" else "🔔 सूचना"
            notif_label = f"{notif_icon}"
            try:
                import asyncio
                from frontend.utils.api_client import get_unread_count
                r = asyncio.run(get_unread_count())
                if r.status_code == 200:
                    cnt = r.json().get("count", 0)
                    if cnt > 0:
                        notif_label += f" ({cnt})"
            except Exception:
                pass
            if st.button(notif_label, key="nav_notifications", use_container_width=True):
                st.session_state.page = "notifications"
                st.rerun()

            st.markdown("<hr style='opacity:0.2;margin:20px 0;'>", unsafe_allow_html=True)

            pages = {
                "home": ("🏠 Home" if lang == "en" else "🏠 गृह"),
                "feed": ("📱 Feed" if lang == "en" else "📱 फिड"),
                "friends": ("👥 Friends" if lang == "en" else "👥 साथीहरू"),
                "profile": ("👤 Profile" if lang == "en" else "👤 प्रोफाइल"),
            }

            for key, label in pages.items():
                active = "active" if st.session_state.page == key else ""
                if st.button(label, key=f"nav_{key}", use_container_width=True):
                    st.session_state.page = key
                    st.rerun()

            st.markdown("<hr style='opacity:0.2;margin:20px 0;'>", unsafe_allow_html=True)

            logout_label = "🚪 Logout" if lang == "en" else "🚪 लग आउट"
            if st.button(logout_label, use_container_width=True):
                st.session_state.token = None
                st.session_state.user = None
                st.session_state.page = "home"
                st.rerun()

        else:
            prompt_text = (
                "Log in or sign up to start your streak! 🔥"
                if lang == "en"
                else "लग इन वा साइन अप गर्नुहोस्! 🔥"
            )
            login_btn = "🔑 Login" if lang == "en" else "🔑 लग इन"
            signup_btn = "📝 Sign Up" if lang == "en" else "📝 साइन अप"
            st.markdown(
                f"<p style='color:rgba(255,255,255,0.6);text-align:center;'>{prompt_text}</p>",
                unsafe_allow_html=True,
            )
            if st.button(login_btn, use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
            if st.button(signup_btn, use_container_width=True):
                st.session_state.page = "register"
                st.rerun()

        footer_text = (
            "Made with 💜 for Nepali Youth"
            if lang == "en"
            else "नेपाली युवाका लागि 💜"
        )
        st.markdown(
            f"<p style='color:rgba(255,255,255,0.3);font-size:0.7rem;text-align:center;"
            f"margin-top:50px;'>{footer_text}</p>",
            unsafe_allow_html=True,
        )


def main():
    init_session_state()
    st.markdown(get_custom_css(st.session_state.dark_mode), unsafe_allow_html=True)
    sidebar_nav()

    page = st.session_state.page

    if not st.session_state.token:
        if page == "register":
            from frontend.pages.register import show
            show()
        else:
            from frontend.pages.login import show
            show()
    else:
        if page == "home":
            from frontend.pages.home import show
            show()
        elif page == "notifications":
            from frontend.pages.notifications import show
            show()
        elif page == "feed":
            from frontend.pages.feed import show
            show()
        elif page == "friends":
            from frontend.pages.friends import show
            show()
        elif page == "profile":
            from frontend.pages.profile import show
            show()
        elif page == "login":
            from frontend.pages.home import show
            show()
        else:
            from frontend.pages.home import show
            show()


if __name__ == "__main__":
    main()
