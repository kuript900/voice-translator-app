import streamlit as st
from deep_translator import GoogleTranslator
import edge_tts
import asyncio
import uuid
import os

# 言語表示名 → 言語コード（翻訳用）と 音声ID（音声用）
languages = {
    "日本語":  ("ja", "ja-JP-NanamiNeural"),
    "英語":    ("en", "en-US-JennyNeural"),
    "フランス語": ("fr", "fr-FR-DeniseNeural"),
    "スペイン語": ("es", "es-ES-ElviraNeural"),
    "ポルトガル語": ("pt", "pt-BR-FranciscaNeural"),
    "ドイツ語": ("de", "de-DE-KatjaNeural")
}

st.set_page_config(page_title="翻訳＆音声アプリ", layout="centered")
st.title("🌐 多言語 翻訳 & 音声アプリ")

text = st.text_input("翻訳する文章を入力してください")

col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("翻訳元の言語", list(languages.keys()), index=0)
with col2:
    tgt_lang = st.selectbox("翻訳先の言語", list(languages.keys()), index=1)

if st.button("翻訳して音声再生＆ダウンロード"):
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
            audio_data = f.read()
            st.audio(audio_data, format="audio/mp3")
            st.download_button("🎧 音声をダウンロード", audio_data, file_name="translated.mp3")

        os.remove(filename)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

