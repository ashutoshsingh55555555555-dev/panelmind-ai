import streamlit as st

from utils.questions import (
    get_questions,
    get_adaptive_follow_up
)

from utils.analyzer import analyze_answer

from utils.feedback import generate_feedback
from utils.voice import transcribe_audio


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PanelMind AI",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --ink: #18212f;
        --muted: #667085;
        --line: #e6eaf0;
        --paper: #fbfcfe;
        --blue: #2563eb;
        --teal: #0f9f9a;
    }

    .stApp {
        background:
            radial-gradient(circle at 8% 0%, rgba(37, 99, 235, 0.09), transparent 28%),
            radial-gradient(circle at 92% 18%, rgba(15, 159, 154, 0.08), transparent 24%),
            var(--paper);
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
    }

    .stApp p,
    .stApp label,
    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: var(--ink);
    }

    [data-testid="stTextArea"] textarea,
    [data-testid="stTextInput"] input,
    [data-baseweb="textarea"] textarea,
    [data-baseweb="input"] input {
        background: #ffffff !important;
        color: #18212f !important;
        -webkit-text-fill-color: #18212f !important;
        caret-color: #2563eb !important;
        border: 1px solid #cfd8e6 !important;
        border-radius: 12px !important;
    }

    [data-testid="stTextArea"] textarea::placeholder,
    [data-testid="stTextInput"] input::placeholder {
        color: #667085 !important;
        opacity: 1 !important;
    }

    [data-testid="stAlert"] p,
    [data-testid="stAlert"] [data-testid="stMarkdownContainer"] {
        color: #18212f !important;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        color: #18212f !important;
    }

    [data-testid="stSidebar"] {
        background: #162033;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    [data-testid="stSidebar"] * {
        color: #eef4ff;
    }

    [data-testid="stSidebar"] [data-testid="stInfo"] {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
    }

    [data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #18212f !important;
    }

    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif;
        letter-spacing: 0;
        color: var(--ink);
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }

    .main-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(2.4rem, 5vw, 4.2rem);
        line-height: 1;
        font-weight: 700;
        text-align: center;
        color: var(--ink);
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        color: var(--muted);
        font-size: 1rem;
        margin-bottom: 2.5rem;
    }

    .eyebrow {
        color: var(--blue);
        font-size: 0.74rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
    }

    .hero-panel {
        padding: 2.4rem;
        border: 1px solid var(--line);
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.82);
        box-shadow: 0 18px 50px rgba(24, 33, 47, 0.08);
        margin: 1rem 0 1.5rem;
    }

    .hero-panel h2 {
        font-size: clamp(1.7rem, 3vw, 2.6rem);
        margin: 0 0 0.6rem;
    }

    .hero-panel p {
        color: var(--muted);
        font-size: 1.05rem;
        line-height: 1.7;
        max-width: 720px;
        margin: 0;
    }

    .session-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        padding: 0.85rem 1rem;
        border: 1px solid var(--line);
        border-radius: 12px;
        background: #ffffff;
        color: var(--muted);
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }

    .session-bar strong {
        color: var(--ink);
    }

    .live-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--teal);
        margin-right: 0.4rem;
        box-shadow: 0 0 0 4px rgba(15, 159, 154, 0.12);
    }

    .question-card {
        padding: 2rem 2.2rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #eef5ff, #f5fbfb);
        border: 1px solid #dce7f5;
        border-left: 5px solid var(--blue);
        margin: 1rem 0 1.5rem;
        box-shadow: 0 12px 30px rgba(37, 99, 235, 0.07);
    }

    .question-card h2, .question-card h3 {
        margin: 0;
        line-height: 1.35;
    }

    .question-label {
        color: var(--blue);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 0.7rem;
    }

    .score {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 4.5rem;
        font-weight: bold;
        text-align: center;
        color: var(--blue);
        padding: 1rem;
    }

    div.stButton > button {
        background: #ffffff !important;
        color: #18212f !important;
        -webkit-text-fill-color: #18212f !important;
        border-radius: 10px;
        border: 1px solid #d7deea;
        font-weight: 700;
        min-height: 2.8rem;
        transition: transform 120ms ease, box-shadow 120ms ease;
    }

    div.stButton > button[kind="primary"],
    div.stButton > button[data-testid="baseButton-primary"] {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    div.stButton > button[kind="primary"],
    div.stButton > button[data-testid="baseButton-primary"] {
        background: #2563eb !important;
        border-color: #2563eb !important;
    }

    div.stButton > button[kind="primary"] p,
    div.stButton > button[data-testid="baseButton-primary"] p {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 18px rgba(24, 33, 47, 0.12);
    }

    div.stButton > button[kind="primary"] {
        background: var(--blue);
        border-color: var(--blue);
        color: white;
    }

    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 1rem;
    }

    [data-testid="stProgressBar"] > div > div {
        background: linear-gradient(90deg, var(--blue), var(--teal));
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🤖 PanelMind AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI Interview Panel Simulator with Adaptive Follow-Up Questions'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "started" not in st.session_state:
    st.session_state.started = False

if "finished" not in st.session_state:
    st.session_state.finished = False

if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "current_question_text" not in st.session_state:
    st.session_state.current_question_text = ""

if "is_follow_up" not in st.session_state:
    st.session_state.is_follow_up = False

if "answers" not in st.session_state:
    st.session_state.answers = []

if "interview_type" not in st.session_state:
    st.session_state.interview_type = "Technical Interview"

if "answered_count" not in st.session_state:
    st.session_state.answered_count = 0


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ Interview Settings")

interview_type = st.sidebar.selectbox(
    "Interview Type",
    [
        "Technical Interview",
        "HR Interview",
        "General Interview"
    ]
)

num_questions = st.sidebar.slider(
    "Number of Base Questions",
    3,
    5,
    3
)

voice_mode = False

if hasattr(st, "audio_input"):
    voice_mode = st.sidebar.toggle(
        "Enable voice mode",
        value=False,
        help="Record your answer and PanelMind AI will transcribe it before analysis."
    )
else:
    st.sidebar.caption("Voice mode requires a newer Streamlit version.")

st.sidebar.markdown("---")

st.sidebar.info(
    """
    💡 **How PanelMind AI works**

    1. Ask a base question
    2. Analyze your answer
    3. Detect answer strength
    4. Generate adaptive follow-up
    5. Give personalized feedback
    """
)


# ============================================================
# START SCREEN
# ============================================================

if not st.session_state.started:

    st.markdown(
        '<div class="hero-panel">'
        '<div class="eyebrow">Adaptive interview practice</div>'
        '<h2>Walk into your next interview prepared.</h2>'
        '<p>Practice realistic answers, get instant coaching, and let the panel adapt its next question to your response.</p>'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Interview Mode",
            interview_type
        )

    with col2:
        st.metric(
            "Questions",
            num_questions
        )

    with col3:
        st.metric(
            "AI Feature",
            "Adaptive"
        )

    st.markdown(
        '<div class="session-bar"><span><span class="live-dot"></span>Ready when you are</span>'
        '<span>Instant feedback · Adaptive follow-ups</span></div>',
        unsafe_allow_html=True
    )

    if st.button(
        "🚀 Start Interview",
        use_container_width=True,
        type="primary"
    ):

        st.session_state.questions = get_questions(
            interview_type,
            num_questions
        )

        st.session_state.current_question = 0

        st.session_state.current_question_text = (
            st.session_state.questions[0]
        )

        st.session_state.is_follow_up = False

        st.session_state.answers = []
        st.session_state.answered_count = 0

        st.session_state.interview_type = interview_type

        st.session_state.started = True
        st.session_state.finished = False

        st.rerun()


# ============================================================
# INTERVIEW SCREEN
# ============================================================

elif (
    st.session_state.started
    and not st.session_state.finished
):

    total_questions = len(
        st.session_state.questions
    )

    current = st.session_state.current_question

    # --------------------------------------------------------
    # Progress
    # --------------------------------------------------------

    answered = st.session_state.answered_count

    st.markdown(
        f'<div class="session-bar"><span><span class="live-dot"></span><strong>Live interview</strong> · {st.session_state.interview_type}</span>'
        f'<span>Answered <strong>{answered}</strong> of {total_questions}</span></div>',
        unsafe_allow_html=True
    )

    st.progress(
        answered / total_questions,
        text=f"Interview progress · {answered}/{total_questions} answers reviewed"
    )

    if st.session_state.is_follow_up:

        st.info("🧠 ADAPTIVE FOLLOW-UP QUESTION")

    else:

        st.info("🎯 BASE INTERVIEW QUESTION")

    # --------------------------------------------------------
    # Question
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="question-card">
        <div class="question-label">{'Adaptive follow-up' if st.session_state.is_follow_up else 'Base question'}</div>
        <h2>
        {st.session_state.current_question_text}
        </h2>

        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Answer
    # --------------------------------------------------------

    recorded_audio = None

    if voice_mode:
        st.markdown("### 🎙️ Voice Practice")
        st.caption(
            "Record your answer to simulate real interview pressure. "
            "You can still edit or replace the transcript below."
        )
        recorded_audio = st.audio_input(
            "Record your answer",
            sample_rate=16000,
            key=f"voice_{current}_{st.session_state.is_follow_up}"
        )

        if recorded_audio:
            st.audio(recorded_audio)

    answer = st.text_area(
        "✍️ Your Answer",
        height=180,
        placeholder=(
            "Type your answer here...\n\n"
            "Tip: Explain what you did, why you did it, "
            "and what result you achieved."
        ),
        key=f"answer_{current}_{st.session_state.is_follow_up}"
    )

    # --------------------------------------------------------
    # Submit
    # --------------------------------------------------------

    if st.button(
        "🧠 Analyze My Answer",
        use_container_width=True,
        type="primary"
    ):

        if not answer.strip():

            if recorded_audio:
                with st.spinner("Transcribing your answer..."):
                    try:
                        answer = transcribe_audio(
                            recorded_audio.getvalue()
                        )
                    except RuntimeError as error:
                        st.error(str(error))
                        answer = ""

            if answer.strip():
                st.info("Voice answer transcribed successfully. Analyzing it now...")

            else:
                st.warning("Please type an answer or record one first.")

        if answer.strip():

            with st.spinner(
                "PanelMind AI is analyzing your answer..."
            ):

                # --------------------------------------------
                # Analyze
                # --------------------------------------------

                analysis = analyze_answer(
                    st.session_state.current_question_text,
                    answer
                )

                # --------------------------------------------
                # Feedback
                # --------------------------------------------

                feedback = generate_feedback(
                    st.session_state.current_question_text,
                    answer,
                    analysis
                )

                # --------------------------------------------
                # Adaptive follow-up
                # --------------------------------------------

                adaptive = get_adaptive_follow_up(
                    answer,
                    st.session_state.current_question_text
                )

                # --------------------------------------------
                # Save answer
                # --------------------------------------------

                st.session_state.answers.append(
                    {
                        "question":
                            st.session_state.current_question_text,

                        "answer":
                            answer,

                        "score":
                            analysis["score"],

                        "strength":
                            analysis["strength"],

                        "analysis":
                            analysis,

                        "feedback":
                            feedback,

                        "follow_up":
                            adaptive["follow_up"],

                        "voice_used":
                            recorded_audio is not None
                    }
                )

                st.session_state.answered_count += 1

            # =================================================
            # SHOW SCORE
            # =================================================

            st.markdown("## 📊 Answer Analysis")

            st.markdown(
                f'<div class="session-bar"><span>Feedback for your latest response</span><span><strong>{len(answer.split())}</strong> words · <strong>{analysis["strength"].title()}</strong> signal</span></div>',
                unsafe_allow_html=True
            )

            score = analysis["score"]

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Score",
                    f"{score}/100"
                )

            with col2:

                st.metric(
                    "Answer Strength",
                    analysis["strength"].upper()
                )

            with col3:

                st.metric(
                    "Words",
                    len(answer.split())
                )

            # =================================================
            # ANALYSIS
            # =================================================

            st.markdown("### 🧠 AI Analysis")

            st.write(
                analysis["analysis"]
            )

            # =================================================
            # STRENGTHS & WEAKNESSES
            # =================================================

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("### 💪 Strengths")

                for item in analysis["strengths"]:

                    st.success(
                        f"✓ {item}"
                    )

            with col2:

                st.markdown("### ⚠️ Areas to Improve")

                for item in analysis["weaknesses"]:

                    st.warning(
                        f"• {item}"
                    )

            # =================================================
            # FEEDBACK
            # =================================================

            st.markdown("### 💡 Personalized Feedback")

            st.info(
                feedback["overall"]
            )

            st.write(
                feedback["improvement"]
            )

            # =================================================
            # ADAPTIVE FOLLOW-UP
            # =================================================

            st.markdown("---")

            st.markdown(
                "## 🧠 PanelMind AI Follow-Up"
            )

            if analysis["strength"] == "strong":

                st.success(
                    "🔥 Strong answer detected! "
                    "Increasing interview difficulty."
                )

            elif analysis["strength"] == "weak":

                st.warning(
                    "💡 Your answer needs clarification. "
                    "The panel will ask a simpler follow-up."
                )

            else:

                st.info(
                    "🎯 Your answer is reasonable. "
                    "The panel will explore it deeper."
                )

            st.markdown(
                f"""
                <div class="question-card">

                <h3>
                {adaptive["follow_up"]}
                </h3>

                </div>
                """,
                unsafe_allow_html=True
            )

            # =================================================
            # FOLLOW-UP BUTTON
            # =================================================

            if st.session_state.is_follow_up:

                # Follow-up completed
                if current + 1 < total_questions:

                    if st.button(
                        "➡️ Next Base Question",
                        use_container_width=True
                    ):

                        st.session_state.current_question += 1

                        st.session_state.current_question_text = (
                            st.session_state.questions[
                                st.session_state.current_question
                            ]
                        )

                        st.session_state.is_follow_up = False

                        st.rerun()

                else:

                    if st.button(
                        "🏆 Finish Interview",
                        use_container_width=True
                    ):

                        st.session_state.finished = True

                        st.rerun()

            else:

                # Move from base question to follow-up
                if st.button(
                    "🧠 Answer Adaptive Follow-Up",
                    use_container_width=True
                ):

                    st.session_state.current_question_text = (
                        adaptive["follow_up"]
                    )

                    st.session_state.is_follow_up = True

                    st.rerun()


# ============================================================
# FINAL REPORT
# ============================================================

else:

    st.markdown(
        "# 🏆 Final Interview Report"
    )

    answers = st.session_state.answers

    if not answers:

        st.warning(
            "No answers were recorded."
        )

    else:

        # ----------------------------------------------------
        # Overall Score
        # ----------------------------------------------------

        total_score = sum(
            item["score"]
            for item in answers
        )

        average_score = round(
            total_score / len(answers)
        )

        st.markdown(
            f"""
            <div class="score">
            {average_score}/100
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(
            average_score / 100
        )

        # ----------------------------------------------------
        # Performance
        # ----------------------------------------------------

        if average_score >= 80:

            st.success(
                "🌟 Excellent interview performance!"
            )

        elif average_score >= 60:

            st.info(
                "👍 Good performance with some areas to improve."
            )

        else:

            st.warning(
                "💪 Keep practicing. Your answers need more depth."
            )

        st.markdown("---")

        # ----------------------------------------------------
        # Summary
        # ----------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Questions Answered",
                len(answers)
            )

        with col2:

            strong_count = sum(
                1
                for item in answers
                if item["strength"] == "strong"
            )

            st.metric(
                "Strong Answers",
                strong_count
            )

        with col3:

            weak_count = sum(
                1
                for item in answers
                if item["strength"] == "weak"
            )

            st.metric(
                "Weak Answers",
                weak_count
            )

        # ----------------------------------------------------
        # Detailed Report
        # ----------------------------------------------------

        st.markdown(
            "## 📋 Question-by-Question Report"
        )

        for i, item in enumerate(
            answers,
            start=1
        ):

            with st.expander(
                f"Question {i} — "
                f"Score: {item['score']}/100"
            ):

                st.markdown(
                    f"**Question:** {item['question']}"
                )

                st.markdown(
                    f"**Your Answer:** {item['answer']}"
                )

                st.markdown(
                    f"**Strength:** "
                    f"{item['strength'].upper()}"
                )

                st.markdown(
                    "### 🧠 Analysis"
                )

                st.write(
                    item["analysis"]["analysis"]
                )

                st.markdown(
                    "### 💪 Strengths"
                )

                for strength in item["analysis"]["strengths"]:

                    st.write(
                        f"✓ {strength}"
                    )

                st.markdown(
                    "### ⚠️ Weaknesses"
                )

                for weakness in item["analysis"]["weaknesses"]:

                    st.write(
                        f"• {weakness}"
                    )

                st.markdown(
                    "### 💡 Improvement"
                )

                st.write(
                    item["feedback"]["improvement"]
                )

        # ----------------------------------------------------
        # Restart
        # ----------------------------------------------------

        st.markdown("---")

        if st.button(
            "🔄 Start New Interview",
            use_container_width=True
        ):

            st.session_state.clear()

            st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🤖 PanelMind AI | Adaptive AI Interview Panel Simulator"
)
