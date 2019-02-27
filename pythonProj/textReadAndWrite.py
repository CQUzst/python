text='This is my first test.\nThis is the second line.\nThis the third line'
print(text)   # 输入换行命令\n，要注意斜杆的方向。注意换行的格式和c++一样
my_file=open('my file.txt','w')
my_file.write(text)
my_file.close()

append_text='\nThis is appended file.'  # 为这行文字提前空行 "\n"
my_file=open('my file.txt','a')   # 'a'=append 以增加内容的形式打开
my_file.write(append_text)
my_file.close()

file=open('my file.txt','r')
content=file.readlines()
for item in content:
    print (item)
