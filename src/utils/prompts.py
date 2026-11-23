def make_prompt(question, task="vqa", language="vi", max_chars=1500):
    if task not in ("vqa", "caption"):
        raise ValueError("task: vqa/caption")
    if task == "vqa" and (not isinstance(question, str) or not question.strip()):
        raise ValueError("Vui lòng nhập câu hỏi")
    if len(question) > max_chars:
        raise ValueError("Câu hỏi quá dài")

    if language == "vi":
        if task == "caption":
            return (
                "Bạn là trợ lý học tập phân tích hình ảnh y khoa. "
                "Hãy mô tả ngắn gọn bằng tiếng Việt (2-3 câu) những gì quan sát được trực tiếp trên ảnh: "
                "loại ảnh chụp (ví dụ X-quang, CT, MRI), bộ phận cơ thể và các cấu trúc giải phẫu chính nhìn thấy rõ. "
                "Không đưa ra kết luận chẩn đoán bệnh chắc chắn."
            )
        return (
            "Bạn là trợ lý học tập phân tích hình ảnh y khoa. "
            "Hãy trả lời ngắn gọn, rõ ràng bằng tiếng Việt dựa trên những gì nhìn thấy trong ảnh. "
            "Nếu câu hỏi liên quan đến bệnh lý hoặc tổn thương, hãy mô tả đặc điểm quan sát được và lưu ý cần bác sĩ chuyên khoa đánh giá thêm. "
            "Chỉ trả lời 'Không đủ thông tin' khi ảnh quá mờ hoặc hoàn toàn không liên quan đến câu hỏi.\n"
            f"Câu hỏi: {question.strip()}"
        )

    if task == "caption":
        return (
            "You are an educational medical-image assistant. "
            "Briefly describe in English (2-3 sentences) what is directly visible in the image: "
            "imaging modality, body part, and main anatomical structures. Do not give a definitive diagnosis."
        )
    return (
        "You are an educational medical-image assistant. "
        "Answer briefly in English based on what is visible in the image. "
        "Only say 'Insufficient information' if the image is unreadable or unrelated.\n"
        f"Question: {question.strip()}"
    )