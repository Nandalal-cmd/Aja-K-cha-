import streamlit as st
import asyncio
from frontend.utils.api_client import register as api_register


def show():
    lang = st.session_state.language
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        join_title = "🎉 Join the Fun!" if lang == "en" else "🎉 मजामा सामेल हुनुहोस्!"
        join_sub = "Complete daily challenges, earn streaks, vibe with friends!" if lang == "en" else "दैनिक च्यालेन्जहरू पूरा गर्नुहोस्, स्ट्रीक जित्नुहोस्!"
        st.markdown(
            f"<p class='big-title' style='margin-top:30px;'>{join_title}</p>"
            f"<p class='subtitle'>{join_sub}</p>",
            unsafe_allow_html=True,
        )

        with st.container():
            st.markdown(
                "<div style='background:rgba(255,255,255,0.1);border-radius:20px;padding:30px;"
                "backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,0.15);'>",
                unsafe_allow_html=True,
            )

            create_title = "Create Account ✨" if lang == "en" else "खाता बनाउनुहोस् ✨"
            st.markdown(
                f"<h3 style='color:white;text-align:center;font-family:Baloo 2;margin-bottom:20px;'>"
                f"{create_title}</h3>",
                unsafe_allow_html=True,
            )

            user_label = "Username" if lang == "en" else "प्रयोगकर्ता नाम"
            user_placeholder = "Choose a cool username" if lang == "en" else "राम्रो प्रयोगकर्ता नाम छान्नुहोस्"
            display_label = "Display Name" if lang == "en" else "प्रदर्शन नाम"
            display_placeholder = "What should we call you?" if lang == "en" else "हामी तपाईंलाई के भनौं?"
            pass_label = "Password" if lang == "en" else "पासवर्ड"
            pass_placeholder = "Create a password (min 4 chars)" if lang == "en" else "पासवर्ड बनाउनुहोस् (न्यूनतम ४ वर्ण)"
            confirm_label = "Confirm Password" if lang == "en" else "पासवर्ड पुष्टि"
            confirm_placeholder = "Type password again" if lang == "en" else "पासवर्ड फेरि टाइप गर्नुहोस्"
            signup_btn = "Sign Up 🚀" if lang == "en" else "साइन अप 🚀"

            username = st.text_input(user_label, placeholder=user_placeholder, key="reg_user")
            display_name = st.text_input(
                display_label, placeholder=display_placeholder, key="reg_display"
            )
            password = st.text_input(
                pass_label, placeholder=pass_placeholder, type="password", key="reg_pass"
            )
            confirm = st.text_input(
                confirm_label, placeholder=confirm_placeholder, type="password", key="reg_confirm"
            )

            if st.button(signup_btn, use_container_width=True):
                fill_warn = "Please fill in all fields" if lang == "en" else "कृपया सबै फिल्ड भर्नुहोस्"
                pass_mismatch = "Passwords don't match!" if lang == "en" else "पासवर्ड मेल खाएन!"
                pass_short = "Password must be at least 4 characters" if lang == "en" else "पासवर्ड कम्तीमा ४ वर्णको हुनुपर्छ"
                if not (username and display_name and password and confirm):
                    st.warning(fill_warn)
                elif password != confirm:
                    st.error(pass_mismatch)
                elif len(password) < 4:
                    st.error(pass_short)
                else:
                    spinner_msg = "Creating account..." if lang == "en" else "खाता बनाउँदै..."
                    with st.spinner(spinner_msg):
                        try:
                            resp = asyncio.run(api_register(username, display_name, password))
                            if resp.status_code == 200:
                                data = resp.json()
                                st.session_state.token = data["access_token"]
                                st.session_state.user = data["user"]
                                st.session_state.page = "home"
                                st.rerun()
                            else:
                                detail = resp.json().get("detail", "Registration failed")
                                st.error(f"❌ {detail}")
                        except Exception as e:
                            conn_err = f"❌ Connection error: {e}" if lang == "en" else f"❌ जडान त्रुटि: {e}"
                            st.error(conn_err)

            st.markdown("</div>", unsafe_allow_html=True)

            login_link = "← Already have an account? Login" if lang == "en" else "← पहिले नै खाता छ? लग इन"
            if st.button(login_link):
                st.session_state.page = "login"
                st.rerun()
