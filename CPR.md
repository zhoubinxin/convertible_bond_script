
# 转股溢价率中位数获取

## Python 环境配置

详细安装步骤参考 [Python安装与环境配置超详细保姆级教程](https://blog.csdn.net/m0_57081622/article/details/127180996)

## iFind Python 环境配置

1. [点击下载](http://ft.10jqka.com.cn/index.php?c=index&a=download) 同花顺数据接口
2. 第一次下载的用户，请您先打开文件夹内的 SuperCommand 并登录您的账号
3. 登录后，系统会要求您修复相关编程语言环境，请按照指示修复相关环境
4. 或在登录后点击工具中的环境设置选项，选中 Python 后点击确定按钮
5. 然后选中安装的 Python 路径，点击继续

## 安装 Pycharm

1. [点击下载](https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=windows&code=PCC)
2. 注意要勾选 `Add "bin" folder to the PATH`
![](pic/1.png)

3. 其他步骤点击 `next` 即可

详细安装步骤 [pycharm安装教程](https://blog.csdn.net/qq_44809707/article/details/122501118)

> 在 PyCharm 的设置 ->插件中可以安装中文插件

## 运行 Python 程序

1. 在 PyCharm 右上角点击文件 ->新建项目
![[pic/2.png]]

2. 创建完成后，在当前目录下右键创建 Python 文件
3. [下载或复制代码](https://github.com/ZhouBinxin/CPR/blob/master/CPR_1.py)
4. 安装必要的第三方库
	```bash
	pip install -r requirements.txt
	```

> 安装过慢可以考虑更换国内源 [pycharm如何更换国内镜像源](https://blog.csdn.net/Zenglih/article/details/106975435)

5. 根据需要修改代码![根据需要修改代码](#程序相关)
6. 右键运行![300](3.png)

## 程序相关  

1. `username`中填写同花顺账号，`password`中填写同花顺密码
2. `data_consider`中设置数据筛选的条件，
3. 如果仅需要一天数据，需要将 `start_date` 和 `end_date` 设置为同一天
4. `get_median()`函数用于获取转股溢价率中位数
5. `get_number()`函数获取数据如下：纯债到期收益率大于0的转债个数/当天所有转债数