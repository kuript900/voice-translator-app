import streamlit as st
from deep_translator import GoogleTranslator
import edge_tts
import asyncio
import uuid
import os

# 翻訳対応言語（表示用とコードのマッピング）
languages = {
    "日本語": "ja",
    "英語": "en",
    "フランス語": "fr",
    "スペイン語": "es",
    "ポルトガル語": "pt",
    "ドイツ語": "de"
}

st.set_page_config(page_title="翻訳＆音声アプリ", layout="centered")
st.title("🌐 多言語 翻訳 & 音声アプリ")

# 入力欄と言語選択
text = st.text_input("翻訳する文章を入力してください")

col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("翻訳元の言語", list(languages.keys()), index=0)
with col2:
    tgt_lang = st.selectbox("翻訳先の言語", list(languages.keys()), index=1)

# 実行ボタン
if st.button("翻訳して音声再生＆ダウンロード"):
    try:
        # 翻訳処理
        translated = GoogleTranslator(
            source=languages[src_lang],
            target=languages[tgt_lang]
        ).translate(text)

        st.success(f"翻訳結果：{translated}")

        # 音声ファイル名生成
        output_file = f"{uuid.uuid4().hex}.mp3"

        # 非同期で音声生成（edge-tts）
        async def create_audio(text, lang_code, filename):
            communicate = edge_tts.Communicate(text, lang_code)
            await communicate.save(filename)

        asyncio.run(create_audio(translated, languages[tgt_lang], output_file))

        # 再生とダウンロード
        with open(output_file, "rb") as audio_file:
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3")
            st.download_button(
                label="🎧 音声をダウンロード",
                data=audio_bytes,
                file_name="translated_audio.mp3",
                mime="audio/mpeg"
            )

        os.remove(output_file)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

