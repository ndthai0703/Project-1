import re

def format_answer(text,answer_type,language):
    text=text.strip()
    if answer_type=="open": return text
    normalized=re.sub(r"[.!。]+$","",text).strip().casefold()
    # Strict closed output: never infer yes/no from a longer ambiguous explanation.
    yes={"yes","có"}; no={"no","không"}
    if normalized in yes: return "Có" if language=="vi" else "Yes"
    if normalized in no: return "Không" if language=="vi" else "No"
    return "Không đủ thông tin" if language=="vi" else "Insufficient information"
