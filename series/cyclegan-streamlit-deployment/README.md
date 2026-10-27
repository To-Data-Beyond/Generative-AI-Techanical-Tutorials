# CycleGAN Streamlit Deployment

| Part | Article | Notebook |
| --- | --- | --- |
| 1 | [Build the CycleGAN Streamlit app](https://todatabeyond.com/blog/building-and-deploying-a-gan-streamlit-web-app-on-heroku-part-1) | [01_CycleGAN_Streamlit_App.ipynb](01_CycleGAN_Streamlit_App.ipynb) |
| 2 | [Prepare Heroku deployment](https://todatabeyond.com/blog/building-and-deploying-a-gan-streamlit-web-app-on-heroku-part-2) | [02_Heroku_Deployment.ipynb](02_Heroku_Deployment.ipynb) |

Run the notebooks in fresh Python 3.11 kernels. They install pinned dependencies
and use temporary workspaces. Part 1 executes both official CycleGAN generators
on all four original source images and tests Streamlit controls. Part 2 tests
local Git remotes and the real Procfile startup command. It does not log into
Heroku, provision paid resources, or claim a remote deployment.

The unavailable original Keras `.h5` models were replaced, with the author's
approval, by the [CycleGAN authors' pretrained PyTorch models](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix).
Both checkpoints are SHA-256 checked, and the architecture is revision-pinned.
The original source code remains verbatim in nonexecuting notebook appendices.
The new outputs are not reproductions of the historical Keras screenshots.
The original photographs are downloaded at an immutable source-repository commit.

## Run the app locally

From this directory:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On Windows PowerShell, use `.\.venv\Scripts\Activate.ps1` for activation.
The first model selection downloads about 44 MiB per generator to `.model-cache/`.
Do not commit model weights or uploaded files. No inference API key is needed.
For deployment, copy this directory as the application root and check current
Heroku memory/build limits and billing before creating or scaling resources.
The default CPU PyTorch install is platform-dependent; on Linux choose the
official CPU wheel index when accelerator packages are not needed.

The runtime downloads the unmodified authors' `networks.py` at commit
`2a7afba2895d52556dd5dfe07e8555ef657ced6f`. Its BSD license is included in
[CYCLEGAN-LICENSE.txt](CYCLEGAN-LICENSE.txt). These marks/models are identified
for educational use, not endorsement or a guarantee of training-data rights.
