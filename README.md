# JSFinder GUI

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

JSFinder GUI是基于原版[JSFinder](https://github.com/Threezh1/JSFinder)命令行工具开发的图形界面版本，用于从网页和JavaScript文件中提取URL和子域名。

## ✨ 功能特点

- 🖥️ **现代化GUI界面** - 基于tkinter开发的用户友好界面
- 🔍 **多种扫描模式** - 支持URL扫描和文件批量扫描
- 🚀 **深度扫描** - 可以递归扫描页面中的链接
- 📄 **JS文件分析** - 专门针对JavaScript文件的URL提取
- 💾 **结果导出** - 支持将结果保存到文件
- 📊 **实时进度** - 实时显示扫描进度和日志
- 🏷️ **分类显示** - 分别显示URLs和子域名
- 📦 **一键打包** - 支持打包为独立EXE文件

## 🎯 预览截图

![](https://sm.ms/image/Lf3mwNPFST4lVtQ)

## 安装要求

- Python 3.6+
- requests
- beautifulsoup4
- urllib3

## 使用说明

### 扫描模式

#### URL扫描
1. 选择"URL扫描"模式
2. 输入目标URL（如：https://example.com）
3. 可选：输入Cookie信息用于认证
4. 选择扫描选项：
   - **深度扫描**：递归扫描页面中的所有链接
   - **JS文件扫描**：专门分析JavaScript文件

#### 文件扫描
1. 选择"文件扫描"模式
2. 选择包含URL列表的文本文件
3. 文件格式：每行一个URL
4. 选择是否进行JS文件扫描

### 扫描选项

- **深度扫描**：会访问目标页面中的所有链接，进行递归扫描
- **JS文件扫描**：专门分析JavaScript文件中的URL模式

### 输出设置

- **保存URLs到文件**：将发现的所有URL保存到指定文件
- **保存子域名到文件**：将提取的子域名保存到指定文件

### 结果查看

扫描结果会在三个标签页中显示：

1. **URLs** - 发现的所有URL列表
2. **子域名** - 提取的子域名列表  
3. **扫描日志** - 详细的扫描过程日志

## 功能按钮

- **开始扫描** - 启动扫描任务
- **停止扫描** - 中止正在进行的扫描
- **清空结果** - 清除所有显示的结果
- **导出结果** - 将所有结果导出到文件

## 文件结构

```
JSFinder_GUI/
├── JSFinder.py          # 原版JSFinder核心逻辑
├── JSFinder_GUI.py      # GUI主程序
├── requirements.txt     # 依赖列表
├── start_gui.bat       # Windows启动脚本
└── README.md           # 说明文档
```

## 使用示例

### 扫描单个网站
1. 选择"URL扫描"
2. 输入：`https://example.com`
3. 勾选"深度扫描"
4. 点击"开始扫描"

### 批量扫描
1. 准备文件`urls.txt`，内容如下：
```
https://site1.com
https://site2.com
https://site3.com
```
2. 选择"文件扫描"
3. 选择`urls.txt`文件
4. 点击"开始扫描"

## 注意事项

- 深度扫描可能耗时较长，请耐心等待
- 某些网站可能需要设置Cookie才能正常访问
- 建议在良好的网络环境下使用
- 请遵守目标网站的robots.txt和相关法律法规

## 故障排除

### 常见问题

1. **提示缺少依赖库**
   - 运行：`pip install -r requirements.txt`

2. **无法访问某些网站**
   - 检查网络连接
   - 尝试设置Cookie
   - 某些网站可能有反爬虫机制

3. **扫描结果为空**
   - 检查URL是否正确
   - 确认目标网站可正常访问
   - 尝试不同的扫描选项

## 致谢

- 原版JSFinder作者：[Threezh1](https://threezh1.github.io/)
- 正则表达式来源：[LinkFinder](https://github.com/GerbenJavado/LinkFinder)

## 许可证

本项目遵循原版JSFinder的许可证条款。
