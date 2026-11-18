import re
def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()
def tokens(text: str):
    return re.findall(r"[a-z0-9₹%]+", normalize(text))
