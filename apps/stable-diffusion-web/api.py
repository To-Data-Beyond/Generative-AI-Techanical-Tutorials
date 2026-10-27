from io import BytesIO
from threading import Lock
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
import torch
from diffusers import StableDiffusionPipeline

MODEL_ID = "CompVis/stable-diffusion-v1-4"
MODEL_REVISION = "133a221b8aa7292a167afc5127cb63fb5005638b"
DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32
pipe = None
inference_lock = Lock()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["Content-Type"],
)


def get_pipeline():
    global pipe
    if pipe is None:
        pipe = StableDiffusionPipeline.from_pretrained(
            MODEL_ID, revision=MODEL_REVISION, variant="fp16",
            torch_dtype=DTYPE, use_safetensors=True, token=False,
        )
        pipe.vae.enable_slicing()
        if DEVICE == "mps":
            pipe.enable_attention_slicing()
        pipe.to(DEVICE)
        pipe.set_progress_bar_config(disable=True)
    assert pipe.safety_checker is not None
    return pipe


@app.get("/")
def generate(
    prompt: Annotated[str, Query(min_length=1, max_length=500)],
    seed: Annotated[int, Query(ge=0, le=2**32 - 1)] = 1024,
):
    prompt = prompt.strip()
    if not prompt:
        raise HTTPException(422, "Prompt cannot be blank")
    # One worker and one lock prevent shared scheduler-state races.
    with inference_lock, torch.inference_mode():
        pipeline = get_pipeline()
        result = pipeline(
            prompt, guidance_scale=7, height=256, width=256,
            num_inference_steps=50,
            generator=torch.Generator("cpu").manual_seed(seed),
        )
    if result.nsfw_content_detected and any(result.nsfw_content_detected):
        raise HTTPException(400, "Image was blocked by the model safety checker")
    buffer = BytesIO()
    result.images[0].save(buffer, format="PNG")
    return Response(buffer.getvalue(), media_type="image/png")
