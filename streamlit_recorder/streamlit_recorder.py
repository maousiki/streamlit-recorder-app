import streamlit as st
import numpy as np
import soundfile as sf
import tempfile
import time

st.set_page_config(page_title="Voice Recorder App", layout="centered")

st.title("\ud83c\udfa4 \u9332\u97f3\u30a2\u30d7\u30ea (\u30b9\u30de\u30db\u5bfe\u5fdc\u30b7\u30f3\u30d7\u30eb\u7248)")

# 録音ボタンデザイン
st.markdown("""
<style>
button[kind="primary"] {
    background-color: red;
    color: white;
    height: 4em;
    width: 4em;
    border-radius: 50%;
    font-size: 2em;
}
</style>
""", unsafe_allow_html=True)

# 録音データエリア
st.write("\n\ud83d\udd0a \u9332\u97f3\u30dcタンを押して録音を開始！")

# 録音計測用タイマー
recording = False
start_time = None

# セッションステート保持
if 'recording' not in st.session_state:
    st.session_state.recording = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# 録音ボタン
if not st.session_state.recording:
    if st.button("\ud83c\udf99\ufe0f", key="start_record"):
        st.session_state.recording = True
        st.session_state.start_time = time.time()
else:
    if st.button("\u23f9\ufe0f", key="stop_record"):
        st.session_state.recording = False
        elapsed = time.time() - st.session_state.start_time

        st.success(f"\u9332\u97f3終了！\u9332音時間: {int(elapsed//60)}\u5206{int(elapsed%60)}\u79d2")

        uploaded_audio = st.file_uploader("\u9332\u97f3\u30c7\u30fc\u30bf\u3092\u30a2\u30c3\u30d7\u30ed\u30fc\u30c9\u3057\u3066\u304f\u3060\u3055\u3044", type=["wav", "mp3"])

        if uploaded_audio is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
                tmp_wav.write(uploaded_audio.read())
                audio_file_path = tmp_wav.name

            # 保存ボタン
            with open(audio_file_path, "rb") as f:
                st.download_button(
                    label="\ud83d\udce5 \u9332\u97f3\u30c7\u30fc\u30bfをダ\u30a6\u30f3\u30ed\u30fc\u30c9",
                    data=f,
                    file_name="recorded_audio.wav",
                    mime="audio/wav"
                )

        else:
            st.info("\u9332\u97f3デ\u30fc\u30bfがまだないよ！")

    # 録音中はタイマー表示
    if st.session_state.recording and st.session_state.start_time:
        elapsed = time.time() - st.session_state.start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        st.markdown(f"## \u9332\u97f3中: {minutes:02d}:{seconds:02d}")

# 破棄ボタン
if st.button("\u274c \u7834\u68c4", key="cancel"):
    st.session_state.recording = False
    st.session_state.start_time = None
    st.warning("\u9332\u97f3を\u7834\u68c4しま\u3057\u305f")
