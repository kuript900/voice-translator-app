st.markdown(
    f"""
    <audio id="audioPlayer" src="data:audio/mp3;base64,{b64_audio}" preload="auto"></audio>
    <button id="playButton">▶️ 再生スタート</button>
    <script>
        const audio = document.getElementById("audioPlayer");
        const button = document.getElementById("playButton");

        let maxCount = {int(repeat_count)};
        let count = 0;

        button.addEventListener("click", async () => {{
            count = 1;
            try {{
                await audio.play();
            }} catch (e) {{
                console.log("初回再生に失敗", e);
            }}
        }});

        audio.addEventListener("ended", async () => {{
            if (count < maxCount) {{
                count++;
                try {{
                    await audio.play();
                }} catch (e) {{
                    console.log("リピート再生に失敗", e);
                }}
            }}
        }});
    </script>
    """,
    unsafe_allow_html=True
)


