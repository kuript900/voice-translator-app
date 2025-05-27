import streamlit as st
from deep_translator import GoogleTranslator
import edge_tts
import asyncio
import uuid
import os
import base64
from pydub import AudioSegment

# 言語対応とVoice ID
languages = {
    "日本語": ("ja", "ja-JP-NanamiNeural"),
    "英語": ("en", "en-US-JennyNeural"),
    "フランス語": ("fr", "fr-FR-DeniseNeural"),
    "スペイン語": ("es", "es-ES-ElviraNeural"),
    "ポルトガル語": ("pt", "pt-BR-FranciscaNeural"),
    "ドイツ語": ("de", "de-DE-KatjaNeural")
}

st.set_page_config(page_title="翻訳＆音声リピートアプリ", layout="centered")
st.title("🌐 多言語 翻訳 & 音声リピートアプリ")

text = st.text_input("翻訳する文章を入力してください")

col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("翻訳元の言語", list(languages.keys()), index=0)
with col2:
    tgt_lang = st.selectbox("翻訳先の言語", list(languages.keys()), index=1)

repeat_count = st.number_input("🔁 自動再生の回数", min_value=1, max_value=10, value=1)

def concatenate_audio(file_path: str, repeat_count: int, output_path: str):
    original = AudioSegment.from_file(file_path, format="mp3")
    combined = original * repeat_count
    combined.export(output_path, format="mp3")
    return output_path

if st.button("翻訳して音声生成"):
    try:
        src_code, _ = languages[src_lang]
        tgt_code, voice_id = languages[tgt_lang]

        translated = GoogleTranslator(source=src_code, target=tgt_code).translate(text)
        st.success(f"翻訳結果：{translated}")

        temp_file = f"{uuid.uuid4().hex}.mp3"
        final_file = f"{uuid.uuid4().hex}_repeated.mp3"

        async def generate_audio(text, voice, file):
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(file)

        asyncio.run(generate_audio(translated, voice_id, temp_file))

        # 音声を結合して繰り返す
        concatenate_audio(temp_file, int(repeat_count), final_file)

        # 音声をバイナリで読み込み
        with open(final_file, "rb") as f:
            audio_data = f.read()

        # 再生とダウンロード
        st.audio(audio_data, format="audio/mp3")
        st.download_button("🎧 音声をダウンロード", audio_data, file_name="translated.mp3")

        # 一時ファイル削除
        os.remove(temp_file)
        os.remove(final_file)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

