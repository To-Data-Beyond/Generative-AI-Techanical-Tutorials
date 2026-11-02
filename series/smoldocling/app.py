"""Local SmolDocling OCR app. Run: streamlit run app.py --server.address=127.0.0.1"""

import hashlib
import io
import threading

from PIL import Image, UnidentifiedImageError
import streamlit as st
import torch
from transformers import AutoModelForImageTextToText, AutoProcessor
from docling_core.types.doc import DoclingDocument
from docling_core.types.doc.document import DocTagsDocument

MODEL_ID = "docling-project/SmolDocling-256M-preview"
REVISION = "ce51f56c4ebe36e0b1c3a55f67b261ba22a50bf8"
MAX_BYTES = 5 * 1024 * 1024
MAX_PIXELS = 10_000_000
DEVICE = "cpu"


def decode_image(data):
    if not isinstance(data, bytes) or not 0 < len(data) <= MAX_BYTES:
        raise ValueError("Upload a nonempty image of at most 5 MB.")
    try:
        with Image.open(io.BytesIO(data)) as source:
            if source.format not in {"PNG", "JPEG", "TIFF"}:
                raise ValueError("Use PNG, JPEG or single-page TIFF, not PDF.")
            if source.width * source.height > MAX_PIXELS:
                raise ValueError("The image must contain at most 10 million pixels.")
            if getattr(source, "n_frames", 1) != 1:
                raise ValueError("Upload a single-page image.")
            source.load()
            return source.convert("RGB")
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as error:
        raise ValueError("The file is not a supported readable image.") from error


@st.cache_resource
def load_model():
    torch.set_num_threads(4)
    processor = AutoProcessor.from_pretrained(MODEL_ID, revision=REVISION, token=False)
    model = AutoModelForImageTextToText.from_pretrained(
        MODEL_ID, revision=REVISION, token=False,
        dtype=torch.float32, attn_implementation="eager"
    ).to(DEVICE).eval()
    return processor, model, threading.Lock()


def ocr_pipeline(image):
    if not isinstance(image, Image.Image) or image.width * image.height > MAX_PIXELS:
        raise ValueError("Expected a supported PIL image.")
    processor, model, lock = load_model()
    messages = [{"role": "user", "content": [
        {"type": "image"}, {"type": "text", "text": "Convert this page to docling."}
    ]}]
    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
    inputs = processor(text=prompt, images=[image.convert("RGB")], return_tensors="pt").to(DEVICE)
    with lock, torch.inference_mode():
        generated = model.generate(**inputs, max_new_tokens=8192, do_sample=False)
    tokens = generated[:, inputs.input_ids.shape[1]:]
    if tokens.shape[1] >= 8192:
        raise RuntimeError("OCR reached its token limit; no incomplete result is returned.")
    tags = processor.batch_decode(tokens, skip_special_tokens=False)[0].lstrip()
    if "<doctag>" not in tags or "</doctag>" not in tags:
        raise RuntimeError("The model did not return a complete document.")
    parsed = DocTagsDocument.from_doctags_and_image_pairs([tags], [image])
    document = DoclingDocument.load_from_doctags(parsed, document_name="Document")
    markdown = document.export_to_markdown()
    if not markdown.strip():
        raise RuntimeError("No text was extracted.")
    return markdown


def main():
    st.set_page_config(page_title="Document OCR Extractor", page_icon="📄", layout="wide")
    st.title("Document OCR Text Extractor")
    st.markdown("Upload a PNG, JPEG or single-page TIFF of at most 5 MB. OCR runs locally on CPU.")
    uploaded = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg", "tif", "tiff"], key="document", max_upload_size=5)
    if uploaded is None:
        st.session_state.pop("ocr_result", None)
        st.session_state.pop("input_digest", None)
        return
    data = uploaded.getvalue()
    digest = hashlib.sha256(data).hexdigest()
    if st.session_state.get("input_digest") != digest:
        st.session_state.pop("ocr_result", None)
    st.session_state["input_digest"] = digest
    try:
        image = decode_image(data)
    except ValueError as error:
        st.session_state.pop("ocr_result", None)
        st.error(str(error))
        return
    left, right = st.columns(2)
    with left:
        st.subheader("Uploaded Image")
        st.image(image, width="stretch")
    if st.button("Extract text", key="extract"):
        st.session_state.pop("ocr_result", None)
        try:
            with st.spinner("Processing the image..."):
                st.session_state["ocr_result"] = ocr_pipeline(image)
        except (ValueError, RuntimeError, OSError):
            st.error("OCR could not finish. Check the image and local model installation.")
    result = st.session_state.get("ocr_result")
    if result is not None:
        with right:
            st.subheader("Extracted Text")
            st.markdown(result, unsafe_allow_html=False)
        st.download_button("Download Extracted Text", data=result.encode("utf-8"),
                           file_name="extracted_text.md", mime="text/markdown", key="download")


if __name__ == "__main__":
    main()
