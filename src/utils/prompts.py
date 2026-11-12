def make_prompt(question, task="vqa", language="vi", max_chars=1500):
    if task not in ("vqa","caption"): raise ValueError("task: vqa/caption")
    if task=="vqa" and (not isinstance(question,str) or not question.strip()):
        raise ValueError("Vui lòng nhập câu hỏi")
    if len(question)>max_chars: raise ValueError("Câu hỏi quá dài")
    if language=="vi":
        instruction=("Đây là thử nghiệm hỏi đáp ảnh y khoa phục vụ học tập. "
          "Trả lời ngắn gọn bằng tiếng Việt, chỉ dựa trên ảnh. "
          "Nếu không thể xác định từ ảnh, nói rõ không đủ thông tin. "
          "Không bịa dấu hiệu, số đo hoặc chẩn đoán chắc chắn. ")
        return instruction+("Mô tả ngắn những gì quan sát được trong ảnh." if task=="caption" else "Câu hỏi: "+question.strip())
    instruction=("This is an educational medical-image experiment. Answer briefly in English using only the image. "
      "If the image is insufficient, say so. Do not invent findings, measurements or a definitive diagnosis. ")
    return instruction+("Briefly describe the visible image." if task=="caption" else "Question: "+question.strip())
