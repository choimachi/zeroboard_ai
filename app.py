import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="ZEROBOARD AI",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 ZEROBOARD AI")
st.caption("AI経営会議システム")
st.write("あなたがCEO。AI役員が議論し、最終判断はあなたが行います。")
st.divider()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

topic = st.text_area(
    "CEO、今日の議題を入力してください",
    placeholder="例：AIを使って月10万円を目指せる新規事業を考える",
    height=120
)

members = {
    "💡 新規事業担当": """
あなたは新規事業責任者です。
固定観念にとらわれず、収益化できる具体的なアイデアを考えてください。
初期費用、収益モデル、最初の行動まで具体化してください。
""",

    "📣 マーケティング担当": """
あなたはマーケティング責任者です。
誰に、何を、どう売るかを考えてください。
集客方法、販売方法、差別化、最初の顧客獲得方法を具体化してください。
""",

    "💰 財務担当": """
あなたは財務責任者です。
利益、コスト、必要資金、収益化までの期間を重視してください。
数字を可能な範囲で具体的に示してください。
""",

    "🛠 実行・技術担当": """
あなたは実行責任者兼技術責任者です。
実際に実現できるかを検討してください。
必要なツール、作業、技術、最初の7日間の行動を具体化してください。
""",

    "⚠️ リスク担当": """
あなたは厳しいリスク管理責任者です。
他の役員が見落としそうな問題を探してください。
失敗要因、法的・金銭的・競争上のリスクと、その対策を提示してください。
"""
}


def ask_ai(role, topic):
    response = client.responses.create(
        model="gpt-6-luna",
        instructions=role,
        input=f"""
CEOからの議題：
{topic}

日本語で回答してください。
抽象論ではなく、CEOが実際に判断できる具体性を重視してください。
""",
    )
    return response.output_text


if st.button("🚀 AI経営会議を開始", type="primary"):

    if not topic.strip():
        st.warning("まず議題を入力してください。")
        st.stop()

    opinions = {}

    try:
        with st.spinner("AI役員5名が分析中..."):
            for name, role in members.items():
                opinions[name] = ask_ai(role, topic)

        st.success("役員の一次分析が完了しました。")

        st.header("🏢 AI役員会")

        for name, opinion in opinions.items():
            with st.expander(name, expanded=True):
                st.write(opinion)

        meeting_text = "\n\n".join(
            f"【{name}】\n{opinion}"
            for name, opinion in opinions.items()
        )

        with st.spinner("役員の意見を比較し、議長AIが最終提案を作成中..."):

            final_response = client.responses.create(
                model="gpt-6-luna",
                instructions="""
あなたはZEROBOARD AIの議長です。

複数のAI役員の意見を鵜呑みにせず、
一致点・対立点・弱点を比較してください。

CEOの代わりに最終決定してはいけません。
CEOが自分で判断できる材料を作ってください。

以下の順番で日本語でまとめてください。

1. 最も有望な具体案
2. 各役員の一致点
3. 意見が割れたポイント
4. 想定収益モデル
5. 主なリスク
6. 最初の7日間の行動計画
7. CEOが最終判断する前に確認すべきこと
""",
                input=f"""
CEOの議題：
{topic}

各AI役員の一次分析：
{meeting_text}
"""
            )

        st.divider()
        st.header("📋 議長AI 最終提案")
        st.write(final_response.output_text)

        st.divider()
        st.header("👑 CEO最終判断")
        st.info("AIは提案まで。最終決定はCEOであるあなたが行います。")

        decision = st.radio(
            "この案件をどうしますか？",
            ["未決定", "✅ 採用", "⏸️ 保留", "❌ 却下"]
        )

        if decision != "未決定":
            st.success(f"CEO判断：{decision}")

    except Exception as e:
        st.error("AIとの接続でエラーが発生しました。")
        st.code(str(e))
