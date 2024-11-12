# antiPIGAI
If your English teacher don't allow you copy your homework on fking pigai.org, antiPIGAI can help you!  
(useless if you aren't a Chinese student)  

__English version later, i am tired.__

通过模拟键盘输入的方式将指定文件或输入输出到指定窗口(例如 批改网)

### 运行环境
PS: 如果有人看我后面就发布exe版本, 说不定还有个gui  
使用的第三方库是`pyautogui`和`pygetwindow`, 都可以使用pip安装(应该吧)  

### 命令行使用
首先, 需要手动打开需要输入的窗口. 例如, 先打开'第xxxx号作文- 批改网'之类的, 只要保证关键字出现在窗口标题就可以了.  
程序内置了命令行提示符, 在程序目录下运行
```
python antiPIGAI_old.py ./test.txt --key=批改网
```
使用`--key`输入需要检索的关键字, 默认就是'批改网'.  
需要输入一个字符串, 默认情况下将作为文件路径. 如果希望直接输入这个字符串, 请使用`--text_input`.  
可以使用`-i`或`--interval`指定输入字符间隔的时间, 单位是秒, 默认0.01.  
可以使用`-e`或`--english`锁定输入时的输入法为英文, 默认不锁定.  
__注: 最近的测试中发现使用命令行时输入法锁定似乎失效了, 在这种情况下, 请使用`--check_time`__  
可以使用`--check_time`指定开始自动输入前暂停的时间, 单位是秒, 默认为0. 这时你可以确认活动窗格确实是你需要的, 以及输入法为英文(注意, 目前程序不支持中文输入)  

### 非常不建议在程序运行过程中切换活动窗口, 我们不知道究竟会发生什么
