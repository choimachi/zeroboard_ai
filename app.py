import streamlit as st

st.set_page_config(
    page_title="ZEROBOARD AI",
    page_icon="🧠"
)

st.title("🧠 ZEROBOARD AI")
st.write("AI経営会議システム")

st.divider()

topic = st.text_input(
    "CEO、今日の議題を入力してください",
    placeholder="例：AIを使って月10万円稼げる新規事業を考える"
)

if st.button("🚀 AI経営会議を開始"):
    if topic:
        st.subheader("📋 本日の議題")
        st.write(topic)

        st.subheader("🤖 AI役員")
        st.write("🚀 NOVA — 新規事業")
        st.write("📣 PULSE — マーケティング")
        st.write("🧠 CORE — 技術・AI開発")
        st.write("💰 LEDGER — 財務")
        st.write("😈 VETO — 批判・リスク")

        st.success("AI役員会を開始しました。")
    else:
        st.warning("まず議題を入力してください。")
