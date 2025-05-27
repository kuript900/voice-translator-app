import streamlit as st
from deep_translator import GoogleTranslator
import edge_tts
import asyncio
import uuid
import os

# 多言語対応
languages = {
    "日本語": "ja",
    "英語": "en",
    "フランス語": "fr",
    "スペイン語": "es",
    "ポルトガル語": "pt",
    "ドイツ語": "de"
}

st.set_page_config(page_title="多言語翻訳＆音声アプリ", layout="centered")
st.title("多言語 翻訳 & 音声再生アプリ")

# 入力と言語選択
text = st.text_input("翻訳する文章を入力してください")

col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("翻訳元の言語", list(languages.keys()), index=0)
with col2:
    tgt_lang = st.selectbox("翻訳先の言語", list(languages.keys()), index=1)

# 翻訳と音声処理
if st.button("翻訳して音声再生・ダウンロード"):
    try:
        translated = GoogleTranslator(
            source=languages[src_lang],
            target=languages[tgt_lang]
        ).translate(text)

        st.success(f"翻訳結果：{translated}")

        # 音声ファイル生成（非同期処理）
        output_path = f"{uuid.uuid4()}.mp3"

        async def generate_audio(text, lang_code, filename):
            communicate = edge_tts.Communicate(text, lang_code)
            await communicate.save(filename)

        asyncio.run(generate_audio(translated, languages[tgt_lang], output_path))

        # 再生 & ダウンロードリンク
        with open(output_path, "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")
            st.download_button("音声をダウンロード", audio_file, file_name="translation.mp3")

        os.remove(output_path)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
