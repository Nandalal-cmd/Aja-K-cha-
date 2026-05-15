import streamlit as st
import asyncio
from frontend.utils.api_client import login as api_login


def show():
    lang = st.session_state.language
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        subtitle = "Daily challenges for Nepali youth 🇳🇵" if lang == "en" else "नेपाली युवाका लागि दैनिक च्यालेन्जहरू 🇳🇵"
        st.markdown(
            "<p class='big-title' style='margin-top:40px;'>🔥</p>"
            "<p class='big-title'>Aaj K Garne?</p>"
            f"<p class='subtitle'>{subtitle}</p>",
            unsafe_allow_html=True,
        )

        with st.container():
            st.markdown(
                "<div style='background:rgba(255,255,255,0.1);border-radius:20px;padding:30px;"
                "backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,0.15);'>",
                unsafe_allow_html=True,
            )

            welcome = "Welcome Back! 🤙" if lang == "en" else "फेरि स्वागत छ! 🤙"
            st.markdown(
                f"<h3 style='color:white;text-align:center;font-family:Baloo 2;margin-bottom:20px;'>"
                f"{welcome}</h3>",
                unsafe_allow_html=True,
            )

            user_label = "Username" if lang == "en" else "प्रयोगकर्ता नाम"
            user_placeholder = "Enter your username" if lang == "en" else "तपाईंको प्रयोगकर्ता नाम प्रविष्ट गर्नुहोस्"
            pass_label = "Password" if lang == "en" else "पासवर्ड"
            pass_placeholder = "Enter your password" if lang == "en" else "तपाईंको पासवर्ड प्रविष्ट गर्नुहोस्"
            login_btn = "Login 🔥" if lang == "en" else "लग इन 🔥"
            username = st.text_input(user_label, placeholder=user_placeholder, key="login_user")
            password = st.text_input(
                pass_label, placeholder=pass_placeholder, type="password", key="login_pass"
            )

            if st.button(login_btn, use_container_width=True):
                if username and password:
                    spinner_msg = "Logging in..." if lang == "en" else "लग इन हुँदै..."
                    with st.spinner(spinner_msg):
                        try:
                            resp = asyncio.run(api_login(username, password))
                            if resp.status_code == 200:
                                data = resp.json()
                                st.session_state.token = data["access_token"]
                                st.session_state.user = data["user"]
                                st.session_state.page = "home"
                                st.rerun()
                            else:
                                detail = resp.json().get("detail", "Invalid credentials")
                                st.error(f"❌ {detail}")
                        except Exception as e:
                            conn_err = f"❌ Connection error: {e}" if lang == "en" else f"❌ जडान त्रुटि: {e}"
                            st.error(conn_err)
                else:
                    fill_warn = "Please fill in all fields" if lang == "en" else "कृपया सबै फिल्ड भर्नुहोस्"
                    st.warning(fill_warn)

            st.markdown("</div>", unsafe_allow_html=True)

            col_a, col_b = st.columns(2)
            with col_a:
                no_account = "No account?" if lang == "en" else "खाता छैन?"
                st.markdown(
                    f"<p style='text-align:center;color:rgba(255,255,255,0.7);margin-top:15px;'>"
                    f"{no_account}</p>",
                    unsafe_allow_html=True,
                )
            with col_b:
                signup_btn = "Sign Up 📝" if lang == "en" else "साइन अप 📝"
                if st.button(signup_btn):
                    st.session_state.page = "register"
                    st.rerun()
