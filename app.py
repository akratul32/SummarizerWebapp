import os
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
os.environ["KMP_DUPLICATE_LIB_OK"] = "True"

import streamlit as st
import validators
import tempfile
import tiktoken

from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    UnstructuredURLLoader,
    PyPDFLoader,
    Docx2txtLoader,
)

from langchain_openai import ChatOpenAI
from youtube_loader import CustomYouTubeTranscriptLoader

st.set_page_config(page_title="🧠 Smart Summarizer", page_icon="📖", layout="wide")

st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #e0f7fa, #e1f5fe);
            color: #000000;
        }
        .stButton button {
            background-color: #4caf50;
            color: white;
            border-radius: 10px;
            font-weight: bold;
        }
        .stTextInput>div>div>input {
            background-color: #f0f0f0;
        }
        .stRadio > div {
            padding: 10px;
            background-color: #ffffff44;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🧠 Smart Summarizer")
st.markdown("#### Instantly summarize YouTube videos, PDFs, Word docs, or web pages using GPT-4o")

with st.sidebar:
    st.header("🔐 API & Input")
    openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")
    st.markdown("---")
    st.header("📂 Choose Source")
    model_name = st.selectbox("🧠 Choose OpenAI Model", ["gpt-4o", "gpt-4", "gpt-3.5-turbo"])

source_type = st.radio(
    "Select the type of content to summarize:",
    ("YouTube Video", "Web Page", "PDF File", "Word Document"),
    horizontal=True
)

input_data = None
uploaded_file = None

if source_type in ["YouTube Video", "Web Page"]:
    input_data = st.text_input(f"🔗 Enter {source_type} URL")

if source_type in ["PDF File", "Word Document"]:
    uploaded_file = st.file_uploader(f"📁 Upload your {source_type}", type=["pdf", "docx"])

summary_prompt = PromptTemplate.from_template(
    """
    You are a helpful assistant. Your goal is to help the user understand the content by:
    1. Providing a clear and informative summary.
    2. Including key bullet points on major topics discussed, important facts, and takeaways.

    Content: {text}
    """
)

def truncate_to_token_limit(text, max_tokens=3000):
    encoding = tiktoken.encoding_for_model("gpt-4")
    tokens = encoding.encode(text)
    truncated_tokens = tokens[:max_tokens]
    return encoding.decode(truncated_tokens)

if st.button("✨ Summarize Now"):
    if not openai_api_key.strip():
        st.error("Please enter your OpenAI API key.")

    elif source_type in ["YouTube Video", "Web Page"] and not input_data.strip():
        st.error("Enter a valid URL.")

    elif source_type in ["YouTube Video", "Web Page"] and not validators.url(input_data):
        st.error("Invalid URL format.")

    elif source_type in ["PDF File", "Word Document"] and not uploaded_file:
        st.error("Please upload a file.")

    else:
        try:
            st.info("Initializing LLM and extracting content...")
            progress_bar = st.progress(10)

            llm = ChatOpenAI(
                model=model_name,
                api_key=openai_api_key,
                temperature=0
            )
            progress_bar.progress(20)

            if source_type == "YouTube Video":
                loader = CustomYouTubeTranscriptLoader(input_data)
                docs = loader.load()

            elif source_type == "Web Page":
                loader = UnstructuredURLLoader(
                    urls=[input_data],
                    ssl_verify=False,
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                docs = loader.load()

            elif source_type == "PDF File":
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_file_path = tmp_file.name
                loader = PyPDFLoader(tmp_file_path)
                docs = loader.load()
                os.unlink(tmp_file_path)

            elif source_type == "Word Document":
                with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_file_path = tmp_file.name
                loader = Docx2txtLoader(tmp_file_path)
                docs = loader.load()
                os.unlink(tmp_file_path)

            progress_bar.progress(40)

            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            split_docs = splitter.split_documents(docs)

            for doc in split_docs:
                doc.page_content = truncate_to_token_limit(doc.page_content, max_tokens=3000)

            st.markdown("### 🔍 Input Chunks")
            for i, doc in enumerate(split_docs):
                with st.expander(f"Chunk {i+1}"):
                    st.markdown(doc.page_content)

            try:
                chain = load_summarize_chain(
                    llm=llm,
                    chain_type="map_reduce",
                    map_prompt=summary_prompt,
                    combine_prompt=summary_prompt,
                    return_intermediate_steps=False,
                    verbose=False
                )
                progress_bar.progress(70)
                result = chain.invoke(split_docs)
                progress_bar.progress(100)
            except Exception:
                chain = load_summarize_chain(
                    llm=llm,
                    chain_type="stuff",
                    prompt=summary_prompt
                )
                result = chain.invoke(split_docs[:2])

            st.success("✅ Summary generated!")

            if isinstance(result, dict) and "output_text" in result:
                st.markdown("### 📋 Final Summary")
                summary_text = result["output_text"]
                st.markdown(
                    f"<div style='background-color:#f9f9f9;padding:15px;border-radius:10px'>{summary_text}</div>",
                    unsafe_allow_html=True
                )

                st.download_button(
                    label="📅 Download Summary as .txt",
                    data=summary_text,
                    file_name="summary.txt",
                    mime="text/plain"
                )

            else:
                st.markdown("### 📋 Summary")
                st.write(result)

        except Exception as e:
            st.error("⚠️ Something went wrong during processing.")
            st.exception(e)
