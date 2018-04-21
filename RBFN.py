# -*- coding: utf-8 -*-
"""
Author: zst
Description: 径向基神经网络
Github: https://github.com/CQUzst
learn from：Octavio Arriaga
Github: https://github.com/oarriaga
"""
import numpy as np
import matplotlib.pyplot as plt

class RBFN(object):

    def __init__(self, input_shape, hidden_shape, sigma = 1.0):
        """
        # 参数
            input_shape: 输入数据的维度
            hidden_shape: the number
            hidden_shape: 隐藏层节点数
            sigam是平滑因子，可以控制高斯函数的平滑度，越小越平滑
        """
        self.input_shape = input_shape
        self.hidden_shape = hidden_shape
        self.sigma = sigma
        self.centers = None
        self.weights = None

    #核函数定义为： exp（-sigma*||dist^2||）
    def _kernel_function(self, center, data_point):
        return np.exp(-self.sigma*np.linalg.norm(center-data_point)**2)

    #使用核函数计算插值矩阵，X为输入训练集
    def _calculate_interpolation_matrix(self,X):
        #初始化矩阵G的大小，行X个，列hidden_number
        G = np.zeros((X.shape[0], self.hidden_shape))
        #data_point_arg表示X的序号，data_point表示第i个数的值
        for data_point_arg, data_point in enumerate(X):
            for center_arg, center in enumerate(self.centers):
                G[data_point_arg,center_arg] = self._kernel_function(center,data_point)
        return G

    def fit(self,X,Y):
        """
        # Arguments
            X: 训练集
            Y: 结果
        """
        #对X序号进行洗牌，转化成列表形式
        random_args = np.random.permutation(X.shape[0]).tolist()
        #x是打乱的X排序
        x=[X[arg] for arg in random_args]
        #centers取打乱的x中的前hidden_shape个数
        self.centers=x[:self.hidden_shape]

        G = self._calculate_interpolation_matrix(X)
        inv_G=np.linalg.pinv(G)
        self.weights = np.dot(inv_G,Y)

    def predict(self,X):
        G = self._calculate_interpolation_matrix(X)
        predictions = np.dot(G, self.weights)
        return predictions
if __name__ == "__main__":
    x = np.linspace(0,10,100)
    y = np.cos(x)
    model = RBFN(input_shape = 1, hidden_shape = 20,sigma=1.0)
    model.fit(x,y)
    x1=np.linspace(0,12,120)
    y_pred = model.predict(x1)
    print y_pred

    plt.plot(x,y,'b-',label='real')
    plt.plot(x1,y_pred,'r-',label='fit')
    plt.legend(loc='upper right')
    plt.title('Interpolation using a RBFN')
    plt.show()