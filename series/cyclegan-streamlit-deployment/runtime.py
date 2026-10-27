"""Pinned, checksum-verified CycleGAN inference using the authors' networks."""
from pathlib import Path
import functools
import hashlib
import importlib.util
from io import BytesIO
import os
import urllib.request

import numpy as np
from PIL import Image, ImageOps, UnidentifiedImageError
import torch

REVISION = "2a7afba2895d52556dd5dfe07e8555ef657ced6f"
SOURCE_REVISION = "cb72d148da8d4d47be06c9e244e9b5e4c211ed25"
SOURCE_BASE = (
    "https://raw.githubusercontent.com/youssefHosni/"
    f"Practical-Computer-Vision-In-Python/{SOURCE_REVISION}/"
    "Generative%20Adversial%20Networks/"
    "Build%20and%20Deploy%20a%20GAN%20Streamlit%20App%20on%20Heroku/"
)
MODELS = {
    "Horse 2 Zebra GAN": ("horse2zebra", "5bfc34b154035be1cd592cd273fdf328810bee4756044c9cf7deb8d4b6d2fadb"),
    "Zebra 2 Horse GAN": ("zebra2horse", "839095a46c20b2c38fbadae9d626b2a7646035159483d29f4735eedde1de3059"),
}


def download(url, target, digest=None):
    target = Path(target)
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        request = urllib.request.Request(url, headers={"User-Agent": "ToDataBeyond-Tutorial"})
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = response.read()
        if digest and hashlib.sha256(payload).hexdigest() != digest:
            raise ValueError("Downloaded asset checksum does not match")
        target.write_bytes(payload)
    if digest and hashlib.sha256(target.read_bytes()).hexdigest() != digest:
        raise ValueError("Cached asset checksum does not match")
    return target


def load_model(selection, cache_dir):
    name, digest = MODELS[selection]
    cache_dir = Path(cache_dir)
    source = download(
        f"https://raw.githubusercontent.com/junyanz/pytorch-CycleGAN-and-pix2pix/{REVISION}/models/networks.py",
        cache_dir / "networks.py",
        "2bfcb7adb19f7b7ff6fd8dd76e313200acf000e96784b920658a62e1a11fc04f",
    )
    spec = importlib.util.spec_from_file_location("pinned_cyclegan_networks", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    norm = functools.partial(torch.nn.InstanceNorm2d, affine=False, track_running_stats=False)
    model = module.ResnetGenerator(3, 3, 64, norm_layer=norm, use_dropout=False, n_blocks=9)
    weights = download(
        f"https://efrosgans.eecs.berkeley.edu/cyclegan/pretrained_models/{name}.pth",
        cache_dir / f"{name}.pth", digest,
    )
    state = torch.load(weights, map_location="cpu", weights_only=True)
    # Old InstanceNorm checkpoints contain statistics which current InstanceNorm
    # does not track. Remove only these known obsolete buffers, then load strictly.
    for key in list(state):
        if key.endswith(("running_mean", "running_var", "num_batches_tracked")):
            del state[key]
    model.load_state_dict(state, strict=True)
    return model.eval()


def load_image(image_source):
    if hasattr(image_source, "read"):
        data = image_source.read(5 * 1024 * 1024 + 1)
        if len(data) > 5 * 1024 * 1024:
            raise ValueError("Image exceeds 5 MiB")
        image_source = BytesIO(data)
    try:
        with Image.open(image_source) as image:
            if image.format not in {"JPEG", "PNG"}:
                raise ValueError("Use a JPEG or PNG image")
            if image.width * image.height > 16_000_000:
                raise ValueError("Image exceeds 16 million pixels")
            image = ImageOps.exif_transpose(image).convert("RGB")
            image = image.resize((256, 256), Image.Resampling.BICUBIC)
            array = np.asarray(image, dtype=np.float32) / 127.5 - 1.0
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise ValueError("Invalid image") from exc
    return torch.from_numpy(array.transpose(2, 0, 1).copy()).unsqueeze(0)


def generate_image(model, image):
    if tuple(image.shape) != (1, 3, 256, 256) or not torch.isfinite(image).all():
        raise ValueError("Expected a finite 1 x 3 x 256 x 256 tensor")
    if image.min() < -1 or image.max() > 1:
        raise ValueError("Input must be normalized to [-1, 1]")
    with torch.inference_mode():
        generated = model(image)
    if not torch.isfinite(generated).all():
        raise ValueError("Model produced non-finite output")
    return ((generated[0].cpu().permute(1, 2, 0).numpy() + 1) / 2).clip(0, 1)
