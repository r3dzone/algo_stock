from PyQt5.QtWidgets import *
import sys
import win32com.client

pw_file = open('C:/Users/R3dzone/Desktop/stock_passwd.txt', 'r')
pw = []
for i in pw_file.readlines():
    pw.append(i.rstrip("\n"))

id = pw[0] 
pswd = pw[1]
cert_pswd = pw[2]
account_pswd = pw[3]

class XASessionHandler:
    def OnLogin(self, code, msg):
        if code == "0000":
            print("login Success:"+pw[0])
        else:
            print("login failure code:" + code + " msg:" + msg)

class XAQueryHandler:  # 계좌정보 조회
    flag = 0
    def OnReceiveData(self, code):
        print("code"+code)
        flag = 1
        print("데이터 수신")
        test = XAQuery()
        test.query_print()

    def OnReceiveMessage(self, code,a,b):
        print(code)
        print(a)
        print(b)


class XASession:
    def __init__(self):
        self.session = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionHandler)
        self.session.ConnectServer("demo.ebestsec.co.kr", 20001)

    def login(self, id, pswd, cert):
        self.session.Login(id, pswd, cert, 0, False)

    def account_find(self):
        account_list = []
        account_num = self.session.GetAccountListCount()
        print("계좌 수:" + str(account_num))
        for i in range(account_num):
            account_addr = self.session.GetAccountList(i)
            account_list.append(account_addr)
            print("계좌번호:" + account_addr)
        return account_list

class XAQuery:
    def __init__(self):
        self.query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryHandler)

    def query_example(self):
        print("쿼리 실행전")
        self.query.ResFileName = "C:/eBEST/xingAPI/Res/t1102.res"
        self.query.SetFieldData("t1102InBlock", "shcode", 0, "000040")
        self.query.Request(0)
        print("리퀘스트 보냄")

    def query_print(self):
        print("쿼리 프린트 시점")
        stock_name = self.query.GetFieldData("t1102OutBlock", "hname", 0)
        price = self.query.GetFieldData("t1102OutBlock", "price", 0)
        return stock_name + "의 현재가:" + price

# 메인 윈도우
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.session = XASession()
        self.session.login(id,pswd,cert_pswd)

        self.btn = QPushButton("계좌 조회",self)
        self.btn.move(10,10)
        self.btn.clicked.connect(self.get_account)

        self.query1 = XAQuery()
        self.btn2 = QPushButton("가격 조회",self)
        self.btn2.move(200,10)
        self.btn2.clicked.connect(self.get_price)
        
    def get_account(self):
        accounts = self.session.account_find()
        print(accounts)

    def get_price(self):
        print(self.query1.query_example())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()


