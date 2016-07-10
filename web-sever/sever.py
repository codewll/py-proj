# coding: utf-8

import http.server
import sys
import os
import subprocess

'''
一个web服务器一般要按照下面的步骤工作：
    1.等待某个人连接我们的服务器并向我们发送一个HTTP请求
    2.解析该请HTTP求
    3.(*)了解该请求希望请求的内容
    4.(*)服务器根据请求抓取需要的数据（从服务器本地文件中读,或者程序(这里为python脚本)动态生成）
    5.(*)将数据格式化为请求需要的格式
    6.送回HTTP响应
其中http.sever模块已经完成了1.2.6中的工作，我们只需要在它的基础上完成3.4.5部分的
任务就行了。
'''

# HTTP header
#--------------------------------------------------------
class RequestHeadler(http.server.BaseHTTPRequestHandler):
    """处理请求并返回页面 """

    # 出错时显示的页面
    error_page = '''
        <html>
            <body>
                <h1>Error accessing {path}</h1>
                <p>{msg}</p>
            </body>
        </html>
    '''

    # 处理GET请求
    def do_GET(self):
        try:
            # 获取请求的文件完整路径
            full_path = os.getcwd() + "/web-doc" + self.path
            # "/web-doc"是默认的服务器文件目录

            #------------------ 下面根据请求的路径进行dispatch

            #路径不存在
            if not os.path.exists(full_path):
                raise ServerException("file %s not found" % self.path)

            # 路径是python脚本
            elif os.path.isfile(full_path) and full_path.endswith(".py"):
                self.run_cgi(full_path)

            #路径是html文件
            elif os.path.isfile(full_path) and full_path.endswith(".html"):
                self.handle_file(full_path,"text/html")

            # 路径是目录且包含index.html 文件
            elif os.path.isdir(full_path) and os.path.isfile(full_path + "/index.html"):
                self.handle_file(full_path + "index.html", "text/html")

            elif os.path.isfile(full_path) and full_path.endswith(".jpg"):
                self.handle_file(full_path,"image/jpg")
            else:   # 其它情况(可以拓展，如增加处理声音文件的dispatch)
                raise ServerException("Unknow object: %s" % self.path)

        except Exception as e:
            self.handle_error(e)



    # ----------- 其它辅助函数

    # auxiliary func: 处理python脚本文件
    def run_cgi(self,full_path):
        data = subprocess.check_output(["python3",full_path])
        # check_output(["程序名","程序参数"]),能给像在命令行一样执行程序和参数，并返回结果(二进制数据)。
        self.send_content(data,200,"text/html")


    # auxiliary func: 处理html文件
    def handle_file(self, full_path, file_type):
        try:
            with open(full_path,'rb') as f: # !!! 这里以二进制方式打开
                content = f.read()
            self.send_content(content,200,file_type)  # 200代表成功的状态码
        except IOError as e:
            msg = "%s can not be read: %s" % (self.path, e)
            self.handle_error(msg)


    # auxiliary func: 处理异常
    def handle_error(self, e):
        content = self.error_page.format(path = self.path, msg = e)
        self.send_content(bytes(content,'UTF-8'),404,"text/html") # content是字符串，要转成二进制数据


    # auxiliary func: 生成 HTTP header
    def send_content(self,content,status,file_type):
        self.send_response(status) #状态码
        self.send_header("Content-Type",file_type) #content的文件类型
        self.send_header("Content-Length",str(len(content))) # content大小
        self.end_headers()

        self.wfile.write(content) # !!! content必须是二进制数据





# 自定义的服务器内部异常类
#--------------------------------------------------------
class ServerException(Exception):
    """docstring for ServerException"""
    pass




# 创建服务器并运行
#--------------------------------------------------------
if __name__ == "__main__":
    serverAdderss = ('',8080)
    server = http.server.HTTPServer(serverAdderss, RequestHeadler)
    server.serve_forever()
