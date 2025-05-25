import streamlit as st
from gtts import gTTS
from deep_translator import GoogleTranslator
from io import BytesIO
import base64

# ページ設定（スマホ最適化）
st.set_page_config(page_title="翻訳付き音声作成アプリ", layout="centered")

# タイトル（小さめ）
st.markdown("<h2 style='text-align: center;'>翻訳付き音声作成アプリ</h2>", unsafe_allow_html=True)

# 入力欄
text = st.text_area("しゃべらせたい日本語を入力してください")

# 繰り返し回数
repeat_count = st.number_input("リピート回数（自動再生）", min_value=1, max_value=10, value=1, step=1)

# 実行ボタン
if st.button("英語で音声を作る"):
    if text:
        try:
            # 安定した翻訳（deep-translator）
            translated = GoogleTranslator(source='ja', target='en').translate(text)
            st.write("翻訳：", translated)

            # 音声作成
            tts = gTTS(translated, lang='en')
            mp3_fp = BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            audio_data = mp3_fp.read()
            audio_base64 = base64.b64encode(audio_data).decode()

            # プレイヤー表示（手動でも再生可能）
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

        except Exception as e:
            st.error("エラーが発生しました。翻訳または音声の処理で問題があります。")
            st.exception(e)
    else:
        st.warning("日本語を入力してください。")


