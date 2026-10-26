# Generative Adversarial Networks series

One folder for the series notebooks and its linked table of contents.

| Part | Article | Notebook |
| --- | --- | --- |
| 1 | [A Gentle Introduction to GANs](https://todatabeyond.com/blog/a-gentle-introduction-to-generative-adversarial-networks-gans) | [Architecture](./01_GAN_Architecture.ipynb) · [Colab](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/generative-adversarial-networks/01_GAN_Architecture.ipynb) |
| 2 | [How to Train GANs](https://todatabeyond.com/blog/you-probably-know-gans-but-do-you-know-how-to-train-it) | [Training](./02_GAN_Training.ipynb) · [Colab](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/generative-adversarial-networks/02_GAN_Training.ipynb) |
| 3 | [Evaluating Generated Images](https://todatabeyond.com/blog/how-on-earth-can-we-evaluate-the-generated-images-by-gans) | Conceptual article |
| 4 | [Important GAN Models and Applications](https://todatabeyond.com/blog/overview-of-important-gan-models-and-applications) | Conceptual article |
| 5 | [Building and Training a GAN from Scratch](https://todatabeyond.com/blog/building-and-training-gan-model-from-scratch-in-python) | [Full tutorial](./05_GAN_From_Scratch.ipynb) · [Colab](https://colab.research.google.com/github/To-Data-Beyond/Generative-AI-Techanical-Tutorials/blob/main/series/generative-adversarial-networks/05_GAN_From_Scratch.ipynb) |

Run each notebook from top to bottom in a fresh Python 3.11+ kernel. Setup pins
TensorFlow 2.20.0, Keras 3.15.1 and NumPy 2.4.6. CPU is sufficient; no API key.
Part 1 checks the complete source network architectures without training.
Part 2 downloads official MNIST and executes the source batch-update examples,
plus independent repeated update/frozen-weight checks. It does not claim to
reproduce the historical 9,500-epoch source illustration. Full source code,
including original mistakes, is preserved in nonexecuting appendices.

Part 5 executes the original 1,000 random-batch training iterations on the full
Fashion-MNIST training array, saves twenty 100-image grids, and verifies both
optimizers and discriminator freezing. These are not 1,000 complete dataset
passes or reproduction of the historical 10,000-iteration source figure.
The final generator uses the author-approved tanh correction to match image
normalization. The tested 1,000-step run shows collapse; execution checks do
not establish sample quality or reproduce the historical garment examples.
All five series article destinations now use the published website routes,
both here and throughout the website series navigation.
