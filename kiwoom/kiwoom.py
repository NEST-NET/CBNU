import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
COM_CODE = "005930" # 삼성전자
COM_DATE = "20190516"
class KiwoomAPIWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 300, 500)
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.CommConnect()
        self.kiwoom.OnEventConnect.connect(self.event_connect)
        # Tran 수신시 이벤트
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)
        # TextEdit 생성
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(0, 0, 200, 200)
        self.text_edit.setEnabled(False)
        # 버튼 생성
        btn1 = QPushButton("조회", self)
        btn1.setGeometry(0, 202, 200, 60)
        btn1.clicked.connect(self.btn1_clicked)
    def btn1_clicked(self):
        self.callStockPrice()
    def callStockPrice(self):
        # 파라미터 세팅
        self.kiwoom.SetInputValue("종목코드", COM_CODE)
        self.kiwoom.SetInputValue("기준일자", COM_DATE)
        self.kiwoom.SetInputValue("수정주가구분", "0")
        # sRQName, sTrCode, nPrevNext, sScreenNo
        res = self.kiwoom.CommRqData("opt10081_주가조회", "opt10081", 0, "10081")
        if res == 0:
            print('주가 요청' + str(res))
        else:
            print('주가 요청' + str(res))
    # CallBack 함수
    def event_connect(self, nErrCode):
        if nErrCode == 0:
            self.text_edit.append("Login Success")
    # CallBack 함수
    def receive_trdata(self):
        accounts = self.kiwoom.GetLoginInfo("ACCNO")    # 내 계좌 저장
        account = accounts.split(';')
        print(account[0])
        self.kiwoom.SendOrder("시장가매수", "0101", account[0], 1, "005930", 10, 0, "03", "")    # 삼성전자 매수



if __name__ == "__main__":
    app = QApplication(sys.argv)
    kaWindow = KiwoomAPIWindow()
    kaWindow.show()
    app.exec_()