import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import requests
from bs4 import BeautifulSoup
from collections import Counter
import pdfplumber

def summarize_text(text, ratio=0.2):
    """Summarizes the given text based on frequency analysis."""
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    
    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in STOP_WORDS and word.text.lower() not in punctuation:
            word_frequencies[word.text] = word_frequencies.get(word.text, 0) + 1

    max_frequency = max(word_frequencies.values(), default=1)
    for word in word_frequencies:
        word_frequencies[word] /= max_frequency

    sentence_scores = {}
    for sent in doc.sents:
        for word in sent:
            if word.text.lower() in word_frequencies:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word.text.lower()]

    select_length = max(1, int(len(list(doc.sents)) * ratio))  # Ensure at least 1 sentence
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    
    return " ".join([sent.text for sent in summary])

def scrape_wikipedia(keywords):
    """Fetches and summarizes Wikipedia content for given keywords."""
    text_output = ""
    for keyword in keywords:
        url = f"https://en.wikipedia.org/wiki/{keyword}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        text_output += f"\n📖 Wikipedia summary for '{keyword}':\n"

        content = soup.find(id="content")
        if not content:
            text_output += "Content not found.\n"
            continue

        text = " ".join(p.text for p in content.find_all("p")[:3])  # First 3 paragraphs
        text_output += summarize_text(text, ratio=0.3) + "\n"
        text_output += f"\n🔗 Read more: {url}\n"
    
    return text_output

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def main():
    print("\n📌 Welcome to the Text Summarizer 📌\n")
    print("1️⃣ Summarize Text")
    print("2️⃣ Summarize a PDF")
    print("3️⃣ Scrape Wikipedia")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    if choice == "1":
        text = input("\nEnter or paste the text to summarize:\n")
        summary = summarize_text(text)
        print("\n📄 **Summary:**\n", summary)
    
    elif choice == "2":
        pdf_path = input("\nEnter the path to the PDF file: ").strip()
        try:
            pdf_text = extract_text_from_pdf(pdf_path)
            if not pdf_text:
                print("⚠️ No text found in the PDF.")
            else:
                summary = summarize_text(pdf_text)
                print("\n📄 **PDF Summary:**\n", summary)
        except Exception as e:
            print(f"❌ Error processing PDF: {e}")
    
    elif choice == "3":
        keywords = input("\nEnter Wikipedia search terms (comma-separated): ").split(',')
        keywords = [kw.strip() for kw in keywords]
        print("\nFetching Wikipedia summaries... 📚")
        print(scrape_wikipedia(keywords))
    
    else:
        print("⚠️ Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
