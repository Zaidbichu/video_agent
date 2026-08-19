import os
import tempfile

import streamlit as st
from dotenv import load_dotenv

from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import summarize, generate_title
from core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions,
)
from core.rag_engine import build_rag_chain, ask_question


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(99, 102, 241, 0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(168, 85, 247, 0.08),
                transparent 30%
            ),
            #09090b;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        background: #0c0c0f;
        border-right: 1px solid rgba(255,255,255,0.07);
    }

    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        min-height: 42px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
    }

    /* ======================================================
       INPUTS
       ====================================================== */

    .stTextInput > div > div {
        border-radius: 12px;
    }

    .stSelectbox > div > div {
        border-radius: 12px;
    }

    /* ======================================================
       CHAT
       ====================================================== */

    [data-testid="stChatMessage"] {
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.06);
    }

    /* ======================================================
       TABS
       ====================================================== */

    button[data-baseweb="tab"] {
        font-weight: 600;
    }

    /* ======================================================
       DIVIDER
       ====================================================== */

    hr {
        border-color: rgba(255,255,255,0.07);
    }

    /* ======================================================
       FILE UPLOADER
       ====================================================== */

    [data-testid="stFileUploader"] {
        border-radius: 14px;
    }

    /* ======================================================
       METRIC
       ====================================================== */

    [data-testid="stMetric"] {
        background: rgba(24,24,27,0.6);
        padding: 1rem;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.07);
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "processing" not in st.session_state:
    st.session_state.processing = False


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def reset_session():
    """Reset the current analysis session."""

    st.session_state.result = None
    st.session_state.chat_history = []
    st.session_state.processing = False


def count_words(text):
    """Return word count."""

    if not text:
        return 0

    return len(text.split())


def run_pipeline(
    source,
    language,
    progress_bar,
    status_box,
):
    """
    Execute the complete AI video pipeline.
    """

    try:

        # ====================================================
        # STEP 1
        # ====================================================

        status_box.info(
            "🎧 Preparing your video/audio..."
        )

        progress_bar.progress(10)

        chunks = process_input(source)

        progress_bar.progress(25)

        status_box.success(
            "✓ Audio preparation completed"
        )

        # ====================================================
        # STEP 2
        # ====================================================

        status_box.info(
            "🎙️ Transcribing your content..."
        )

        transcript = transcribe_all(
            chunks,
            language,
        )

        progress_bar.progress(50)

        status_box.success(
            "✓ Transcription completed"
        )

        # ====================================================
        # STEP 3
        # ====================================================

        status_box.info(
            "🧠 Generating AI insights..."
        )

        title = generate_title(
            transcript
        )

        progress_bar.progress(58)

        # ====================================================
        # STEP 4
        # ====================================================

        summary = summarize(
            transcript
        )

        progress_bar.progress(68)

        # ====================================================
        # STEP 5
        # ====================================================

        action_items = extract_action_items(
            transcript
        )

        progress_bar.progress(76)

        # ====================================================
        # STEP 6
        # ====================================================

        decisions = extract_key_decisions(
            transcript
        )

        progress_bar.progress(84)

        # ====================================================
        # STEP 7
        # ====================================================

        questions = extract_questions(
            transcript
        )

        progress_bar.progress(90)

        # ====================================================
        # STEP 8
        # ====================================================

        status_box.info(
            "💬 Building your AI knowledge base..."
        )

        rag_chain = build_rag_chain(
            transcript
        )

        progress_bar.progress(100)

        status_box.success(
            "🎉 Analysis completed successfully!"
        )

        return {
            "title": title,
            "transcript": transcript,
            "summary": summary,
            "action_items": action_items,
            "key_decisions": decisions,
            "open_questions": questions,
            "rag_chain": rag_chain,
        }

    except Exception as error:

        progress_bar.empty()

        status_box.error(
            "❌ Something went wrong while processing "
            "your content."
        )

        with st.expander(
            "View technical error"
        ):
            st.exception(error)

        return None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🎬 AI Video Assistant")

    st.caption(
        "Transform long videos into structured "
        "knowledge and actionable insights."
    )

    st.divider()

    # --------------------------------------------------------
    # LANGUAGE
    # --------------------------------------------------------

    st.subheader("⚙️ Configuration")

    language = st.selectbox(
        "Transcription language",
        options=[
            "english",
            "hindenglish",
        ],
        index=0,
        help=(
            "Select the language used in your "
            "video or audio."
        ),
    )

    st.divider()

    # --------------------------------------------------------
    # SOURCE
    # --------------------------------------------------------

    st.subheader("📥 Input Source")

    input_mode = st.radio(
        "Choose your source",
        options=[
            "YouTube URL",
            "Local File",
        ],
    )

    st.divider()

    # --------------------------------------------------------
    # SESSION
    # --------------------------------------------------------

    if st.session_state.result:

        st.subheader("📊 Current Session")

        transcript = st.session_state.result.get(
            "transcript",
            "",
        )

        st.metric(
            "Transcript Words",
            f"{count_words(transcript):,}",
        )

        if st.button(
            "🗑️ Start New Analysis",
            use_container_width=True,
        ):

            reset_session()

            st.rerun()

    st.divider()

    st.caption(
        "AI Video Assistant"
    )

    st.caption(
        "Powered by your existing AI pipeline"
    )


# ============================================================
# HERO SECTION
# ============================================================

st.title(
    "🎬 AI Video Assistant"
)

st.markdown(
    """
    ### Turn long videos into actionable intelligence.

    Upload a video or audio file, or paste a YouTube URL.
    Your AI assistant will **transcribe**, **summarize**,
    **extract action items**, identify **key decisions**,
    and let you **chat with the content**.
    """
)

st.divider()


# ============================================================
# INPUT SECTION
# ============================================================

st.subheader("🚀 Start a New Analysis")

input_source = None


# ============================================================
# YOUTUBE
# ============================================================

if input_mode == "YouTube URL":

    youtube_url = st.text_input(
        "YouTube URL",
        placeholder=(
            "https://www.youtube.com/watch?v=..."
        ),
        help=(
            "Paste a public YouTube video URL."
        ),
    )

    if youtube_url.strip():

        input_source = youtube_url.strip()


# ============================================================
# LOCAL FILE
# ============================================================

else:

    uploaded_file = st.file_uploader(
        "Upload your video or audio",
        type=[
            "mp4",
            "mkv",
            "mov",
            "avi",
            "webm",
            "mp3",
            "wav",
            "m4a",
            "flac",
        ],
        help=(
            "Supported video/audio formats."
        ),
    )

    if uploaded_file:

        suffix = os.path.splitext(
            uploaded_file.name
        )[1]

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        )

        temp_file.write(
            uploaded_file.getbuffer()
        )

        temp_file.close()

        input_source = temp_file.name

        st.success(
            f"✓ {uploaded_file.name} ready for analysis"
        )


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.write("")

button_col1, button_col2, button_col3 = st.columns(
    [1, 1.4, 1]
)

with button_col2:

    analyze_button = st.button(
        "✨ Analyze with AI",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# RUN PIPELINE
# ============================================================

if analyze_button:

    if not input_source:

        st.warning(
            "⚠️ Please provide a YouTube URL or "
            "upload a file first."
        )

    else:

        st.session_state.processing = True

        progress_bar = st.progress(
            0
        )

        status_box = st.empty()

        result = run_pipeline(
            source=input_source,
            language=language,
            progress_bar=progress_bar,
            status_box=status_box,
        )

        if result:

            st.session_state.result = result

            st.session_state.chat_history = []

            st.session_state.processing = False

            st.rerun()


# ============================================================
# RESULTS
# ============================================================

result = st.session_state.result


if result:

    st.divider()

    # ========================================================
    # GENERATED TITLE
    # ========================================================

    st.subheader(
        "📌 " + str(
            result.get(
                "title",
                "Untitled Video",
            )
        )
    )

    st.caption(
        "AI-generated title based on the video content"
    )

    # ========================================================
    # METRICS
    # ========================================================

    transcript = result.get(
        "transcript",
        "",
    )

    summary = result.get(
        "summary",
        "",
    )

    word_count = count_words(
        transcript
    )

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:

        st.metric(
            "📝 Words",
            f"{word_count:,}",
        )

    with metric2:

        st.metric(
            "🧠 Summary",
            "Ready",
        )

    with metric3:

        st.metric(
            "⚡ Actions",
            "Extracted",
        )

    with metric4:

        st.metric(
            "💬 AI Chat",
            "Ready",
        )

    st.divider()

    # ========================================================
    # RESULTS TABS
    # ========================================================

    overview_tab, actions_tab, decisions_tab, questions_tab, transcript_tab, chat_tab = st.tabs(
        [
            "📋 Overview",
            "⚡ Action Items",
            "🔑 Decisions",
            "❓ Questions",
            "📜 Transcript",
            "💬 Ask AI",
        ]
    )

    # ========================================================
    # OVERVIEW
    # ========================================================

    with overview_tab:

        st.subheader(
            "📝 Executive Summary"
        )

        st.markdown(
            summary
        )

        st.divider()

        st.subheader(
            "💡 About This Analysis"
        )

        st.info(
            "The AI assistant analyzed the complete "
            "transcript and extracted the most important "
            "information from the content."
        )

        st.divider()

        st.subheader(
            "📊 Analysis Overview"
        )

        info1, info2, info3 = st.columns(3)

        with info1:

            st.write(
                "**🎙️ Transcription**"
            )

            st.success(
                "Completed"
            )

        with info2:

            st.write(
                "**🧠 AI Analysis**"
            )

            st.success(
                "Completed"
            )

        with info3:

            st.write(
                "**💬 RAG Assistant**"
            )

            st.success(
                "Ready"
            )

    # ========================================================
    # ACTION ITEMS
    # ========================================================

    with actions_tab:

        st.subheader(
            "⚡ Action Items"
        )

        st.caption(
            "Tasks and follow-up actions identified by AI."
        )

        action_items = result.get(
            "action_items",
            "",
        )

        if action_items:

            st.markdown(
                action_items
            )

        else:

            st.info(
                "No action items were identified."
            )

    # ========================================================
    # DECISIONS
    # ========================================================

    with decisions_tab:

        st.subheader(
            "🔑 Key Decisions"
        )

        st.caption(
            "Important decisions identified from the content."
        )

        decisions = result.get(
            "key_decisions",
            "",
        )

        if decisions:

            st.markdown(
                decisions
            )

        else:

            st.info(
                "No key decisions were identified."
            )

    # ========================================================
    # QUESTIONS
    # ========================================================

    with questions_tab:

        st.subheader(
            "❓ Open Questions"
        )

        st.caption(
            "Questions that remain unanswered or require follow-up."
        )

        questions = result.get(
            "open_questions",
            "",
        )

        if questions:

            st.markdown(
                questions
            )

        else:

            st.info(
                "No open questions were identified."
            )

    # ========================================================
    # TRANSCRIPT
    # ========================================================

    with transcript_tab:

        st.subheader(
            "📜 Full Transcript"
        )

        st.caption(
            f"{word_count:,} words"
        )

        st.text_area(
            "Transcript",
            value=transcript,
            height=600,
            label_visibility="collapsed",
        )

        st.divider()

        download_col1, download_col2 = st.columns(2)

        with download_col1:

            st.download_button(
                label="⬇️ Download Transcript",
                data=transcript,
                file_name="transcript.txt",
                mime="text/plain",
                use_container_width=True,
            )

        with download_col2:

            st.download_button(
                label="⬇️ Download Summary",
                data=summary,
                file_name="summary.txt",
                mime="text/plain",
                use_container_width=True,
            )

    # ========================================================
    # AI CHAT
    # ========================================================

    with chat_tab:

        st.subheader(
            "💬 Chat with your Video"
        )

        st.caption(
            "Ask questions about the content. "
            "The AI uses your transcript as its knowledge base."
        )

        st.divider()

        # ----------------------------------------------------
        # Suggested Questions
        # ----------------------------------------------------

        if not st.session_state.chat_history:

            st.write(
                "**Try asking:**"
            )

            suggestion1, suggestion2, suggestion3 = st.columns(3)

            with suggestion1:

                st.info(
                    "💡 What are the main points?"
                )

            with suggestion2:

                st.info(
                    "⚡ What action items were discussed?"
                )

            with suggestion3:

                st.info(
                    "🔑 What decisions were made?"
                )

        # ----------------------------------------------------
        # CHAT HISTORY
        # ----------------------------------------------------

        for message in st.session_state.chat_history:

            with st.chat_message(
                message["role"]
            ):

                st.markdown(
                    message["content"]
                )

        # ----------------------------------------------------
        # CHAT INPUT
        # ----------------------------------------------------

        question = st.chat_input(
            "Ask anything about this video..."
        )

        if question:

            # USER MESSAGE
            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": question,
                }
            )

            with st.chat_message(
                "user"
            ):

                st.markdown(
                    question
                )

            # AI MESSAGE
            with st.chat_message(
                "assistant"
            ):

                with st.spinner(
                    "🧠 Thinking..."
                ):

                    try:

                        answer = ask_question(
                            result["rag_chain"],
                            question,
                        )

                    except Exception as error:

                        answer = (
                            "I couldn't process that "
                            "question.\n\n"
                            f"Error: `{error}`"
                        )

                st.markdown(
                    answer
                )

            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )


# ============================================================
# EMPTY STATE
# ============================================================

else:

    st.write("")

    empty_col1, empty_col2, empty_col3 = st.columns(
        [1, 2, 1]
    )

    with empty_col2:

        st.markdown(
            "<h1 style='text-align:center;'>🎬</h1>",
            unsafe_allow_html=True,
        )

        st.subheader(
            "Your AI workspace is ready"
        )

        st.write(
            """
            Add a YouTube video or upload a local media file
            above to generate a transcript, summary,
            action items, key decisions and an interactive
            AI chat.
            """
        )

        st.write("")

        feature1, feature2, feature3 = st.columns(3)

        with feature1:

            st.info(
                """
                ### 🎙️ Transcribe

                Convert speech into searchable text.
                """
            )

        with feature2:

            st.info(
                """
                ### 🧠 Understand

                Generate summaries and insights.
                """
            )

        with feature3:

            st.info(
                """
                ### 💬 Ask AI

                Chat with your video using RAG.
                """
            )

        st.write("")

        st.caption(
            "Start by entering a YouTube URL or uploading a file above."
        )