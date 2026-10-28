import * as tf from '@tensorflow/tfjs';

async function main() {
  let initialized = false;
  if (typeof window !== 'undefined') {
    try { initialized = await tf.setBackend('webgl'); }
    catch { initialized = false; }
  }
  if (!initialized) await tf.setBackend('cpu');
  await tf.ready();
  console.log('Backend:', tf.getBackend());

  const model = tf.sequential();
  model.add(tf.layers.dense({units: 64, activation: 'relu', inputShape: [4],
    kernelInitializer: tf.initializers.glorotUniform({seed: 42})}));
  model.add(tf.layers.dense({units: 3, activation: 'softmax',
    kernelInitializer: tf.initializers.glorotUniform({seed: 43})}));
  model.compile({optimizer: 'sgd', loss: 'categoricalCrossentropy', metrics: ['accuracy']});

  const data = tf.randomNormal([100, 4], 0, 1, 'float32', 42);
  const classIds = tf.randomUniform([100], 0, 3, 'int32', 43);
  const labels = tf.oneHot(classIds, 3);
  const labelSums = labels.sum(1);
  if (!(await labelSums.data()).every(value => value === 1)) throw Error('Invalid class labels');
  labelSums.dispose();
  classIds.dispose();
  let epochs = 0;
  const history = await model.fit(data, labels, {
    epochs: 10, shuffle: false,
    callbacks: {onEpochEnd(epoch, logs) {
      if (!Number.isFinite(logs.loss) || !Number.isFinite(logs.acc)) throw Error('Non-finite training');
      epochs++;
      console.log(`Epoch ${epoch + 1}: loss=${logs.loss.toFixed(6)}, accuracy=${logs.acc.toFixed(6)}`);
    }}
  });
  if (epochs !== 10 || history.history.loss.length !== 10) throw Error('Incomplete training');
  const prediction = model.predict(data);
  if (prediction.shape.join(',') !== '100,3' || !(await prediction.data()).every(Number.isFinite)) {
    throw Error('Invalid prediction shape or values');
  }
  const probabilities = await prediction.sum(1).data();
  if (!probabilities.every(value => Math.abs(value - 1) < 1e-5)) throw Error('Invalid probabilities');
  console.log('PASS: all 100 rows, valid one-hot labels, ten complete epochs, finite 100x3 predictions and normalized probabilities. Random labels are not a quality benchmark.');
  prediction.dispose();
  model.dispose();
  data.dispose();
  labels.dispose();
  return {backend: tf.getBackend(), epochs, rows: 100, classes: 3};
}

main().then(result => {
  console.log(JSON.stringify(result));
  if (typeof document !== 'undefined') {
    document.querySelector('#result').textContent = JSON.stringify(result, null, 2);
  }
}).catch(error => {
  console.error(error);
  if (typeof document !== 'undefined') document.querySelector('#result').textContent = 'ERROR: ' + error.message;
  else process.exitCode = 1;
});
