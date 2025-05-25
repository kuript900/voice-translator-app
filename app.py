import streamlit as st
from gtts import gTTS
from deep_translator import LibreTranslator
from io import BytesIO
import base64

# タイトルを少し小さく
st.markdown("<h4 style='text-align: center;'>翻訳付き音声作成アプリ</h4>", unsafe_allow_html=True)

text = st.text_area("しゃべらせたい日本語を入力してください")
repeat_count = st.number_input("リピート回数（自動再生）", min_value=1, max_value=10, value=1, step=1)

if st.button("英語で音声を作る"):
    if text:
        try:
            translated_text = LibreTranslator(source="ja", target="en").translate(text)
            st.write("翻訳：", translated_text)

            # 音声作成
            tts = gTTS(translated_text, lang='en')
            mp3_fp = BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            audio_data = mp3_fp.read()
            audio_base64 = base64.b64encode(audio_data).decode()

            # リピート再生のJS
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
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
    else:
        st.warning("日本語を入力してください。")

