from pathlib import Path
import os

import streamlit as st
import torch

from runtime import MODELS, SOURCE_BASE, download, generate_image, load_image, load_model

torch.set_num_threads(2)
CACHE = Path(os.environ.get("TDB_CYCLEGAN_CACHE", Path(__file__).parent / ".model-cache"))


@st.cache_resource
def get_model(selection):
    return load_model(selection, CACHE)


st.title("Horse Zebra GAN Web App")
pick = st.selectbox("Please select a GAN model to use:", list(MODELS))
animal, target = ("horse", "zebra") if pick == "Horse 2 Zebra GAN" else ("zebra", "horse")
st.write(f"Convert a {animal} image into a {target} image with CycleGAN.")
use_default = st.button("Try with Default Image")
uploaded = st.file_uploader(f"Upload a {animal} image", type=["jpg", "jpeg", "png"])
if use_default or uploaded is not None:
    try:
        source = uploaded if uploaded is not None else download(SOURCE_BASE + animal + ".jpg", CACHE / (animal + ".jpg"))
        image = load_image(source)
        st.subheader("Input image")
        st.image(((image[0].permute(1, 2, 0).numpy() + 1) / 2).clip(0, 1))
        with st.spinner("Generating image..."):
            result = generate_image(get_model(pick), image)
        st.subheader("Generated image")
        st.image(result)
    except ValueError as exc:
        st.error(str(exc))
