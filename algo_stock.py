#algo_stock.py
import win32com.client
import pythoncom


class login: #로그인
    login_state = 0
    
    def OnLogin(self,code,msg):
        if code == "0000":
            print("login Success:"+pw[0])
            login.login_state = 1
        else:
            print("login failure code:"+code+" msg:"+msg)
            
class XAQueryHandler_T1102: #계좌정보 조회
    query_state = 0
    
    def OnReceiveData(self,code):
        XAQueryHandler_T1102.query_state = 1

class XATradeHandler_trade: #현물 정상주문 CSPAT00600
    query_state = 0
    
    def OnReceiveData(self,code):
        XATradeHandler_trade.query_state = 1
        

pw_file = open('C:/Users/R3dzone/Desktop/stock_passwd.txt', 'r')
pw = []
for i in pw_file.readlines():
    pw.append(i.rstrip("\n"))

id = pw[0] 
pswd = pw[1]
cert_pswd = pw[2]
account_pswd = pw[3] 

XASession = win32com.client.DispatchWithEvents("XA_Session.XASession",login)
XASession.ConnectServer("127.0.0.1",20001)#XingAce
#XASession.ConnectServer("demo.ebestsec.co.kr",20001)#demo trade system
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
print(stock_name+"의 현재가:"+price)

XATrade = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery",XATradeHandler_trade)
XATrade.ResFileName = "C:/eBEST/xingAPI/Res/CSPAT00600.res"
XATrade.SetFieldData("CSPAT00600InBlock1","AcntNo",0,account)
XATrade.SetFieldData("CSPAT00600InBlock1","InptPwd",0,account_pswd)
XATrade.SetFieldData("CSPAT00600InBlock1","IsuNo",0,"000040")
XATrade.SetFieldData("CSPAT00600InBlock1","OrdQty",0,1) #거래량
XATrade.SetFieldData("CSPAT00600InBlock1","OrdPrc",0,int(price)-100)
XATrade.SetFieldData("CSPAT00600InBlock1","BnsTpCode",0,"2") #거래타입 1:매도 2:매수
XATrade.SetFieldData("CSPAT00600InBlock1","OrdprcPtnCode",0,"00")
XATrade.SetFieldData("CSPAT00600InBlock1","MgntrnCode",0,"000")
XATrade.SetFieldData("CSPAT00600InBlock1","LoanDt",0,"")
XATrade.SetFieldData("CSPAT00600InBlock1","OrdCndiTpCode",0,"")
print(XATrade.Request(0))

while XATrade.query_state == 0:
    pythoncom.PumpWaitingMessages()
    
ord_num = XATrade.GetFieldData("CSPAT00600OutBlock2","OrdNo",0)
print("현물 매수주문 요청:주문번호"+str(ord_num))
