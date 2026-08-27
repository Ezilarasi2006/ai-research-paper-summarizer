# 📚 AI Research Paper Summarizer

An interactive web application that helps students and researchers quickly understand research papers by uploading and analyzing PDF documents.

## 🚀 Features

* 📄 PDF text extraction
* 📝 Research paper summarization
* 🔑 Keyword extraction
* 📊 Word frequency analysis
* ☁️ Word Cloud generation
* 💬 Question & Answer
* 🌐 Multilingual translation
* 👤 User registration & login
* 🔒 Password recovery
* 🎨 Light/Dark themes

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** FastAPI, Python
* **Database:** SQLite
* **Libraries:** PyMuPDF, PyPDF2, Pandas, Matplotlib, WordCloud, Deep Translator, Requests

## 📂 Project Structure

```text
ai-research-paper-summarizer/
├── app.py
├── backend_api.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── docs/
    ├── requirements.md
    ├── sprint_plan.md
    └── user_stories.md
```

> `users.db` and `__pycache__` are generated locally and excluded from Git.

## ⚙️ Installation

```bash
git clone https://github.com/Ezilarasi2006/ai-research-paper-summarizer.git
cd ai-research-paper-summarizer
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## ▶️ Run the Project

### Backend

```bash
py -m uvicorn backend_api:app --reload
```

### Frontend

```bash
py -m streamlit run app.py
```

## 📖 Usage

1. Register or Login
2. Upload a research paper PDF
3. Extract and analyze the paper
4. Generate a summary
5. View keywords and word cloud
6. Ask questions about the paper
7. Translate the summary

## screenshots
<img width="933" height="411" alt="image" src="https://github.com/user-attachments/assets/547fbead-d775-4b8c-a725-0f37cc7db767" />
<img width="941" height="446" alt="image" src="https://github.com/user-attachments/assets/22bd51ff-93c2-4d64-b79b-9a347f1cf3cd" />


## 🔮 Future Enhancements

* Multiple PDF support
* LLM-based summarization
* Semantic search
* PDF summary export
* Cloud deployment
* Research paper recommendations

## 👩‍💻 Author

**Ezilarasi2006**

## 📄 License

MIT License
