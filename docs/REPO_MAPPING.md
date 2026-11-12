# Cơ sở từ repository người dùng cung cấp

Nguồn: https://github.com/QuangVoAI/DL_MedicalVQA_Project
Commit đã kiểm tra: f666bb938385776c5dea796906d10b9055a658fe.

Đã đọc README, configs, encoder, PhoBERT encoder, MedicalVQAModelA và Dockerfile. Repo gốc chứa VQA DenseNet/PhoBERT/CoAttention và các hướng LLaVA; không có module detector→segmentation tương ứng yêu cầu đề. Không sử dụng các head chưa train của repo để giả có inference.

Bản này là implementation độc lập dựa trên cách tổ chức của repo, không phải nguyên repo đã đổi tên. Không phân phối lại source hoặc checkpoint của tác giả.

| Repo gốc | Bản mở rộng |
|---|---|
| configs/medical_vqa.yaml | Giữ config VQA, thêm vision.yaml |
| src/data | Tiền xử lý ảnh |
| src/models | VLM pretrained; thêm fracture_detector.py và medsam_segmenter.py |
| src/engine | Pipeline VQA, vision và full_pipeline |
| src/utils | Prompt, hậu xử lý, metrics |
| scripts | Kiểm tra môi trường, tải detector |
| app.py | Demo VQA cũ; app_full.py chạy nhánh thị giác mới |
| train_medical.py | Không dùng; người dùng không train |

Thành phần CNN/ViT → visual embeddings; text → embeddings; fusion → decoder nằm trong VLM đồng bộ. Không gọi nó là cùng implementation DenseNet/PhoBERT/CoAttention của repo. Detector và MedSAM là nhánh độc lập mới. Caption/VQA dùng ảnh gốc và metadata CV dạng text; không dùng tensor feature của YOLO làm embedding của Qwen.

Nguồn detector: https://github.com/RuiyangJu/Bone_Fracture_Detection_YOLOv8
Nguồn segmentation: https://github.com/bowang-lab/MedSAM
Kiểm tra license của từng thư viện/model trước khi phân phối hoặc triển khai thương mại, đặc biệt Ultralytics.
