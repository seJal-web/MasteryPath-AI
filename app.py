import streamlit as st
import pandas as pd
import re
import html
import random


# ============================================================
# IMPORT PROJECT FILES
# ============================================================

from src.pdf_processor import (
    extract_text_from_pdf,
    clean_text,
    divide_into_three_parts
)

from src.nlp_processor import find_topics

from src.quiz_generator import generate_ai_questions

from src.ai_tutor import (
    generate_lesson,
    generate_weak_topic_review
)

from src.mastery_model import predict_mastery


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MasteryPath AI",
    page_icon="",
    layout="wide"
)


# ============================================================
# MASTERYPATH AI THEME
# From Confusion to Mastery
# ============================================================

st.markdown(
    """
    <style>

    /* ================================
       MAIN APPLICATION
       ================================ */

    .stApp {
        background-color: #FFFDF8 !important;
        color: #171A1A !important;
    }


    .main {
        background-color: #FFFDF8 !important;
    }


    .journey-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 18px;
        padding: 12px 16px;
        margin: 8px 0 24px 0;
        background: #FFFFFF;
        border: 1px solid #E7DED3;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(81, 68, 95, 0.07);
    }

    .journey-module {
        font-weight: 800;
        color: #51445F !important;
        white-space: nowrap;
    }

    .journey-steps {
        display: flex;
        align-items: center;
        gap: 8px;
        flex: 1;
        justify-content: flex-end;
    }

    .journey-item {
        display: flex;
        align-items: center;
        gap: 7px;
        padding: 7px 11px;
        border-radius: 999px;
        font-size: 13px;
        font-weight: 700;
        white-space: nowrap;
    }

    .journey-icon {
        width: 22px;
        height: 22px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        font-size: 11px;
    }

    .journey-done {
        background: #E7F4E9;
        color: #276B37 !important;
    }

    .journey-done .journey-icon {
        background: #7FB685;
        color: white !important;
    }

    .journey-active {
        background: #51445F;
        color: white !important;
        box-shadow: 0 6px 16px rgba(81, 68, 95, 0.16);
    }

    .journey-active .journey-icon {
        background: #E76F51;
        color: white !important;
    }

    .journey-upcoming {
        background: #F6F1EA;
        color: #756B73 !important;
    }

    .journey-upcoming .journey-icon {
        background: #E2D9D0;
        color: #756B73 !important;
    }

    /* Completely remove Streamlit sidebar */
    section[data-testid="stSidebar"] {
        display: none !important;
    }

    [data-testid="collapsedControl"] {
        display: none !important;
    }

        /* ================================
       TEXT
       ================================ */

    h1,
    h2,
    h3,
    h4,
    p,
    span,
    label {
        color: #171A1A !important;
        opacity: 1 !important;
    }


    /* ================================
       TITLE
       ================================ */

    .main-title {
        color: #51445F !important;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0;
    }


    .subtitle {
        color: #51445F !important;
        font-size: 18px;
        margin-bottom: 25px;
    }


    /* ================================
       CARDS
       ================================ */

    .card {
        background-color: #F1E9DA !important;
        color: #171A1A !important;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        border-left: 5px solid #51445F;
        opacity: 1 !important;
        filter: none !important;
    }


    .card * {
        color: #171A1A !important;
        opacity: 1 !important;
        filter: none !important;
    }


    /* ================================
       CONCEPT CARD
       ================================ */

    .concept-card {
        background-color: #FFFFFF !important;
        color: #171A1A !important;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        border-left: 5px solid #51445F;
        opacity: 1 !important;
        filter: none !important;
    }


    .concept-card * {
        color: #171A1A !important;
        opacity: 1 !important;
        filter: none !important;
    }


    /* ================================
       SUCCESS
       ================================ */

    .success-card {
        background-color: #E4F0E5 !important;
        color: #171A1A !important;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        border-left: 5px solid #7FB685;
        opacity: 1 !important;
    }


    .success-card * {
        color: #171A1A !important;
    }


    /* ================================
       WARNING
       ================================ */

    .warning-card {
        background-color: #FCE5DE !important;
        color: #171A1A !important;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        border-left: 5px solid #E76F51;
        opacity: 1 !important;
    }


    .warning-card * {
        color: #171A1A !important;
    }


    /* ================================
       STAGE
       ================================ */

    .stage-card {
        background-color: #FFFFFF !important;
        color: #171A1A !important;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 2px solid #51445F;
        opacity: 1 !important;
    }


    .stage-card * {
        color: #171A1A !important;
    }


    /* ================================
       PDF CONTENT
       ================================ */

    .pdf-content {
        background-color: #FFFFFF !important;
        color: #171A1A !important;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #DDD5C8;
        line-height: 1.8;
        font-size: 16px;
        white-space: pre-wrap;
        opacity: 1 !important;
    }


    /* ================================
       METRIC
       ================================ */

    .metric-card {
        background-color: #F1E9DA !important;
        color: #171A1A !important;
        padding: 18px;
        border-radius: 15px;
        text-align: center;
    }


    .metric-number {
        font-size: 30px;
        font-weight: 800;
        color: #51445F !important;
    }


    .metric-label {
        font-size: 14px;
        color: #171A1A !important;
    }
    .exam-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 20px;
        background: linear-gradient(135deg, #F1E9DA, #FFFFFF);
        border: 1px solid #DDD5C8;
        border-radius: 22px;
        padding: 24px 28px;
        margin: 10px 0 22px 0;
    }

    .exam-header h1 {
        color: #171A1A !important;
        font-size: 30px;
        margin: 0 0 5px 0;
    }

    .exam-header p {
        color: #5B5360 !important;
        margin: 0;
    }

    .exam-rule {
        min-width: 125px;
        text-align: center;
        background: #51445F;
        color: #FFFFFF !important;
        border-radius: 15px;
        padding: 12px 16px;
        line-height: 1.45;
    }

    .exam-rule * {
        color: #FFFFFF !important;
    }

    .exam-question-card {
        background: #FFFFFF;
        border: 1px solid #DDD5C8;
        border-radius: 18px;
        padding: 20px 22px 14px 22px;
        margin-top: 22px;
        box-shadow: 0 8px 22px rgba(81,68,95,.055);
    }

    .exam-question-number {
        color: #51445F !important;
        font-size: 11px;
        font-weight: 900;
        letter-spacing: .12em;
        margin-bottom: 10px;
    }

    .exam-question-text {
        color: #171A1A !important;
        font-size: 20px;
        line-height: 1.5;
        font-weight: 750;
    }

    div[class*="st-key-exam_option_"] button {
        min-height: 78px !important;
        height: auto !important;
        white-space: normal !important;
        text-align: left !important;
        justify-content: flex-start !important;
        align-items: flex-start !important;
        padding: 15px 17px !important;
        margin-top: 10px !important;
        border-radius: 14px !important;
        border: 1px solid #D8CCBC !important;
        background: #FFFDF8 !important;
        color: #171A1A !important;
        font-weight: 600 !important;
        line-height: 1.45 !important;
        box-shadow: 0 4px 12px rgba(81,68,95,.04) !important;
        transition: all .16s ease !important;
    }

    div[class*="st-key-exam_option_"] button:hover {
        border-color: #51445F !important;
        background: #F9F5FC !important;
        transform: translateY(-1px);
        box-shadow: 0 8px 18px rgba(81,68,95,.09) !important;
    }

    .exam-selected {
        color: #3D6B45 !important;
        font-size: 12px;
        font-weight: 800;
        margin: 6px 0 4px 3px;
    }

    .exam-footer-info {
        display: flex;
        justify-content: space-between;
        margin: 26px 0 8px 0;
        color: #51445F !important;
        font-weight: 750;
        font-size: 14px;
    }

    .term-chip {
        display: inline-block;
        padding: 7px 11px;
        margin: 5px;
        border-radius: 999px;
        background: #EAF3EB;
        border: 1px solid #C5DCC9;
        color: #3D6B45 !important;
        font-weight: 700;
        font-size: 13px;
    }

    .quiz-shell {
        background: #FFFFFF;
        border: 1px solid #DDD5C8;
        border-radius: 22px;
        padding: 26px;
        box-shadow: 0 14px 34px rgba(81,68,95,.08);
        margin-top: 18px;
    }

    .quiz-topline {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        margin-bottom: 10px;
    }

    .quiz-badge {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        background: #F1E9DA;
        color: #51445F !important;
        font-weight: 800;
        font-size: 12px;
    }

    .quiz-topic {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        background: #EAF3EB;
        color: #3D6B45 !important;
        font-weight: 700;
        font-size: 12px;
    }

    .quiz-question {
        color: #171A1A !important;
        font-size: 25px;
        line-height: 1.35;
        font-weight: 800;
        margin: 18px 0 20px 0;
    }

    div[class*="st-key-quiz_option_"] button {
        min-height: 88px !important;
        height: auto !important;
        white-space: normal !important;
        text-align: left !important;
        justify-content: flex-start !important;
        align-items: flex-start !important;
        padding: 16px 18px !important;
        border-radius: 16px !important;
        border: 1px solid #D8CCBC !important;
        background: #FFFDF8 !important;
        color: #171A1A !important;
        font-weight: 650 !important;
        line-height: 1.45 !important;
        box-shadow: 0 6px 16px rgba(81,68,95,.05) !important;
        transition: all .18s ease !important;
    }

    div[class*="st-key-quiz_option_"] button:hover {
        border-color: #51445F !important;
        transform: translateY(-1px);
        box-shadow: 0 10px 22px rgba(81,68,95,.10) !important;
    }

    .quiz-navigation {
        margin-top: 20px;
        padding-top: 18px;
        border-top: 1px solid #E6DED2;
    }

    .quiz-selection-note {
        background: #F7F3EC;
        border-radius: 12px;
        padding: 10px 14px;
        color: #51445F !important;
        font-size: 14px;
        margin-top: 14px;
    }

    .celebration-card {
        background: linear-gradient(135deg, #F1E9DA, #FFFFFF);
        border: 2px solid #7FB685;
        border-radius: 24px;
        padding: 42px 30px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 14px 35px rgba(81, 68, 95, 0.12);
    }

    .celebration-card h1 {
        color: #51445F !important;
        font-size: 42px;
        margin-bottom: 8px;
    }

    .celebration-card h2 {
        color: #171A1A !important;
        margin-bottom: 12px;
    }

    .celebration-icon {
        font-size: 54px;
        margin-bottom: 8px;
    }

    .celebration-score {
        color: #7FB685 !important;
        font-size: 48px;
        font-weight: 800;
        margin: 8px 0 0 0;
    }

    .celebration-label {
        color: #51445F !important;
        font-weight: 700;
        margin-bottom: 18px;
    }

    .celebration-message {
        color: #171A1A !important;
        font-size: 19px;
        line-height: 1.6;
        max-width: 760px;
        margin: 0 auto;
    }

    .next-module-card,
    .final-message-card {
        background: #FFFFFF;
        border: 1px solid #DDD5C8;
        border-left: 6px solid #51445F;
        border-radius: 18px;
        padding: 24px;
        margin: 18px 0;
    }

    .next-module-card h2,
    .final-message-card h2 {
        color: #51445F !important;
    }

    .next-module-card p,
    .final-message-card p {
        color: #171A1A !important;
        font-size: 16px;
        line-height: 1.6;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

def initialize_session_state():

    defaults = {

        # -------------------------------
        # Student information
        # -------------------------------

        "started": False,

        "subject": "",

        "goal": "",

        "level": "",


        # -------------------------------
        # PDF
        # -------------------------------

        "pdf_text": "",

        "modules": [],


        # -------------------------------
        # Module
        # -------------------------------

        "current_module": 0,


        # -------------------------------
        # Learning mode
        # -------------------------------

        "learning_mode": "PDF",


        # -------------------------------
        # Current stage
        # -------------------------------

        "stage": "learning",


        # -------------------------------
        # AI Lesson
        # -------------------------------

        "lesson": {},


        # -------------------------------
        # Knowledge Check
        # -------------------------------

        "knowledge_questions": [],

        "knowledge_score": 0,

        "knowledge_submitted": False,

        "knowledge_answers": {},

        "knowledge_current_question": 0,


        # -------------------------------
        # Weak concepts
        # -------------------------------

        "weak_topics": [],

        "topic_scores": {},


        # -------------------------------
        # Review
        # -------------------------------

        "review": {},


        # -------------------------------
        # Module progress
        # -------------------------------

        "completed_modules": [],

        "module_scores": {},


        # -------------------------------
        # Overall concept performance
        # -------------------------------

        "all_topic_scores": {}

    }


    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


initialize_session_state()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_text(text):

    return html.escape(str(text))


def prepare_pdf_reading(text):
    """Build a concept -> example reading flow from the uploaded PDF only."""

    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()

    raw_sentences = re.split(r"(?<=[.!?])\s+", text)
    sentences = []
    seen = set()

    metadata_pattern = re.compile(
        r"^(file\s*name|filename|file\s*size|size|author|created\s*by|"
        r"creator|producer|pages?|page\s*count|creation\s*date|"
        r"modified\s*date)\s*[:\-]",
        re.IGNORECASE
    )

    for sentence in raw_sentences:
        sentence = re.sub(r"\s+", " ", sentence).strip()

        if len(sentence) < 45:
            continue

        if metadata_pattern.search(sentence):
            continue

        key = sentence.lower()
        if key in seen:
            continue

        seen.add(key)
        sentences.append(sentence)

    topics = find_topics(text)[:12]

    example_pattern = re.compile(
        r"\b(example|for example|for instance|such as|case study|"
        r"case studies|real[- ]world|scenario|illustrat|e\.g\.|"
        r"hiring system|patient|customer|company|organization|case)\b",
        re.IGNORECASE
    )

    def topic_for(sentence):
        for topic in topics:
            if re.search(
                rf"\b{re.escape(topic)}\b",
                sentence,
                re.IGNORECASE
            ):
                return topic
        return topics[0] if topics else "main concept"

    def related_to(sentence, pool):
        topic = topic_for(sentence)
        related = []

        for item in pool:
            if item == sentence:
                continue
            if re.search(
                rf"\b{re.escape(topic)}\b",
                item,
                re.IGNORECASE
            ):
                related.append(item)

        return related

    concept_sentences = []

    # Prefer explanatory sentences, then fill from the remaining PDF content.
    for sentence in sentences:
        if example_pattern.search(sentence):
            continue
        concept_sentences.append(sentence)
        if len(concept_sentences) >= 5:
            break

    if len(concept_sentences) < 5:
        for sentence in sentences:
            if sentence in concept_sentences or example_pattern.search(sentence):
                continue
            concept_sentences.append(sentence)
            if len(concept_sentences) >= 5:
                break

    blocks = []
    used_examples = set()

    for concept in concept_sentences:
        topic = topic_for(concept)

        explicit_examples = [
            sentence for sentence in sentences
            if sentence not in used_examples
            and sentence != concept
            and example_pattern.search(sentence)
            and re.search(
                rf"\b{re.escape(topic)}\b",
                sentence,
                re.IGNORECASE
            )
        ]

        related_sentences = [
            sentence for sentence in related_to(concept, sentences)
            if sentence not in used_examples
        ]

        example = None

        if explicit_examples:
            example = explicit_examples[0]
        elif related_sentences:
            example = related_sentences[0]
        else:
            # Use a different PDF sentence as the closest supporting illustration.
            for sentence in sentences:
                if sentence != concept and sentence not in used_examples:
                    example = sentence
                    break

        if example:
            used_examples.add(example)

        blocks.append({
            "concept": concept,
            "topic": topic,
            "example": example
        })

    return blocks, topics


# ============================================================
# MODULE NAMES
# ============================================================

MODULE_NAMES = [

    "Module 1 — Foundations",

    "Module 2 — Core Concepts",

    "Module 3 — Advanced Concepts"

]


def get_module_name(index):

    return MODULE_NAMES[index]


# ============================================================
# CURRENT MODULE TEXT
# ============================================================

def get_current_module_text():

    index = st.session_state.current_module

    return st.session_state.modules[index]


# ============================================================
# RESET CURRENT MODULE
# ============================================================

def reset_current_module():

    st.session_state.stage = "learning"

    st.session_state.lesson = {}

    st.session_state.knowledge_questions = []

    st.session_state.knowledge_score = 0

    st.session_state.knowledge_submitted = False

    st.session_state.knowledge_answers = {}

    st.session_state.knowledge_current_question = 0

    st.session_state.weak_topics = []

    st.session_state.topic_scores = {}

    st.session_state.review = {}



# ============================================================
# LOCAL PDF KNOWLEDGE CHECK
# ============================================================

def create_pdf_quiz(text):
    """Create five professional MCQs using only the uploaded PDF content."""

    text = re.sub(r"\s+", " ", text or "").strip()

    raw_sentences = re.split(r"(?<=[.!?])\s+", text)

    def clean_sentence(sentence):
        sentence = re.sub(r"\s+", " ", sentence).strip()
        sentence = re.sub(r"^(?:\d+\s*[-.:)]|[•●◦]\s*)", "", sentence)
        return sentence.strip()

    def is_noise(sentence):
        value = sentence.lower().strip()

        if len(value) < 55:
            return True

        patterns = [
            r"^\d+[\s\-:.]*(module|chapter|unit|section)",
            r"^(table of contents|contents|references|bibliography)",
            r"^(module|chapter|unit|section)\s*\d",
            r"\bpage\s*\d+\b",
            r"\bprepared by\b",
            r"\bsubmitted by\b",
            r"\bdepartment of\b",
            r"\bfile name\b",
            r"\bfile size\b",
            r"\bcreated by\b"
        ]

        return any(re.search(pattern, value) for pattern in patterns)

    sentences = []
    seen = set()

    for raw in raw_sentences:
        sentence = clean_sentence(raw)

        if is_noise(sentence):
            continue

        key = sentence.lower()
        if key in seen:
            continue

        seen.add(key)
        sentences.append(sentence)

    if len(sentences) < 5:
        return []

    topics = find_topics(text)[:15]

    def topic_for(sentence):
        for topic in topics:
            if re.search(rf"\b{re.escape(topic)}\b", sentence, re.IGNORECASE):
                return topic
        return "the concept"

    def short_option(sentence, limit=210):
        sentence = re.sub(r"\s+", " ", sentence).strip()
        if len(sentence) <= limit:
            return sentence
        shortened = sentence[:limit].rsplit(" ", 1)[0]
        return shortened + "…"

    # Select source statements from different topic areas where possible.
    selected = []
    used_sources = set()
    used_topics = set()

    for topic in topics:
        matches = [
            sentence for sentence in sentences
            if sentence not in used_sources
            and re.search(rf"\b{re.escape(topic)}\b", sentence, re.IGNORECASE)
        ]

        if matches:
            selected.append((topic, matches[0]))
            used_sources.add(matches[0])
            used_topics.add(topic)

        if len(selected) == 5:
            break

    if len(selected) < 5:
        for sentence in sentences:
            if sentence in used_sources:
                continue
            selected.append((topic_for(sentence), sentence))
            used_sources.add(sentence)
            if len(selected) == 5:
                break

    stems = [
        "Which statement best describes {topic}?",
        "Which statement gives the most accurate explanation of {topic}?",
        "Which statement correctly reflects the role of {topic}?",
        "Which statement is most consistent with the discussion of {topic}?",
        "Which conclusion is supported by the material about {topic}?"
    ]

    questions = []

    for index, (topic, correct_sentence) in enumerate(selected[:5]):
        distractors = [
            sentence for sentence in sentences
            if sentence != correct_sentence
        ]

        # Prefer statements from other topic areas for plausible alternatives.
        other_topic_sentences = [
            sentence for sentence in distractors
            if topic_for(sentence).lower() != topic.lower()
        ]

        pool = other_topic_sentences if len(other_topic_sentences) >= 3 else distractors
        random.shuffle(pool)

        options = [short_option(correct_sentence)]
        for candidate in pool:
            candidate = short_option(candidate)
            if candidate.lower() not in {item.lower() for item in options}:
                options.append(candidate)
            if len(options) == 4:
                break

        if len(options) != 4:
            continue

        correct = options[0]
        random.shuffle(options)

        questions.append({
            "question": stems[index].format(topic=topic.title()),
            "options": options,
            "answer": correct,
            "topic": topic,
            "difficulty": "Exam"
        })

    return questions[:5]


# ============================================================
# LOCAL TARGETED REVIEW
# ============================================================

def create_local_review(text, weak_topics):

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.replace("\n", " ")
    )


    sentences = [

        sentence.strip()

        for sentence in sentences

        if len(sentence.strip()) > 30

    ]


    concepts = []


    for topic in weak_topics:

        relevant_sentences = [

            sentence

            for sentence in sentences

            if topic.lower()
            in sentence.lower()

        ]


        if relevant_sentences:

            explanation = (
                f"The uploaded material explains "
                f"{topic} in the following section: "
                f"{' '.join(relevant_sentences[:2])}"
            )

            example = relevant_sentences[0]

        else:

            explanation = (
                f"Review {topic} carefully in the "
                f"uploaded study material. Focus on "
                f"its meaning, purpose and connection "
                f"with other concepts."
            )

            example = (
                f"Find the section about {topic} "
                f"in the PDF and explain it in "
                f"your own words."
            )


        concepts.append({

            "concept": topic,

            "explanation": explanation,

            "example": example,

            "common_mistake":
                f"Do not only memorize {topic}. "
                f"Make sure you understand its meaning "
                f"and application."

        })


    return {

        "title":
            "Targeted Re-Teaching",

        "intro":
            "Your Knowledge Check shows that "
            "these concepts need more practice.",

        "weak_concepts":
            concepts,

        "key_points": [

            f"Review {topic} carefully."

            for topic in weak_topics

        ]

    }


# ============================================================
# HEADER
# ============================================================

st.markdown(

    '<div class="main-title">MasteryPath AI</div>',

    unsafe_allow_html=True

)


st.markdown(

    '<div class="subtitle">'
    'Learn at your level. Discover your gaps. '
    'Master every concept.'
    '</div>',

    unsafe_allow_html=True

)


# ============================================================
# TOP JOURNEY BAR — NO SIDEBAR
# ============================================================

current_stage_key = st.session_state.get("stage", "learning")
current_module_number = st.session_state.get("current_module", 0) + 1

journey_labels = [
    "1. Upload",
    "2. Learn",
    "3. Assess",
    "4. Improve",
    "5. Master"
]

stage_to_step = {
    "learning": 2,
    "knowledge_check": 3,
    "review": 4,
    "completed": 5
}

active_step = stage_to_step.get(current_stage_key, 1)

step_html = ""

for step_number, label in enumerate(journey_labels, 1):
    if step_number < active_step:
        step_class = "journey-done"
        icon = "✓"
    elif step_number == active_step:
        step_class = "journey-active"
        icon = str(step_number)
    else:
        step_class = "journey-upcoming"
        icon = str(step_number)

    step_html += (
        f'<div class="journey-item {step_class}">'
        f'<span class="journey-icon">{icon}</span>'
        f'<span>{safe_text(label)}</span>'
        '</div>'
    )

journey_html = (
    '<div class="journey-bar">'
    f'<div class="journey-module">Module {current_module_number} of 3</div>'
    f'<div class="journey-steps">{step_html}</div>'
    '</div>'
)

st.markdown(journey_html, unsafe_allow_html=True)


# ============================================================
# START SCREEN
# ============================================================

if not st.session_state.started:

    st.header(
        " Start Your Learning Journey"
    )


    st.write(

        "Enter your learning information and "
        "upload your study material."
    )


    col1, col2 = st.columns(2)


    with col1:

        subject = st.text_input(

            "Subject",

            placeholder=
            "Example: Machine Learning"

        )


        goal = st.text_input(

            "Learning Goal",

            placeholder=
            "Example: Prepare for semester exam"

        )


    with col2:

        level = st.selectbox(

            "Current Knowledge Level",

            [

                "Beginner",

                "Intermediate",

                "Advanced"

            ]

        )


        uploaded_file = st.file_uploader(

            "Upload Study PDF",

            type=["pdf"]

        )


    if st.button(

        " Start Learning",

        type="primary",

        use_container_width=True

    ):

        if not subject.strip():

            st.warning(
                "Please enter your subject."
            )

        elif uploaded_file is None:

            st.warning(
                "Please upload your PDF."
            )

        else:

            try:

                with st.spinner(
                    "Reading your study material..."
                ):

                    text = extract_text_from_pdf(
                        uploaded_file
                    )

                    text = clean_text(text)


                if not text.strip():

                    st.error(
                        "No readable text was found "
                        "in the PDF."
                    )

                else:

                    part1, part2, part3 = (
                        divide_into_three_parts(text)
                    )


                    st.session_state.subject = (
                        subject.strip()
                    )

                    st.session_state.goal = (
                        goal.strip()
                    )

                    st.session_state.level = level

                    st.session_state.pdf_text = text

                    st.session_state.modules = [

                        part1,
                        part2,
                        part3

                    ]

                    st.session_state.current_module = 0

                    st.session_state.learning_mode = "PDF"

                    st.session_state.started = True

                    st.session_state.completed_modules = []

                    st.session_state.module_scores = {}

                    st.session_state.all_topic_scores = {}

                    reset_current_module()

                    st.rerun()


            except Exception as e:

                st.error(
                    "Error while reading the PDF."
                )

                st.exception(e)


    st.stop()


# ============================================================
# LEARNING MODE SELECTOR
# ============================================================

st.divider()

st.header(" Choose Your Learning Experience")
st.caption("Select a learning style for this module.")

mode_options = [
    " AI-Powered Learning",
    " PDF Reading"
]

current_mode_label = (
    mode_options[0]
    if st.session_state.learning_mode == "AI"
    else mode_options[1]
)

selected_mode = st.pills(
    "Learning mode",
    mode_options,
    selection_mode="single",
    default=current_mode_label,
    key="learning_mode_pills",
    label_visibility="collapsed"
)

st.markdown(
    """
    <style>
    div[data-testid="stPills"] {
        background: #F1E9DA !important;
        border: 1px solid #D8CCBC !important;
        border-radius: 18px !important;
        padding: 6px !important;
        box-shadow: 0 10px 28px rgba(81,68,95,.08) !important;
    }

    div[data-testid="stPills"] button {
        min-height: 48px !important;
        border-radius: 13px !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        padding: 8px 22px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if selected_mode == mode_options[0] and st.session_state.learning_mode != "AI":
    st.session_state.learning_mode = "AI"
    reset_current_module()
    st.rerun()

if selected_mode == mode_options[1] and st.session_state.learning_mode != "PDF":
    st.session_state.learning_mode = "PDF"
    reset_current_module()
    st.rerun()


# ============================================================
# PROGRESS DASHBOARD
# ============================================================

st.divider()

st.subheader(
    " Learning Dashboard"
)


total_modules = len(
    st.session_state.modules
)


completed_modules = len(
    st.session_state.completed_modules
)


overall_progress = (

    completed_modules / total_modules

    if total_modules

    else 0

)


current_module = (
    st.session_state.current_module
)


latest_score = (

    st.session_state.module_scores.get(

        current_module,

        0

    )

)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(

        f"""
        <div class="metric-card">

        <div class="metric-number">
        {completed_modules}/{total_modules}
        </div>

        <div class="metric-label">
        Modules Completed
        </div>

        </div>
        """,

        unsafe_allow_html=True

    )


with col2:

    st.markdown(

        f"""
        <div class="metric-card">

        <div class="metric-number">
        {round(overall_progress * 100)}%
        </div>

        <div class="metric-label">
        Overall Progress
        </div>

        </div>
        """,

        unsafe_allow_html=True

    )


with col3:

    st.markdown(

        f"""
        <div class="metric-card">

        <div class="metric-number">
        {latest_score}%
        </div>

        <div class="metric-label">
        Latest Score
        </div>

        </div>
        """,

        unsafe_allow_html=True

    )


with col4:

    try:

        mastery, mastery_level = predict_mastery(

            latest_score,

            1,

            len(st.session_state.weak_topics)

        )

    except Exception:

        mastery = latest_score

        mastery_level = "Unknown"


    st.markdown(

        f"""
        <div class="metric-card">

        <div class="metric-number">
        {mastery}%
        </div>

        <div class="metric-label">
        Estimated Mastery
        </div>

        </div>
        """,

        unsafe_allow_html=True

    )


st.progress(overall_progress)


# ============================================================
# PERFORMANCE VISUALIZATION
# ============================================================

st.subheader(" Performance Overview")

progress_cols = st.columns(total_modules if total_modules else 1)

for i in range(total_modules):
    with progress_cols[i]:
        if i in st.session_state.module_scores:
            module_score = st.session_state.module_scores[i]
            status_text = "Completed"
        elif i == current_module:
            module_score = st.session_state.knowledge_score
            status_text = "Current"
        else:
            module_score = 0
            status_text = "Locked"

        st.markdown(
            f"**Module {i + 1}** — {status_text}"
        )
        st.progress(
            max(0, min(100, module_score)) / 100
        )
        st.caption(f"Score: {module_score}%")

completed_performance = [
    {
        "Module": get_module_name(i),
        "Score": st.session_state.module_scores.get(i, 0)
    }
    for i in range(total_modules)
    if i in st.session_state.module_scores
]

if completed_performance:
    performance_df = pd.DataFrame(completed_performance)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.caption("Module Score Graph")
        st.bar_chart(
            performance_df.set_index("Module")
        )

    with chart_col2:
        st.caption("Learning Progress Plot")
        st.line_chart(
            performance_df.set_index("Module")
        )


# ============================================================
# MODULE STATUS
# ============================================================

st.subheader(
    " Your Modules"
)


for i in range(total_modules):

    if i in st.session_state.completed_modules:

        st.success(

            f" {get_module_name(i)} — Completed"

        )

    elif i == current_module:

        st.info(

            f" {get_module_name(i)} — Current"

        )

    else:

        st.warning(

            f" {get_module_name(i)} — Locked"

        )


# ============================================================
# CURRENT MODULE
# ============================================================

st.divider()

st.header(
    get_module_name(current_module)
)


module_text = get_current_module_text()


# ============================================================
# CURRENT STAGE DISPLAY
# ============================================================

stage_names = {

    "learning":
        " Learning",

    "knowledge_check":
        " Knowledge Check",

    "review":
        " Weak Concept Review",

    "completed":
        " Module Completed"

}


current_stage = stage_names.get(

    st.session_state.stage,

    " Learning"

)


st.markdown(

    f"""
    <div class="stage-card">

    <h3>Current Learning Stage</h3>

    <h2>{safe_text(current_stage)}</h2>

    </div>
    """,

    unsafe_allow_html=True

)


# ============================================================
# ============================================================
# STAGE 1
# LEARNING
# ============================================================
# ============================================================

if st.session_state.stage == "learning":

    st.header(
        " Learn This Module"
    )


    # ========================================================
    # PDF READING MODE
    # ========================================================

    if st.session_state.learning_mode == "PDF":

        concept_blocks, pdf_topics = prepare_pdf_reading(module_text)

        st.markdown(
            """
            <div class="reader-header">
                <div class="reader-kicker">PDF READING</div>
                <h2>Learn the concept step by step</h2>
                <p>Each concept is explained first, followed immediately by one related example taken from the uploaded material.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if concept_blocks:
            for index, block in enumerate(concept_blocks, start=1):
                concept_text = block["concept"]
                example_text = block.get("example")
                topic = block.get("topic", "Concept")

                st.markdown(
                    f"""
                    <div class="concept-learning-card">
                        <div class="concept-number">CONCEPT {index}</div>
                        <div class="concept-topic">{safe_text(str(topic).title())}</div>
                        <h3>{safe_text(concept_text)}</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if example_text:
                    st.markdown(
                        f"""
                        <div class="example-learning-card">
                            <div class="example-label">EXAMPLE</div>
                            <div class="example-text">{safe_text(example_text)}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                if index < len(concept_blocks):
                    st.markdown(
                        '<div class="learning-connector">↓</div>',
                        unsafe_allow_html=True
                    )
        else:
            st.warning("No readable learning content was extracted from this module.")

        if pdf_topics:
            st.markdown("### Important Terms")
            st.caption("Terms identified from the uploaded module.")
            st.markdown(
                "".join(
                    f'<span class="term-chip">{safe_text(topic.title())}</span>'
                    for topic in pdf_topics
                ),
                unsafe_allow_html=True
            )

        with st.expander(" View complete PDF content"):
            st.markdown(
                f"""
                <div class="pdf-content">
                    {safe_text(module_text)}
                </div>
                """,
                unsafe_allow_html=True
            )


    # ========================================================
    # AI MODE
    # ========================================================

    else:

        st.info(

            " AI-Powered Learning is active. "
            "Gemini will explain the module according "
            "to the student's level."
        )


        # ----------------------------------------------------
        # GENERATE LESSON
        # ----------------------------------------------------

        if not st.session_state.lesson:

            if st.button(

                " Generate AI Lesson",

                type="primary",

                use_container_width=True

            ):

                with st.spinner(

                    "Gemini is preparing your personalized lesson..."

                ):

                    try:

                        lesson = generate_lesson(

                            module_text,

                            st.session_state.subject,

                            st.session_state.level

                        )

                    except Exception as e:

                        lesson = {}

                        st.error(
                            f"AI lesson error: {e}"
                        )


                if lesson:

                    st.session_state.lesson = lesson

                    st.rerun()

                else:

                    st.warning(

                        "Gemini is currently unavailable."
                    )


                    st.info(

                        "You can switch to "
                        " PDF Reading Mode and continue "
                        "without Gemini."
                    )


        # ----------------------------------------------------
        # DISPLAY AI LESSON
        # ----------------------------------------------------

        if st.session_state.lesson:

            lesson = st.session_state.lesson


            st.subheader(

                lesson.get(

                    "title",

                    "AI Lesson"

                )

            )


            # Overview
            st.markdown(
                "###  Overview"
            )


            st.write(

                lesson.get(
                    "overview",
                    ""
                )

            )


            # Objectives
            st.markdown(
                "###  Learning Objectives"
            )


            for objective in lesson.get(

                "learning_objectives",

                []

            ):

                st.write(
                    f"• {objective}"
                )


            # Explanation
            st.markdown(
                "###  Simple Explanation"
            )


            st.write(

                lesson.get(
                    "explanation",
                    ""
                )

            )


            # Examples
            st.markdown(
                "###  Real-Life Examples"
            )


            for example in lesson.get(

                "examples",

                []

            ):

                st.markdown(

                    f"""
                    <div class="concept-card">

                    <h3>
                    {safe_text(
                        example.get(
                            "title",
                            "Example"
                        )
                    )}
                    </h3>

                    </div>
                    """,

                    unsafe_allow_html=True

                )


                st.write(

                    example.get(
                        "example",
                        ""
                    )

                )


                st.markdown(
                    "**Why it matters:**"
                )


                st.write(

                    example.get(
                        "why_it_matters",
                        ""
                    )

                )


            # Key points
            st.markdown(
                "###  Key Points"
            )


            for point in lesson.get(

                "key_points",

                []

            ):

                st.write(
                    f"• {point}"
                )


            # Mistakes
            st.markdown(
                "###  Common Mistakes"
            )


            for mistake in lesson.get(

                "common_mistakes",

                []

            ):

                st.write(
                    f"• {mistake}"
                )


            # Important concepts
            st.markdown(
                "###  Important Concepts"
            )


            for concept in lesson.get(

                "important_concepts",

                []

            ):

                st.markdown(

                    f"""
                    <div class="concept-card">

                    <h3>
                     {safe_text(concept)}
                    </h3>

                    </div>
                    """,

                    unsafe_allow_html=True

                )


                st.write(

                    f"Understand the meaning, purpose "
                    f"and role of {concept} in this module."

                )


    # ========================================================
    # NEXT STEP
    # ========================================================

    st.divider()


    st.subheader(
        " Ready to test yourself?"
    )


    if st.button(

        " Start Knowledge Check",

        type="primary",

        use_container_width=True

    ):

        st.session_state.stage = "knowledge_check"

        st.session_state.knowledge_questions = []

        st.session_state.knowledge_submitted = False

        st.session_state.knowledge_answers = {}

        st.session_state.knowledge_current_question = 0

        st.session_state.knowledge_score = 0

        st.rerun()


# ============================================================
# ============================================================
# STAGE 2
# KNOWLEDGE CHECK
# ============================================================
# ============================================================

elif st.session_state.stage == "knowledge_check":

    st.markdown(
        """
        <div class="exam-header">
            <div>
                <div class="exam-kicker">KNOWLEDGE CHECK</div>
                <h1>Module Assessment</h1>
                <p>Choose the single best answer for each question.</p>
            </div>
            <div class="exam-rule">
                <strong>5 MCQs</strong><br>
                <span>70% required</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # CREATE QUESTIONS ONCE
    # ========================================================

    if not st.session_state.knowledge_questions:

        if st.session_state.learning_mode == "AI":

            with st.spinner("Preparing your assessment..."):

                try:
                    questions = generate_ai_questions(
                        module_text,
                        st.session_state.subject,
                        st.session_state.level,
                        5
                    )
                except Exception:
                    questions = []

            if questions:
                st.session_state.knowledge_questions = questions
            else:
                st.session_state.knowledge_questions = create_pdf_quiz(module_text)

        else:

            with st.spinner("Preparing your assessment..."):
                st.session_state.knowledge_questions = create_pdf_quiz(module_text)

    questions = st.session_state.knowledge_questions

    if questions:

        # Always present exactly five questions when the generator has enough content.
        questions = questions[:5]

        for question_index, question in enumerate(questions):

            selected_answer = st.session_state.knowledge_answers.get(question_index)
            letters = ["A", "B", "C", "D"]

            st.markdown(
                f"""
                <div class="exam-question-card">
                    <div class="exam-question-number">QUESTION {question_index + 1}</div>
                    <div class="exam-question-text">{safe_text(question['question'])}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            option_columns = st.columns(2, gap="medium")

            for option_index, option in enumerate(question["options"]):
                column = option_columns[option_index % 2]
                option_key = f"exam_option_{question_index}_{option_index}"
                is_selected = selected_answer == option

                with column:

                    if is_selected:
                        st.markdown(
                            f"""
                            <style>
                            div.st-key-{option_key} button {{
                                background: #F0E9FA !important;
                                color: #51445F !important;
                                border: 2px solid #51445F !important;
                                box-shadow: 0 8px 20px rgba(81,68,95,.13) !important;
                            }}
                            </style>
                            """,
                            unsafe_allow_html=True
                        )

                    if st.button(
                        f"{letters[option_index]}   {option}",
                        key=option_key,
                        use_container_width=True
                    ):
                        st.session_state.knowledge_answers[question_index] = option
                        st.rerun()

            if selected_answer:
                st.markdown(
                    "<div class='exam-selected'>✓ Answer selected</div>",
                    unsafe_allow_html=True
                )

        answered_count = len(st.session_state.knowledge_answers)

        st.markdown(
            f"""
            <div class="exam-footer-info">
                <span>{answered_count} of {len(questions)} answered</span>
                <span>Pass mark: 70%</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(
            answered_count / len(questions),
            text=f"Assessment progress — {answered_count}/{len(questions)}"
        )

        all_answered = answered_count == len(questions)

        if st.button(
            "Submit Assessment",
            type="primary",
            use_container_width=True,
            disabled=not all_answered,
            key="submit_professional_exam"
        ):

            correct = 0
            topic_results = {}

            for i, item in enumerate(questions):
                selected = st.session_state.knowledge_answers.get(i)
                correct_answer = item["answer"]
                topic = item.get("topic", "General")

                if topic not in topic_results:
                    topic_results[topic] = {"correct": 0, "total": 0}

                topic_results[topic]["total"] += 1

                if selected == correct_answer:
                    correct += 1
                    topic_results[topic]["correct"] += 1

            total = len(questions)
            score = round((correct / total) * 100)

            st.session_state.knowledge_score = score
            st.session_state.knowledge_submitted = True

            topic_scores = {}
            weak_topics = []

            for topic, result in topic_results.items():
                topic_score = round(
                    result["correct"] / result["total"] * 100
                )
                topic_scores[topic] = topic_score
                if topic_score < 70:
                    weak_topics.append(topic)

            st.session_state.topic_scores = topic_scores
            st.session_state.weak_topics = weak_topics

            for topic, score_value in topic_scores.items():
                previous = st.session_state.all_topic_scores.get(topic)
                if previous is None:
                    st.session_state.all_topic_scores[topic] = score_value
                else:
                    st.session_state.all_topic_scores[topic] = round(
                        (previous + score_value) / 2
                    )

            if score >= 70:
                st.session_state.stage = "completed"
            else:
                st.session_state.stage = "review"

            st.rerun()

    else:
        st.error("Unable to create the five-question assessment for this module.")


# ============================================================
# KNOWLEDGE CHECK RESULT
# ============================================================

if (
    st.session_state.knowledge_submitted
    and st.session_state.stage in ["knowledge_check", "review"]
):

    score = st.session_state.knowledge_score


    if score >= 70:

        st.markdown(

            f"""
            <div class="success-card">

            <h2>
             Knowledge Check Passed
            </h2>

            <p>
            Score: <b>{score}%</b>
            </p>

            <p>
            You reached the required 70%.
            </p>

            </div>
            """,

            unsafe_allow_html=True

        )

    else:

        st.markdown(

            f"""
            <div class="warning-card">

            <h2>
             More Practice Needed
            </h2>

            <p>
            Score: <b>{score}%</b>
            </p>

            <p>
            Required: <b>70%</b>
            </p>

            </div>
            """,

            unsafe_allow_html=True

        )


# ============================================================
# ============================================================
# STAGE 3
# WEAK CONCEPT DIAGNOSIS + RE-TEACHING
# ============================================================
# ============================================================

if st.session_state.stage == "review":

    st.divider()


    st.header(
        " Weak Concept Diagnosis"
    )


    if st.session_state.weak_topics:

        for topic in st.session_state.weak_topics:

            topic_score = (

                st.session_state.topic_scores.get(

                    topic,

                    0

                )

            )


            st.warning(

                f" {topic} — "
                f"{topic_score}%"

            )

    else:

        st.info(
            "No specific weak topic was identified."
        )


    # ========================================================
    # RE-TEACHING
    # ========================================================

    st.header(
        " Targeted Re-Teaching"
    )


    # --------------------------------------------------------
    # CREATE REVIEW
    # --------------------------------------------------------

    if not st.session_state.review:

        if st.session_state.learning_mode == "AI":

            with st.spinner(

                "Gemini is preparing targeted re-teaching..."

            ):

                try:

                    review = generate_weak_topic_review(

                        module_text,

                        st.session_state.weak_topics,

                        st.session_state.subject,

                        st.session_state.level

                    )

                except Exception:

                    review = {}


            if not review:

                review = create_local_review(

                    module_text,

                    st.session_state.weak_topics

                )

        else:

            review = create_local_review(

                module_text,

                st.session_state.weak_topics

            )


        st.session_state.review = review


    # --------------------------------------------------------
    # DISPLAY REVIEW
    # --------------------------------------------------------

    review = st.session_state.review


    if review:

        st.subheader(

            review.get(
                "title",
                "Targeted Re-Teaching"
            )

        )


        st.write(

            review.get(
                "intro",
                ""
            )

        )


        for concept in review.get(

            "weak_concepts",

            []

        ):

            st.markdown(

                f"""
                <div class="concept-card">

                <h3>
                 {safe_text(
                    concept.get(
                        "concept",
                        "Concept"
                    )
                )}
                </h3>

                </div>
                """,

                unsafe_allow_html=True

            )


            st.markdown(
                "**Explanation**"
            )


            st.write(

                concept.get(
                    "explanation",
                    ""
                )

            )


            st.markdown(
                "**Example**"
            )


            st.write(

                concept.get(
                    "example",
                    ""
                )

            )


            st.markdown(
                "**Common Mistake**"
            )


            st.write(

                concept.get(
                    "common_mistake",
                    ""
                )

            )


        # ----------------------------------------------------
        # RETAKE
        # ----------------------------------------------------

        st.divider()


        st.subheader(
            " Try Again"
        )


        st.write(

            "Review the weak concepts and retake "
            "the Knowledge Check."
        )


        if st.button(

            " Retake Knowledge Check",

            type="primary",

            use_container_width=True

        ):

            st.session_state.stage = "knowledge_check"

            st.session_state.knowledge_questions = []

            st.session_state.knowledge_submitted = False

            st.session_state.knowledge_score = 0

            st.session_state.review = {}

            st.session_state.weak_topics = []

            st.session_state.topic_scores = {}

            st.rerun()


# ============================================================
# ============================================================
# MODULE COMPLETED
# ============================================================
# ============================================================

if st.session_state.stage == "completed":

    score = st.session_state.knowledge_score

    # ========================================================
    # SAVE MODULE RESULT
    # ========================================================

    if current_module not in st.session_state.completed_modules:
        st.session_state.completed_modules.append(
            current_module
        )

    st.session_state.module_scores[
        current_module
    ] = score

    # ========================================================
    # CONGRATULATIONS PAGE
    # ========================================================

    motivational_lines = [
        (
            "Every concept you understand today becomes a "
            "stronger foundation for tomorrow."
        ),
        (
            "Progress is built one concept, one practice, "
            "and one improvement at a time."
        ),
        (
            "You are not just completing modules — you are "
            "building real knowledge and confidence."
        )
    ]

    current_message = motivational_lines[
        min(current_module, len(motivational_lines) - 1)
    ]

    st.markdown(
        f"""
        <div class="celebration-card">
            <div class="celebration-icon"></div>
            <h1>Congratulations!</h1>
            <h2>{safe_text(get_module_name(current_module))} Completed</h2>
            <p class="celebration-score">{score}%</p>
            <p class="celebration-label">Knowledge Check Score</p>
            <p class="celebration-message">{safe_text(current_message)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(
        (current_module + 1) / total_modules
        if total_modules
        else 0
    )

    st.markdown(
        f"**Learning Progress:** {current_module + 1} / {total_modules} modules completed"
    )

    # --------------------------------------------------------
    # Module performance visualization
    # --------------------------------------------------------

    completed_scores = [
        st.session_state.module_scores.get(i, 0)
        for i in range(total_modules)
        if i in st.session_state.completed_modules
    ]

    if completed_scores:
        st.subheader(" Your Performance So Far")

        performance_df = pd.DataFrame({
            "Module": [
                get_module_name(i)
                for i in range(total_modules)
                if i in st.session_state.completed_modules
            ],
            "Score": completed_scores
        })

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.caption("Module Scores")
            st.bar_chart(
                performance_df.set_index("Module")
            )

        with chart_col2:
            st.caption("Score Progression")
            st.line_chart(
                performance_df.set_index("Module")
            )

    # ========================================================
    # NEXT MODULE
    # ========================================================

    if current_module < total_modules - 1:

        next_module = current_module + 1

        st.divider()

        st.markdown(
            f"""
            <div class="next-module-card">
                <h2> Ready for the Next Step?</h2>
                <p>You have unlocked <b>{safe_text(get_module_name(next_module))}</b>.</p>
                <p>Keep the momentum going and continue your journey toward mastery.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            " Continue to Next Module",
            type="primary",
            use_container_width=True
        ):
            st.session_state.current_module = next_module
            reset_current_module()
            st.rerun()

    # ========================================================
    # ALL MODULES COMPLETED
    # ========================================================

    else:

        st.balloons()

        st.divider()

        st.markdown(
            """
            <div class="celebration-card final-celebration">
                <div class="celebration-icon"></div>
                <h1>Learning Journey Complete!</h1>
                <p>You completed all three learning modules.</p>
                <p>Take a moment to appreciate how far you have come.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(1.0)

        scores = [
            st.session_state.module_scores.get(i, 0)
            for i in range(total_modules)
        ]

        final_score = round(
            sum(scores) / len(scores)
        ) if scores else 0

        metric_col1, metric_col2 = st.columns(2)

        with metric_col1:
            st.metric(
                "Overall Learning Score",
                f"{final_score}%"
            )

        with metric_col2:
            st.metric(
                "Modules Completed",
                f"{total_modules}/{total_modules}"
            )

        final_results = pd.DataFrame({
            "Module": [get_module_name(i) for i in range(total_modules)],
            "Score": scores
        })

        st.subheader(" Final Performance")
        st.bar_chart(
            final_results.set_index("Module")
        )

        st.line_chart(
            final_results.set_index("Module")
        )

        st.markdown(
            """
            <div class="final-message-card">
                <h2> Keep Learning</h2>
                <p>
                Mastery is not a destination. It is the result of continuous
                learning, practice, reflection, and improvement.
                </p>
                <p><b>Your next concept is another opportunity to grow.</b></p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# CONCEPT PERFORMANCE
# ============================================================

if st.session_state.all_topic_scores:

    st.divider()


    st.header(
        " Concept Performance"
    )


    concept_data = pd.DataFrame(

        [

            {

                "Concept": topic,

                "Score": score

            }

            for topic, score

            in st.session_state.all_topic_scores.items()

        ]

    )


    if not concept_data.empty:

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.caption("Concept Score Graph")
            st.bar_chart(
                concept_data.set_index("Concept")
            )

        with chart_col2:
            st.caption("Concept Progress Plot")
            st.line_chart(
                concept_data.set_index("Concept")
            )

        strong_topics = concept_data[
            concept_data["Score"] >= 70
        ]["Concept"].tolist()

        weak_topics = concept_data[
            concept_data["Score"] < 70
        ]["Concept"].tolist()

        if strong_topics:
            st.success(
                " Strong concepts: " + ", ".join(strong_topics)
            )

        if weak_topics:
            st.warning(
                " Concepts needing more practice: " +
                ", ".join(weak_topics)
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()


st.caption(

    "MasteryPath AI • From Confusion to Mastery"

)