import io
import warnings
from pathlib import Path
from PIL import Image, ImageOps, UnidentifiedImageError

def prepare_image(source, max_side=768, max_mb=15):
    if isinstance(source, Image.Image):
        image=source.copy()
    else:
        if isinstance(source,(str,Path)):
            path=Path(source)
            if path.stat().st_size > max_mb*1024*1024: raise ValueError("Ảnh vượt dung lượng cho phép")
            raw=path.read_bytes()
        else:
            raw=source.read(max_mb*1024*1024+1) if hasattr(source,"read") else source
        if not isinstance(raw,bytes): raise ValueError("Cần file PNG/JPEG hoặc PIL Image")
        if len(raw)>max_mb*1024*1024: raise ValueError("Ảnh vượt dung lượng cho phép")
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("error",Image.DecompressionBombWarning)
                with Image.open(io.BytesIO(raw)) as im:
                    if im.format not in ("PNG","JPEG"): raise ValueError("Chỉ hỗ trợ PNG/JPEG; hãy xuất DICOM sang ảnh trước")
                    if im.width*im.height>25_000_000: raise ValueError("Ảnh quá lớn: tối đa 25 triệu pixel")
                    im.load(); image=ImageOps.exif_transpose(im).copy()
        except (UnidentifiedImageError,OSError,Image.DecompressionBombWarning,Image.DecompressionBombError) as e:
            raise ValueError("Không đọc được ảnh hợp lệ") from e
    if image.width*image.height>25_000_000: raise ValueError("Ảnh quá lớn")
    image=ImageOps.exif_transpose(image).convert("RGB")
    image.thumbnail((max_side,max_side),Image.Resampling.LANCZOS)
    return image
