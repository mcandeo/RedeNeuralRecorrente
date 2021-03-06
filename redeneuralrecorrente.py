import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf #Version 1.14
import numpy as np
from sklearn.metrics import mean_absolute_error

base = pd.read_csv('bolsa.csv')
base = base.dropna()
base = base.iloc[:,1].values

print(base)
plt.plot(base)
plt.show()

periodos = 30
previsao_futura = 1

x = base[0: (len(base) - len(base) % periodos)]
x_batches = x.reshape(-1, periodos, 1)

y = base[1: (len(base) - (len(base) % periodos)) + previsao_futura]
y_batches = y.reshape(-1, periodos, 1)

x_teste = base[- (periodos + previsao_futura):]
x_teste = x_teste[:periodos]
x_teste = x_teste.reshape(-1, periodos, 1)

y_teste = base[- (periodos):]
y_teste = y_teste.reshape(-1, periodos, 1)

tf.reset_default_graph()
entradas = 1
neuronios_oculta = 100
neuronios_saida = 1

xph = tf.placeholder(tf.float32, [None, periodos, entradas])
yph = tf.placeholder(tf.float32, [None, periodos, neuronios_saida])

celula = tf.contrib.rnn.BasicRNNCell(num_units = neuronios_oculta, activation = tf.nn.relu)
celula = tf.contrib.rnn.OutputProjectionWrapper(celula, output_size=1)

saida_rnn, _ = tf.nn.dynamic_rnn(celula, xph, dtype= tf.float32)
erro = tf.losses.mean_squared_error(labels=yph, predictions=saida_rnn)
otimizador = tf.train.AdamOptimizer(learning_rate = 0.001)

treinamento = otimizador.minimize(erro)

with tf.Session() as sess:
  sess.run(tf.global_variables_initializer())

  for epoch in range(1000):
    custo = sess.run([treinamento, erro], feed_dict = {xph: x_batches, yph: y_batches})
    if epoch % 100 == 0:
      print(epoch + 1, "erro: ", custo)
  previsoes = sess.run(saida_rnn, feed_dict = {xph: x_teste})

y_teste2 = np.ravel(y_teste)
previsoes2 = np.ravel(previsoes)
mae = mean_absolute_error(y_teste2, previsoes2)

plt.subplot()
plt.plot(y_teste2, 'o--', markersize=3, color='g', label='valor real')
plt.plot(previsoes2)
plt.plot(previsoes2, 'w*', markersize=9, color='b', label='previsões')
plt.xlabel('30 dados')
plt.ylabel('valores da ação')
plt.legend()
plt.grid()
plt.show()
