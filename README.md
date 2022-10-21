##  python tools V1.3.2
* 不使用第三方wheel包


## 1.编写python文件

## 2. 编写setup.py文件
```Python
from setuptools import setup, find_packages

setup(
    name="jade_tools",
    version="0.1",
    keywords=("pip", "jade_tools", ""),
    description="jade_tools",
    long_description="xxx",
    license="MIT Licence",

    url="https://jadehh@live.com",
    author="jade",
    author_email="jadehh@live.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["numpy","pillow","imageio"]  # 这个项目需要的第三方库
)
```
## ３．打包为wheel文件

安装wheel
```bash
pip install wheel
```
打包wheel
```bash
pip wheel --wheel-dir=./wheel_dir ./
```
> wheel-dir 为wheel 输出文件夹，后面接项目文件夹（即包含setup.py的文件夹）


## 更新日志
* update 支持不使用图片进行打包
* update 支持python3.7进行打包
* update 路径转换无需判断路径是否真实存在
* update 打包的时候支持文件夹导入
* update 打包成AppImage时候无需icon图标
* update 加入AppImage图标为默认图标
