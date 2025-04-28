import streamlit as st
import numpy as np
import soundfile as sf
import tempfile
import time
from st_audiorec import st_audiorec

st.set_page_config(page_title="\ud83c\udfa4\u9332\u97f3\u30a2\u30d7\u30ea", layout="centered")

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
st.write("\n\ud83d\udd0a \u9332\u97f3\u30dc\u30bf\u30f3を押して録音を開始！")

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

        wav_audio_data = st_audiorec()

        if isinstance(wav_audio_data, np.ndarray):
            # 録音データ保存
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
                sf.write(tmp_wav.name, wav_audio_data, samplerate=44100)
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
            st.info("\u9332\u97f3デ\u30fcタがまだないよ！")

    # 録音中はタイマー表示
    if st.session_state.recording and st.session_state.start_time:
        elapsed = time.time() - st.session_state.start_time
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        st.markdown(f"## \u9332\u97f3中: {minutes:02d}:{seconds:02d}")

# 破棄ボタン
if st.button("\u274c \u7834棄", key="cancel"):
    st.session_state.recording = False
    st.session_state.start_time = None
    st.warning("\u9332\u97f3を\u7834\u68c4しました")
