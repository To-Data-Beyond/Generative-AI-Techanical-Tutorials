"""Four real capabilities, with local media and an explicit hosted vision call."""
import base64
from functools import lru_cache
from io import BytesIO
import os
from pathlib import Path
import tempfile
from urllib.parse import urlsplit
import uuid

from PIL import Image
from pydantic import BaseModel, ConfigDict, Field

IMAGE_MODEL = 'segmind/tiny-sd'
IMAGE_REVISION = 'cad0bd7495fa6c4bcca01b19a723dc91627fe84f'
SPEECH_MODEL = 'facebook/mms-tts-eng'
SPEECH_REVISION = 'c71de0fe7204c83f1c10820a7d696d0b450048ba'

class ToolResult(BaseModel):
    model_config = ConfigDict(extra='forbid')
    tool: str
    text: str = ''
    artifact: str = ''
    sources: list[str] = Field(default_factory=list)

def image_bytes(path):
    """Local PNG/JPEG only: no arbitrary remote fetch, SVG or animation."""
    p = Path(path)
    if not p.is_file() or p.stat().st_size > 5_000_000:
        raise ValueError('Supply a local image no larger than 5 MB.')
    data = p.read_bytes()
    with Image.open(BytesIO(data)) as im:
        if im.format not in ('PNG', 'JPEG') or getattr(im, 'n_frames', 1) != 1:
            raise ValueError('Use a single PNG or JPEG image.')
        if im.width * im.height > 4_000_000:
            raise ValueError('Image exceeds four million pixels.')
        im.verify()
    return data, 'image/png' if data.startswith(b'\x89PNG') else 'image/jpeg'

def web_search_tool(question):
    from ddgs import DDGS
    for backend in ('duckduckgo', 'bing'):
        try:
            rows = list(DDGS(timeout=15).text(question, max_results=3, backend=backend))
        except Exception:
            continue
        rows = [r for r in rows if urlsplit(r.get('href', '')).scheme == 'https'
                and r.get('title') and r.get('body')]
        if rows:
            return ToolResult(tool='web_search', text='\n'.join(
                f"{r['title']}: {r['body']}" for r in rows),
                sources=[r['href'] for r in rows])
    raise RuntimeError('Search returned no usable results; try again later.')

@lru_cache(maxsize=1)
def speech_model():
    from transformers import AutoTokenizer, VitsModel
    tokenizer = AutoTokenizer.from_pretrained(SPEECH_MODEL, revision=SPEECH_REVISION, token=False)
    model = VitsModel.from_pretrained(SPEECH_MODEL, revision=SPEECH_REVISION, token=False).eval().to('cpu')
    return tokenizer, model

def text2speech(text, folder):
    import numpy as np
    import torch
    from scipy.io import wavfile
    if not text.strip() or len(text) > 300:
        raise ValueError('Speech accepts 1–300 characters.')
    tokenizer, model = speech_model()
    inputs = tokenizer(text, return_tensors='pt')
    with torch.inference_mode(), torch.random.fork_rng():
        torch.manual_seed(7)
        waveform = model(**inputs).waveform[0].cpu().numpy()
    if not np.isfinite(waveform).all() or not np.any(waveform):
        raise RuntimeError('Invalid generated waveform.')
    path = Path(folder) / (uuid.uuid4().hex + '.wav')
    wavfile.write(path, model.config.sampling_rate,
                  (np.clip(waveform, -1, 1) * 32767).astype(np.int16))
    return ToolResult(tool='text2speech', artifact=str(path))

@lru_cache(maxsize=1)
def image_model():
    import torch
    from diffusers import StableDiffusionPipeline
    model = StableDiffusionPipeline.from_pretrained(
        IMAGE_MODEL, revision=IMAGE_REVISION, token=False,
        dtype=torch.float32, use_safetensors=False)
    return model.to('cpu')

def text2image(text, folder):
    import torch
    if not text.strip() or len(text) > 400:
        raise ValueError('Image prompt accepts 1–400 characters.')
    result = image_model()(text, width=256, height=256, num_inference_steps=12,
        guidance_scale=7.5, generator=torch.Generator('cpu').manual_seed(7))
    if result.nsfw_content_detected and any(result.nsfw_content_detected):
        raise RuntimeError('The image safety checker rejected the output.')
    path = Path(folder) / (uuid.uuid4().hex + '.png')
    result.images[0].save(path)
    image_bytes(path)
    return ToolResult(tool='text2image', artifact=str(path))

def image2text(path, prompt, client=None):
    from openai import OpenAI
    if os.getenv('RUN_OPENAI') != '1':
        raise RuntimeError('Hosted vision requires explicit RUN_OPENAI=1.')
    data, mime = image_bytes(path)
    client = client or OpenAI(base_url=os.getenv('MULTIMODAL_VISION_URL', 'https://api.openai.com/v1'),
                              max_retries=0, timeout=60)
    response = client.responses.create(
        model=os.getenv('MULTIMODAL_VISION_MODEL', 'gpt-5.4-mini'),
        store=False, max_output_tokens=256, reasoning={'effort': 'none'},
        input=[{'role': 'user', 'content': [
            {'type': 'input_text', 'text': prompt},
            {'type': 'input_image', 'detail': 'low',
             'image_url': f'data:{mime};base64,' + base64.b64encode(data).decode()}]}])
    if response.status != 'completed' or not response.output_text.strip():
        raise RuntimeError('Vision did not return a completed description.')
    return ToolResult(tool='image2text', text=response.output_text)

class Helpers:
    def __init__(self, folder=None, vision_client=None):
        self.folder = Path(folder or tempfile.mkdtemp(prefix='multimodal-results-'))
        self.folder.mkdir(parents=True, exist_ok=True)
        self.vision_client = vision_client

    def execute(self, tool, question, image_path=''):
        registry = {
            'web_search': lambda: web_search_tool(question),
            'text2speech': lambda: text2speech(question, self.folder),
            'text2image': lambda: text2image(question, self.folder),
            'image2text': lambda: image2text(image_path, question, self.vision_client),
        }
        if tool not in registry:
            raise ValueError('Unknown tool; no action was taken.')
        return registry[tool]()
