import socket
import  threading
import datetime
import select
class SockThread(threading.Thread):
    def __init__(self,socket,addr,cli_struct):
        super().__init__()
        self.socket = socket
        self.addr = addr
        self.cli_struct = cli_struct

    def disconnection_times(self):
        name = threading.current_thread().name
        now = datetime.datetime.now()
        Time = now.strftime("%Y/%m/%d %H:%M:%S "+ name +" dis_connection \n")
        ip, port = self.addr
        # 创建日志文件
        fname = str(ip) + '_' + str(port) + '.log'
        f = open(fname, 'a+')
        f.write(Time)
        f.close()
    def lose_data(self,sum,name):
        lose_data = []
        packages = self.cli_struct[0].get('package')
        sum_server = len(packages)
        for i in range(1,sum+1):
            if i not  in packages:
                lose_data.append(i)
        print('--服务端接受数据完毕----\n')
        print('客户端（%s）总共发送 %s 个数据包\n' % (name,sum))
        print('服务端总共接收到 %s 个包\n' % sum_server)
        print('丢失的数据包号为：%s\n' % lose_data)

    def run(self):
        name = threading.current_thread().name
        # self.connection_times()
        self.cli_struct[0].get('sock').append(name)
        while True:
            try:
                d = self.socket.recv(1024)
                string = str(d.decode('utf-8'))
                data = eval(string)
                print('成功接收'+self.addr+'发来的数据(data)：',data)
                # sum为包的总数，package为包号，当package=-1时 代表客户端发送完毕
                sum = data.get('sum')
                package = data.get('no')
                self.cli_struct[0].get('package').append(package)
                if package == -1:
                    self.lose_data(sum,name)
            except Exception as e:
                print(e)
                break
        print(self.cli_struct)
        self.socket.close()
        self.disconnection_times()
    def __del__(self):
        if not self.socket == None:
            self.socket.close()
def connection_times(c_addrs):
        #获取当前时间
        now = datetime.datetime.now()
        #格式化时间
        Time = now.strftime("%Y/%m/%d %H:%M:%S  connection \n")
        ip , port = c_addrs
        #创建日志文件
        fname = str(ip) + '_' + str(port) +'.log'
        f = open(fname, 'a+')
        f.write(Time)
        f.close()
def main():

    #创建套接字
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #绑定端口号 ip
    s.bind(('192.168.116.1',9999))
    #设置监听
    input = [s,]
    output=[]
    other=[]
    s.listen(5)
    while True:
        r_list,w_list,e_list = select.select(input,[],[],1)
        for coon in r_list:
            if coon == s:
                c_socket, c_addrs = coon.accept()
                input.append(c_socket)
                connection_times(c_addrs)
            else:
                data = coon.recv(1024)
                if data :
                    cli_struct = [{
                        "sock": [],
                        "addr": c_addrs,
                        "package": []
                    }]
                    t1 = SockThread(coon, c_addrs,cli_struct)
                    t1.start()
                else:
                    if coon in output:
                        output.remove(coon)
                    input.remove(coon)
if __name__ == '__main__':
    main()



