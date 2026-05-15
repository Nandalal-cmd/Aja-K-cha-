import streamlit as st
import asyncio
from datetime import datetime
from frontend.utils.api_client import get_today_challenge, upload_post, get_my_posts


CHALLENGE_EMOJIS = {
    "funny": "😂",
    "social": "🤝",
    "crazy": "🤪",
    "wholesome": "💖",
    "talent": "🎯",
    "food": "🍜",
}


def show():
    user = st.session_state.user
    lang = st.session_state.language

    try:
        resp = asyncio.run(get_today_challenge())
        if resp.status_code == 200:
            challenge = resp.json()
        else:
            challenge = None
    except Exception:
        challenge = None

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            f"<p style='color:white;font-size:1.2rem;font-weight:600;margin-bottom:5px;'>"
            f"Hey {user.get('display_name','')}! 👋</p>"
            f"<p style='color:rgba(255,255,255,0.7);margin-bottom:20px;'>"
            f"{datetime.now().strftime('%A, %B %d, %Y')}</p>",
            unsafe_allow_html=True,
        )

        if challenge:
            emoji = CHALLENGE_EMOJIS.get(challenge.get("challenge_type", "funny"), "🎯")
            title = challenge.get(f"title_{lang}", challenge.get("title_en"))
            desc = challenge.get(f"description_{lang}", challenge.get("description_en"))

            pts_label = "pts" if lang == "en" else "अंक"
            st.markdown(
                f"<div class='challenge-card'>"
                f"<div class='challenge-emoji'>{emoji}</div>"
                f"<h2 style='text-align:center;font-family:Baloo 2;margin:0;'>{title}</h2>"
                f"<p style='text-align:center;opacity:0.9;margin-top:10px;'>{desc}</p>"
                f"<div style='text-align:center;margin-top:15px;'>"
                f"<span class='streak-badge'>+{challenge.get('points', 10)} {pts_label}</span>"
                f"</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

            expander_label = "📸 Complete this challenge!" if lang == "en" else "📸 यो च्यालेन्ज पूरा गर्नुहोस्!"
            upload_label = "Upload your photo/video proof" if lang == "en" else "आफ्नो फोटो/भिडियो प्रमाण अपलोड गर्नुहोस्"
            caption_label = "Caption (optional)" if lang == "en" else "क्याप्सन (वैकल्पिक)"
            caption_placeholder = "Add a caption to your post..." if lang == "en" else "तपाईंको पोस्टमा क्याप्सन थप्नुहोस्..."
            public_label = "Make public (visible to everyone)" if lang == "en" else "सार्वजनिक गर्नुहोस् (सबैलाई देखिने)"
            post_btn_label = "🚀 Post Challenge!" if lang == "en" else "🚀 च्यालेन्ज पोस्ट गर्नुहोस्!"
            with st.expander(expander_label, expanded=True):
                uploaded_file = st.file_uploader(
                    upload_label,
                    type=["jpg", "jpeg", "png", "mp4", "mov"],
                )
                caption = st.text_area(
                    caption_label,
                    placeholder=caption_placeholder,
                    max_chars=200,
                )
                is_public = st.checkbox(public_label, value=True)

                if uploaded_file and st.button(post_btn_label, use_container_width=True):
                    with st.spinner("Uploading..."):
                        try:
                            file_bytes = uploaded_file.getvalue()
                            resp = asyncio.run(
                                upload_post(
                                    challenge["id"],
                                    caption,
                                    is_public,
                                    file_bytes,
                                    uploaded_file.name,
                                )
                            )
                            if resp.status_code == 200:
                                success_msg = "🎉 Challenge complete! Check the feed!" if lang == "en" else "🎉 च्यालेन्ज पूरा भयो! फिड हेर्नुहोस्!"
                                st.success(success_msg)
                                st.balloons()
                            else:
                                detail = resp.json().get("detail", "Upload failed")
                                st.error(f"❌ {detail}")
                        except Exception as e:
                            err_msg = f"❌ Upload error: {e}" if lang == "en" else f"❌ अपलोड त्रुटि: {e}"
                            st.error(err_msg)
        else:
            no_challenge_title = "No challenge for today?" if lang == "en" else "आजको लागि कुनै च्यालेन्ज छैन?"
            no_challenge_msg = "Check back tomorrow for a new challenge!" if lang == "en" else "नयाँ च्यालेन्जको लागि भोलि फेरि आउनुहोस्!"
            st.markdown(
                f"<div class='challenge-card' style='text-align:center;'>"
                f"<div class='challenge-emoji'>🎉</div>"
                f"<h3 style='font-family:Baloo 2;'>{no_challenge_title}</h3>"
                f"<p>{no_challenge_msg}</p>"
                f"</div>",
                unsafe_allow_html=True,
            )

    with col2:
        recent_title = "Your Recent Posts" if lang == "en" else "तपाईंको हालैका पोस्टहरू"
        st.markdown(
            f"<h3 style='color:white;font-family:Baloo 2;'>{recent_title}</h3>",
            unsafe_allow_html=True,
        )

        try:
            resp = asyncio.run(get_my_posts())
            if resp.status_code == 200:
                posts = resp.json()
                if posts:
                    for post in posts[:5]:
                        title = post.get("challenge", {}).get(f"title_{lang}", "")
                        created = post.get("created_at", "")
                        st.markdown(
                            f"<div class='friend-item'>"
                            f"<div><small style='opacity:0.7;'>{title[:40]}...</small></div>"
                            f"</div>",
                            unsafe_allow_html=True,
                        )
                else:
                    no_posts_msg = "No posts yet. Complete today's challenge! 📸" if lang == "en" else "कुनै पोस्ट छैन। आजको च्यालेन्ज पूरा गर्नुहोस्! 📸"
                    st.markdown(
                        f"<p style='color:rgba(255,255,255,0.5);text-align:center;'>"
                        f"{no_posts_msg}</p>",
                        unsafe_allow_html=True,
                    )
        except Exception:
            pass

        with st.container():
            tips_title = "💡 Tips" if lang == "en" else "💡 सुझाव"
            tip1 = "Post daily to maintain your streak 🔥" if lang == "en" else "आफ्नो स्ट्रीक कायम राख्न दैनिक पोस्ट गर्नुहोस् 🔥"
            tip2 = "React to friends' posts 💜" if lang == "en" else "साथीहरूको पोस्टमा प्रतिक्रिया दिनुहोस् 💜"
            tip3 = "Add friends for more fun 👥" if lang == "en" else "अर्को मजाको लागि साथीहरू थप्नुहोस् 👥"
            st.markdown(
                f"<div style='background:rgba(255,255,255,0.1);border-radius:16px;padding:20px;"
                f"margin-top:20px;text-align:center;'>"
                f"<h4 style='color:white;font-family:Baloo 2;margin:0;'>{tips_title}</h4>"
                f"<ul style='color:rgba(255,255,255,0.7);text-align:left;font-size:0.85rem;"
                f"margin-top:10px;'>"
                f"<li>{tip1}</li>"
                f"<li>{tip2}</li>"
                f"<li>{tip3}</li>"
                f"</ul>"
                f"</div>",
                unsafe_allow_html=True,
            )
