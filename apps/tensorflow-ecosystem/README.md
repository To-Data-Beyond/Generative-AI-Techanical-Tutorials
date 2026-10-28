# TensorFlow ecosystem browser example

The runnable `tfjs-example.mjs` is identical to the JavaScript embedded in
`../../TensorFlow_Ecosystem.ipynb`. Tested with Node 25.6.1, npm 11.10.1 and
TensorFlow.js 4.22.0. No keys, paid API, cloud account or private data.

```bash
npm ci
npm test
npm run build
python -m http.server 3101 --bind 127.0.0.1
```

Open `http://127.0.0.1:3101/`. A compatible browser uses WebGL; otherwise it
falls back to CPU. Node uses the JavaScript CPU implementation. Both real
paths passed all ten epochs on all 100 source-example rows, with valid one-hot
labels and finite normalized 100×3 predictions. These random labels are a
runtime fixture, not a useful classification benchmark. No Node-only
TensorBoard callback is called from browser code.

The Python notebook separately runs the complete MNIST 60,000/10,000 dataset,
all 5+10 epochs, actual TensorBoard event/HTTP checks and ImageNet MobileNetV2
conversion with real Lite inference parity. Its pinned setup includes
`tensorflow==2.20.0 keras==3.15.1 tensorboard==2.20.0 setuptools==80.9.0`;
TensorBoard 2.20 needs pkg_resources supplied by that setuptools version.
The Lite interpreter deprecation and upstream warnings are recorded in the
website import review rather than hidden. The article's seven original blocks
remain verbatim in the notebook's nonexecuting appendix.
