import json
from pathlib import Path

import streamlit as st
import yaml

from src.engine.full_pipeline import FullPipeline
from src.utils.config import ROOT, load_config


st.set_page_config(
    page_title="X-ray Analysis",
    page_icon="◌",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root { --ink:#25332f; --muted:#687873; --line:#d7e2dd; --paper:#f4f7f5; --surface:#ffffff; --accent:#177765; --accent-soft:#e7f2ee; }
    .stApp { background:var(--paper); color:var(--ink); line-height:1.45; }
    .stApp * { box-sizing:border-box; }
    [data-testid="stHeader"] { background:rgba(244,247,245,.92); }
    [data-testid="stSidebar"] { background:#eaf1ed; border-right:1px solid var(--line); }
    [data-testid="stSidebar"] > div:first-child { padding:2rem 1.35rem; }
    .block-container { max-width:1320px; padding:3.2rem 3.5rem 2.5rem; }
    h1,h2,h3 { font-family:'Space Grotesk',sans-serif; letter-spacing:-.02em; color:var(--ink) !important; overflow-wrap:normal; word-break:normal; }
    h1 { font-size:clamp(2.2rem,4vw,4.25rem); line-height:1.06; margin-bottom:.8rem; }
    h2 { font-size:1.3rem; line-height:1.25; }
    p,label,.stMarkdown,.stCaption { font-family:'DM Sans',sans-serif; color:var(--ink); line-height:1.5; }
    .eyebrow { color:var(--accent); font:700 .73rem/1.25 'DM Sans',sans-serif; letter-spacing:.1em; text-transform:uppercase; margin-bottom:1rem; }
    .hero-copy { color:var(--muted); font-size:1.03rem; max-width:47rem; line-height:1.65; margin-bottom:2.1rem; }
    [data-testid="stVerticalBlockBorderWrapper"] { background:var(--surface); border:1px solid var(--line); border-radius:20px; box-shadow:0 10px 28px rgba(35,68,57,.055); }
    [data-testid="stVerticalBlockBorderWrapper"] > div { padding:1.35rem 1.4rem 1.45rem; }
    .kicker { color:var(--muted); font:600 .74rem/1.3 'DM Sans',sans-serif; letter-spacing:.08em; text-transform:uppercase; margin-bottom:.6rem; }
    .panel-title { font:600 1.45rem/1.22 'Space Grotesk',sans-serif; letter-spacing:-.02em; margin-bottom:1.2rem; overflow-wrap:break-word; }
    .empty-state { border:1.5px dashed #9dbcb2; border-radius:16px; padding:3.6rem 1rem; text-align:center; color:var(--muted); background:#f7fbf8; line-height:1.55; }
    .empty-state strong { display:block; color:var(--ink); font:600 1.08rem/1.3 'Space Grotesk',sans-serif; margin-bottom:.35rem; }
    .result-shell { color:var(--ink); margin-top:.2rem; }
    .result-label { color:var(--accent); font:700 .72rem/1.3 'DM Sans',sans-serif; letter-spacing:.1em; text-transform:uppercase; }
    .result-shell p { color:var(--ink); font-size:1.06rem; line-height:1.65; }
    .status-line { color:var(--muted); font-size:.9rem; margin-top:.35rem; }
    .disclaimer { border-left:3px solid #c58b35; background:#fff9ec; border-radius:0 12px 12px 0; padding:.9rem 1rem; color:#6f572d; font-size:.86rem; line-height:1.55; margin-top:2rem; }
    .stButton > button[kind="primary"] { background:var(--accent); border:0; border-radius:12px; min-height:3rem; font-weight:700; transition:transform .2s ease,background .2s ease; }
    .stButton > button[kind="primary"]:hover { background:#096654; transform:translateY(-1px); }
    .stButton > button:focus,.stDownloadButton > button:focus { box-shadow:0 0 0 3px rgba(11,122,104,.24); }
    [data-testid="stFileUploaderDropzone"] { border:1.5px dashed #9dbcb2; border-radius:16px; background:#f7fbf8; min-height:9rem; }
    [data-testid="stFileUploaderDropzone"]:hover { border-color:var(--accent); background:var(--accent-soft); }
    [data-testid="stFileUploader"] { color:var(--ink) !important; }
    [data-testid="stFileUploader"] * { font-family:'DM Sans',sans-serif; }
    [data-testid="stFileUploaderDropzoneInstructions"] { color:var(--muted) !important; line-height:1.45 !important; }
    [data-testid="stFileUploaderDropzoneInstructions"] span,
    [data-testid="stFileUploaderDropzoneInstructions"] small,
    [data-testid="stFileUploaderDropzoneInstructions"] p { color:var(--muted) !important; line-height:1.45 !important; margin:.15rem 0 !important; }
    [data-testid="stFileUploaderDropzone"] button { color:#ffffff !important; background:var(--accent) !important; border:0 !important; border-radius:9px !important; font-weight:700 !important; }
    [data-testid="stFileUploaderDropzone"] button:hover { background:#0e6554 !important; }
    [data-testid="stFileUploaderDropzone"] svg { color:var(--accent) !important; fill:none !important; }
    [data-testid="stFileUploaderFile"] { background:#f0f7f3 !important; border-color:#b9d5ca !important; }
    [data-testid="stFileUploaderFile"] span, [data-testid="stFileUploaderFile"] small { color:var(--ink) !important; }
    [data-testid="stAlert"] { border-radius:14px; color:var(--ink) !important; }
    [data-testid="stAlert"] p { color:var(--ink) !important; }
    [data-testid="stWidgetLabel"] p { color:var(--ink) !important; font-weight:600; line-height:1.4 !important; }
    input, textarea { color:var(--ink) !important; background:#fbfdfc !important; }
    input::placeholder, textarea::placeholder { color:#82908b !important; opacity:1 !important; }
    [data-baseweb="select"] * { color:var(--ink) !important; }
    [role="radiogroup"] label { color:var(--ink) !important; line-height:1.4 !important; min-height:1.5rem; }
    [role="radiogroup"] label p { line-height:1.4 !important; margin:0 !important; }
    [data-testid="stTextInput"] input { line-height:1.4 !important; min-height:2.7rem; }
    .stCaption, [data-testid="stCaptionContainer"] p { color:var(--muted) !important; }
    .stDownloadButton button { color:var(--accent) !important; border-color:#9dc5b8 !important; background:#f5fbf8 !important; border-radius:10px; }
    @media (max-width:800px) { .block-container { padding:2rem 1.1rem; } .panel { min-height:auto; } h1 { font-size:2.45rem; } }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="eyebrow">Vision pipeline · research prototype</div>', unsafe_allow_html=True)
st.title("Phân tích X-quang, theo từng lớp")
st.markdown(
    '<p class="hero-copy">Từ ảnh đầu vào đến phát hiện, vùng dự đoán và hỏi đáp trong một phiên làm việc. Hãy chọn đúng phạm vi ảnh để diễn giải kết quả có trách nhiệm hơn.</p>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Phạm vi phân tích")
    st.caption("Phạm vi giúp chọn nhánh detector phù hợp.")
    scope = st.selectbox(
        "Phạm vi ảnh",
        ["unknown", "pediatric_wrist", "other"],
        format_func=lambda x: {"unknown": "Chưa xác định", "pediatric_wrist": "Cổ tay trẻ em", "other": "Bộ phận / độ tuổi khác"}[x],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown("**Phạm vi detector hiện tại**")
    st.caption("Detector được hỗ trợ cho cổ tay trẻ em. Ảnh khác vẫn có thể chạy caption hoặc VQA, nhưng không nên xem là đã phát hiện tổn thương.")
    st.info("Các model pretrained sẽ được nạp khi phiên khởi động. Lần đầu có thể cần mạng và vài phút.")

left, right = st.columns([1.05, .95], gap="large")
with left:
    with st.container(border=True):
        st.markdown('<div class="kicker">Bước 01 · ảnh đầu vào</div><div class="panel-title">Đưa ảnh vào pipeline</div>', unsafe_allow_html=True)
        upload = st.file_uploader("Ảnh PNG/JPEG", type=["png", "jpg", "jpeg"], help="Không tải ảnh còn thông tin nhận diện cá nhân.", label_visibility="collapsed")
        if upload:
            st.image(upload, caption="Ảnh đầu vào", width="stretch")
        else:
            st.markdown('<div class="empty-state"><strong>Chưa có ảnh</strong>Kéo thả hoặc chọn một ảnh PNG/JPEG để bắt đầu.</div>', unsafe_allow_html=True)

with right:
    with st.container(border=True):
        st.markdown('<div class="kicker">Bước 02 · mục tiêu đọc ảnh</div><div class="panel-title">Chọn tác vụ và đặt câu hỏi</div>', unsafe_allow_html=True)
        question = st.text_input("Câu hỏi tiếng Việt", placeholder="Ví dụ: Có dấu hiệu gãy xương không?")
        task = st.radio("Tác vụ", ["both", "vqa", "caption"], format_func=lambda x: {"both": "Phân tích đầy đủ", "vqa": "Hỏi đáp", "caption": "Mô tả ảnh"}[x], horizontal=True)
        st.caption("Phân tích đầy đủ gồm caption, detector / vùng dự đoán và câu trả lời.")

        if "full_pipeline" not in st.session_state:
            vc = yaml.safe_load((ROOT / "configs/vision.yaml").read_text())
            with st.spinner("Đang chuẩn bị pipeline…"):
                st.session_state.full_pipeline = FullPipeline(load_config(), vc)

        if st.button("Phân tích ảnh →", type="primary", disabled=upload is None, use_container_width=True):
            try:
                with st.spinner("Đang chạy các model pretrained…"):
                    result = st.session_state.full_pipeline.predict(upload.getvalue(), question, scope, ROOT / "results", task)
                st.session_state.full_result = result
            except Exception as e:
                st.error(f"Không chạy được pipeline: {e}")

if "full_result" in st.session_state:
    r = st.session_state.full_result
    v = r["vision"]
    with st.container(border=True):
        st.markdown('<div class="result-shell"><div class="result-label">Kết quả phiên gần nhất</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="status-line">Trạng thái phát hiện / phân vùng: <strong>{v["status"]}</strong></div>', unsafe_allow_html=True)
        if r.get("caption"):
            st.markdown('<div class="result-label" style="margin-top:1.3rem">Mô tả ảnh</div>', unsafe_allow_html=True)
            st.write(r["caption"])
        if r["task"] != "caption":
            st.markdown('<div class="result-label" style="margin-top:1.3rem">Trả lời</div>', unsafe_allow_html=True)
            st.write(r["answer"])

    st.markdown("### Bằng chứng hình ảnh")
    artifacts = v.get("artifacts", {})
    artifact_cols = st.columns(max(1, min(3, len(artifacts))))
    for index, label in enumerate(("input", "overlay", "mask")):
        if label in artifacts:
            path = Path(artifacts[label])
            with artifact_cols[index % len(artifact_cols)]:
                st.image(str(path), caption={"input": "Ảnh gốc", "overlay": "Overlay dự đoán", "mask": "Mask thử nghiệm"}.get(label, label), width="stretch")
                st.download_button("Tải ảnh", path.read_bytes(), path.name, "image/png", key=f"download-{label}", use_container_width=True)

    st.download_button("Tải toàn bộ kết quả JSON", json.dumps(r, ensure_ascii=False, indent=2), "analysis.json", "application/json", use_container_width=True)

st.markdown('<div class="disclaimer"><strong>Lưu ý an toàn:</strong> Mask chỉ là vùng dự đoán thử nghiệm, chưa được xác thực là ranh giới tổn thương. Không phát hiện không có nghĩa là bình thường. Không dùng kết quả để chẩn đoán hoặc quyết định điều trị.</div>', unsafe_allow_html=True)
