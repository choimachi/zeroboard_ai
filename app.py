import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="ZEROBOARD AI",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 ZEROBOARD AI")
st.caption("AI経営会議システム")
st.write("あなたがCEO。4人のAI役員が議論し、最後に議長AIが経営判断をまとめます。")
st.divider()

# OpenAI接続
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 結果を保存する場所
if "meeting_result" not in st.session_state:
    st.session_state.meeting_result = None

if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""

topic = st.text_area(
    "CEO、今日の議題を入力してください",
    placeholder="例：AIを使って月10万円の利益を作れる新規事業を考える",
    height=120
)

def ask_ai(role, topic):
    response = client.responses.create(
        model="gpt-5-mini",
        instructions=role,
        input=f"""
経営会議の議題：
{topic}

日本語で回答してください。
具体的で実行可能な意見を出してください。
結論だけでなく、その理由も簡潔に説明してください。
"""
    )

    return response.output_text


if st.button("🚀 AI経営会議を開始", type="primary"):

    if not topic.strip():
        st.warning("まず議題を入力してください。")

    else:
        try:
            with st.spinner("AI役員が会議中..."):

                strategy = ask_ai(
                    """
あなたはZEROBOARD AIの戦略担当役員です。
市場機会、競争優位、事業モデル、成長可能性の観点から
CEOの議題を分析してください。
""",
                    topic
                )

                marketing = ask_ai(
                    """
あなたはZEROBOARD AIのマーケティング担当役員です。
顧客、集客、販売方法、価格、ブランドの観点から
CEOの議題を分析してください。
""",
                    topic
                )

                finance = ask_ai(
                    """
あなたはZEROBOARD AIの財務担当役員です。
必要資金、売上、利益、コスト、採算性の観点から
CEOの議題を分析してください。
数字を使えるところは具体的に示してください。
""",
                    topic
                )

                risk = ask_ai(
                    """
あなたはZEROBOARD AIのリスク担当役員です。
失敗要因、法的リスク、競合、実行上の問題、
見落としやすい点を厳しく分析してください。
""",
                    topic
                )

                chairman_prompt = f"""
あなたはZEROBOARD AIの議長です。

CEOの議題：
{topic}

以下は4人のAI役員の意見です。

【戦略担当】
{strategy}

【マーケティング担当】
{marketing}

【財務担当】
{finance}

【リスク担当】
{risk}

これらを統合してCEO向けの最終経営判断を作ってください。

必ず以下の形式で回答してください。

## 🎯 経営判断
実行すべきか、修正すべきか、見送るべきかを説明

## 💡 理由
重要な理由を整理

## 💰 収益モデル
どうやって利益を作るか

## ⚠️ 最大のリスク
最も注意すべき問題

## 🚀 最初の一歩
CEOが今日からできる具体的な行動

## 📅 7日間アクションプラン
Day1〜Day7まで具体的に提示
"""

                final = client.responses.create(
                    model="gpt-5-mini",
                    input=chairman_prompt
                ).output_text

                # 結果を保存
                st.session_state.last_topic = topic

                st.session_state.meeting_result = {
                    "strategy": strategy,
                    "marketing": marketing,
                    "finance": finance,
                    "risk": risk,
                    "final": final
                }

        except Exception as e:
            st.error("AIとの通信でエラーが発生しました。")
            st.code(str(e))


# 保存された結果を表示
if st.session_state.meeting_result:

    result = st.session_state.meeting_result

    st.divider()
    st.header("🏢 AI経営会議")

    st.subheader("📋 議題")
    st.write(st.session_state.last_topic)

    with st.expander("🧠 戦略担当役員"):
        st.markdown(result["strategy"])

    with st.expander("📣 マーケティング担当役員"):
        st.markdown(result["marketing"])

    with st.expander("💰 財務担当役員"):
        st.markdown(result["finance"])

    with st.expander("⚠️ リスク担当役員"):
        st.markdown(result["risk"])

    st.divider()

    st.header("👑 議長AI 最終判断")
    st.markdown(result["final"])

    st.success("AI経営会議が完了しました。")
