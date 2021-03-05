#algo_stock.py
import win32com.client
import pythoncom


class login:
    login_state = 0
    
    def OnLogin(self,code,msg):
        if code == "0000":
            print("login OK")
            login.login_state = 1
        else:
            print("login failure")

pw_file = open('C:/Users/unknown/Desktop/stock_passwd.txt', 'r')
pw = []
for i in pw_file.readlines():
    pw.append(i.rstrip("\n"))

id = pw[0]
pswd = pw[1]
cert_pswd = pw[2] 

initXASession = win32com.client.DispatchWithEvents("XA_Session.XASession",login)
initXASession.ConnectServer("demo.ebestsec.co.kr",20001)
initXASession.Login(id,pswd,cert_pswd,0,0)

while login.login_state == 0:
    pythoncom.PumpWaitingMessages()