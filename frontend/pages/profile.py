import streamlit as st
import asyncio
from frontend.utils.api_client import get_me, get_my_posts, get_friends, update_profile, upload_avatar
from frontend.components.avatar import show_avatar


def show():
    try:
        resp = asyncio.run(get_me())
        if resp.status_code == 200:
            profile = resp.json()
        else:
            profile = st.session_state.user
    except Exception:
        profile = st.session_state.user

    if not profile:
        return

    lang = st.session_state.language

    if "profile_editing" not in st.session_state:
        st.session_state.profile_editing = False

    col1, col2 = st.columns([1, 2])

    with col1:
        show_avatar(
            profile.get("display_name", ""),
            profile.get("avatar_url"),
            size=120,
            font_size="3rem",
        )

    no_bio = "No bio yet 🌱" if lang == "en" else "कुनै बायो छैन 🌱"
    with col2:
        if st.session_state.profile_editing:
            edit_title = "Edit Profile" if lang == "en" else "प्रोफाइल सम्पादन"
            st.markdown(
                f"<h3 style='color:white;font-family:Baloo 2;margin:0 0 15px 0;'>{edit_title}</h3>",
                unsafe_allow_html=True,
            )
            avatar_label = "Profile Photo" if lang == "en" else "प्रोफाइल फोटो"
            avatar_file = st.file_uploader(
                avatar_label,
                type=["jpg", "jpeg", "png"],
                key="edit_avatar",
            )
            if avatar_file:
                with st.spinner("Uploading avatar..."):
                    try:
                        r = asyncio.run(
                            upload_avatar(avatar_file.getvalue(), avatar_file.name)
                        )
                        if r.status_code == 200:
                            updated = r.json()
                            st.session_state.user = updated
                            st.success("Avatar updated! 🎉")
                            st.rerun()
                        else:
                            st.error(f"❌ {r.json().get('detail', 'Upload failed')}")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            name_label = "Display Name" if lang == "en" else "प्रदर्शन नाम"
            bio_label = "Bio" if lang == "en" else "बायो"
            phone_label = "Phone" if lang == "en" else "फोन"
            new_name = st.text_input(
                name_label,
                value=profile.get("display_name", ""),
                key="edit_display_name",
            )
            new_bio = st.text_area(
                bio_label,
                value=profile.get("bio", "") or "",
                max_chars=200,
                key="edit_bio",
            )
            new_phone = st.text_input(
                phone_label,
                value=profile.get("phone", "") or "",
                key="edit_phone",
            )
            save_btn = "💾 Save" if lang == "en" else "💾 सेभ"
            cancel_btn = "Cancel" if lang == "en" else "रद्द"
            col_save, col_cancel = st.columns(2)
            with col_save:
                if st.button(save_btn, use_container_width=True):
                    data = {}
                    if new_name != profile.get("display_name"):
                        data["display_name"] = new_name
                    if new_bio != (profile.get("bio") or ""):
                        data["bio"] = new_bio
                    if new_phone != (profile.get("phone") or ""):
                        data["phone"] = new_phone
                    if data:
                        with st.spinner("Saving..."):
                            try:
                                r = asyncio.run(update_profile(data))
                                if r.status_code == 200:
                                    updated = r.json()
                                    st.session_state.user = updated
                                    st.session_state.profile_editing = False
                                    st.success("Profile updated! 🎉")
                                    st.rerun()
                                else:
                                    detail = r.json().get("detail", "Update failed")
                                    st.error(f"❌ {detail}")
                            except Exception as e:
                                st.error(f"❌ Error: {e}")
                    else:
                        st.session_state.profile_editing = False
                        st.rerun()
            with col_cancel:
                if st.button(cancel_btn, use_container_width=True):
                    st.session_state.profile_editing = False
                    st.rerun()
        else:
            st.markdown(
                f"<h2 style='color:white;font-family:Baloo 2;margin:0;'>{profile.get('display_name','')}</h2>"
                f"<p style='color:rgba(255,255,255,0.6);'>@{profile.get('username','')}</p>"
                f"<p style='color:rgba(255,255,255,0.7);'>{profile.get('bio', no_bio)}</p>",
                unsafe_allow_html=True,
            )
            edit_btn = "✏️ Edit Profile" if lang == "en" else "✏️ प्रोफाइल सम्पादन"
            if st.button(edit_btn, use_container_width=True):
                st.session_state.profile_editing = True
                st.rerun()

    streak = profile.get("streak") or {}
    cur_streak_label = "Current Streak 🔥" if lang == "en" else "हालको स्ट्रीक 🔥"
    best_streak_label = "Best Streak 🏆" if lang == "en" else "उत्कृष्ट स्ट्रीक 🏆"
    friends_label = "Friends 👥" if lang == "en" else "साथीहरू 👥"
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(
            f"<div style='text-align:center;background:rgba(255,255,255,0.1);border-radius:16px;"
            f"padding:15px;'>"
            f"<p style='font-size:2rem;font-weight:700;color:white;margin:0;'>{streak.get('current_streak', 0)}</p>"
            f"<p style='color:rgba(255,255,255,0.6);margin:0;font-size:0.85rem;'>{cur_streak_label}</p>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with col_b:
        st.markdown(
            f"<div style='text-align:center;background:rgba(255,255,255,0.1);border-radius:16px;"
            f"padding:15px;'>"
            f"<p style='font-size:2rem;font-weight:700;color:white;margin:0;'>{streak.get('longest_streak', 0)}</p>"
            f"<p style='color:rgba(255,255,255,0.6);margin:0;font-size:0.85rem;'>{best_streak_label}</p>"
            f"</div>",
            unsafe_allow_html=True,
        )
    with col_c:
        st.markdown(
            f"<div style='text-align:center;background:rgba(255,255,255,0.1);border-radius:16px;"
            f"padding:15px;'>"
            f"<p style='font-size:2rem;font-weight:700;color:white;margin:0;'>{profile.get('friend_count', 0)}</p>"
            f"<p style='color:rgba(255,255,255,0.6);margin:0;font-size:0.85rem;'>{friends_label}</p>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin:20px 0;'></div>", unsafe_allow_html=True)

    posts_title = "📸 Your Posts" if lang == "en" else "📸 तपाईंको पोस्टहरू"
    st.markdown(
        f"<h3 style='color:white;font-family:Baloo 2;'>{posts_title}</h3>",
        unsafe_allow_html=True,
    )

    try:
        resp = asyncio.run(get_my_posts())
        if resp.status_code == 200:
            posts = resp.json()
        else:
            posts = []
    except Exception:
        posts = []

    if posts:
        post_cols = st.columns(3)
        for idx, post in enumerate(posts):
            with post_cols[idx % 3]:
                title = post.get("challenge", {}).get(
                    f"title_{lang}", post.get("challenge", {}).get("title_en", "")
                )
                react_label = "reactions" if lang == "en" else "प्रतिक्रियाहरू"
                st.markdown(
                    f"<div style='background:rgba(255,255,255,0.1);border-radius:12px;padding:12px;"
                    f"margin-bottom:10px;text-align:center;'>"
                    f"<p style='color:white;font-size:0.85rem;margin:0;'>{title[:50]}...</p>"
                    f"<p style='color:rgba(255,255,255,0.5);font-size:0.75rem;margin:5px 0 0;'>"
                    f"💜 {post.get('reaction_count', 0)} {react_label}</p>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
    else:
        no_posts_msg = "No posts yet. Complete today's challenge! 📸" if lang == "en" else "कुनै पोस्ट छैन। आजको च्यालेन्ज पूरा गर्नुहोस्! 📸"
        st.markdown(
            f"<p style='color:rgba(255,255,255,0.5);text-align:center;padding:30px;'>"
            f"{no_posts_msg}</p>",
            unsafe_allow_html=True,
        )
