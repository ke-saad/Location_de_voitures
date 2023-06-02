import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMainWindow,QLabel,QFileDialog,QPushButton,QListWidget
import sqlite3

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("Welcome_page.ui", self)
        self.login.clicked.connect(self.gotologin)
        self.create.clicked.connect(self.gotosignup)

    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    
    def gotosignup(self):
        signup = SignupScreen()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("Login_page.ui", self)
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login2.clicked.connect(self.loginFunction)
        self.create.clicked.connect(self.gotosignup)

    def loginFunction(self):
        user=self.Email.text()
        password=self.Password.text()
        if len(user)==0 or len(password)==0:
            self.success.setText("")
            self.error.setText("Fill all the blanks")
        elif user=='admin' and password=='admin':
            self.gotoadmin1()
        else:
            conn = sqlite3.connect("verification.sqlite")
            cur1 = conn.cursor()
            query = "SELECT Email, Password FROM login WHERE Email ='"+user+"'"
            cur1.execute(query)
            result = cur1.fetchone()
            print(result)
            if result is None:
                self.success.setText("")
                self.error.setText("incorrecte email")
            else:
                if user==result[0] and password==result[1]:
                    #self.error.setText("")
                    #self.success.setText("Successfuly connected")
                    self.gotouser()

                elif password != result[1]:
                    self.success.setText("")
                    self.error.setText("incorrecte password")
             
    def gotosignup(self):
        signup = SignupScreen()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def gotoadmin1(self):
        admin1 = Admin1()
        widget.addWidget(admin1)
        widget.setCurrentIndex(widget.currentIndex() + 1) 
    def gotouser(self):
        conn = sqlite3.connect("verification.sqlite")
        cur1 = conn.cursor()
        query = "SELECT Nom, Email FROM login WHERE Email ='"+self.Email.text()+"'" 
        cur1.execute(query)
        result = cur1.fetchone()
        conn.close()

        if result is not None:
            username = result[0]
            user = User1(username)
            widget.addWidget(user)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        


class User1(QDialog):
    def __init__(self, username):
        super(User1, self).__init__()
        loadUi("client_page.ui", self)

        output_text = f"Welcome {username}"
        self.username.setText(output_text)
       

    

class Admin1(QDialog):
    def __init__(self):
        super(Admin1, self).__init__()
        loadUi("Adminfirst_page.ui", self)
        self.ajout.clicked.connect(self.gotoadmin2) 
        self.liste_v.clicked.connect(self.liste_voiture)
        self.list_c.clicked.connect(self.liste_clients)
    def gotoadmin2(self):
        admin2 = Admin2()
        widget.addWidget(admin2)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def liste_voiture(self):
        liste_v = Liste_v()
        widget.addWidget(liste_v)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def liste_clients(self):
        liste_c = Liste_c()
        widget.addWidget(liste_c)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class Admin2(QDialog):
    def __init__(self):
        super(Admin2, self).__init__()
        loadUi("Adminsecond_page.ui", self)
        self.button = self.findChild(QPushButton, "Image")
        self.label = self.findChild(QLabel, "test")
        self.Ajouter.clicked.connect(self.Ajouter_voiture)
        self.button.clicked.connect(self.clicker)
        self.binary_code = None
    
    def clicker(self):
        fname = QFileDialog.getOpenFileName(self, "Open File", "", "All files (*);;Python Files(*.py)")
        if fname[0] :
            self.error.setText("")
            self.fname = fname[0]
            with open(self.fname, "rb") as binary_image:
                self.binary_code = binary_image.read()
                print(self.binary_code)
        else:
            self.error.setText("error")

    def Ajouter_voiture(self):
        Marque_v = self.Marque.text()
        Modele_v = self.Modele.text()

        Type_v = self.Type_carburant.text()
        Place_v = self.Nombres_place.text()
        Transmission_v = self.Transmission.text()
        Prix_v = self.Prix_loc.text()
        Dispo_v = self.Disponibilite.text()

        conn = sqlite3.connect("verification.sqlite")
        cur1 = conn.cursor()
        user_info = [Marque_v, Modele_v, self.binary_code, Type_v, Place_v, Transmission_v, Prix_v, Dispo_v]
        cur1.execute('INSERT INTO voiture(Marque, Modele, Image, Type_carburant, Nombre_places, Transmission, Prix_location, Disponibilite) VALUES(?,?,?,?,?,?,?,?)', user_info)
        conn.commit()
        conn.close()

        
            

        





class Liste_v(QDialog):
    def __init__(self):
        super(Liste_v, self).__init__()
        loadUi("Liste_voiture.ui", self)
        self.loaddata()
    def loaddata(self):
        conn = sqlite3.connect("verification.sqlite")
        cur1 = conn.cursor()
        query = "SELECT * FROM voiture"
        self.Listev.setRowCount(5)
        tablerow = 0
        for r in cur1.execute(query):
            self.Listev.setItem(tablerow,0,QtWidgets.QTableWidgetItem(str(r[0])))
            self.Listev.setItem(tablerow,1,QtWidgets.QTableWidgetItem(str(r[1])))
            self.Listev.setItem(tablerow,2,QtWidgets.QTableWidgetItem(str(r[2])))
            self.Listev.setItem(tablerow,3,QtWidgets.QTableWidgetItem(str(r[3])))
            self.Listev.setItem(tablerow,4,QtWidgets.QTableWidgetItem(str(r[4])))
            self.Listev.setItem(tablerow,5,QtWidgets.QTableWidgetItem(str(r[5])))
            self.Listev.setItem(tablerow,6,QtWidgets.QTableWidgetItem(str(r[6])))
            self.Listev.setItem(tablerow,7,QtWidgets.QTableWidgetItem(str(r[7])))
            self.Listev.setItem(tablerow,8,QtWidgets.QTableWidgetItem(str(r[8])))
            tablerow+=1
        

class Liste_c(QDialog):
    def __init__(self):
        super(Liste_c, self).__init__()
        loadUi("Liste_clients.ui", self)
        self.loaddata()
    def loaddata(self):
        conn = sqlite3.connect("verification.sqlite")
        cur2 = conn.cursor()
        query1 = "SELECT * FROM login"
        self.listec.setRowCount(20)
        tablerow1 = 0
        for r2 in cur2.execute(query1):
            self.listec.setItem(tablerow1,0,QtWidgets.QTableWidgetItem(str(r2[0])))
            self.listec.setItem(tablerow1,1,QtWidgets.QTableWidgetItem(str(r2[1])))
            self.listec.setItem(tablerow1,2,QtWidgets.QTableWidgetItem(str(r2[2])))
            self.listec.setItem(tablerow1,3,QtWidgets.QTableWidgetItem(str(r2[3])))
            self.listec.setItem(tablerow1,4,QtWidgets.QTableWidgetItem(str(r2[4])))
            self.listec.setItem(tablerow1,5,QtWidgets.QTableWidgetItem(str(r2[5])))
            self.listec.setItem(tablerow1,6,QtWidgets.QTableWidgetItem(str(r2[6])))
            self.listec.setItem(tablerow1,7,QtWidgets.QTableWidgetItem(str(r2[7])))
            tablerow1+=1



class SignupScreen(QDialog):
    def __init__(self):
        super(SignupScreen, self).__init__()
        loadUi("Createaccount_page.ui", self)
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.CPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup.clicked.connect(self.SignupFunction)
    
    def SignupFunction(self):
        nom_c=self.Nom.text()
        prenom_c=self.Prenom.text()
        cin_c=self.Cin.text()
        adress_c=self.Adress.text()
        tel_c=self.Tel.text()
        email_c=self.Email.text()
        password_c=self.Password.text()
        CPassword_c=self.CPassword.text()
        if len(nom_c)==0 or len(prenom_c)==0 or len(cin_c)==0 or len(adress_c)==0 or len(tel_c)==0 or len(email_c)==0 or len(password_c)==0 or len(CPassword_c)==0:
            self.success.setText("")
            self.error.setText("Fill all the blanks")
        elif CPassword_c != password_c:
            self.success.setText("")
            self.error.setText("Passwords does not match")
        else:
            conn = sqlite3.connect("verification.sqlite")
            cur1 = conn.cursor()
            user_info=[nom_c,prenom_c,cin_c,adress_c,tel_c,email_c,password_c]
            cur1.execute('INSERT INTO login(Nom,Prenom,Cin,Adress,Tel,Email,Password) VALUES(?,?,?,?,?,?,?)',user_info)
            conn.commit()
            self.error.setText("")
            self.success.setText("Added successfully")
            conn.close()
            
            



    
            
            
            


app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(391)
widget.setFixedWidth(651)
widget.setWindowTitle("Gestion de location de voiture")
widget.show()
try:
    sys.exit(app.exec())
except:
    print("Exiting")
