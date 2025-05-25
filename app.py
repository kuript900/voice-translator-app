import streamlit as st
from gtts import gTTS
from googletrans import Translator
from io import BytesIO
import base64

# タイトルを小さく表示
st.markdown("<h4 style='text-align: center;'>翻訳付き音声作成アプリ</h4>", unsafe_allow_html=True)

text = st.text_area("しゃべらせたい日本語を入力してください")
repeat_count = st.number_input("リピート回数（自動再生）", min_value=1, max_value=10, value=1, step=1)

if st.button("英語で音声を作る"):
    if text:
        translator = Translator()
        translated = translator.translate(text, src='ja', dest='en')
        st.write("翻訳：", translated.text)

        # 音声生成
        tts = gTTS(translated.text, lang='en')
        mp3_fp = BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        audio_data = mp3_fp.read()
        audio_base64 = base64.b64encode(audio_data).decode()

        # 再生プレイヤー
        st.audio(audio_data, format='audio/mp3')

        # JavaScriptで自動リピート再生
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
        st.components.v1.html(js_code)
    else:
        st.warning("日本語を入力してください。")


