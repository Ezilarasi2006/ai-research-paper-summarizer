# 📚 AI Research Paper Summarizer

An AI-powered web application that helps students, researchers, and professionals quickly understand research papers. Users can upload PDF files, generate summaries, extract keywords, visualize word frequency, create word clouds, and ask questions related to the uploaded document.

---

## 🚀 Features

- 📄 Upload research papers in PDF format
- 📝 Automatic text extraction from PDFs
- 🤖 AI-generated research paper summaries
- 🔑 Keyword extraction
- ☁️ Word Cloud generation
- 📊 Word Frequency Analysis
- 💬 Ask questions about the uploaded paper
- 🌐 Translate summaries into multiple languages
- 👤 User Registration and Login
- 🔒 Password Recovery using Security Questions
- 🎨 Light and Dark Theme Support

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- FastAPI
- Python

### Database
- SQLite

### Python Libraries
- PyMuPDF (fitz)
- PyPDF2
- Pandas
- Matplotlib
- WordCloud
- Deep Translator
- Requests

---

## 📂 Project Structure

```
ai_research_paper_summarizer/
│
├── app.py                 # Streamlit Frontend
├── backend_api.py         # FastAPI Backend
├── requirements.txt
├── users.db               # SQLite Database
├── README.md
├── LICENSE
│
└── docs/
    ├── requirements.md
    ├── sprint_plan.md
    └── user_stories.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Ezilarasi2006/ai-research-paper-summarizer.git
```

### 2. Navigate to the Project Folder

```bash
cd ai-research-paper-summarizer
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Backend

Start the FastAPI server:

```bash
py -m uvicorn backend_api:app --reload
```

The backend will run at:

```
http://127.0.0.1:8000
```

---

## ▶️ Run the Frontend

Start the Streamlit application:

```bash
py -m streamlit run app.py
```

The application will automatically open in your default web browser.

---

## 📖 How to Use

1. Register a new account or log in.
2. Upload a research paper in PDF format.
3. The system extracts the text automatically.
4. View the generated summary.
5. Extract important keywords.
6. Generate a Word Cloud.
7. Analyze word frequency.
8. Ask questions related to the uploaded paper.
9. Translate the summary into your preferred language.

---

## 📦 Requirements

Install all required packages:

```bash
pip install -r requirements.txt
```

---

## 🎯 Project Objectives

- Reduce the time required to understand lengthy research papers.
- Generate concise and meaningful summaries.
- Improve research productivity.
- Provide an interactive question-answering experience.
- Support multilingual understanding of research papers.

---

## 🔮 Future Enhancements

- Multiple PDF upload support
- AI-powered semantic search
- Research paper recommendations
- Export summaries as PDF
- Cloud deployment
- Advanced Large Language Model (LLM) integration

---

## 📸 Screenshots

<img width="929" height="425" alt="image" src="https://github.com/user-attachments/assets/d55c473b-b4a2-4d23-89b9-e5c6a02523cc" />
<img width="922" height="410" alt="image" src="https://github.com/user-attachments/assets/f1bcb6b4-d95b-4500-aba9-bebde6079ef9" />
<img width="928" height="422" alt="image" src="https://github.com/user-attachments/assets/edff4596-ef34-40dc-ad38-ae3edba4825c" />



---

## 📄 License

This project is licensed under the MIT License.



