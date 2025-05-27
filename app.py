import streamlit as st
from deep_translator import GoogleTranslator
import edge_tts
import asyncio
import uuid
import os
import base64
import subprocess

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

# ffmpeg でMP3をリピート結合する関数
def repeat_audio_ffmpeg(input_file, repeat_count, output_file):
    with open("concat_list.txt", "w") as f:
        for _ in range(repeat_count):
            f.write(f"file '{input_file}'\n")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "concat_list.txt", "-c", "copy", output_file], check=True)
    os.remove("concat_list.txt")

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

        # ffmpeg でリピート結合
        repeat_audio_ffmpeg(temp_file, int(repeat_count), final_file)

        with open(final_file, "rb") as f:
            audio_data = f.read()

        st.audio(audio_data, format="audio/mp3")
        st.download_button("🎧 音声をダウンロード", audio_data, file_name="translated.mp3")

        os.remove(temp_file)
        os.remove(final_file)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

