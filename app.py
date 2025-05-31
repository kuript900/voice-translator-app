import streamlit as st
from deep_translator import GoogleTranslator
import edge_tts
import asyncio
import uuid
import os
import base64
from pathlib import Path
from tempfile import NamedTemporaryFile

# 言語対応
languages = {
    "日本語": "ja",
    "英語": "en",
    "フランス語": "fr",
    "スペイン語": "es",
    "ポルトガル語": "pt",
    "ドイツ語": "de"
}

st.set_page_config(page_title="多言語翻訳＆音声再生アプリ", layout="centered")
st.markdown("<h1 style='text-align: center; font-size: 24px;'>多言語 翻訳 & 音声アプリ</h1>", unsafe_allow_html=True)

text = st.text_input("翻訳する文章を入力してください")

col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("翻訳元の言語", list(languages.keys()), index=0)
with col2:
    tgt_lang = st.selectbox("翻訳先の言語", list(languages.keys()), index=1)

repeat_count = st.number_input("リピート回数", min_value=1, max_value=10, value=1, step=1)

if st.button("翻訳して音声再生・ダウンロード"):
    try:
        translated = GoogleTranslator(source=languages[src_lang], target=languages[tgt_lang]).translate(text)
        st.success(f"翻訳結果: {translated}")

        # ファイル名生成
        uid = str(uuid.uuid4())
        single_file = f"{uid}_one.mp3"
        repeated_file = f"{uid}_repeated.mp3"

        # 音声生成（非同期）
        async def gen():
            communicate = edge_tts.Communicate(text=translated, voice="en-US-JennyNeural")
            await communicate.save(single_file)

        asyncio.run(gen())

        # MP3をバイナリで複製
        with open(single_file, "rb") as f:
            segment = f.read()

        # リピート結合
        with open(repeated_file, "wb") as out:
            for _ in range(repeat_count):
                out.write(segment)

        # base64にして再生埋め込み
        with open(repeated_file, "rb") as f:
            audio_bytes = f.read()
            b64_audio = base64.b64encode(audio_bytes).decode()

        html_audio = f"""
        <audio controls>
            <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
            お使いのブラウザでは再生できません。
        </audio>
        """
        st.markdown(html_audio, unsafe_allow_html=True)

        # ダウンロードボタン
        st.download_button("📥 音声をダウンロード", data=audio_bytes, file_name="voice.mp3", mime="audio/mp3")

        # 後処理
        os.remove(single_file)
        os.remove(repeated_file)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
