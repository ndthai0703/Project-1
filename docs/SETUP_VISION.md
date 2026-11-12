# Chạy nhánh tự động bổ sung

1. Cài môi trường như README, rồi `pip install -r requirements-vision.txt`.
2. Chạy `python -m scripts.download_detector`. Script tải checkpoint chính thức của RuiyangJu/Bone_Fracture_Detection_YOLOv8. Đây là checkpoint chuyên cổ tay trẻ em GRAZPEDWRI-DX; không phải YOLO COCO mặc định.
3. Tải `medsam_vit_b.pth` theo mục checkpoint trong https://github.com/bowang-lab/MedSAM và đặt tại `checkpoints/medsam_vit_b.pth`. Cần đúng MedSAM ViT-B, không phải SAM ViT-B thông thường. Link trọng số và điều kiện tải do tác giả quản lý; không kèm trọng số trong ZIP.
4. Chạy `streamlit run app_full.py`.

CLI:
```bash
python analyze.py --image data/images/wrist.png --scope pediatric_wrist --question "Ảnh có vùng nghi gãy xương không?"
```

`--scope` là metadata do người dùng cung cấp, KHÔNG phải tự động nhận diện anatomy/age. Chọn other/unknown sẽ bỏ detector/segmentation và báo unsupported_scope; caption/VQA vẫn chạy với cảnh báo. Không được chọn pediatric_wrist để giả hỗ trợ các ảnh khác.

Detector tự tạo box; không khoanh tay. MedSAM nhận từng box và sinh mask; không biến box thành hình chữ nhật giả làm segmentation. Ảnh cùng hệ tọa độ dùng cho cả detector và MedSAM. Mask được nội suy về kích thước ảnh xử lý, lưu PNG và overlay. JSON ghi hệ tọa độ, điểm detector, diện tích pixel và mask status; không quy đổi pixel sang mm hay coi điểm detector là độ tin cậy y khoa.

Caption/VQA hiện nhận ảnh gốc và metadata text (box, số pixel mask, trạng thái). Chưa đưa ROI/overlay như ảnh thứ hai vào model; không tuyên bố VLM nhìn thấy hình mask. Nhánh caption không nhận câu hỏi. No detection không được biến thành kết luận normal. MedSAM có thể phân vùng xương thay vì đường gãy; phải đánh giá mask đối chiếu nhãn chuyên gia trước khi gọi là segmentation tổn thương chính xác.

Mặc định vision chạy CPU để tránh tranh VRAM với Qwen; có thể đổi device trong configs/vision.yaml. Không train/fine-tune; chỉ inference. Thư viện, trọng số và RAM sử dụng lớn hơn phiên bản chỉ VQA. Bản này không cam kết nhẹ trên mọi máy.

## Đánh giá cần làm
Detection: precision/recall và mAP trên box thật, đặc biệt false negatives. Segmentation: Dice/IoU với mask tổn thương thật, tách khỏi mask cơ quan. VQA: đúng theo ảnh, nhất quán với kết quả CV và không bịa. Không có ground truth segmentation thì chưa chứng minh hoàn thành chất lượng phân vùng chỉ từ overlay đẹp.
