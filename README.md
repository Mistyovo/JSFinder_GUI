# JSFinder GUI

![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

JSFinder GUI 是基于经典的 [JSFinder](https://github.com/Threezh1/JSFinder) 命令行工具开发的现代化图形界面版本。这是一个专业的网络安全工具，用于从网页和JavaScript文件中智能提取URL、子域名等敏感信息，广泛应用于渗透测试、漏洞挖掘和网络侦察场景。

## ✨ 核心功能

- 🖥️ **直观的GUI界面** - 基于tkinter构建的现代化用户界面，操作简单直观
- 🎯 **双重扫描模式** - 支持单URL深度扫描和批量文件扫描两种模式
- � **智能深度扫描** - 递归分析页面中的所有链接，发现隐藏的资源路径
- 📄 **JavaScript专项分析** - 使用高级正则表达式深度挖掘JS代码中的URL模式
- 🌐 **子域名发现** - 自动提取和识别目标域名的所有子域名
- 💾 **灵活的结果导出** - 支持分类保存URLs和子域名到独立文件
- 📊 **实时监控反馈** - 实时显示扫描进度、统计信息和详细日志
- 🔧 **Cookie支持** - 支持自定义Cookie进行认证访问
- 📦 **独立部署** - 支持打包为独立可执行文件，无需Python环境

## 🎯 界面预览

![JSFinder GUI界面](https://s2.loli.net/2025/08/07/Lf3mwNPFST4lVtQ.png)

*现代化的图形用户界面，支持多标签页结果展示和实时扫描监控*

## 🛠️ 环境要求

### 系统要求
- **操作系统**: Windows 7+ / Linux / macOS 10.12+
- **Python版本**: Python 3.6 或更高版本
- **内存**: 建议512MB以上可用内存

### 依赖库
```
requests>=2.25.1        # HTTP请求处理
beautifulsoup4>=4.9.3   # HTML解析
urllib3>=1.26.0         # URL处理和连接池管理
```

## 🚀 快速开始

### 方法一：直接运行（推荐）

1. **克隆项目**
```bash
git clone https://github.com/Mistyovo/JSFinder_GUI.git
cd JSFinder_GUI
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **启动程序**
```bash
python JSFinder_GUI.py
```

### 方法二：构建独立可执行文件

1. **安装PyInstaller**
```bash
pip install pyinstaller
```

2. **构建EXE文件**
```bash
pyinstaller JSFinder_GUI.spec
```

3. **运行程序**
```bash
./dist/JSFinder_GUI/JSFinder_GUI.exe
```

## 📖 详细使用指南

### 扫描模式说明

#### 🌐 URL扫描模式
针对单个目标网站进行深度分析：

1. **基础设置**
   - 在"目标URL"框中输入完整的URL（如：`https://example.com`）
   - 可选：在"Cookie"框中输入认证信息（格式：`name=value; name2=value2`）

2. **扫描选项**
   - ✅ **深度扫描**：递归分析页面中发现的所有链接
   - ✅ **JS文件扫描**：专门分析JavaScript文件中的URL模式

#### 📁 文件扫描模式
对多个目标进行批量扫描：

1. **准备URL列表文件**
   ```
   https://site1.com
   https://site2.com/page
   https://site3.com/api
   ```

2. **选择文件**
   - 点击"浏览"按钮选择包含URL列表的文本文件
   - 支持的文件格式：`.txt`, `.list`, `.urls`

### 🔧 高级功能配置

#### 扫描选项详解

- **深度扫描**: 启用后会递归访问发现的所有内部链接，进行多层次分析
- **JS文件扫描**: 使用专业正则表达式模式识别JavaScript代码中的隐藏URL

#### 输出设置

- **保存URLs到文件**: 将所有发现的URL按分类保存到指定文件
- **保存子域名到文件**: 将提取的子域名去重后保存到独立文件

### 📊 结果解读

扫描完成后，结果将在三个标签页中分类显示：

1. **📋 URLs标签页**
   - 显示所有发现的URL链接
   - 按类型分类（API端点、静态资源、页面链接等）

2. **🌍 子域名标签页**
   - 显示从目标中提取的所有子域名
   - 自动去重和排序

3. **📝 扫描日志标签页**
   - 详细的扫描过程记录
   - 错误信息和调试信息
   - 扫描统计和性能指标

## ⚡ 操作控制

### 功能按钮说明

- **🟢 开始扫描**: 启动扫描任务，按钮变为禁用状态
- **🔴 停止扫描**: 中止正在进行的扫描任务
- **🗑️ 清空结果**: 清除所有标签页中的扫描结果
- **📤 导出结果**: 将当前所有结果批量导出到文件

### 实时监控

- **状态指示器**: 显示当前扫描状态（就绪/扫描中/已完成）
- **进度统计**: 实时显示已发现的URL和子域名数量
- **扫描日志**: 详细记录每个扫描步骤和发现的信息

## 📁 项目结构

```
JSFinder_GUI/
├── JSFinder.py              # 核心扫描引擎（原版JSFinder逻辑）
├── JSFinder_GUI.py          # GUI主程序和界面逻辑
├── JSFinder_GUI.spec        # PyInstaller打包配置文件
├── requirements.txt         # Python依赖包列表
├── README.md               # 项目说明文档
├── build/                  # PyInstaller构建临时文件夹
└── dist/                   # 打包后的可执行文件输出目录
```

## 💡 实际应用场景

### 🔐 渗透测试
- **信息收集阶段**: 快速发现目标网站的隐藏页面和API端点
- **资产发现**: 自动化收集目标的子域名资产
- **攻击面分析**: 识别潜在的攻击入口点

### 🛡️ 安全审计
- **代码审计**: 分析前端JavaScript代码中的敏感信息泄露
- **资产盘点**: 全面梳理企业的Web资产和子域名
- **安全评估**: 发现可能存在安全风险的URL路径

### 🔍 威胁情报
- **域名监控**: 持续监控目标组织的新增子域名
- **恶意软件分析**: 提取恶意网页中的C&C服务器地址
- **钓鱼网站分析**: 分析钓鱼页面的资源结构

## 🎮 使用示例

### 示例1：单站点深度扫描
```
目标URL: https://example.com
Cookie: sessionid=abc123; csrftoken=xyz789
扫描选项: ✅深度扫描 ✅JS文件扫描
预期结果: 发现约50-200个URL，5-15个子域名
```

### 示例2：批量目标扫描
**准备targets.txt文件:**
```
https://site1.com
https://api.site2.com
https://admin.site3.com
```
```
扫描模式: 文件扫描
选择文件: targets.txt
扫描选项: ✅JS文件扫描
预期结果: 多目标综合分析结果
```

### 示例3：JavaScript代码深度挖掘
```
目标URL: https://app.example.com/assets/main.js
扫描选项: ✅JS文件扫描
预期发现: API端点、配置文件路径、隐藏功能URL
```

## ⚠️ 重要注意事项

### 🔒 法律合规
- **仅限授权测试**: 只能对自己拥有或已获得明确书面授权的目标进行扫描
- **遵守法律法规**: 严格遵守当地网络安全法律法规和相关政策
- **尊重robots.txt**: 建议在扫描前检查目标网站的robots.txt文件
- **负责任披露**: 发现安全问题时应采用负责任的披露流程

### 🌐 技术限制
- **网络环境**: 建议在稳定的网络环境下使用，避免频繁的网络中断
- **反爬虫机制**: 某些网站可能具有反爬虫保护，会限制或阻止扫描
- **扫描深度**: 深度扫描可能耗时较长，特别是对于大型网站
- **内存使用**: 大规模扫描时可能消耗较多内存，建议监控系统资源

### 🎯 最佳实践
- **合理设置扫描间隔**: 避免对目标服务器造成过大压力
- **适当使用Cookie**: 对于需要认证的页面，正确设置Cookie信息
- **结果验证**: 对扫描结果进行人工验证，避免误报
- **定期更新**: 保持工具和依赖库的最新版本

## 🔧 故障排除

### 常见问题解决方案

#### 1. 依赖库安装失败
```bash
# 问题描述：pip install 时出现错误
# 解决方案：
pip install --upgrade pip
pip install -r requirements.txt --user
# 或使用国内镜像源：
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

#### 2. 网络连接问题
```bash
# 问题描述：无法访问目标网站
# 诊断步骤：
curl -I https://target-site.com
ping target-site.com
# 解决方案：检查网络连接、防火墙设置、代理配置
```

#### 3. 扫描结果为空
- **检查URL格式**: 确保URL包含完整的协议（http://或https://）
- **验证网站状态**: 手动访问目标网站确认其可正常访问
- **调整扫描参数**: 尝试启用/禁用不同的扫描选项
- **检查权限**: 某些内容可能需要登录后才能访问

#### 4. 程序运行缓慢
- **减少扫描深度**: 对于大型网站，建议先进行浅层扫描
- **关闭不必要功能**: 如果只需要URL，可以关闭子域名扫描
- **优化系统资源**: 关闭其他占用大量内存的程序

#### 5. GUI界面异常
```bash
# 问题描述：图形界面显示异常或无法启动
# 解决方案：
# Linux系统需要安装tkinter：
sudo apt-get install python3-tk
# macOS系统：
brew install python-tk
```

## 🤝 开源协议与致谢

### 📝 许可证
本项目继承原版JSFinder的开源协议条款，采用MIT许可证发布。

### 🙏 特别致谢
- **[Threezh1](https://threezh1.github.io/)** - 原版JSFinder作者，提供了核心的URL提取算法
- **[GerbenJavado/LinkFinder](https://github.com/GerbenJavado/LinkFinder)** - 提供了JavaScript URL提取的正则表达式模式
- **Python开源社区** - 提供了强大的第三方库支持

### 🌟 贡献指南
欢迎提交Issues和Pull Requests来帮助改进这个项目：

1. **Bug报告**: 详细描述问题复现步骤和环境信息
2. **功能建议**: 提出新功能需求和改进建议
3. **代码贡献**: 遵循现有代码风格，添加适当的注释和测试

### 📞 联系方式
- **GitHub**: [https://github.com/Mistyovo/JSFinder_GUI](https://github.com/Mistyovo/JSFinder_GUI)
- **Issues**: 项目相关问题请通过GitHub Issues提交

---

> ⚡ **免责声明**: 本工具仅供网络安全研究和教育目的使用。使用者需对自己的行为负责，开发者不承担任何法律责任。请确保在合法授权的范围内使用本工具。
