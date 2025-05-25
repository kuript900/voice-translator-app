import streamlit as st
from gtts import gTTS
from googletrans import Translator
from io import BytesIO
import base64

# ページ設定（スマホ対応）
st.set_page_config(page_title="翻訳付き音声作成アプリ", layout="centered")

# タイトル（サイズ小さめに調整）
st.markdown("""
    <h1 style='font-size:24px; text-align:center;'>翻訳付き音声作成アプリ</h1>
""", unsafe_allow_html=True)

# 入力欄
text = st.text_area("英語にしたい日本語を入力してください")
repeat_count = st.number_input("リピート回数（自動再生）", min_value=1, max_value=10, value=1, step=1)

# 実行ボタン
if st.button("英語で音声を作る"):
    if text:
        translator = Translator()
        translated = translator.translate(text, src='ja', dest='en')
        st.write("翻訳：", translated.text)

        tts = gTTS(translated.text, lang='en')
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        audio_data = mp3_fp.read()
        audio_base64 = base64.b64encode(audio_data).decode()

        js_code = f"""
        <script>
        var count = 0;
        var maxCount = {repeat_count};
        var audio = new Audio("data:audio/mp3;base64,{audio_base64}");
        audio.play();
        audio.onended = function() {{
            count++;
            if(count < maxCount) {{
                audio.currentTime = 0;
                audio.play();
            }}
        }};
        </script>
        """

        st.audio(audio_data, format="audio/mp3")
        st.components.v1.html(js_code)
    else:
        st.warning("日本語を入力してください。")


