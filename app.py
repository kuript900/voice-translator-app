import streamlit as st
from deep_translator import GoogleTranslator
import edge_tts
import asyncio
import uuid
import os
import base64

# 対応言語と音声ID
languages = {
    "日本語":  ("ja", "ja-JP-NanamiNeural"),
    "英語":    ("en", "en-US-JennyNeural"),
    "フランス語": ("fr", "fr-FR-DeniseNeural"),
    "スペイン語": ("es", "es-ES-ElviraNeural"),
    "ポルトガル語": ("pt", "pt-BR-FranciscaNeural"),
    "ドイツ語": ("de", "de-DE-KatjaNeural")
}

st.set_page_config(page_title="翻訳＆自動リピート音声アプリ", layout="centered")
st.title("🌐 多言語 翻訳 & 自動音声リピート")

# 入力・言語選択
text = st.text_input("翻訳する文章を入力してください")

col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("翻訳元の言語", list(languages.keys()), index=0)
with col2:
    tgt_lang = st.selectbox("翻訳先の言語", list(languages.keys()), index=1)

repeat_count = st.number_input("🔁 自動再生回数", min_value=1, max_value=10, value=1)

if st.button("翻訳・音声生成・自動再生"):
    try:
        src_code, _ = languages[src_lang]
        tgt_code, voice_id = languages[tgt_lang]

        translated = GoogleTranslator(source=src_code, target=tgt_code).translate(text)
        st.success(f"翻訳結果：{translated}")

        filename = f"{uuid.uuid4().hex}.mp3"

        async def create_audio(text, voice, filename):
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(filename)

        asyncio.run(create_audio(translated, voice_id, filename))

        with open(filename, "rb") as f:
            audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()

            st.markdown("🔊 指定回数だけ自動で再生されます")

            # JavaScriptで完全制御されたaudioタグと再生処理
            st.markdown(
                f"""
                <script>
                let count = 1;
                let maxCount = {int(repeat_count)};
                const audio = new Audio("data:audio/mp3;base64,{b64}");
                audio.play();

                audio.addEventListener('ended', () => {{
                    if (count < maxCount) {{
                        count++;
                        audio.play();
                    }}
                }});
                </script>
                """,
                unsafe_allow_html=True
            )

            st.download_button("🎧 音声をダウンロード", audio_bytes, file_name="translated.mp3")
        os.remove(filename)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")



