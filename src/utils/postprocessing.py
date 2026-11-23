import re

def format_answer(text, answer_type, language):
    text = text.strip()
    if answer_type == "open":
        return text
    normalized = re.sub(r"[.!。,;:]+$", "", text).strip().casefold()
    first_word = normalized.split()[0] if normalized else ""
    if first_word in {"yes", "có"}:
        return "Có" if language == "vi" else "Yes"
    if first_word in {"no", "không"} and not normalized.startswith("không đủ"):
        return "Không" if language == "vi" else "No"
    return "Không đủ thông tin" if language == "vi" else "Insufficient information"