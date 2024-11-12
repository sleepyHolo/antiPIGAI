# antiPIGAI
使用python浏览器自动化测试工具绕过www.pigai.org无法复制作文的困难.之前使用python模拟键盘输入以达到相同目的的程序现在被放在./old/中.[README_old.md](https://github.com/sleepyHolo/antiPIGAI/blob/main/old/README_old.md).  

## 运行环境
使用`selenium`进行浏览器自动化工作,使用`webdriver_manager`自动安装相应浏览器驱动(如果愿意手动安装驱动并配置程序的ini文件的话可以不安装这个包).这两个包均可使用pip安装.  
```
pip install selenium
pip install webdriver-manager
```  
## 命令行使用
由于目前作文搜索只能基于批改网作文id,因此需要用户首先手动获取作文id(由于一些难以确定的原因,程序获取所有作文id和名称的功能没有按预想的运行,因此id只能手动获取).  
id和作文文档是必须提供的:  
```
python ./antiPIGAI.py 12345 "hello world.txt"
```  
默认情况下作文标题将使用作文文档的名称,不过可以使用`-t`或`--title`指定标题.标题将使用str类的title方法处理,因此即使全小写也没有问题.  
程序必须配合一个配置文件工作,配置文件可以使用`--config`指定.默认情况下,配置文件使用`./antiPIGAI_cofig.ini`,也就是我在这个仓库提供的同名文件.  
默认情况下登录批改网的用户名和密码由配置文件提供,可以使用`--username`和`--password`进行覆盖.  
提供`--driver`用于指定不同于配置文件的浏览器驱动,不过所指定的浏览器必须在配置文件中出现.详情请参见'配置文件'节.  
使用`--reinstall`参数可以强制重新安装对应浏览器驱动.  
参数详细使用请参考命令行`-h`或`--help`,亦可参见源码.  
## 配置文件
### 用户配置
用户配置应该在配置文件'user'节中.  
默认浏览器由'driver'决定,模板里面随便填的edge.  
默认用户名和密码分别由'username'和'password'指定,请务必将模板里面对应值改为你的用户名和密码,因为随便填的admin和12345.  
### 浏览器配置
浏览器节的名称是`selenium.webdriver`下的相应包的名称.  
浏览器'driver'的值是`selenium.webdriver`下相应类的名称.  
浏览器'package'和'manager'分别是`webdriver_manager`下的类名和上层路径.如果不使用`webdriver_manager`的话就不必理会,另外Safari并没有单独的驱动.  
注意,测试使用的浏览器是Edge.因此可能使用其他浏览器时会出现问题,如果这样,请告诉我,非常感谢.  
