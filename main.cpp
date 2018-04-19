#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
using namespace cv;
using namespace std;


Point Center(vector<vector<Point> > contours2, int i)//得到三个方框的中心点位置
{
	int centerx = 0, centery = 0, n = contours2[i].size();
	centerx = (contours2[i][n / 4].x + contours2[i][n * 2 / 4].x + contours2[i][3 * n / 4].x + contours2[i][n - 1].x) / 4;
	centery = (contours2[i][n / 4].y + contours2[i][n * 2 / 4].y + contours2[i][3 * n / 4].y + contours2[i][n - 1].y) / 4;
	Point point1 = Point(centerx, centery);
	return point1;
}

int main(int argc, char** argv[])
{
	Mat src = imread("2.jpg", 1);
	Mat gray,src1,thresh;
	src1 = src.clone();

	cvtColor(src, gray, CV_BGR2GRAY);//先灰度化
	blur(gray, gray, Size(3, 3));//中值滤波模糊处理

	imshow("gray", gray);

	vector<vector<Point> > contours,contours2,contours3;
	vector<Vec4i> hierarchy;
	threshold(gray, thresh, 80, 255, 1);//二值化
	findContours(thresh, contours, hierarchy, CV_RETR_TREE, CHAIN_APPROX_NONE, Point(0, 0));//寻找轮廓

	
	int a,b,c,d;
	for (int i = 0; i< contours.size(); i++)//遍历轮廓
	{
		//hierarchy[i][3] != -1 [ , , ,-1],第四个数表示父轮廓
		//如果为-1标志着没有父轮廓,即表示轮廓i是最外面的轮廓
		if (hierarchy[i][3] == -1)//i是最外面的轮廓
		{
			a = hierarchy[i][2];
			d = i;
			if (a!=-1)//a是i的子轮廓，第一层子轮廓存在
			{
				b =  hierarchy[a][2];
				if (b!=-1)//b是a的子轮廓,b是i的孙轮廓，第二层子轮廓存在
				{
					c = hierarchy[b][2];
					if (c==-1)//c是重孙，第三层子轮廓不存在
					{
							contours2.push_back(contours[d]);//找到所需轮廓，将轮廓收集
					}
				}
			}
		}
	}

	vector<Moments>mu(contours2.size());//比较轮廓面积大小
	for (int i = 0; i < contours2.size(); i++)
	{
		mu[i] = moments(contours2[i], 0);
	}
	vector<Point2f>mc(contours2.size());
	double max = 0;
	double sum = 0;
	double average = 0;
	int e=0;
	for (int i = 0; i < contours2.size(); i++)
	{
		mc[i] = Point2f(static_cast<float> (mu[i].m10/mu[i].m00),static_cast<float>(mu[i].m10 / mu[i].m00));
			sum += mu[i].m00;//累加轮廓面积
	}
	average = sum / contours2.size(); //计算所有轮廓平均面积
	for (int i = 0; i < contours2.size(); i++)
	{
		mc[i] = Point2f(static_cast<float> (mu[i].m10 / mu[i].m00), static_cast<float>(mu[i].m10 / mu[i].m00));
		if (abs(mu[i].m00 - average) > max)
		{
			max = abs(mu[i].m00 - average);//查找第i个轮廓面积与平均面积差值的最大值
			e = i;//返回面积差值最大的轮廓的i值
		}
	}
	
	for (int i = 0; i < contours2.size(); i++)
	{
		cout << "【第" << i << "个轮廓的mu面积为：】" << mu[i].m00 << endl;
		if (i!=e)//排除轮廓面积差值最大的轮廓
		{
			contours3.push_back(contours2[i]);
			drawContours(src1, contours2, i, Scalar(255, 0, 0), -1);
		}
	}

	Point point[4];
	for (int i = 0; i < contours3.size(); i++)
	{
		point[i] = Center(contours3, i);//将最终比较得到的三个轮廓中心点连线
	}
		line(src1, point[0], point[1], Scalar(0, 255, 0), 2);
		line(src1, point[0], point[2], Scalar(0, 255, 0), 2);
		line(src1, point[2], point[1], Scalar(0, 255, 0), 2);

		imshow("src1", src1);
		waitKey();
		return 0;
}