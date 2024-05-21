import streamlit as st
from PIL import Image
from datetime import datetime
from ocr_vision_api import img_to_csv

def ocr_func():
    st.title('OCRアプリケーション')

    # セッションステートに処理回数を保持
    if 'process_count' not in st.session_state:
        st.session_state.process_count = 0
        st.session_state.max_process_count = 10

    remaining_attempts = st.session_state.max_process_count - st.session_state.process_count
    st.write(f'残りの処理回数: {remaining_attempts}')

    if remaining_attempts > 0:
        # ファイルアップローダーを作成
        uploaded_file = st.file_uploader("画像ファイルを選択してください", type=['png', 'jpg', 'jpeg', 'webp'])

        if uploaded_file is not None:
            # MIMEタイプをチェック
            if uploaded_file.type.startswith('image/'):
                # PILで画像を開く
                image = Image.open(uploaded_file)
                st.image(image, caption='アップロードされた画像', use_column_width=True)

                current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                image.save(f'./images/{current_time}.jpg')

                # ロードスピナーを表示
                with st.spinner('画像を処理中...'):
                    dataframe = img_to_csv(image, 'checkup_results.csv')

                # 処理回数を増加
                st.session_state.process_count += 1

                # 出力
                st.write(dataframe)
            else:
                st.error('アップロードされたファイルは画像ではありません。')
    else:
        st.error('処理回数の上限に達しました。')

if __name__ == '__main__':
    ocr_func()
