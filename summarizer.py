from transformers import pipeline
from pdfminer.high_level import extract_text

# Load summarizer only once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_text_from_pdf(path):
    return extract_text(path)

def summarize_text(text):
    # HuggingFace models have input limits (~1024-4096 tokens), so chunk
    max_chunk = 1000
    text_chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
    summary = ""

    for chunk in text_chunks:
        result = summarizer(chunk, max_length=120, min_length=30, do_sample=False)
        summary += result[0]['summary_text'] + " "

    return summary.strip()
