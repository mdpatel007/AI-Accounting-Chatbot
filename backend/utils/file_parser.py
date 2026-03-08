from fastapi import UploadFile

def extract_text_from_txt(file) -> str:
    """
    Extract text from TXT or Markdown files.
    """
    try:
        content = file.read().decode("utf-8")
        return content.strip()
    except Exception as e:
        print("File parse error:", e)
        return ""