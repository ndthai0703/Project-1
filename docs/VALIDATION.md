# Validation bản nhánh thị giác

- 16 tests (tests/test_vision.py và tests/test_pipeline.py) pass: điều phối 2 nhánh, kiểm tra ảnh, ngoài phạm vi không tải model, không detection không tải MedSAM, clip bounding box, mask đúng hệ tọa độ và số pixel, chuyển metadata CV sang VQA. Test dùng doubles, không dùng trọng số thật.
- compileall pass.
- Detector checkpoint tải thành công từ release tác giả. SHA256: 301abc1774c28dd7c5adbcf1e8a79ed6771273615238b62dd179b622292b3a81. Trọng số không đóng gói trong ZIP.
- Chưa kiểm thử inference thật detector, MedSAM, Qwen, full UI hoặc CUDA cho bản này. Chưa tải MedSAM; người dùng tải theo SETUP_VISION.md.
- Chưa có đo accuracy, mAP, Dice/IoU hoặc benchmark tốc độ/RAM. Không coi mask là nhãn tổn thương đúng nếu chưa đánh giá.
- Các kiểm thử của bản VQA trước không thay thế kiểm chứng full pipeline mới.
