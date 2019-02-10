# tensorflow hello world
# run in python 3.6 tensorflow 1.12

import tensorflow as tf
import numpy as np
# 引入绘图表（为了清晰了解训练结果）
import matplotlib.pyplot as plt
# create data
# 创建一个随机的数据集
x_data = np.random.rand(100).astype(np.float32)
y_data = 4*x_data+np.random.random_sample((100,)).astype(np.float32)

# 随机初始化 权重
Weights = tf.Variable(tf.random_uniform([1], -1.0, 1.0))
biases = tf.Variable(tf.zeros([1]))

# 估计的y值
y = Weights*x_data + biases

# 估计的y和真实的y，计算cost
loss = tf.reduce_sum(tf.square(y-y_data))

# 梯度下降优化
optimizer = tf.train.GradientDescentOptimizer(0.001)  #  学习率
train = optimizer.minimize(loss)

"""
到目前为止, 我们只是建立了神经网络的结构, 还没有使用这个结构. 
在使用这个结构之前, 我们必须先初始化所有之前定义的Variable
"""
# init = tf.initialize_all_variables() # tf 马上就要废弃这种写法
init = tf.global_variables_initializer()  # 替换成这样就好

#创建会话
sess = tf.Session()
sess.run(init)          #  用 Session来 run 每一次 training 的数据.

# print (x_data)
# print (y_data)

for step in range(1000):
    sess.run(train)
    if step % 20 == 0:
        print(step, sess.run(Weights), sess.run(biases))
plt.plot(x_data, y_data, 'ro', label='train data')
plt.plot(x_data, sess.run(y), label='tain result')
plt.legend()
plt.show()
""" 
线性回归： http://www.jianshu.com/p/ecb36d1441af
梯度下降的公式推导 ： http://www.jianshu.com/p/200591639c2c
"""
