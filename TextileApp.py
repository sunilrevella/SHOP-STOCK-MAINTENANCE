import sys
import mysql.connector
from datetime import date
from PyQt5.QtWidgets import QMainWindow,QApplication
from TextileUI import *

class Textiles(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui =Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.submit.clicked.connect(self.entry)
        self.ui.arrivaldate.clicked.connect(self.arrivalDate)
        self.ui.comboBox.currentIndexChanged.connect(self.places)
        self.ui.reset.clicked.connect(self.clear)
        self.ui.exit.clicked.connect(self.exit)

        self.ui.update.clicked.connect(self.updateStock)
        self.ui.pushButton.clicked.connect(self.getDetails)
        self.ui.view.clicked.connect(self.viewStock)
        self.ui.delete_2.clicked.connect(self.deleteStock)
        

    def arrivalDate(self):
        self.date=self.ui.calendarWidget.selectedDate()
        self.ui.lineEdit_5.setText(self.date.toString("yyyy/MM/dd"))
    def places(self):
        self.places = self.ui.comboBox.currentText()
    def clear(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        self.ui.lineEdit_5.clear()
        self.ui.lineEdit_6.clear()
        self.ui.lineEdit_7.clear()
        self.ui.lineEdit_8.clear()
    def exit(self):
        sys.exit()
    def getDetails(self):
        myconn = mysql.connector.connect(host = "localhost", user = "root",password = "naveen",database = "textile")  
        cur = myconn.cursor()
        pid = int(self.ui.lineEdit.text())
        
        sql='select * from stock where id=%s'
        val=[(pid)]
        cur.execute(sql,val)
        r=cur.fetchone()
        print(r)

        self.ui.lineEdit_2.setText(str(r[1]))
        self.ui.lineEdit_3.setText(str(r[2]))
        self.ui.lineEdit_4.setText(str(r[3]))
        self.ui.lineEdit_6.setText(str(r[5]))        
        self.ui.lineEdit_7.setText(str(r[6]))
        self.ui.lineEdit_8.setText(str(r[8]))
        
        self.ui.lineEdit_5.setText(date.isoformat(r[4]))
        
        myconn.close()
    def viewStock(self):
        myconn = mysql.connector.connect(host = "localhost", user = "root",password = "naveen",database = "textile")  
        cur = myconn.cursor()
        cur.execute("select * from stock")
        res=cur.fetchall()
        self.ui.tableWidget.setRowCount(0)
        for r_no, r_data in enumerate(res):
            self.ui.tableWidget.insertRow(r_no)
            for c_no, data in enumerate(r_data):
                self.ui.tableWidget.setItem(r_no,c_no,QtWidgets.QTableWidgetItem(str(data)))
        myconn.close()
    def deleteStock(self):
        
        myconn = mysql.connector.connect(host = "localhost", user = "root",password = "naveen",database = "textile")  
        cur = myconn.cursor()
        pid = int(self.ui.lineEdit_9.text())

        sql='delete from stock where id=%s'
        val=[(pid)]
        cur.execute(sql,val)
        myconn.commit()
        myconn.close()
        QtWidgets.QMessageBox.about(self,"Success","Sucessfully Deleted")
        self.statusBar().showMessage('Sucessfully Deleted')
        self.clear()
        
    def entry(self):
        myconn = mysql.connector.connect(host = "localhost", user = "root",password = "naveen",database = "textile")  
        cur = myconn.cursor()
        pid = int(self.ui.lineEdit.text())
        pcode = self.ui.lineEdit_2.text()
        name = self.ui.lineEdit_3.text()
        price = float(self.ui.lineEdit_4.text())
        da = self.ui.lineEdit_5.text()
        vname = self.ui.lineEdit_6.text()
        vnumber = self.ui.lineEdit_7.text()
        place = self.places
        quantity = int(self.ui.lineEdit_8.text())
        
        sql="insert into stock(id,pcode,Name,price,date_of_arrival, Vendor_name, Vendor_Number, place, quantity) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
        val=(pid,pcode,name,price,da,vname,vnumber,place,quantity)
        cur.execute(sql,val)
        myconn.commit()
        myconn.close()
        QtWidgets.QMessageBox.about(self,"Success","Sucessfully Inserted")
        self.statusBar().showMessage('Sucessfully Inserted')
        self.clear()

    def updateStock(self):
        myconn = mysql.connector.connect(host = "localhost", user = "root",password = "naveen",database = "textile")  
        cur = myconn.cursor()
        
        pid = int(self.ui.lineEdit.text())
        pcode = self.ui.lineEdit_2.text()
        name = self.ui.lineEdit_3.text()
        price = float(self.ui.lineEdit_4.text())
        da = self.ui.lineEdit_5.text()
        vname = self.ui.lineEdit_6.text()
        vnumber = self.ui.lineEdit_7.text()
        place = self.places
        quantity = int(self.ui.lineEdit_8.text())

        sql='update stock set PCode=%s, Name=%s,price=%s,date_of_arrival=%s,Vendor_Name=%s,Vendor_Number=%s,Place=%s,Quantity=%s where id=%s'
        val=(pcode,name,price,da,vname,vnumber,place,quantity,pid)

        cur.execute(sql,val)
        myconn.commit()
        myconn.close()

        QtWidgets.QMessageBox.about(self,"Success","Sucessfully Updated")
        self.statusBar().showMessage('Sucessfully Updated')
        self.clear()
    
if __name__=="__main__":
    app = QApplication(sys.argv)
    w = Textiles()
    list_of_items=''
    d={}
    myconn = mysql.connector.connect(host = "localhost", user = "root",password = "naveen",database = "textile")  
    cur = myconn.cursor()
    w.show()
    sys.exit(app.exec_())
