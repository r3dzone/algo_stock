#algo_stock.py
import win32com.client
import pythoncom


class login:
    login_state = 0
    
    def OnLogin(self,code,msg):
        if code == "0000":
            print("login Success:"+pw[0])
            login.login_state = 1
        else:
            print("login failure code:"+code+" msg:"+msg)
            
class XAQueryHandler_T1102:
    query_state = 0
    
    def OnReceiveData(self,code):
        XAQueryHandler_T1102.query_state = 1
        

pw_file = open('C:/Users/R3dzone/Desktop/stock_passwd.txt', 'r')
pw = []
for i in pw_file.readlines():
    pw.append(i.rstrip("\n"))

id = pw[0] 
pswd = pw[1]
cert_pswd = pw[2] 

XASession = win32com.client.DispatchWithEvents("XA_Session.XASession",login)
XASession.ConnectServer("demo.ebestsec.co.kr",20001)#demo trade system
#XASession.ConnectServer("hts.ebestsec.co.kr",20001)#real trade system
XASession.Login(id,pswd,cert_pswd,0,0)

while login.login_state == 0:
    pythoncom.PumpWaitingMessages()
    
account_num = XASession.GetAccountListCount()
print("계좌 수:"+str(account_num))

for i in range(account_num):
    account = XASession.GetAccountList(i)
    print("계좌정보:"+account)

XAQuery_T1102 = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery",XAQueryHandler_T1102)
XAQuery_T1102.ResFileName = "C:/eBEST/xingAPI/Res/t1102.res"
XAQuery_T1102.SetFieldData("t1102InBlock","shcode",0,"000040")
XAQuery_T1102.Request(0)

while XAQueryHandler_T1102.query_state == 0:
    pythoncom.PumpWaitingMessages()


stock_name = XAQuery_T1102.GetFieldData("t1102OutBlock","hname",0)
price = XAQuery_T1102.GetFieldData("t1102OutBlock","price",0)
print(stock_name+"의 현재가:"+str(price))

