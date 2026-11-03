"""Explicit configuration; importing this module never starts inference."""
import os
from pathlib import Path
import tempfile
from dotenv import load_dotenv

# Configure storage before importing CrewAI. Do not change HOME.
os.environ.setdefault('CREWAI_STORAGE_DIR', str(Path(tempfile.mkdtemp(prefix='multimodal-crew-'))))
os.environ.setdefault('OTEL_SDK_DISABLED', 'true')
os.environ.setdefault('CREWAI_TELEMETRY_DISABLED', 'true')
load_dotenv(Path(__file__).with_name('.env'), override=False)

def make_llm(interceptor=None):
    from crewai import LLM
    if os.getenv('RUN_OPENAI') != '1':
        raise RuntimeError('Set RUN_OPENAI=1 only after configuring your API key and budget.')
    if not os.getenv('OPENAI_API_KEY'):
        raise RuntimeError('Configure OPENAI_API_KEY outside the notebook.')
    # Compatible providers can override both URL and model. Check their tool/
    # structured-output support before use; a compatible URL is not a guarantee.
    return LLM(model='openai/' + os.getenv('MULTIMODAL_MODEL', 'gpt-5.4-mini'),
               base_url=os.getenv('MULTIMODAL_BASE_URL', 'https://api.openai.com/v1'),
               max_completion_tokens=512, reasoning_effort='none',
               timeout=60, max_retries=0, stream=False, store=False,
               interceptor=interceptor)
