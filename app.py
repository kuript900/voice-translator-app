import streamlit as st
from deep_translator import GoogleTranslator
import edge_tts
import asyncio
import uuid
import os
from pydub import AudioSegment

# 言語設定
languages = {
    "日本語": "ja",
    "英語": "en",
    "フランス語": "fr",
    "スペイン語": "es",
    "ポルトガル語": "pt",
    "ドイツ語": "de"
}

# ページ設定
st.set_page_config(page_title="多言語翻訳＆音声再生アプリ", layout="centered")
st.markdown("<h1 style='text-align: center; font-size: 24px;'>多言語 翻訳 & 音声アプリ</h1>", unsafe_allow_html=True)

# 入力
text = st.text_input("翻訳する文章を入力してください")

col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("翻訳元の言語", list(languages.keys()), index=0)
with col2:
    tgt_lang = st.selectbox("翻訳先の言語", list(languages.keys()), index=1)

repeat_count = st.number_input("リピート回数", min_value=1, max_value=10, value=1, step=1)

# 翻訳と音声生成
if st.button("翻訳して音声再生・ダウンロード"):
    try:
        # 翻訳
        translated = GoogleTranslator(source=languages[src_lang], target=languages[tgt_lang]).translate(text)
        st.success(f"翻訳結果: {translated}")

        # 一時ファイル名
        unique_id = str(uuid.uuid4())
        temp_filename = f"{unique_id}.mp3"
        final_filename = f"repeat_{unique_id}.mp3"

        # 音声生成（非同期）
        async def generate_tts():
            communicate = edge_tts.Communicate(text=translated, voice="en-US-JennyNeural")
            await communicate.save(temp_filename)

        asyncio.run(generate_tts())

        # リピート結合
        sound = AudioSegment.from_file(temp_filename, format="mp3")
        repeated = sound * repeat_count
        repeated.export(final_filename, format="mp3")

        # 再生とダウンロード
        st.audio(final_filename)
        with open(final_filename, "rb") as f:
            st.download_button("音声をダウンロード", f, file_name="voice.mp3")

        # 後始末
        os.remove(temp_filename)
        os.remove(final_filename)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")




