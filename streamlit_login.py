import streamlit as st
import pyrebase

# Firebaseの設定
firebaseConfig = {
    'apiKey': "your-api-key",
    'authDomain': "your-auth-domain",
    'projectId': "your-project-id",
    'storageBucket': "your-storage-bucket",
    'messagingSenderId': "your-messaging-sender-id",
    'appId': "your-app-id",
    'measurementId': "your-measurement-id"
}

# Firebaseの初期化
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# ユーザー認証のための関数
def sign_in(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user
    except:
        return None

# 認証が必要なページを表示する関数
def dashboard():
    st.title("Dashboard")
    st.write("Welcome to the dashboard!")
    if st.button("Logout"):
        del st.session_state['user']
        st.experimental_rerun()

# ログインページを表示する関数
def login():
    st.title("Login")

    # ログインフォーム
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        user = sign_in(email, password)
        if user:
            st.success(f"Logged in as {user['email']}")
            st.session_state['user'] = user
            st.experimental_rerun()  # ページをリロードしてセッションステートを確認
        else:
            st.error("Invalid credentials")

def run():
    # ユーザーがログインしているかどうかを確認
    if 'user' in st.session_state:
        dashboard()
    else:
        login()

if __name__ == '__main__':
    run()
