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
    def __init__(self):
        self.XAQuery = None #XAQuery
        self.flag = False

    def get_field(self,BlockName,FieldName,Occurs):
        self.BlockName = BlockName
        self.FieldName = FieldName
        self.Occurs = Occurs

    def connect(self,tmp):
        self.XAQuery = tmp

    def OnReceiveData(self, code):
        print("code"+code)
        print("수신성공")
        self.flag = True
        print(self.BlockName+ self.FieldName)
        self.XAQuery.get_field_data(self.BlockName,self.FieldName,self.Occurs)

    def OnReceiveMessage(self, code,a,b):
        return code
        #print("쿼리 수신")

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
        self.query.connect(self)
        self.data = []

    def set_query(self,res_name,BlockName,FieldName,Occurs,Data): #TR이름, TR의 블록명 , 블록의 필드명, 반복여부,데이터
        base_addr = "C:/eBEST/xingAPI/Res/"
        self.query.ResFileName = base_addr+res_name+".res"
        self.query.SetFieldData(BlockName,FieldName,Occurs,Data)

    def request(self):
        self.query.Request(0)

    def get_field_data(self,BlockName,FieldName,Occurs): #블록명 , 블록의 필드명, 반복여부
        self.data.append(self.query.GetFieldData(BlockName,FieldName,Occurs))
        print(self.query.GetFieldData(BlockName,FieldName,Occurs))

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

    def get_account(self):
        accounts = self.session.account_find()
        print(accounts)

    def get_price(self):
        self.query = XAQuery()
        self.query.set_query("t1102","t1102InBlock","shcode", 0, "000040")
        #"t1102OutBlock", "price", 0
        self.query.request()
        print("flag = "+str(self.query.query.flag))
        #self.query.query.get_field("t1102OutBlock", "hname", 0)
        self.query.query.get_field("t1102OutBlock", "price", 0)
        #print(query.data.len)
        print("데이터 출력")
        #print(self.query.data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()


