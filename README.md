# kingkong

解密哥斯拉webshell管理工具流量

# Usage

1. wireshark之类的流量包
2. 导出所有http对象，放置到文件夹
3. 编辑`kingkong.py`脚本，第88行`#config`，配置获取到的样本password、key，以及刚才的文件夹路径
4. py -2 kingkong.py

**目前只支持jsp，base64+aes的payload**
