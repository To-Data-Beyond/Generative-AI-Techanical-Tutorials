import os
import tempfile
import hashlib
from pathlib import Path
from functools import lru_cache
import torch
from PIL import Image
import gradio as gr
from transformers import BlipProcessor, BlipForConditionalGeneration
from huggingface_hub import snapshot_download

MODEL_ID = "Salesforce/blip-image-captioning-base"
REVISION = "82a37760796d32b1411fe092ab5d4e227313294b"
WEIGHT_SHA256 = "d6638651a5526cc2ede56f2b5104d6851b0755816d220e5e046870430180c767"

@lru_cache(maxsize=1)
def load_captioner():
    checkpoint = Path(snapshot_download(MODEL_ID, revision=REVISION, token=False,
        cache_dir=Path(tempfile.gettempdir()) / "tdb-archive27-model-cache",
        allow_patterns=["*.json", "*.txt", "pytorch_model.bin"]))
    with (checkpoint / "pytorch_model.bin").open("rb") as handle:
        if hashlib.file_digest(handle, "sha256").hexdigest() != WEIGHT_SHA256:
            raise RuntimeError("Unexpected official checkpoint bytes")
    processor = BlipProcessor.from_pretrained(checkpoint, local_files_only=True)
    model = BlipForConditionalGeneration.from_pretrained(checkpoint,
        local_files_only=True, dtype=torch.float32).to("cpu").eval()
    return processor, model

def caption_image(image):
    if not isinstance(image, Image.Image):
        raise ValueError("Upload an image first")
    if image.width < 1 or image.height < 1 or image.width * image.height > 4_000_000:
        raise ValueError("Use an image with at most four million pixels")
    image = image.convert("RGB")
    processor, model = load_captioner()
    inputs = processor(images=image, return_tensors="pt")
    with torch.inference_mode():
        tokens = model.generate(**inputs, max_new_tokens=40, do_sample=False, num_beams=1)
    result = processor.decode(tokens[0], skip_special_tokens=True).strip()
    if not result:
        raise RuntimeError("The model returned an empty caption")
    return result

def build_demo():
    return gr.Interface(fn=caption_image,
        inputs=gr.Image(type="pil", image_mode="RGB", sources=["upload"], label="Upload an image"),
        outputs=gr.Textbox(label="Caption"), api_name="caption",
        title="BLIP Image Captioning", flagging_mode="never").queue(default_concurrency_limit=1, max_size=8)

if __name__ == "__main__":
    host = "0.0.0.0" if os.getenv("SPACE_ID") else "127.0.0.1"
    build_demo().launch(server_name=host, server_port=int(os.getenv("PORT", "7860")), share=False)
