import streamlit as st
import asyncio
from frontend.utils.api_client import get_notifications, mark_notification_read, mark_all_notifications_read


def show():
    lang = st.session_state.language
    notif_title = "🔔 Notifications" if lang == "en" else "🔔 सूचनाहरू"
    st.markdown(
        f"<h2 style='color:white;font-family:Baloo 2;'>{notif_title}</h2>",
        unsafe_allow_html=True,
    )

    try:
        resp = asyncio.run(get_notifications())
        if resp.status_code == 200:
            notifications = resp.json()
        else:
            notifications = []
    except Exception:
        notifications = []

    has_unread = any(not n.get("is_read") for n in notifications)
    if has_unread:
        mark_all_label = "✅ Mark All Read" if lang == "en" else "✅ सबै पढिएको चिन्ह"
        if st.button(mark_all_label, use_container_width=True):
            try:
                asyncio.run(mark_all_notifications_read())
                st.rerun()
            except Exception:
                pass

    no_notifs = "No notifications yet" if lang == "en" else "कुनै सूचना छैन"
    if not notifications:
        st.markdown(
            f"<p style='color:rgba(255,255,255,0.5);text-align:center;padding:40px;'>"
            f"{no_notifs}</p>",
            unsafe_allow_html=True,
        )
        return

    for n in notifications:
        bg = "rgba(255,255,255,0.15)" if not n.get("is_read") else "rgba(255,255,255,0.05)"
        border = "1px solid rgba(255,255,255,0.25)" if not n.get("is_read") else "none"
        st.markdown(
            f"<div style='background:{bg};border-radius:12px;padding:12px 16px;"
            f"margin-bottom:8px;border:{border};'>"
            f"<p style='color:white;margin:0;font-size:0.9rem;'>{n['message']}</p>"
            f"<p style='color:rgba(255,255,255,0.4);margin:3px 0 0;font-size:0.75rem;'>"
            f"{n['created_at'][:19].replace('T', ' ')}</p>"
            f"</div>",
            unsafe_allow_html=True,
        )

        if not n.get("is_read"):
            mark_label = "Mark as read" if lang == "en" else "पढिएको चिन्ह"
            if st.button(mark_label, key=f"read_{n['id']}"):
                try:
                    asyncio.run(mark_notification_read(n["id"]))
                    st.rerun()
                except Exception:
                    pass
