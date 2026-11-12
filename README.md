# Bản mở rộng theo repo DL_MedicalVQA_Project

Đã bổ sung nhánh tự động detector → box → MedSAM → mask/overlay → caption/VQA. **Chạy `streamlit run app_full.py`**, không phải app.py nếu muốn dùng đầy đủ nhánh thị giác. Xem `docs/SETUP_VISION.md` trước khi chạy: cần tải checkpoint detector và MedSAM, không cần train. Detector mặc định chỉ hỗ trợ cổ tay trẻ em; ảnh khác vẫn có caption/VQA nhưng không được coi là đã phát hiện/phân vùng tổn thương.

Model phân vùng sinh mask thử nghiệm trong box, chưa được kiểm chứng bám đúng đường gãy. Bản này chưa chạy đầy đủ các trọng số từ đầu đến cuối.

# Cập nhật: giữ luồng hai nhánh của sơ đồ

Mặc định giao diện chạy **Caption + Hỏi đáp**: một ảnh đi vào hai nhánh độc lập, kết quả hiển thị cùng nhau. Chọn câu trả lời mở hoặc đóng (Có/Không/Không đủ thông tin). Dùng Qwen để giữ tiếng Việt. Xem `docs/architecture.md` để đối chiếu từng khối; fusion và decoder dùng trọng số nội bộ checkpoint, nhánh đóng không phải MLP riêng.

```bash
python predict.py --image data/images/example.png --question "Ảnh có thể hiện phổi không?" --task both --answer-type closed
```

# medicalVQA_project — pretrained, không cần train

Project hỏi đáp ảnh y khoa phục vụ đồ án. Chạy pretrained vision-language model trực tiếp, không train/fine-tune, không cần bộ dữ liệu để chạy demo. Dataset chỉ cần nếu muốn đo chất lượng.

## 1. Chọn model

| Profile | Model | Ngôn ngữ sử dụng | Ghi chú |
|---|---|---|---|
| Mặc định | Qwen/Qwen3-VL-2B-Instruct | Prompt và câu trả lời tiếng Việt | Lựa chọn thử nghiệm tiếng Việt; phải đánh giá trên bộ câu hỏi thực tế |
| Nhẹ | HuggingFaceTB/SmolVLM-500M-Instruct | Tiếng Anh | 500M, nhẹ hơn; không hứa khả năng tiếng Việt |

Cả hai là VLM tổng quát, không phải model được xác thực chẩn đoán. Không thể cam kết “đủ chính xác y khoa” chỉ từ kích thước model. Không tự tạo phần trăm confidence.

Qwen 2B có khoảng 4 GB riêng trọng số ở 16-bit, CPU float32 khoảng 8 GB riêng trọng số; RAM/VRAM thực cần cao hơn vì vision encoder, cache, activations và framework. Nên bắt đầu với máy RAM 16 GB hoặc GPU 8 GB, đây là ước lượng lập kế hoạch, không phải benchmark. 4-bit giảm bộ nhớ trọng số, không giảm mọi thành phần. SmolVLM model card báo 1.23 GB GPU RAM cho một ảnh trong cấu hình của tác giả; máy và phiên bản khác có thể khác. CPU có thể chậm.

## 2. Cài đặt

Python 3.10–3.12 được khuyến nghị; đã kiểm tra phần mã và import bằng Python 3.12. Mở terminal trong thư mục project.

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```
Linux/macOS:
```bash
source .venv/bin/activate
```

CPU (phù hợp thử SmolVLM):
```bash
python -m pip install --upgrade pip
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
python -m scripts.check_environment
```

NVIDIA GPU: cài cặp torch/torchvision phù hợp CUDA từ https://pytorch.org/get-started/locally/ trước, rồi `pip install -r requirements.txt`. Không cài bản CPU ở bước trên nếu muốn dùng GPU.

Tuỳ chọn CUDA 4-bit:
```bash
pip install -r requirements-4bit.txt
```
Bật checkbox 4-bit ở giao diện, hoặc sửa `model.load_in_4bit: true` trong YAML khi dùng CLI. Không dùng tuỳ chọn này với CPU trong project.

## 3. Chạy demo

```bash
streamlit run app.py
```

Mở URL hiện trong terminal (thường http://localhost:8501). Chọn model, tải PNG/JPEG, nhập câu hỏi, nhấn Phân tích ảnh. Có tác vụ mô tả ảnh bằng cùng model, không phải tải thêm BLIP. Lần đầu tải trọng số từ Hugging Face, cần Internet và vài GB dung lượng trống; các lần sau dùng cache. Project không gửi ảnh đến API suy luận bên ngoài. Không có API key bắt buộc với các checkpoint công khai này.

Muốn nhẹ nhất: chọn **SmolVLM 500M · English**, hỏi “Which body part is shown in this image?”. Muốn thử tiếng Việt: chọn Qwen và hỏi “Ảnh này thể hiện bộ phận nào?”.

## 4. Chạy bằng CLI

```bash
python predict.py --image data/images/example.png --question "Ảnh này thể hiện bộ phận nào?" --output results/prediction.json
python predict.py --config configs/smolvlm.yaml --image data/images/example.png --question "Which body part is shown?"
python predict.py --image data/images/example.png --task caption
```

`example.png` phải là ảnh bạn tự cung cấp. Không kèm ảnh bệnh nhân hay kết quả giả trong bản phát hành. Chỉ nhận PNG/JPEG; DICOM cần xuất đúng window/level sang ảnh trước. Thu nhỏ ảnh giữ tỷ lệ, nhưng có thể mất dấu hiệu nhỏ; điều chỉnh `max_image_side` nếu đủ bộ nhớ.

## 5. Cấu trúc

```text
medicalVQA_project/
├── app.py                      # Streamlit
├── predict.py                  # Hỏi đáp / caption CLI
├── evaluate.py                 # Đánh giá zero-shot, không train
├── configs/                    # Qwen / SmolVLM
├── src/
│   ├── data/preprocessing.py   # Đọc, kiểm tra, resize ảnh
│   ├── models/pretrained_vlm.py# Tải pretrained và generate
│   ├── engine/pipeline.py      # Điều phối đầu vào / đầu ra
│   └── utils/                 # Config, prompt, metrics
├── scripts/check_environment.py
├── tests/test_pipeline.py
├── docs/architecture.md
├── data/                      # Ảnh và nhãn đánh giá do bạn cung cấp
└── results/                   # Kết quả JSON
```

## 6. Đánh giá mà không huấn luyện

Dùng `data/evaluation.example.json` làm mẫu schema, thay tên ảnh, câu hỏi, đáp án bằng dữ liệu có nhãn thật. Một mẫu có `image`, `question`, và `answers` (danh sách đáp án chấp nhận) hoặc `answer`. Chạy:

```bash
python evaluate.py --data data/evaluation.json --image-dir data/images --output results/evaluation.json
```

Script xuất exact match và token F1 sau chuẩn hoá chữ/punctuation. Đây là metric trùng khớp văn bản, không phải xác nhận đúng y khoa; câu dài và đáp án ngắn có thể bị chấm thấp dù cùng ý. Nên bổ sung đánh giá thủ công tính đúng, bịa thông tin và từ chối phù hợp. Không có accuracy thực nghiệm trong gói vì chưa chạy bộ dữ liệu y khoa có nhãn.

## 7. Kiểm thử và giới hạn

```bash
pip install -r requirements-dev.txt
python -m pytest -q
```

Unit tests dùng model giả được ghi rõ để kiểm tra điều phối, kiểm tra ảnh, prompt, metric; không chứng minh chất lượng model thật. Xem `docs/VALIDATION.md` để biết những gì đã chạy. Code không có fallback trả lời mẫu khi tải model thất bại: lỗi được báo rõ.

Nếu OOM: chọn SmolVLM; giảm `max_image_side`/`max_new_tokens`; dùng CUDA 4-bit cho Qwen. Nếu tải lỗi: kiểm tra Internet và dung lượng cache. Sau khi tải thành công có thể đặt `local_files_only: true`. Đổi profile trên giao diện sẽ giải phóng model của phiên hiện tại; nhiều phiên người dùng vẫn có thể dùng nhiều bộ nhớ.

## 8. Nguồn và phạm vi kế thừa

Tham khảo cấu trúc repo https://github.com/QuangVoAI/DL_MedicalVQA_Project tại commit `f666bb938385776c5dea796906d10b9055a658fe` (đọc ngày 2026-11-11). Bộ mã này viết lại độc lập theo yêu cầu không train; không sao chép model/checkpoint của tác giả. Giữ cách phân chia configs/src/data/models/engine/utils/scripts. Không giữ LSTM/PhoBERT/DenseNet/custom Co-Attention vì các khối ghép mới cần huấn luyện.

Nguồn model và API:
- https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct
- https://huggingface.co/HuggingFaceTB/SmolVLM-500M-Instruct
- https://pytorch.org/get-started/locally/

Trọng số tải riêng, tuân theo license/model card của nhà phát hành. Đây là prototype học tập, không dùng để chẩn đoán hoặc quyết định điều trị.
