import streamlit as st
from deep_translator import GoogleTranslator
import edge_tts
import asyncio
import uuid
import os
from pydub import AudioSegment
import base64

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

        # ファイル名
        uid = str(uuid.uuid4())
        temp_file = f"{uid}.mp3"
        final_file = f"repeat_{uid}.mp3"

        # 音声生成
        async def generate():
            communicate = edge_tts.Communicate(text=translated, voice="en-US-JennyNeural")
            await communicate.save(temp_file)

        asyncio.run(generate())

        # リピート処理
        audio = AudioSegment.from_file(temp_file, format="mp3")
        repeated = audio * repeat_count
        repeated.export(final_file, format="mp3")

        # base64エンコードして埋め込みプレーヤー作成
        with open(final_file, "rb") as f:
            audio_bytes = f.read()
            b64_audio = base64.b64encode(audio_bytes).decode()

        audio_html = f"""
        <audio controls>
            <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
            お使いのブラウザでは再生できません。
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

        # ダウンロードボタン
        st.download_button("📥 音声をダウンロード", data=audio_bytes, file_name="voice.mp3", mime="audio/mp3")

        # 一時ファイル削除
        os.remove(temp_file)
        os.remove(final_file)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")





