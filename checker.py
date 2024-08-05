import re
import tkinter as tk
from tkinter import scrolledtext, filedialog
from nltk.corpus import words
import nltk
import language_tool_python
import docx
import fitz  # PyMuPDF

try:
    nltk.download('words')
except Exception as e:
    print(f"NLTK Download Error: {e}")

try:
    tool = language_tool_python.LanguageTool('en-US')
except language_tool_python.ServerException as e:
    print(f"LanguageTool Initialization Error: {e}")

def checkSpelling(text):
    wordList = set(words.words())
    misspelled = []
    for word in re.findall(r'\b\w+\b', text):
        if word.lower() not in wordList:
            misspelled.append(word)
    return misspelled

def checkGrammar(text):
    matches = tool.check(text)
    return matches

def checkText():
    text = textArea.get("1.0", tk.END)
    spellingErrors = checkSpelling(text)
    grammarErrors = checkGrammar(text)

    #total_errors = len(spellingErrors) + len(grammarErrors)

    result = "Spelling Errors:\n"
    if spellingErrors:
        result += ", ".join(spellingErrors)
    else:
        result += "None"

    result += "\n\nGrammar Errors:\n"
    if grammarErrors:
        for match in grammarErrors:
            result += f"{match.context} -> {match.message}\n"
    else:
        result += "None"

    #result += f"\n\nTotal Errors: {total_errors}"

    resultArea.config(state=tk.NORMAL)
    resultArea.delete("1.0", tk.END)
    resultArea.insert(tk.END, result)
    resultArea.config(state=tk.DISABLED)

def uploadFile():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("Word documents", "*.docx"), ("PDF files", "*.pdf")])
    if file_path:
        if file_path.endswith(".txt"):
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            text = '\n'.join([para.text for para in doc.paragraphs])
        elif file_path.endswith(".pdf"):
            pdf_document = fitz.open(file_path)
            text = ""
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                text += page.get_text()

        textArea.delete("1.0", tk.END)
        textArea.insert(tk.END, text)

root = tk.Tk()
root.title("Spelling and Grammar Checker")

textArea = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15)
textArea.pack(pady=10)

uploadButton = tk.Button(root, text="Upload", command=uploadFile)
uploadButton.pack(pady=5)

checkButton = tk.Button(root, text="Check", command=checkText)
checkButton.pack(pady=5)

resultArea = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15, state=tk.DISABLED)
resultArea.pack(pady=10)

root.mainloop()