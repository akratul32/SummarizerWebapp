
---

## 🦜 Smart Summarizer

**Smart Summarizer** is a Streamlit-based web app that lets you instantly summarize content from multiple sources using Groq’s blazing-fast LLMs (LLaMA 3). Whether you're analyzing a YouTube video, PDF, Word document, or a web article, this app extracts the core ideas and presents them in a concise, user-friendly format.

---

### 🔍 Features

* 🎥 **YouTube Video Summarization** – Extracts transcripts using a custom loader and summarizes them with LLaMA 3.
* 🌐 **Web Page Summarization** – Supports dynamic scraping and text summarization for any URL.
* 📄 **PDF & Word Document Summarization** – Upload `.pdf` or `.docx` files for instant summarization.
* 💬 **Custom Prompt Template** – Tailored for extracting summaries and key takeaways.
* 🎨 **Beautiful UI** – Stylish Streamlit interface with gradient background, collapsible sections, and emoji-enhanced labels.
* 📥 **Download Summary** – Save the final output as a `.txt` file with one click.
* 🚀 **Powered by Groq's LLaMA 3** – Fast, low-latency inference using `langchain_groq`.

---

### 📦 Tech Stack

* **Frontend/UI**: Streamlit
* **LLM Backend**: LangChain + Groq API (LLaMA 3)
* **Parsing & Loaders**: LangChain community loaders, `youtube-transcript-api`, PyPDF2, docx2txt
* **Python Libraries**: `langchain`, `streamlit`, `docx2txt`, `validators`, `PyPDF2`, `youtube-transcript-api`

---

### 🚀 How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/smart-summarizer.git
   cd smart-summarizer
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Add your **Groq API Key** in the sidebar.

4. Run the app:

   ```bash
   streamlit run app.py
   ```

---

### 📂 Folder Structure

```
smart-summarizer/
├── app.py                      # Main Streamlit web app
├── youtube_loader.py          # Custom YouTube transcript loader
├── requirements.txt           # Python dependencies
└── README.md                  # Project description
```

---

### 📌 To-Do / Future Enhancements

* Add PDF download option for summaries
* Enable multilingual summarization
* Integrate export to Google Sheets
* Add audio/video upload support (via Whisper or Speech-to-Text)

---

### 📄 License

MIT License. Feel free to fork, remix, and improve!

---

