
# iFind转股溢价率中位数获取

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
![[pic/教程/1.png]]

3. 其他步骤点击 `next` 即可

详细安装步骤 [pycharm安装教程](https://blog.csdn.net/qq_44809707/article/details/122501118)

> 在 PyCharm 的设置 ->插件中可以安装中文插件

## 运行 Python 程序

1. 在 PyCharm 右上角点击文件 ->新建项目
![[pic/教程/2.png]]

2. 创建完成后，在当前目录下右键创建 Python 文件
3. [下载或复制代码](https://github.com/ZhouBinxin/CPR/blob/master/iFind/iFind3.0.py)
4. 安装必要的第三方库 (以下操作二选一)
	1. 将鼠标放在爆红的代码上，点击弹出的安装软件包选项
	2. 在命令行工具 (win+R 然后输入 cmd) 中执行以下代码
	```bash
	# 安装 numpy
	pip install numpy

	# 安装 pandas
	pip install pandas
	```

> 安装过慢可以考虑更换国内源 [pycharm如何更换国内镜像源](https://blog.csdn.net/Zenglih/article/details/106975435)

```bash
# 安装 numpy，使用清华大学镜像源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple numpy

# 安装 pandas，使用阿里云镜像源
pip install -i https://mirrors.aliyun.com/pypi/simple pandas
```

1. 右键运行![300](3.png)

## 程序相关  

1. 如果仅需要一天数据，需要将 `main()` 函数中的 `start_date` 和 `end_date` 设置为同一天
2. `calculate_median()` 函数参数说明
	1. `consider_value`、`consider_blance`、`consider_issue`
		1. 当值为 `True` 时，表示筛选时使用该参数
		2. 当值为 `False` 时，表示筛选时不使用该参数
	2. 修改筛选范围  
	```python  
	# 转股价值
    consider_value = True
    max_value = 120
    min_value = 100

    # 债券余额范围
    consider_balance = False
    max_balance = 100
    min_balance = 5

    # 债券评级
    consider_issue = False
    issue = "AA+"
	```
	3. 确定筛选边界
		1. 转股价值：value_condition = (not consider_value) or (**min_value < f027_value <= max_value**)
		2. 债券余额：balance_condition = (not consider_balance) or (**min_balance < data_balance**)