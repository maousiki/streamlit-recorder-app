import streamlit as st
import numpy as np
import time
import tempfile
from st_audiorec import st_audiorec

st.set_page_config(page_title="Voice Recorder App", layout="centered")

st.title("🎤 録音アプリ (スマホ対応ブラウザ録音版)")

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

st.write("\n🔊 録音ボタンを押して録音を開始！")

# 録音機能呼び出し
wav_audio_data = st_audiorec()

# 録音が終了してデータがある場合
if wav_audio_data is not None:
    st.success("録音完了！保存してダウンロードできます")

    # 一時ファイルに保存
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        tmp_wav.write(wav_audio_data)
        tmp_path = tmp_wav.name

    with open(tmp_path, "rb") as f:
        st.download_button(
            label="📥 録音データをダウンロード",
            data=f,
            file_name="recorded_audio.wav",
            mime="audio/wav"
        )

# 破棄ボタン
if st.button("❌ 破棄"):
    st.warning("録音データを破棄しました (ページを更新してください)")
