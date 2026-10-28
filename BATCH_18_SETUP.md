# Standalone companions: Phi-1.5, TensorFlow and portfolio tools

All 22 code cells (5/11/6) passed fresh Python 3.11.14 kernels. Git notebooks
are output-free and preserve all twelve original source code fragments in
nonexecuting appendices. No paid APIs, API keys or remote deployment.

Use separate environments for these tutorials. Install Jupyter/ipykernel to
run notebooks, plus the relevant pinned packages:

```bash
# Phi_1_5_Textbook_Data.ipynb
python -m pip install torch==2.10.0 transformers==4.57.6 huggingface-hub==0.36.2

# TensorFlow_Ecosystem.ipynb; Node/npm must also be available
python -m pip install tensorflow==2.20.0 keras==3.15.1 tensorboard==2.20.0 setuptools==80.9.0

# Data_Science_Portfolio_Tools.ipynb
python -m pip install voila==0.5.8 ipywidgets==8.1.8 nbclient==0.10.4 ipykernel==6.30.1
```

Phi-1.5 uses the official MIT-licensed 2.84GB safetensors checkpoint at
`77aa61eeac94fbf33d492b9f2744c98b42d5b5eb`, verifies its SHA-256, uses the
native Transformers implementation without remote code and selects CUDA,
MPS or CPU explicitly. It ran on MPS float32. It preserves the full original
prime-function prompt and 200-total-token bound. Generation is displayed,
not automatically executed; it may include an unfinished continuation at the
bound. The companion checks token prefix, finite logits and an independent
first-token argmax, not the article's research benchmarks or safety claims.

TensorFlow runs the full 60,000/10,000 MNIST split and 5+10 epochs, checking
all 28,125 optimizer updates, summary events, the actual TensorBoard dashboard
and the 2/3 manual accuracy scalar. Swish uses Keras directly, not retired
Addons. The complete ImageNet MobileNetV2 converts and matches Lite inference
within 0.000001 maximum probability difference on the same seeded input.
The synthetic input tests conversion parity, not classification quality.
See [the JavaScript app](./apps/tensorflow-ecosystem/) for the same ten-epoch
module tested on real Node CPU and browser WebGL.

Voilà uses a supplied fictional three-project fixture. Real widget callbacks
filter 3→1→2→3 cards; text is escaped and instances have separate state.
The notebook creates an output-free temporary dashboard and a scoped kernelspec,
then tests real standalone and authenticated Jupyter-extension routes on
loopback only. Each server is terminated afterward. No cloud account, paid
hosting, public tunnel or mamba installation is claimed. The mamba command is
preserved as an optional setup path; the tested installation is from PyPI.

Some validation environments reuse temporary dependencies and inherit system
packages; only the Voilà environment was newly created for this batch. Fresh
kernels do not mean every dependency was reinstalled from scratch. Upstream
TensorFlow/Lite/pkg_resources and kernel-process warnings are recorded in the
website's detailed review. No failed-run output substitutes for final results.
