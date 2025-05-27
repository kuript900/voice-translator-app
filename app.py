import streamlit as st
from deep_translator import GoogleTranslator
import edge_tts
import asyncio
import uuid
import os
import base64

# 言語と言語ごとの TTS ボイス
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

# 入力UI
text = st.text_input("翻訳する文章を入力してください")

col1, col2 = st.columns(2)
with col1:
    src_lang = st.selectbox("翻訳元の言語", list(languages.keys()), index=0)
with col2:
    tgt_lang = st.selectbox("翻訳先の言語", list(languages.keys()), index=1)

repeat_count = st.number_input("🔁 自動再生の回数", min_value=1, max_value=10, value=1)

# メイン処理
if st.button("翻訳して音声生成"):
    try:
        src_code, _ = languages[src_lang]
        tgt_code, voice_id = languages[tgt_lang]

        translated = GoogleTranslator(source=src_code, target=tgt_code).translate(text)
        st.success(f"翻訳結果：{translated}")

        filename = f"{uuid.uuid4().hex}.mp3"

        async def generate_audio(text, voice, file):
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(file)

        asyncio.run(generate_audio(translated, voice_id, filename))

        with open(filename, "rb") as f:
            audio_data = f.read()
            b64_audio = base64.b64encode(audio_data).decode()

        # 再生保険
        st.markdown("🧪 音声が再生されない場合、以下からも再生してみてください：")
        st.audio(audio_data, format="audio/mp3")

        # JSでリピート再生対応
        st.markdown("📱 再生ボタンを押すと指定回数だけ自動で再生されます：")
        st.markdown(
            f"""
            <audio id="audioPlayer" src="data:audio/mp3;base64,{b64_audio}"></audio>
            <button id="playButton">▶️ 再生スタート</button>
            <script>
                let count = 1;
                const maxCount = {int(repeat_count)};
                const button = document.getElementById("playButton");
                const audio = document.getElementById("audioPlayer");

                button.addEventListener("click", () => {{
                    count = 1;
                    audio.play();
                }});

                audio.onended = () => {{
                    if (count < maxCount) {{
                        count++;
                        audio.play();
                    }}
                }};
            </script>
            """,
            unsafe_allow_html=True
        )

        # ダウンロードボタン
        st.download_button("🎧 音声をダウンロード", audio_data, file_name="translated.mp3")

        os.remove(filename)

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

