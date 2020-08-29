import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
COM_CODE = "005930" # 삼성전자
COM_DATE = "20200701" # 기준일자 600 거래일 전일 부터 현제까지 받아옴
ACC_NUM = "81437139" # 계좌 번호
class KiwoomAPIWindow(QMainWindow):
    acc_list = []
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 1000, 1000)
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.CommConnect()
        self.kiwoom.OnEventConnect.connect(self.event_connect)
        # Tran 수신시 이벤트
        self.kiwoom.OnReceiveTrData.connect(self.receive_trdata)
        self.kiwoom.OnReceiveMsg.connect(self.receive_msg)
        self.kiwoom.OnReceiveChejanData.connect(self.receive_chejan)
        # TextEdit 생성
        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(0, 0, 200, 30)
        self.text_edit.setEnabled(True)
        # TextEdit2 생성
        self.text_edit_acc = QTextEdit(self)
        self.text_edit_acc.setGeometry(202, 0, 200, 30)
        self.text_edit_acc.setEnabled(True)
        # TextEdit2 생성
        self.text_edit_info = QTextEdit(self)
        self.text_edit_info.setGeometry(0, 32, 400, 900)
        self.text_edit_info.setEnabled(True)
        # TextEdit2 생성
        self.text_edit_chejan = QTextEdit(self)
        self.text_edit_chejan.setGeometry(402, 150, 500, 800)
        self.text_edit_chejan.setEnabled(True)
        # TextEdit2 생성
        self.text_edit_code = QTextEdit(self)
        self.text_edit_code.setGeometry(404, 0, 200, 30)
        self.text_edit_code.setEnabled(True)
        self.text_edit_code.setText(COM_CODE)
        # 버튼 생성
        btn1 = QPushButton("조회", self)
        btn1.setGeometry(402, 30, 100, 30)
        btn1.clicked.connect(self.btn1_clicked)
        # 버튼 생성
        btn_order = QPushButton("거래", self)
        btn_order.setGeometry(402, 60, 100, 30)
        btn_order.clicked.connect(self.btn_order_clicked)

        self.text_edit_qtt = QTextEdit(self)
        self.text_edit_qtt.setGeometry(402, 90, 100, 30)
        self.text_edit_qtt.setEnabled(True)

        self.text_edit_qtt_str = QTextEdit(self)
        self.text_edit_qtt_str.setGeometry(502, 90, 100, 30)
        self.text_edit_qtt_str.setText("개수")
        self.text_edit_qtt_str.setEnabled(False)

        self.text_edit_price = QTextEdit(self)
        self.text_edit_price.setGeometry(402, 120, 100, 30)
        self.text_edit_price.setEnabled(True)

        self.text_edit_price_str = QTextEdit(self)
        self.text_edit_price_str.setGeometry(502, 120, 100, 30)
        self.text_edit_price_str.setText("가격")
        self.text_edit_price_str.setEnabled(False)


    def btn1_clicked(self):
        self.text_edit_info.clear()
        self.callStockPrice()
    def btn_order_clicked(self):
        self.text_edit_info.clear()
        self.sendOrder(1) #인자 : 신규매수
    def callStockPrice(self):
        # 파라미터 세팅
        self.kiwoom.SetInputValue("종목코드", self.text_edit_code.toPlainText())
        self.kiwoom.SetInputValue("기준일자", COM_DATE)
        self.kiwoom.SetInputValue("수정주가구분", "0")
        # sRQName, sTrCode, nPrevNext, sScreenNo
        res = self.kiwoom.CommRqData("opt10081_주가조회", "opt10081", 0, "10081")
        if res == 0:
            print('주가 요청 성공!!!!!!' + str(res))
        else:
            print('주가 요청 실패 !!!!!!' + str(res))

    def sendOrder(self, order_type):
        hogaGB = '00' #지정가:00 , 시장가:03
        qtt_str = self.text_edit_qtt.toPlainText()
        price_str = self.text_edit_price.toPlainText()

        if (qtt_str == ""):
            self.text_edit_info.setText("Order Error! 정보 부족!")
            return
        qtt = int(qtt_str)
        price = 0
        if (price_str == ""):
            hogaGB = '03';
        else:
            price = int(price_str)

        self.kiwoom.SendOrder("주식주문", "0000", self.acc_list[0], order_type, self.text_edit_code.toPlainText(), qtt, price, hogaGB, "")
    # CallBack 함수
    def event_connect(self, nErrCode):
        if nErrCode == 0:
            self.text_edit.append("Login Success")
            acc = self.kiwoom.GetLoginInfo('ACCNO')
            self.acc_list = acc.split(';')
            self.text_edit_acc.append(self.acc_list[0])
            self.acc_list.append('81437139')
            self.kiwoom.KOA_Functions(("ShowAccountWindow"), (""))

    # CallBack 함수
    def receive_trdata(self, sScrNo, sRQName, sTrCode, sRecordName, sPreNext, nDataLength, sErrorCode, sMessage, sSplmMsg):
        if sRQName == "opt10081_주가조회":
            dataCount = self.kiwoom.GetRepeatCnt(sTrCode, sRQName)
            print('총 데이터 수 : ', dataCount)
            code = self.kiwoom.GetCommData(sTrCode, sRQName, 0, "종목코드")
            print("종목코드: " + code)
            print("------------------------------")
            # 가장최근에서 10 거래일 전까지 데이터 조회
            for dataIdx in range(0, 10):
                inputVal = ["일자", "거래량", "시가", "고가", "저가", "현재가"]
                outputVal = ['', '', '', '', '', '']
                for idx, j in enumerate(inputVal):
                    outputVal[idx] = self.kiwoom.GetCommData(sTrCode, sRQName, dataIdx, j)
                for idx, output in enumerate(outputVal):
                    print(inputVal[idx] + output)
                    self.text_edit_info.append(inputVal[idx] + output)
                print('----------------')
                self.text_edit_info.append('---------------')
        if sRQName == "주식주문":
            dataCount = self.kiwoom.GetRepeatCnt(sTrCode, sRQName)
            print('주식주문 데이터수 : ', dataCount)

            for dataIdx in range(0, dataCount):
                order_num = self.kiwoom.GetCommData(sTrCode, sRQName, dataIdx, "주문번호")
                self.text_edit_info.append("trdata[" + dataIdx + "] 주문번호: " +order_num )



    def receive_msg(self, sScrNo, sRQName, sTrCode, sMsg):
        if (sRQName == "주식주문"):
            self.text_edit_info.append("Tr Code : " + sTrCode)
            self.text_edit_info.append("Message : " + sMsg)
    def receive_chejan(self, sGubun, nItemCnt, sFIdList):
        # sGubun 체결구분 접수와 체결시 '0' 국내주식 잔고 전달은 '1' 파생잔고 전달은 '4'
        self.text_edit_chejan.append(sFIdList)
        if (sGubun == '0'):
            acc = self.kiwoom.GetChejanData('9201')
            self.text_edit_chejan.append("계좌번호 : " + acc)
            pass
        elif (sGubun == '1'):
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    kaWindow = KiwoomAPIWindow()
    kaWindow.show()
    app.exec_()