import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
# 创造散点图
x_data = np.random.rand(100).astype(np.float32)
y_data = x_data*0.1 + 0.3
#可视化
# fig = plt.figure()
# ax1 = fig.add_subplot(1, 1, 1)
# ax1.scatter(x_data, y_data)
# plt.show()
#w和b初始化
Weights = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
biases = tf.Variable(tf.zeros([1]))

y = Weights*x_data + biases
loss = tf.reduce_mean(tf.square(y-y_data))
optimizer = tf.train.GradientDescentOptimizer(0.1)
train = optimizer.minimize(loss)
init = tf.global_variables_initializer()  # 替换成这样就好
sess = tf.Session()
sess.run(init)          # Very important

for step in range(2001):
    sess.run(train)
    if step % 20 == 0:
        print(step, sess.run(Weights), sess.run(biases))
