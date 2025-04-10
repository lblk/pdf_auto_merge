## 运行Running it
```
python main.py
```
## 打包pkg and deploy to .exe
```
pyinstaller --onefile --windowed --add-data "fonts/*;fonts" main.py
```
## 操作说明
### 概览
![图片描述](images/docs/step1.png)
### 第一步：选中你要合并的文件夹
建议文件夹及其子文件夹中只包含pdf文件
![图片描述](images/docs/step2.png)
### 第二步：选择你输出的目录及文件名
![图片描述](images/docs/step3.png)
### 第三步：运行程序开始合并pdf
![图片描述](images/docs/step4.png)
### 第四步：给合并好的pdf加上目录页
![图片描述](images/docs/step5.png)

## 补充描述
如果你需要的仅仅是利用pdf书签信息自动生成目录页，只要从上述第二步开始，就能实现你想要的效果（就是不要进行第一步或者第一步选一个空文件夹，第二步选择你带书签信息的pdf，就行）
