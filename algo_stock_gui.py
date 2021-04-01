from PyQt5.QtWidgets import *
import sys
import win32com.client
import pythoncom

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
    def __init__(self):
        self.XAQuery = None #XAQuery
        self.flag = False

    def connect(self,tmp):
        self.XAQuery = tmp

    def OnReceiveData(self, code):
        self.flag = True

class XASession:
    def __init__(self):
        self.session = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionHandler)
        self.session.ConnectServer("127.0.0.1", 20001)

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
        self.query.connect(self)

    def set_res(self,res_name):
        base_addr = "C:/eBEST/xingAPI/Res/"
        self.query.ResFileName = base_addr+res_name+".res"

    def set_query(self,BlockName,FieldName,Occurs,Data): #TR이름, TR의 블록명 , 블록의 필드명, 반복여부,데이터
        self.query.SetFieldData(BlockName,FieldName,Occurs,Data)

    def request(self):
        error_code = self.query.Request(0)
        if error_code < 0:
            print(self.query.GetErrorMessage(error_code))

        while self.query.flag == False:
            pythoncom.PumpWaitingMessages()

    def get_field_data(self,BlockName,FieldName,Occurs): #블록명 , 블록의 필드명, 반복여부
        return self.query.GetFieldData(BlockName,FieldName,Occurs)

# 메인 윈도우
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.session = XASession()
        self.session.login(id,pswd,cert_pswd)

        self.btn = QPushButton("계좌 조회",self)
        self.btn.move(10,10)
        self.btn.clicked.connect(self.get_account)

        self.btn2 = QPushButton("가격 조회",self)
        self.btn2.move(200,10)
        self.btn2.clicked.connect(self.get_price)

        self.btn3 = QPushButton("매수",self)
        self.btn3.move(10,50)
        self.btn3.clicked.connect(self.buy)

    def get_account(self):
        global account_addr
        account_addr = self.session.account_find()[0]
        print(account_addr)

    def get_price(self):
        self.query = XAQuery()
        self.query.set_res("t1102")
        self.query.set_query("t1102InBlock","shcode", 0, "000040")
        self.query.request()
        hname = self.query.get_field_data("t1102OutBlock", "hname", 0)
        global price
        price = self.query.get_field_data("t1102OutBlock", "price", 0)
        print(hname+"의 현재가격: "+price)

    def buy(self):
        XATrade = XAQuery()
        XATrade.set_res("CSPAT00600")
        XATrade.set_query("CSPAT00600InBlock1", "AcntNo", 0, account_addr)
        XATrade.set_query("CSPAT00600InBlock1", "InptPwd", 0, account_pswd)
        XATrade.set_query("CSPAT00600InBlock1", "IsuNo", 0, "000040") #주식번호
        XATrade.set_query("CSPAT00600InBlock1", "OrdQty", 0, 1)  # 거래량
        XATrade.set_query("CSPAT00600InBlock1", "OrdPrc", 0, int(price) - 100) #거래가격
        XATrade.set_query("CSPAT00600InBlock1", "BnsTpCode", 0, "2")  # 거래타입 1:매도 2:매수
        XATrade.set_query("CSPAT00600InBlock1", "OrdprcPtnCode", 0, "00")
        XATrade.set_query("CSPAT00600InBlock1", "MgntrnCode", 0, "000")
        XATrade.set_query("CSPAT00600InBlock1", "LoanDt", 0, "")
        XATrade.set_query("CSPAT00600InBlock1", "OrdCndiTpCode", 0, "")
        XATrade.request()

        ord_num = XATrade.get_field_data("CSPAT00600OutBlock2", "OrdNo", 0)
        print("현물 매수주문 요청:주문번호" + str(ord_num))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()