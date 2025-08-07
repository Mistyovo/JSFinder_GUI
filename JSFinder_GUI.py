#!/usr/bin/env python3
# coding: utf-8
# JSFinder GUI Version
# Based on original JSFinder by Threezh1

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import queue
import sys
import os
from datetime import datetime
import requests
from requests.packages import urllib3
from urllib.parse import urlparse
import re

# 直接导入BeautifulSoup和核心函数
try:
    from bs4 import BeautifulSoup
except ImportError:
    messagebox.showerror("错误", "缺少依赖库：BeautifulSoup4\n请运行：pip install beautifulsoup4")
    sys.exit(1)

# 从JSFinder模块导入函数
try:
    from JSFinder import (
        extract_URL, Extract_html, process_url, find_last, 
        find_by_url, find_subdomain, find_by_url_deep, find_by_file
    )
except ImportError:
    messagebox.showerror("错误", "无法找到JSFinder.py文件，请确保文件在同一目录下")
    sys.exit(1)

class JSFinderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("JSFinder GUI - URL和子域名提取工具")
        self.root.geometry("1000x430")
        self.root.resizable(False, False)  # 禁止调整窗口大小
        self.root.maxsize(1000, 430)  # 设置最大尺寸
        self.root.minsize(1000, 430)  # 设置最小尺寸
        
        # 禁用SSL警告
        urllib3.disable_warnings()
        
        # 创建队列用于线程间通信
        self.result_queue = queue.Queue()
        self.running = False
        
        # 设置样式
        self.setup_styles()
        
        # 创建界面
        self.create_widgets()
        
        # 启动结果检查
        self.check_queue()
        
    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置样式
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        style.configure('Section.TLabel', font=('Arial', 10, 'bold'))
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))
        
    def create_widgets(self):
        """创建主界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)  # 右侧结果区域更宽
        main_frame.rowconfigure(0, weight=1)  # 主要内容区域可伸缩
        
        # 创建左侧控制面板
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        control_frame.columnconfigure(0, weight=1)
        
        # 创建右侧结果面板
        result_panel = ttk.Frame(main_frame)
        result_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        result_panel.columnconfigure(0, weight=1)
        result_panel.rowconfigure(0, weight=1)
        
        # 输入模式选择
        mode_frame = ttk.LabelFrame(control_frame, text="扫描模式", padding="10")
        mode_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        mode_frame.columnconfigure(1, weight=1)
        
        self.mode_var = tk.StringVar(value="url")
        ttk.Radiobutton(mode_frame, text="URL扫描", variable=self.mode_var, 
                       value="url", command=self.on_mode_change).grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(mode_frame, text="文件扫描", variable=self.mode_var, 
                       value="file", command=self.on_mode_change).grid(row=0, column=1, sticky=tk.W)
        
        # URL输入区域
        self.url_frame = ttk.LabelFrame(control_frame, text="URL设置", padding="10")
        self.url_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.url_frame.columnconfigure(1, weight=1)
        
        ttk.Label(self.url_frame, text="目标URL:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.url_entry = ttk.Entry(self.url_frame, font=('Arial', 10))
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        self.url_entry.insert(0, "https://example.com")
        
        ttk.Label(self.url_frame, text="Cookie:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.cookie_entry = ttk.Entry(self.url_frame, font=('Arial', 10))
        self.cookie_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 5), pady=(5, 0))
        
        # 文件输入区域
        self.file_frame = ttk.LabelFrame(control_frame, text="文件设置", padding="10")
        self.file_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.file_frame.columnconfigure(1, weight=1)
        
        ttk.Label(self.file_frame, text="输入文件:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.file_entry = ttk.Entry(self.file_frame, font=('Arial', 10))
        self.file_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        
        self.browse_button = ttk.Button(self.file_frame, text="浏览", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=(5, 0))
        
        # 扫描选项
        options_frame = ttk.LabelFrame(control_frame, text="扫描选项", padding="10")
        options_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.deep_var = tk.BooleanVar()
        self.js_var = tk.BooleanVar()
        
        ttk.Checkbutton(options_frame, text="深度扫描", variable=self.deep_var).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="JS文件扫描", variable=self.js_var).grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        
        # 输出设置
        output_frame = ttk.LabelFrame(control_frame, text="输出设置", padding="10")
        output_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        self.save_urls_var = tk.BooleanVar()
        self.save_subdomains_var = tk.BooleanVar()
        
        ttk.Checkbutton(output_frame, text="保存URLs到文件", 
                       variable=self.save_urls_var, command=self.on_save_option_change).grid(row=0, column=0, sticky=tk.W)
        self.url_output_entry = ttk.Entry(output_frame, font=('Arial', 10))
        self.url_output_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 5))
        self.url_output_entry.insert(0, "urls_output.txt")
        
        ttk.Checkbutton(output_frame, text="保存子域名到文件", 
                       variable=self.save_subdomains_var, command=self.on_save_option_change).grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.subdomain_output_entry = ttk.Entry(output_frame, font=('Arial', 10))
        self.subdomain_output_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=(5, 0))
        self.subdomain_output_entry.insert(0, "subdomains_output.txt")
        
        # 控制按钮
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=5, column=0, pady=(5, 0))
        
        self.start_button = ttk.Button(button_frame, text="开始扫描", 
                                     command=self.start_scan, style='Action.TButton')
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="停止扫描", 
                                    command=self.stop_scan, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="清空结果", command=self.clear_results)
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.export_button = ttk.Button(button_frame, text="导出结果", command=self.export_results)
        self.export_button.pack(side=tk.LEFT)
        
        # 进度条
        self.progress = ttk.Progressbar(control_frame, mode='indeterminate')
        self.progress.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # 结果显示区域（右侧面板）
        result_frame = ttk.LabelFrame(result_panel, text="扫描结果", padding="10")
        result_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(1, weight=1)
        
        # 结果统计
        self.stats_label = ttk.Label(result_frame, text="就绪", font=('Arial', 10))
        self.stats_label.grid(row=0, column=0, sticky=tk.W)
        
        # 创建Notebook用于分页显示结果
        self.notebook = ttk.Notebook(result_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 0))
        
        # URLs标签页
        self.urls_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.urls_frame, text="URLs")
        
        # 创建带有水平和垂直滚动条的文本框
        urls_container = ttk.Frame(self.urls_frame)
        urls_container.pack(fill=tk.BOTH, expand=True)
        
        self.urls_text = tk.Text(urls_container, font=('Consolas', 9), 
                                wrap=tk.NONE, state=tk.DISABLED)
        
        # 垂直滚动条
        urls_v_scrollbar = ttk.Scrollbar(urls_container, orient=tk.VERTICAL, command=self.urls_text.yview)
        self.urls_text.configure(yscrollcommand=urls_v_scrollbar.set)
        
        # 水平滚动条
        urls_h_scrollbar = ttk.Scrollbar(urls_container, orient=tk.HORIZONTAL, command=self.urls_text.xview)
        self.urls_text.configure(xscrollcommand=urls_h_scrollbar.set)
        
        # 布局
        self.urls_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        urls_v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        urls_h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        urls_container.grid_columnconfigure(0, weight=1)
        urls_container.grid_rowconfigure(0, weight=1)
        
        # 子域名标签页
        self.subdomains_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.subdomains_frame, text="子域名")
        
        # 创建带有水平和垂直滚动条的文本框
        subdomains_container = ttk.Frame(self.subdomains_frame)
        subdomains_container.pack(fill=tk.BOTH, expand=True)
        
        self.subdomains_text = tk.Text(subdomains_container, font=('Consolas', 9), 
                                      wrap=tk.NONE, state=tk.DISABLED)
        
        # 垂直滚动条
        subdomains_v_scrollbar = ttk.Scrollbar(subdomains_container, orient=tk.VERTICAL, command=self.subdomains_text.yview)
        self.subdomains_text.configure(yscrollcommand=subdomains_v_scrollbar.set)
        
        # 水平滚动条
        subdomains_h_scrollbar = ttk.Scrollbar(subdomains_container, orient=tk.HORIZONTAL, command=self.subdomains_text.xview)
        self.subdomains_text.configure(xscrollcommand=subdomains_h_scrollbar.set)
        
        # 布局
        self.subdomains_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        subdomains_v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        subdomains_h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        subdomains_container.grid_columnconfigure(0, weight=1)
        subdomains_container.grid_rowconfigure(0, weight=1)
        
        # 日志标签页
        self.log_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.log_frame, text="扫描日志")
        
        # 创建带有水平和垂直滚动条的文本框
        log_container = ttk.Frame(self.log_frame)
        log_container.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_container, font=('Consolas', 9), 
                               wrap=tk.NONE, state=tk.DISABLED)
        
        # 垂直滚动条
        log_v_scrollbar = ttk.Scrollbar(log_container, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_v_scrollbar.set)
        
        # 水平滚动条
        log_h_scrollbar = ttk.Scrollbar(log_container, orient=tk.HORIZONTAL, command=self.log_text.xview)
        self.log_text.configure(xscrollcommand=log_h_scrollbar.set)
        
        # 布局
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        log_h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        log_container.grid_columnconfigure(0, weight=1)
        log_container.grid_rowconfigure(0, weight=1)
        
        # 初始化界面状态
        self.on_mode_change()
        self.on_save_option_change()
        
    def on_mode_change(self):
        """模式切换处理"""
        mode = self.mode_var.get()
        if mode == "url":
            self.url_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
            self.file_frame.grid_remove()
        else:
            self.file_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
            self.url_frame.grid_remove()
    
    def on_save_option_change(self):
        """保存选项变化处理"""
        self.url_output_entry.config(state=tk.NORMAL if self.save_urls_var.get() else tk.DISABLED)
        self.subdomain_output_entry.config(state=tk.NORMAL if self.save_subdomains_var.get() else tk.DISABLED)
    
    def browse_file(self):
        """浏览文件"""
        filename = filedialog.askopenfilename(
            title="选择包含URL的文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if filename:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, filename)
    
    def log_message(self, message):
        """添加日志消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # 更新界面
        self.root.update_idletasks()
    
    def update_results(self, urls, subdomains):
        """更新结果显示"""
        # 更新URLs
        self.urls_text.config(state=tk.NORMAL)
        self.urls_text.delete(1.0, tk.END)
        if urls:
            for url in urls:
                self.urls_text.insert(tk.END, url + "\n")
        self.urls_text.config(state=tk.DISABLED)
        
        # 更新子域名
        self.subdomains_text.config(state=tk.NORMAL)
        self.subdomains_text.delete(1.0, tk.END)
        if subdomains:
            for subdomain in subdomains:
                self.subdomains_text.insert(tk.END, subdomain + "\n")
        self.subdomains_text.config(state=tk.DISABLED)
        
        # 更新统计信息
        url_count = len(urls) if urls else 0
        subdomain_count = len(subdomains) if subdomains else 0
        self.stats_label.config(text=f"找到 {url_count} 个URL，{subdomain_count} 个子域名")
    
    def start_scan(self):
        """开始扫描"""
        # 验证输入
        mode = self.mode_var.get()
        if mode == "url":
            url = self.url_entry.get().strip()
            if not url:
                messagebox.showerror("错误", "请输入目标URL")
                return
            if not url.startswith(('http://', 'https://')):
                messagebox.showerror("错误", "URL必须以http://或https://开头")
                return
        else:
            file_path = self.file_entry.get().strip()
            if not file_path:
                messagebox.showerror("错误", "请选择输入文件")
                return
            if not os.path.exists(file_path):
                messagebox.showerror("错误", "文件不存在")
                return
        
        # 更新界面状态
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress.start()
        
        # 清空之前的结果
        self.clear_results()
        
        # 启动扫描线程
        scan_thread = threading.Thread(target=self.scan_worker)
        scan_thread.daemon = True
        scan_thread.start()
        
        self.log_message("开始扫描...")
    
    def stop_scan(self):
        """停止扫描"""
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress.stop()
        self.log_message("扫描已停止")
    
    def scan_worker(self):
        """扫描工作线程"""
        try:
            mode = self.mode_var.get()
            urls = None
            main_url = None
            cookie = self.cookie_entry.get().strip() or None
            
            if mode == "url":
                url = self.url_entry.get().strip()
                main_url = url
                
                if self.deep_var.get():
                    self.result_queue.put(("log", "开始深度扫描..."))
                    urls = find_by_url_deep(url, cookie=cookie)
                else:
                    self.result_queue.put(("log", "开始常规扫描..."))
                    urls = find_by_url(url, js=self.js_var.get(), cookie=cookie)
                    
            else:
                file_path = self.file_entry.get().strip()
                self.result_queue.put(("log", f"开始扫描文件: {file_path}"))
                urls = find_by_file(file_path, js=self.js_var.get())
                if urls and len(urls) > 0:
                    main_url = urls[0]
            
            if not self.running:
                return
                
            if urls:
                self.result_queue.put(("log", f"找到 {len(urls)} 个URL"))
                
                # 提取子域名
                if main_url:
                    subdomains = find_subdomain(urls, main_url)
                    self.result_queue.put(("log", f"找到 {len(subdomains)} 个子域名"))
                else:
                    subdomains = []
                
                # 保存结果
                if self.save_urls_var.get():
                    url_file = self.url_output_entry.get().strip()
                    if url_file:
                        try:
                            with open(url_file, 'w', encoding='utf-8') as f:
                                for url in urls:
                                    f.write(url + "\n")
                            self.result_queue.put(("log", f"URLs已保存到: {url_file}"))
                        except Exception as e:
                            self.result_queue.put(("log", f"保存URLs失败: {str(e)}"))
                
                if self.save_subdomains_var.get():
                    subdomain_file = self.subdomain_output_entry.get().strip()
                    if subdomain_file:
                        try:
                            with open(subdomain_file, 'w', encoding='utf-8') as f:
                                for subdomain in subdomains:
                                    f.write(subdomain + "\n")
                            self.result_queue.put(("log", f"子域名已保存到: {subdomain_file}"))
                        except Exception as e:
                            self.result_queue.put(("log", f"保存子域名失败: {str(e)}"))
                
                # 发送结果
                self.result_queue.put(("result", urls, subdomains))
            else:
                self.result_queue.put(("log", "未找到任何URL"))
                self.result_queue.put(("result", [], []))
                
        except Exception as e:
            self.result_queue.put(("log", f"扫描出错: {str(e)}"))
            self.result_queue.put(("result", [], []))
        
        finally:
            if self.running:
                self.result_queue.put(("complete",))
    
    def check_queue(self):
        """检查结果队列"""
        try:
            while True:
                item = self.result_queue.get_nowait()
                if item[0] == "log":
                    self.log_message(item[1])
                elif item[0] == "result":
                    self.update_results(item[1], item[2])
                elif item[0] == "complete":
                    self.stop_scan()
                    self.log_message("扫描完成")
        except queue.Empty:
            pass
        
        # 继续检查
        self.root.after(100, self.check_queue)
    
    def clear_results(self):
        """清空结果"""
        self.urls_text.config(state=tk.NORMAL)
        self.urls_text.delete(1.0, tk.END)
        self.urls_text.config(state=tk.DISABLED)
        
        self.subdomains_text.config(state=tk.NORMAL)
        self.subdomains_text.delete(1.0, tk.END)
        self.subdomains_text.config(state=tk.DISABLED)
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        self.stats_label.config(text="就绪")
    
    def export_results(self):
        """导出结果"""
        if not self.urls_text.get(1.0, tk.END).strip() and not self.subdomains_text.get(1.0, tk.END).strip():
            messagebox.showwarning("警告", "没有结果可导出")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = filedialog.asksaveasfilename(
            title="导出结果",
            defaultextension=".txt",
            initialname=f"jsfinder_results_{timestamp}.txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("=" * 50 + "\n")
                    f.write("JSFinder 扫描结果\n")
                    f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 50 + "\n\n")
                    
                    # 写入URLs
                    urls_content = self.urls_text.get(1.0, tk.END).strip()
                    if urls_content:
                        f.write("发现的URLs:\n")
                        f.write("-" * 20 + "\n")
                        f.write(urls_content + "\n\n")
                    
                    # 写入子域名
                    subdomains_content = self.subdomains_text.get(1.0, tk.END).strip()
                    if subdomains_content:
                        f.write("发现的子域名:\n")
                        f.write("-" * 20 + "\n")
                        f.write(subdomains_content + "\n\n")
                    
                    # 写入日志
                    log_content = self.log_text.get(1.0, tk.END).strip()
                    if log_content:
                        f.write("扫描日志:\n")
                        f.write("-" * 20 + "\n")
                        f.write(log_content + "\n")
                
                messagebox.showinfo("成功", f"结果已导出到: {filename}")
                
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {str(e)}")

def main():
    root = tk.Tk()
    app = JSFinderGUI(root)
    
    # 设置窗口关闭处理
    def on_closing():
        if app.running:
            if messagebox.askokcancel("确认", "正在扫描中，确定要退出吗？"):
                app.stop_scan()
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # 启动主循环
    root.mainloop()

if __name__ == "__main__":
    main()
