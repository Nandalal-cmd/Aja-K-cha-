import streamlit as st
import asyncio
from frontend.utils.api_client import (
    search_users,
    send_friend_request,
    accept_friend_request,
    reject_friend_request,
    get_friends,
    get_pending_requests,
    remove_friend,
)
from frontend.components.friend_item import show_friend_item


def show():
    lang = st.session_state.language
    friends_title = "👥 Friends" if lang == "en" else "👥 साथीहरू"
    st.markdown(
        f"<h2 style='color:white;font-family:Baloo 2;'>{friends_title}</h2>",
        unsafe_allow_html=True,
    )

    tab1_label = "🔍 Search" if lang == "en" else "🔍 खोज"
    tab2_label = "📨 Requests" if lang == "en" else "📨 अनुरोध"
    tab3_label = "👫 My Friends" if lang == "en" else "👫 मेरा साथीहरू"
    tab1, tab2, tab3 = st.tabs([tab1_label, tab2_label, tab3_label])

    with tab1:
        find_label = "Find your buddies and add them!" if lang == "en" else "आफ्ना साथीहरू खोज्नुहोस् र थप्नुहोस्!"
        st.markdown(
            f"<p style='color:rgba(255,255,255,0.7);'>{find_label}</p>",
            unsafe_allow_html=True,
        )

        search_label = "Search by username or display name" if lang == "en" else "प्रयोगकर्ता नाम वा प्रदर्शन नामले खोज्नुहोस्"
        search_placeholder = "e.g., ram, sita, buddy..." if lang == "en" else "जस्तै: राम, सीता..."
        query = st.text_input(
            search_label,
            placeholder=search_placeholder,
            key="search_input",
        )

        if query:
            with st.spinner("Searching..."):
                try:
                    resp = asyncio.run(search_users(query))
                    if resp.status_code == 200:
                        users = resp.json().get("users", [])
                    else:
                        users = []
                except Exception:
                    users = []

            if users:
                add_friend_btn = "➕ Add Friend" if lang == "en" else "➕ साथी थप्नुहोस्"
                for u in users:
                    display = u.get("display_name", "Unknown")
                    uname = u.get("username", "")
                    show_friend_item(display, uname, lang=lang)
                    if st.button(add_friend_btn, key=f"add_{u['id']}"):
                        try:
                            r = asyncio.run(send_friend_request(u["id"]))
                            if r.status_code == 200:
                                sent_msg = f"Request sent to {display}! 🎉" if lang == "en" else f"{display} लाई अनुरोध पठाइयो! 🎉"
                                st.success(sent_msg)
                                st.rerun()
                            else:
                                detail = r.json().get("detail", "Couldn't send request")
                                st.warning(detail)
                        except Exception as e:
                            st.error(f"Error: {e}")
            else:
                no_users = "No users found 🧐" if lang == "en" else "कुनै प्रयोगकर्ता फेला परेन 🧐"
                st.markdown(
                    f"<p style='color:rgba(255,255,255,0.5);text-align:center;margin-top:20px;'>"
                    f"{no_users}</p>",
                    unsafe_allow_html=True,
                )

    with tab2:
        pending_label = "Pending friend requests" if lang == "en" else "पर्खिरहेका साथी अनुरोधहरू"
        st.markdown(
            f"<p style='color:rgba(255,255,255,0.7);'>{pending_label}</p>",
            unsafe_allow_html=True,
        )

        try:
            resp = asyncio.run(get_pending_requests())
            if resp.status_code == 200:
                requests = resp.json()
            else:
                requests = []
        except Exception:
            requests = []

        if requests:
            accept_btn = "✅ Accept" if lang == "en" else "✅ स्वीकार"
            reject_btn = "❌ Reject" if lang == "en" else "❌ अस्वीकार"
            for req in requests:
                from_user = req.get("from_user", {})
                display = from_user.get("display_name", "Unknown")
                uname = from_user.get("username", "")

                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    show_friend_item(display, uname, lang=lang)
                with col2:
                    if st.button(accept_btn, key=f"accept_{req['id']}"):
                        try:
                            r = asyncio.run(accept_friend_request(req["id"]))
                            if r.status_code == 200:
                                accepted_msg = f"You and {display} are now friends! 🎉" if lang == "en" else f"तपाईं र {display} अब साथी हुनुहुन्छ! 🎉"
                                st.success(accepted_msg)
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")
                with col3:
                    if st.button(reject_btn, key=f"reject_{req['id']}"):
                        try:
                            r = asyncio.run(reject_friend_request(req["id"]))
                            if r.status_code == 200:
                                st.rerun()
                        except Exception:
                            pass
        else:
            no_pending = "No pending requests 📭" if lang == "en" else "कुनै पर्खिरहेको अनुरोध छैन 📭"
            st.markdown(
                f"<p style='color:rgba(255,255,255,0.5);text-align:center;margin-top:20px;'>"
                f"{no_pending}</p>",
                unsafe_allow_html=True,
            )

    with tab3:
        friends_list_label = "Your friends list" if lang == "en" else "तपाईंको साथी सूची"
        st.markdown(
            f"<p style='color:rgba(255,255,255,0.7);'>{friends_list_label}</p>",
            unsafe_allow_html=True,
        )

        try:
            resp = asyncio.run(get_friends())
            if resp.status_code == 200:
                friends = resp.json()
            else:
                friends = []
        except Exception:
            friends = []

        if friends:
            unfriend_label = "🗑️ Unfriend" if lang == "en" else "🗑️ साथी हटाउनुहोस्"
            for f in friends:
                col1, col2 = st.columns([4, 1])
                with col1:
                    s = f.get("streak") or {}
                    streak = s.get("current_streak", 0)
                    show_friend_item(
                        f.get("display_name", "Unknown"),
                        f.get("username", ""),
                        streak=streak,
                        lang=lang,
                    )
                with col2:
                    if st.button(unfriend_label, key=f"unfriend_{f['id']}"):
                        try:
                            r = asyncio.run(remove_friend(f["id"]))
                            if r.status_code == 200:
                                st.rerun()
                        except Exception:
                            pass
        else:
            no_friends_title = "No friends yet!" if lang == "en" else "कुनै साथी छैन!"
            no_friends_msg = "Search for your buddies and add them to see their posts!" if lang == "en" else "तपाईंका साथीहरू खोज्नुहोस् र तिनीहरूका पोस्ट हेर्न थप्नुहोस्!"
            st.markdown(
                f"<div style='text-align:center;padding:40px 20px;'>"
                f"<p style='font-size:3rem;'>👥</p>"
                f"<h3 style='color:white;font-family:Baloo 2;'>{no_friends_title}</h3>"
                f"<p style='color:rgba(255,255,255,0.6);'>{no_friends_msg}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )
