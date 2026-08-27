import io
import streamlit as st
import sqlite3
from PyPDF2 import PdfReader
from collections import Counter
import pandas as pd
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from deep_translator import GoogleTranslator
import fitz

st.set_page_config(page_title="AI Research Paper Summarizer", layout="wide")

# -------------------------
# STYLE
# -------------------------
def apply_theme(theme):
    if theme == "Dark":
        st.markdown("""
        <style>
        :root { color-scheme: dark; }
        html, body, [data-testid="stAppViewContainer"], .stApp, .main, section.main,
        .block-container, [data-testid="stSidebar"], .stSidebar {
            background-color: #071b2d !important;
            color: #f8fafc !important;
        }
        [data-testid="stSidebar"], .stSidebar {
            background-color: #071b2d !important;
            border-right: 1px solid rgba(148, 163, 184, 0.2) !important;
        }
        [data-testid="stSidebar"] *, .stSidebar * {
            color: #f8fafc !important;
            background-color: transparent !important;
        }
        header[data-testid="stHeader"] {
            background: transparent !important;
            border-bottom: none !important;
        }
        .app-title {
            color: #f8fafc !important;
        }
        .stApp, .stMarkdown, .stText, p, li, label, h1, h2, h3, h4, h5, h6, div, span,
        .stSelectbox label, .stTextInput label, .stTextArea label {
            color: #f8fafc !important;
        }
        input, textarea, select, .stTextInput > div > div > input, .stTextArea > div > textarea,
        .stSelectbox > div > div > div, .stFileUploader > div,
        [data-baseweb="select"] > div, [data-testid="stFileUploaderDropzone"],
        [data-testid="stForm"], .stForm {
            background-color: #0f172a !important;
            color: #f8fafc !important;
            border: 1px solid #334155 !important;
        }
        .stSelectbox [role="combobox"], .stSelectbox [data-baseweb="select"] {
            background-color: #0f172a !important;
            color: #f8fafc !important;
        }
        .stSelectbox > div > div,
        .stSelectbox > div > div > div,
        .stSelectbox div[role="combobox"],
        .stSelectbox [data-baseweb="select"] > div,
        .stSelectbox [data-baseweb="select"] {
            background-color: #0f172a !important;
            color: #f8fafc !important;
            border-color: #334155 !important;
        }
        ul[role="listbox"],
        div[role="listbox"],
        [data-baseweb="popover"] {
            background-color: #0f172a !important;
            color: #f8fafc !important;
        }
        [role="option"], [role="option"] > div {
            background-color: #0f172a !important;
            color: #f8fafc !important;
        }
        [role="option"][aria-selected="true"] {
            background-color: rgba(59, 130, 246, 0.18) !important;
            color: #f8fafc !important;
        }
        [data-testid="stSidebar"] div[role="radio"] {
            width: 100% !important;
            border-radius: 10px !important;
            padding: 8px 10px !important;
            margin: 4px 0 !important;
            display: flex !important;
            align-items: center !important;
            transition: background 0.2s ease !important;
        }
        [data-testid="stSidebar"] div[role="radio"][aria-checked="true"] {
            background: rgba(59, 130, 246, 0.18) !important;
            box-shadow: inset 0 0 0 1px rgba(96, 165, 250, 0.7) !important;
        }
        [data-testid="stSidebar"] div[role="radio"] > div:first-child,
        [data-testid="stSidebar"] div[role="radio"] > span:first-child {
            border: 2px solid #e2e8f0 !important;
            background: transparent !important;
            width: 14px !important;
            height: 14px !important;
            border-radius: 50% !important;
            margin-right: 10px !important;
            flex-shrink: 0 !important;
        }
        [data-testid="stSidebar"] div[role="radio"][aria-checked="true"] > div:first-child,
        [data-testid="stSidebar"] div[role="radio"][aria-checked="true"] > span:first-child {
            background: #ff4d8d !important;
            border-color: #ff4d8d !important;
            box-shadow: inset 0 0 0 3px #fff !important;
        }
        .sidebar-current-page {
            margin: 10px 0 8px 0 !important;
            padding: 7px 10px !important;
            border-radius: 6px !important;
            background: rgba(148, 163, 184, 0.08) !important;
            border-left: 3px solid #60a5fa !important;
            color: #f8fafc !important;
            font-size: 0.86rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.01em !important;
        }
        .stButton > button, button[kind="primary"], [data-testid="baseButton-primary"] {
            background-color: #2563eb !important;
            color: white !important;
            border: 1px solid #93c5fd !important;
            border-radius: 10px !important;
            box-shadow: 0 0 6px rgba(147, 197, 253, 0.35) !important;
            font-weight: 600 !important;
            opacity: 1 !important;
            visibility: visible !important;
        }
        .stButton > button:hover, button[kind="primary"]:hover, [data-testid="baseButton-primary"]:hover {
            background-color: #3b82f6 !important;
            border-color: #bfdbfe !important;
        }
        .stDataFrame table, .stDataFrame th, .stDataFrame td {
            color: #f8fafc !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        :root { color-scheme: light; }
        html, body, [data-testid="stAppViewContainer"], .stApp, .main, section.main,
        .block-container, [data-testid="stSidebar"], .stSidebar {
            background-color: #f8fafc !important;
            color: #111827 !important;
        }
        [data-testid="stSidebar"], .stSidebar {
            background-color: #eef2ff !important;
            border-right: 1px solid rgba(148, 163, 184, 0.3) !important;
        }
        [data-testid="stSidebar"] *, .stSidebar * {
            color: #111827 !important;
        }
        header[data-testid="stHeader"] {
            background: #ffffff !important;
        }
        .app-title {
            color: #1f4e79 !important;
        }
        .stApp, .stMarkdown, .stText, p, li, label, h1, h2, h3, h4, h5, h6, div, span,
        .stSelectbox label, .stTextInput label, .stTextArea label {
            color: #111827 !important;
        }
        input, textarea, select, .stTextInput > div > div > input, .stTextArea > div > textarea,
        .stSelectbox > div > div > div, .stFileUploader > div,
        [data-baseweb="select"] > div, [data-testid="stFileUploaderDropzone"] {
            background-color: white !important;
            color: #111827 !important;
            border: 1px solid #cbd5e1 !important;
        }
        .stSelectbox [role="combobox"], .stSelectbox [data-baseweb="select"] {
            background-color: white !important;
            color: #111827 !important;
        }
        [data-testid="stSidebar"] div[role="radio"] {
            width: 100% !important;
            border-radius: 10px !important;
            padding: 8px 10px !important;
            margin: 4px 0 !important;
            display: flex !important;
            align-items: center !important;
            transition: background 0.2s ease !important;
        }
        [data-testid="stSidebar"] div[role="radio"][aria-checked="true"] {
            background: rgba(31, 78, 121, 0.12) !important;
            box-shadow: inset 0 0 0 1px rgba(31, 78, 121, 0.6) !important;
        }
        [data-testid="stSidebar"] div[role="radio"] > div:first-child,
        [data-testid="stSidebar"] div[role="radio"] > span:first-child {
            border: 2px solid #475569 !important;
            background: transparent !important;
            width: 14px !important;
            height: 14px !important;
            border-radius: 50% !important;
            margin-right: 10px !important;
            flex-shrink: 0 !important;
        }
        [data-testid="stSidebar"] div[role="radio"][aria-checked="true"] > div:first-child,
        [data-testid="stSidebar"] div[role="radio"][aria-checked="true"] > span:first-child {
            background: #ff4d8d !important;
            border-color: #ff4d8d !important;
            box-shadow: inset 0 0 0 3px #fff !important;
        }
        .sidebar-current-page {
            margin: 10px 0 8px 0 !important;
            padding: 7px 10px !important;
            border-radius: 6px !important;
            background: rgba(148, 163, 184, 0.10) !important;
            border-left: 3px solid #1f4e79 !important;
            color: #111827 !important;
            font-size: 0.86rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.01em !important;
        }
        .stButton > button, button[kind="primary"], [data-testid="baseButton-primary"] {
            background-color: #1f4e79 !important;
            color: white !important;
            border-radius: 10px !important;
            border: 1px solid #1f4e79 !important;
            font-weight: 600 !important;
            opacity: 1 !important;
            visibility: visible !important;
        }
        .stButton > button:hover, button[kind="primary"]:hover, [data-testid="baseButton-primary"]:hover {
            background-color: #173d5e !important;
        }
        .block-container {
            padding-top: 1rem;
        }
        .stDataFrame table, .stDataFrame th, .stDataFrame td {
            color: #111827 !important;
        }
        </style>
        """, unsafe_allow_html=True)


if "theme" not in st.session_state:
    st.session_state.theme = "Light"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "raw_summary" not in st.session_state:
    st.session_state.raw_summary = ""

if "chat_query" not in st.session_state:
    st.session_state.chat_query = ""

if "chat_answer" not in st.session_state:
    st.session_state.chat_answer = ""

if "uploaded_name" not in st.session_state:
    st.session_state.uploaded_name = None

apply_theme(st.session_state.theme)

st.markdown("<h1 class='app-title' style='text-align:center;'>🤖 AI Research Paper Summarizer</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])
with col2:
    theme_choice = st.selectbox("Theme", ["Light", "Dark"], index=0 if st.session_state.theme == "Light" else 1, key="top_theme")
    if theme_choice != st.session_state.theme:
        st.session_state.theme = theme_choice
        apply_theme(st.session_state.theme)

# -------------------------
# DATABASE
# -------------------------
@st.cache_resource
def get_connection():
    conn = sqlite3.connect("users.db", check_same_thread=False)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS login_logs(
    username TEXT
    )
    """)

    conn.execute("INSERT OR IGNORE INTO users VALUES (?,?)", ("admin","admin123"))
    conn.commit()
    return conn

conn = get_connection()
cursor = conn.cursor()

# -------------------------
# TRANSLATION
# -------------------------
def translate_text(text, language):
    if not text:
        return ""

    lang_map = {"English":"en","Tamil":"ta","Hindi":"hi","Malayalam":"ml"}
    if language == "English":
        return text

    try:
        translated = GoogleTranslator(source='auto', target=lang_map[language]).translate(text)
        error_markers = (
            "Error 500",
            "There was an error",
            "That’s an error",
            "That's an error",
            "Server Error",
            "Unable to translate",
        )
        if translated is None:
            return text
        translated_text = str(translated)
        if any(marker in translated_text for marker in error_markers):
            return text
        return translated_text
    except Exception:
        return text

# -------------------------
# STOPWORDS
# -------------------------
stopwords = {"a","an","the","and","or","is","are","was","were","to","of","in","on","for","with","that","this","it","as","by","at","from","be"}

# -------------------------
# FUNCTIONS
# -------------------------
def normalize_text(text):
    if not text:
        return ""
    text = text.replace("\x0c", "\n")
    text = re.sub(r"-\n", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s*\n\s*", "\n", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def trim_title_candidates(line):
    lower = line.lower()
    separators = [
        "corresponding authors", "corresponding author", "department of", "faculty of", "university",
        "institute", "hospital", "centre", "center", "keywords", "abstract", "received",
        "accepted", "published", "digital object identifier", "doi:", "doi ", "email", "www.", "http"
    ]
    for sep in separators:
        idx = lower.find(sep)
        if idx > 20:
            return line[:idx].strip()
    author_match = re.search(r"\s[A-Z]{2,}(?:\s[A-Z]{2,}){1,}", line)
    if author_match and author_match.start() > 20:
        return line[:author_match.start()].strip()
    return line.strip()


def is_author_or_affiliation(line):
    lower = line.lower()
    if len(line.split()) <= 6 and any(name in lower for name in ["university", "institute", "department", "centre", "center", "school", "college", "laboratory", "lab", "hospital", "company", "inc", "ltd", "corporation"]):
        return True
    if re.search(r"\b(?:and|,|;|&|\band\b)\s+[A-Z][a-z]", line) and len(line.split()) <= 10:
        return True
    if re.match(r"^[A-Z][a-z]+\s+[A-Z][a-z]+", line) and len(line.split()) <= 8:
        return True
    return False


def is_bad_title_line(line):
    lower = line.lower()
    bad_prefixes = (
        "abstract", "introduction", "conclusion", "references", "keywords",
        "figure", "table", "appendix", "acknowledgement", "acknowledgments",
        "received", "accepted", "published", "doi", "corresponding author",
        "email", "www.", "http",
    )
    bad_terms = re.compile(r"\b(received|accepted|published|submission|version|arxiv|journal|page|article|corresponding|department|university|institute|hospital|centre|center)\b", re.I)
    if any(lower.startswith(prefix) for prefix in bad_prefixes):
        return True
    if bad_terms.search(lower):
        return True
    if any(tag in lower for tag in ["doi:", "digital object identifier", "email", "@"]):
        return True
    words = line.split()
    if len(words) < 2 or len(words) > 80:
        return True
    if sum(1 for ch in line[:20] if ch.isdigit()) > 0 and len(words) <= 6:
        return True
    return False


def build_title_from_lines(lines):
    for idx, line in enumerate(lines):
        if is_bad_title_line(line):
            continue
        candidate = trim_title_candidates(line)
        if len(candidate.split()) < 3:
            continue
        full_title = candidate
        for next_line in lines[idx + 1: idx + 6]:
            if is_bad_title_line(next_line) or is_author_or_affiliation(next_line):
                break
            next_words = next_line.split()
            if len(next_words) < 2 or len(next_words) > 25:
                break
            if next_line.strip().startswith("("):
                break
            if re.search(r"\b(author|authors|et al|corresponding|university|institute|department|hospital|research|laboratory|lab|centre|center|college|school)\b", next_line, re.I):
                break
            full_title += " " + trim_title_candidates(next_line)
        if len(full_title.split()) >= 4:
            return full_title.strip()
    return None


def extract_title_from_pdf(pdf_file):
    def is_bad_title_line(line):
        lower = line.lower()
        bad_prefixes = (
            "abstract", "introduction", "conclusion", "references", "keywords",
            "figure", "table", "appendix", "acknowledgement", "acknowledgments",
            "received", "accepted", "published", "doi", "corresponding author",
            "email", "www.", "http",
        )
        bad_terms = re.compile(r"\b(received|accepted|published|submission|version|arxiv|journal|page|article|corresponding|department|university|institute|hospital|centre|center)\b", re.I)
        if any(lower.startswith(prefix) for prefix in bad_prefixes):
            return True
        if bad_terms.search(lower):
            return True
        if any(tag in lower for tag in ["doi:", "digital object identifier", "email", "@"]):
            return True
        words = line.split()
        if len(words) < 3 or len(words) > 60:
            return True
        if sum(1 for ch in line[:20] if ch.isdigit()) > 0 and len(words) <= 6:
            return True
        return False

    try:
        if hasattr(pdf_file, "getvalue"):
            pdf_bytes = pdf_file.getvalue()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            metadata_title = (doc.metadata or {}).get("title", "")
            if metadata_title and len(metadata_title.split()) >= 3:
                doc.close()
                return trim_title_candidates(metadata_title.strip())
            if len(doc) > 0:
                first_page = doc[0]
                page_dict = first_page.get_text("dict")
                block_lines = []
                for block in page_dict.get("blocks", []):
                    for line in block.get("lines", []):
                        text = " ".join(span.get("text", "") for span in line.get("spans", [])).strip()
                        if text:
                            block_lines.append(text)

                candidate = build_title_from_lines(block_lines)
                if candidate:
                    doc.close()
                    return trim_title_candidates(candidate)

                page_text = first_page.get_text("text") or ""
                raw_lines = [line.strip() for line in page_text.splitlines() if line.strip()]
                candidate = build_title_from_lines(raw_lines)
                if candidate:
                    doc.close()
                    return trim_title_candidates(candidate)
    except Exception:
        pass
    return None


def extract_publication_year(text):
    if not text:
        return None
    years = re.findall(r"\b(?:19\d{2}|20\d{2})\b", text)
    if years:
        # prefer year after received/accepted/published markers
        match = re.search(r"(?:received|accepted|published|date of publication|publication date)[:\s]+(19\d{2}|20\d{2})", text, re.I)
        if match:
            return match.group(1)
        return years[0]
    return None


def extract_text(pdf):
    text_parts = []

    try:
        if hasattr(pdf, "getvalue"):
            pdf_bytes = pdf.getvalue()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            for page in doc:
                page_text = page.get_text("text")
                if page_text and page_text.strip():
                    text_parts.append(page_text.strip())
            doc.close()
    except Exception:
        text_parts = []

    if not text_parts:
        try:
            if hasattr(pdf, "getvalue"):
                reader = PdfReader(io.BytesIO(pdf.getvalue()))
                for page in reader.pages:
                    page_text = page.extract_text() or ""
                    if page_text and page_text.strip():
                        text_parts.append(page_text.strip())
        except Exception:
            text_parts = []

    if not text_parts:
        return ""

    return normalize_text("\n\n".join(text_parts))


def get_title(text, pdf_file=None):
    if not text:
        return "Title not found"

    if pdf_file is not None:
        pdf_title = extract_title_from_pdf(pdf_file)
        if pdf_title:
            return pdf_title

    bad_prefixes = (
        "abstract", "introduction", "conclusion", "references", "keywords",
        "figure", "table", "appendix", "acknowledgement", "acknowledgments",
        "received", "accepted", "published", "doi", "corresponding author",
        "email", "www.", "http",
    )
    bad_terms = re.compile(r"\b(received|accepted|published|submission|version|arxiv|journal|page|article|corresponding|department|university|institute|hospital|centre|center)\b", re.I)

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for idx, line in enumerate(lines[:80]):
        lower = line.lower()
        if any(lower.startswith(prefix) for prefix in bad_prefixes):
            continue
        if bad_terms.search(lower):
            continue
        if any(tag in lower for tag in ["doi:", "digital object identifier", "email", "@"]):
            continue
        words = line.split()
        if len(words) < 4 or len(words) > 40:
            continue
        if sum(1 for ch in line[:20] if ch.isdigit()) > 0 and len(words) <= 6:
            continue
        candidate = trim_title_candidates(line)
        if candidate:
            full_title = candidate
            for next_line in lines[idx+1: idx+3]:
                next_lower = next_line.lower()
                if any(next_lower.startswith(prefix) for prefix in bad_prefixes):
                    break
                if bad_terms.search(next_lower):
                    break
                if any(tag in next_lower for tag in ["doi:", "digital object identifier", "email", "@"]):
                    break
                if is_author_or_affiliation(next_line):
                    break
                next_words = next_line.split()
                if len(next_words) < 3 or len(next_words) > 15:
                    break
                full_title += " " + trim_title_candidates(next_line)
            return full_title.strip()

    return lines[0] if lines else "Title not found"


def generate_summary(text):
    cleaned = normalize_text(text)
    if not cleaned:
        return "No meaningful content found."

    sentences = re.split(r'(?<=[.!?])\s+', cleaned)
    sentences = [s.strip() for s in sentences if len(s.split()) >= 8]

    if not sentences:
        sentences = [s.strip() for s in re.split(r'\n+', cleaned) if len(s.split()) >= 8]

    if not sentences:
        words = cleaned.split()
        if not words:
            return "No meaningful content found."
        return " ".join(words[:100]) + ("..." if len(words) > 100 else "")

    selected = sentences[:5]
    return " ".join(selected)

def extract_keywords(text):
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    words = [w for w in words if w not in stopwords]
    return Counter(words).most_common(10)

def word_frequency(text):
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    words = [w for w in words if w not in stopwords]
    return pd.DataFrame(Counter(words).most_common(10), columns=["Word","Count"])

def show_wordcloud(text):
    wc = WordCloud(width=800, height=400, background_color="white").generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wc)
    ax.axis("off")
    st.pyplot(fig)

def extract_abstract(text):
    cleaned = normalize_text(text)
    if not cleaned:
        return "No abstract found."

    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
    for i, line in enumerate(lines):
        if line.lower().startswith("abstract"):
            abstract_lines = []
            for nxt in lines[i + 1: i + 8]:
                if nxt.lower().startswith(("keywords", "introduction", "conclusion", "references")):
                    break
                abstract_lines.append(nxt)
            if abstract_lines:
                return " ".join(abstract_lines[:6])

    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    for sentence in sentences:
        if len(sentence.split()) >= 8:
            return sentence.strip()

    return cleaned[:500]


def chat_answer(question, text, pdf_file=None):
    cleaned = normalize_text(text)
    q = question.strip().lower()

    if not q:
        return "Please ask a question."

    if re.search(r"\b(title|paper title|name of paper|paper name)\b", q):
        if pdf_file is not None:
            return get_title(cleaned, pdf_file)
        return get_title(cleaned)

    if re.search(r"\b(publication year|year|published in|published)\b", q):
        year = extract_publication_year(cleaned)
        return year or "Publication year not found."

    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", cleaned) if s.strip()]

    for sentence in sentences:
        if q in sentence.lower():
            words = sentence.split()
            if len(words) > 30:
                return " ".join(words[:25]) + "..."
            return sentence

    q_words = [word for word in re.findall(r"[a-zA-Z]{3,}", q) if len(word) > 2]
    matches = []
    for sentence in sentences:
        sentence_lower = sentence.lower()
        if any(word in sentence_lower for word in q_words):
            matches.append(sentence)
    if matches:
        best = min(matches, key=lambda s: len(s.split()))
        words = best.split()
        if len(words) > 30:
            return " ".join(words[:25]) + "..."
        return best

    return "I could not find a direct answer in the document."

# -------------------------
# ADMIN VIEW USERS (FIXED)
# -------------------------
def view_logged_users():
    st.subheader("👀 Users Accessing App")

    # only non-admin count
    cursor.execute("SELECT COUNT(DISTINCT username) FROM login_logs WHERE username != 'admin'")
    st.metric("Total Users", cursor.fetchone()[0])

    # only unique non-admin users
    cursor.execute("""
        SELECT DISTINCT username 
        FROM login_logs 
        WHERE username != 'admin'
    """)

    users = cursor.fetchall()

    for u in users:
        st.write("•", u[0])

# -------------------------
# AUTH
# -------------------------
def register():
    st.subheader("Register")
    user = st.text_input("Username").strip().lower()
    pwd = st.text_input("Password", type="password").strip()

    if st.button("Register"):
        cursor.execute("SELECT * FROM users WHERE username=?", (user,))
        if cursor.fetchone():
            st.error("User already exists")
        else:
            cursor.execute("INSERT INTO users VALUES (?,?)",(user,pwd))
            conn.commit()
            st.success("Registered successfully")

def login():
    st.subheader("Login")
    user = st.text_input("Username").strip().lower()
    pwd = st.text_input("Password", type="password").strip()

    if st.button("Login"):
        cursor.execute("SELECT * FROM users WHERE username=?",(user,))
        data = cursor.fetchone()

        if not data:
            st.error("User not found")
        elif data[1] != pwd:
            st.error("Wrong password")
        else:
            st.session_state.logged_in = True
            st.session_state.username = user

            # log login
            cursor.execute("INSERT INTO login_logs VALUES (?)", (user,))
            conn.commit()

            st.success("Login successful")

def forgot_password():
    st.subheader("Forgot Password")
    user = st.text_input("Enter Username").strip().lower()

    if st.button("Get Password"):
        cursor.execute("SELECT password FROM users WHERE username=?", (user,))
        data = cursor.fetchone()

        if data:
            st.success(f"Your password is: {data[0]}")
        else:
            st.error("User not found")

# -------------------------
# DASHBOARD
# -------------------------
def dashboard():

    st.sidebar.success("Logged in as " + st.session_state.username)

    if "current_sidebar_page" not in st.session_state:
        st.session_state.current_sidebar_page = "Summarizer"

    language = st.selectbox("🌐 Select Language",
                           ["English","Tamil","Hindi","Malayalam"])

    if st.session_state.username == "admin":
        menu_options = ["Users Activity","Summarizer","Insights","Keywords","Frequency","Word Cloud","Chat"]
    else:
        menu_options = ["Summarizer","Insights","Keywords","Frequency","Word Cloud","Chat"]

    menu = st.sidebar.radio("Menu", menu_options, index=menu_options.index(st.session_state.current_sidebar_page) if st.session_state.current_sidebar_page in menu_options else 0)
    st.session_state.current_sidebar_page = menu
    st.sidebar.markdown(f"<div class='sidebar-current-page'>Current page: {menu}</div>", unsafe_allow_html=True)

    if menu == "Users Activity":
        view_logged_users()
        return

    uploaded = st.file_uploader("Upload Research Paper PDF", type="pdf")
    text = ""

    if uploaded:
        current_name = uploaded.name
        if st.session_state.uploaded_name != current_name:
            st.session_state.uploaded_name = current_name
            st.session_state.summary = ""
            st.session_state.chat_query = ""
            st.session_state.chat_answer = ""

        try:
            reader = PdfReader(io.BytesIO(uploaded.getvalue()))
            st.write("Total Pages:", len(reader.pages))
        except Exception:
            st.write("Total Pages:", "Unknown")

        text = extract_text(uploaded)

        if text.strip():
            st.subheader("Paper Title")
            paper_title = get_title(text, uploaded)
            st.write(translate_text(paper_title, language))
            publication_year = extract_publication_year(text)
            if publication_year:
                st.markdown(f"**Publication Year:** {publication_year}")
        else:
            st.warning("The uploaded file could not be read as a readable PDF. Please upload a standard research paper PDF.")
    else:
        st.info("Upload a research paper")

    if menu == "Summarizer":
        if uploaded and st.button("Generate Summary"):
            st.session_state.raw_summary = generate_summary(text)
            st.session_state.summary = translate_text(st.session_state.raw_summary, language)
        elif st.session_state.raw_summary:
            st.session_state.summary = translate_text(st.session_state.raw_summary, language)

        if uploaded:
            st.text_area("Summary", st.session_state.summary, height=200)
            if st.session_state.summary:
                st.download_button("Download Summary", st.session_state.summary)

    elif menu == "Insights":
        if uploaded:
            st.metric("Total Words", len(text.split()))
            st.metric("Total Sentences", len(text.split(".")))

    elif menu == "Keywords":
        if uploaded:
            df = pd.DataFrame(extract_keywords(text), columns=["Keyword","Frequency"])
            st.table(df)
            st.bar_chart(df.set_index("Keyword"))

    elif menu == "Frequency":
        if uploaded:
            df = word_frequency(text)
            st.bar_chart(df.set_index("Word"))

    elif menu == "Word Cloud":
        if uploaded:
            show_wordcloud(text)

    elif menu == "Chat":
        if uploaded:
            if "chat_query" not in st.session_state:
                st.session_state.chat_query = ""
            if "chat_answer" not in st.session_state:
                st.session_state.chat_answer = ""

            q = st.text_input("Ask question", key="chat_query")
            if st.button("Get Answer", key="chat_button"):
                if q.strip():
                    st.session_state.chat_answer = translate_text(chat_answer(q, text, uploaded), language)
                else:
                    st.session_state.chat_answer = "Please enter a question."

            if st.session_state.chat_answer:
                st.text_area("Answer", st.session_state.chat_answer, height=150)
            elif q:
                st.info("Click Get Answer to receive a response.")
        else:
            st.info("Upload a research paper to enable chat")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# -------------------------
# MAIN
# -------------------------
st.sidebar.title("📌 Navigation")

if "current_route" not in st.session_state:
    st.session_state.current_route = "Login"

page = st.sidebar.radio("Go to", ["Login","Register","Forgot Password"], index=["Login","Register","Forgot Password"].index(st.session_state.current_route))
st.session_state.current_route = page
st.sidebar.markdown(f"<div class='sidebar-current-page'>Current page: {page}</div>", unsafe_allow_html=True)

if st.session_state.logged_in:
    dashboard()
else:
    if page == "Login":
        login()
    elif page == "Register":
        register()
    else:
        forgot_password()