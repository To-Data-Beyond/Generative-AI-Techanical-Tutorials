---
title: BLIP Image Captioning
emoji: 🖼️
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 6.31.0
python_version: '3.11'
app_file: app.py
pinned: false
license: apache-2.0
---

# BLIP Image Captioning

Install requirements.txt, then run `python app.py` locally. The default binds
127.0.0.1:7860 with no public tunnel. The application uses CPU inference and a
pinned official BSD-3-Clause BLIP checkpoint; its caption may be inaccurate.

To deploy, copy app.py, requirements.txt and this README into **your own**
Gradio Space. On Spaces, SPACE_ID selects the required container bind address.
Choose visibility deliberately: a public Space's API is public. For a private
Space use a read-scoped HF_TOKEN with gradio_client.Client(..., token=...).
Do not commit a token or .env. This batch tests local HTTP/auth, not hosted
Space creation, billing or private-Hub authorization.
