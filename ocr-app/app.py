import streamlit as st
import auth_functions
from PIL import Image
from streamlit_ocr import ocr_func

## -------------------------------------------------------------------------------------------------
## Not logged in -----------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
if 'user_info' not in st.session_state:
    col1,col2,col3 = st.columns([1,2,1])

    col2.title('OCRデモアプリ')

    # Authentication form layout
    do_you_have_an_account = col2.selectbox(label='アカウントを持っていますか？', options=("はい", "いいえ", "パスワードを忘れた"))
    auth_form = col2.form(key='Authentication form',clear_on_submit=False)
    email = auth_form.text_input(label='Email')
    password = auth_form.text_input(label='Password',type='password') if do_you_have_an_account in {'はい','いいえ'} else auth_form.empty()
    auth_notification = col2.empty()

    col2.write('認証メールが届かない場合は、迷惑メールフォルダをご確認ください')

    # Sign In
    if do_you_have_an_account == "はい" and auth_form.form_submit_button(label='ログイン',use_container_width=True,type='primary'):
        with auth_notification, st.spinner('Signing in'):
            auth_functions.sign_in(email,password)

    # Create Account
    elif do_you_have_an_account == 'いいえ' and auth_form.form_submit_button(label='アカウント作成',use_container_width=True,type='primary'):
        with auth_notification, st.spinner('Creating account'):
            auth_functions.create_account(email,password)

    # Password Reset
    elif do_you_have_an_account == 'パスワードを忘れた' and auth_form.form_submit_button(label='パスワードをリセット',use_container_width=True,type='primary'):
        with auth_notification, st.spinner('Sending password reset link'):
            auth_functions.reset_password(email)

    # Authentication success and warning messages
    if 'auth_success' in st.session_state:
        auth_notification.success(st.session_state.auth_success)
        del st.session_state.auth_success
    elif 'auth_warning' in st.session_state:
        auth_notification.warning(st.session_state.auth_warning)
        del st.session_state.auth_warning

## -------------------------------------------------------------------------------------------------
## Logged in --------------------------------------------------------------------------------------
## -------------------------------------------------------------------------------------------------
else:
    # OCR function
    ocr_func()

    st.markdown("お問い合わせは[こちら](https://docs.google.com/forms/d/e/1FAIpQLSfW9PwinbhJd2EWGia0wd-_ryJCdjzs4YZtHLT5tmW21abFhg/viewform)まで")

    st.divider()

    # About the creator
    st.markdown("### 作成者について:")

    prof_img = Image.open('./daichi.png')
    st.image(prof_img, caption='Daichi Nagashima')

    st.markdown("[X](https://x.com/longislandtea3)")
    st.markdown("[Linkedin](https://www.linkedin.com/in/daichi-nagashima-3a1b3b1b3/)")
    st.markdown(" **医師** として働く傍ら、**画像生成AI -Stable Diffusion-** のチューニングを試み、当時最高レベルの写真生成AIモデルを作成."
                  + "  \n モデルの精度は高く評価され、その後の写真生成AIに大きな影響を与えた"
                  + "  \n AIベンチャーにヘッドハンティングされ、医師からAIエンジニアに転身"
                  + "  \n 一年間AIシステム開発・アプリ製作に携わり2024年5月退職"
                  + "  \n 現在はフリーランスで生成AIの医療への応用に挑戦している")

    # Sign out
    st.sidebar.markdown('### ログアウト:')
    st.sidebar.button(label='ログアウト',on_click=auth_functions.sign_out,type='primary')

    st.sidebar.divider()

    # Delete Account
    st.sidebar.markdown('### アカウントを削除:')
    password = st.sidebar.text_input(label='パスワードを入力',type='password')
    st.sidebar.button(label='アカウントを削除',on_click=auth_functions.delete_account,args=[password],type='primary')