import streamlit as st
from deep_translator import GoogleTranslator
import edge_tts
import asyncio
import uuid
import os
import base64

# 言語とTTSボイスの設定
languages = {
    "日本語": ("ja", "ja-JP-NanamiNeural"),
    "英語": ("en", "en-US-JennyNeural"),
    "フランス語": ("fr", "fr-FR-DeniseNeural"),
    "スペイン語": ("es", "es-ES-ElviraNeural"),
    "ポルトガル語": ("pt", "pt-BR-FranciscaNeural"),
    "ドイツ語": ("de", "de-DE-KatjaNeural")
}

st.set_page_config(page_title="多言語翻訳＆音声アプリ", layout="centered")
st.title("🌍 多言語 翻訳 & 音声再生アプリ")

text = st.text_input("翻訳する文章を入力してください")

col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("翻訳元の言語", list(languages.keys()), index=0)
with col2:
    tgt_lang = st.selectbox("翻訳先の言語", list(languages.keys()), index=1)

repeat_count = st.number_input("🔁 再生回数を指定してください", min_value=1, max_value=10, value=1, step=1)

async def generate_audio(text, voice, filename):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(filename)

def get_audio_download_link(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:audio/mp3;base64,{b64}" download="voice.mp3">📥 音声をダウンロード</a>'

if st.button("翻訳して音声再生・ダウンロード"):
    if text.strip() == "":
        st.warning("⚠️ テキストを入力してください。")
    else:
        try:
            src_code, _ = languages[src_lang]
            tgt_code, voice = languages[tgt_lang]

            translated = GoogleTranslator(source=src_code, target=tgt_code).translate(text)
            st.success(f"✅ 翻訳結果: {translated}")

            # テキストをリピート回数分つなげて読み上げ
            repeated_text = (" " + translated) * repeat_count
            filename = f"{uuid.uuid4()}.mp3"

            asyncio.run(generate_audio(repeated_text.strip(), voice, filename))

            with open(filename, "rb") as f:
                audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/mp3")

            st.markdown(get_audio_download_link(filename), unsafe_allow_html=True)

            os.remove(filename)

        except Exception as e:
            st.error(f"❌ エラーが発生しました: {e}")



