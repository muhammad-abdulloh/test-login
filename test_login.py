import os
import mysql.connector

class User:
    def __init__(self):
        self.username = None
        self.login = None
        self.password = None
        self.age = None
        self.list_login_and_password = ["login", "password"]
        self.new_login = None
        self.new_password = None
        """Bizning serverimizdan qaysidir userga va qaysidir base dan foydalanishi uchun ruhsat berishimiz kerak"""
        """Biz signup degan userga test_base degan database ga ruhsat berdik"""
        self.mydb = mysql.connector.connect(host="localhost", user="userup", password="userup21", database="test_base")
        self.mycursor = self.mydb.cursor()
        """Endi test_base ni ichiga kirdi va u yer bo'm bo'sh endi table ochish kerak
        Agarda test_base ni ichida login degan table yo'q bo'lsa uni ochsin ya'ni login degan table ochsin agrda bo'lsa ochmasin"""

        self.create_table = self.mycursor.execute("""CREATE TABLE IF NOT EXISTS login (id int(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                                          username VARCHAR(30), login VARCHAR(30),
                                          password VARCHAR(30), age int(4))""")

    """
    Endi birinchi dasturimiz ishga tushganda bizdan SignUp yoki SignIn ni so'raydi qaysi birini tanlaysiz deb 
    SignUp --> bu registratsiya qismi
    SignIn --> bu login parol terib tizimga kiradigan qismi 
    """
    def choose(self):
        self.clear_console()
        self.show_entering()
        enter = input("Tanlovni kiriting [1/2] ")
        while enter not in ['1', '2']:
            self.clear_console()
            self.show_entering()
            enter = input("Tanlovni kiriting [1/2] ")
        if enter == '1':
            self.registration()
        else:
            self.log_in()

    @staticmethod
    def show_entering():
        print("""
        1. SignUp
        2. SignIn
        """)

    """Registratsiya qismi bu"""
    def registration(self):
        self.clear_console()
        print("Bu registratsiya qismi")

        input_name = input("Ismingizni kiriting: ").strip().capitalize()
        while not input_name.isalpha() or input_name == "":
            self.clear_console()
            print("Ismingizni kiritishda hatolik bor yoki raqam aralashgan \niltmos boshqatdan kiriting")
            input_name = input("Ismingizni kiriting: ").strip().capitalize()

        input_login = input("Loginingizni kiriting: ").strip()
        while input_login == "" or self.check_login(input_login):
            self.clear_console()
            print("Logingizni kiritishda hatolik bor  \nyoki bunday foydalanuvchi bor")
            input_login = input("Loginni kiriting: ").strip()

        input_password = input("Parolingizni kiriting: ").strip()
        while input_password == "":
            self.clear_console()
            print("Parolni boshqatdan kiriting")
            input_password = input("Parolni kiriting: ").strip()

        input_coniform_password = input("Parolni ikkinchi marta takror kiriting: ").strip()
        while input_coniform_password == "" or input_password != input_coniform_password:
            self.clear_console()
            print("Ikkinchi marta parolni takrorlashda hatolik bor qaytadan kiriting")
            input_coniform_password = input("Parolni ikkinchi marta takror kiriting: ")



        input_age = input("Yoshingizni kiriting: ").strip()
        while input_age == "" or not input_age.isnumeric():
            self.clear_console()
            print("Yoshingizni kiritishda hatolik bor iltmos qaytadan kiriting")
            input_age = input("Yoshingizni kiriting: ").strip()
        input_age = int(input_age)

        self.username = input_name
        self.login = input_login
        self.password = input_password
        self.age = input_age
        self.write_db()
        self.clear_console()
        print("Tabriklaymiz siz muvaffaqiyatli ro'yxatdan o'tdingiz")

    """Loginni tekshiradigon qismi ya'ni kiritilgan login bazada bormi yoki yo'qmi shuni aniqlaydi
    bazada bo'lsa True yo'q bo'lsa False qaytadi
    """
    def check_login(self, login_user):
        self.mycursor.execute(f'SELECT * FROM login WHERE login="{login_user}"')
        result = self.mycursor.fetchall()
        if result:
            return True
        else:
            return False

    """Bunisi esa endi loginni ham parolniham ikkovini bor ligini tekshiradi"""
    def check_login_password(self, login_user, password_user):
        self.mycursor.execute(f'SELECT * FROM login WHERE login="{login_user}" AND password="{password_user}"')
        result = self.mycursor.fetchall()
        if result:
            return True
        else:
            return False
    """Endi biz Registratsiyadan o'tgandan kegin kiritgan ma'lumotlarimizni bazaga yozib boramiz"""
    def write_db(self):
        self.mycursor.execute(f'INSERT INTO login (username, login, password, age) VALUES '
                              f'("{self.username}", "{self.login}", "{self.password}", {self.age})')
        self.mydb.commit()

    """Bu bizning SignIn qismimiz ya'ni tizimga kirish qismi bu bo'limda 
    login va parol tekshiriladi va to'g'ri bo'lsa tizimga kiradi"""
    def log_in(self):
        self.clear_console()
        input_old_login = input("Loginingizni kiriting: ").strip()
        input_old_password = input("Passwordingizni kiriting: ").strip()
        while not self.check_login_password(input_old_login, input_old_password):
            self.clear_console()
            print("Loginingiz yoki parolingiz hato qaytadan kiriting")
            input_old_login = input("Loginingizni kiriting: ").strip()
            input_old_password = input("Passwordingizni kiriting: ").strip()
        self.list_login_and_password[0] = input_old_login
        self.list_login_and_password[1] = input_old_password
        # print(self.list_login_and_password)
        self.clear_console()
        print("Tizimga kirdingiz")

        print("""
        Login yoki password ingizni o'zgartirishni hohlaysizmi: 
        1. Loginni o'zgartirish.
        2. Parolni o'zgartirish.
        3. Log Out qilish.
        4. Delete account qilish.
        5. Hech narsani o'zgartirmayman.
        """)
        choose = input("Tanlovni kiriting: ").strip()

        while choose == "" or choose not in ["1", "2", "3", "4", "5"]:
            self.clear_console()
            print("Kiritishda hatolik bor takror kiriting!")
            choose = input("Tanlovni kiriting: ")
        if choose == "1":
            self.change_login()
        elif choose == "2":
            self.change_password()
        elif choose == "3":
            self.log_out()
        elif choose == "4":
            self.clear_console()
            print("Rostanham accountingizni o'chirib yubormoqchimisiz o'ylab ko'ring")
            yes_or_no = input("Yes or No [y/n]").strip().lower()
            while yes_or_no == "" or yes_or_no not in ['y', 'Y', 'n', 'N']:
                self.clear_console()
                print("To'g'ri kiritish bo'lmadi nimadur hato ketgan")
                yes_or_no = input("Yes or No [y/n]").strip().lower()
            if yes_or_no == "y":
                self.delete_account()
            elif yes_or_no == "n":
                """Yana SignIn qismiga kirib qoladi"""
                self.log_in()
        else:
            print("Gazini bosing!")

    """Loginni o'zgartiradigon qismi"""
    def change_login(self):
        self.clear_console()
        self.new_login = input("Yangi loginingizni kiriting: ").strip()
        while self.new_login == "":
            self.clear_console()
            print("Loginni kiritishda hatolik bor qaytadan kiriting: ")
            self.new_login = input("Yangi loginingizni kiriting: ").strip()

        self.mycursor.execute(f'UPDATE login SET login="{self.new_login}" '
                              f'WHERE login="{self.list_login_and_password[0]}"')
        self.mydb.commit()

    """parolni o'zgartiradigon qismi"""
    def change_password(self):
        self.clear_console()
        self.new_password = input("Yangi passwordni kiriting: ").strip()

        while self.new_password == "":
            self.clear_console()
            print("Passwordni kiritshda hatolik bor takror kiriting")
            self.new_password = input("Yangi password ni kiriting: ").strip()

        self.mycursor.execute(f'UPDATE login SET password="{self.new_password}"'
                              f'WHERE password="{self.list_login_and_password[1]}"')
        self.mydb.commit()

    """log out ya'ni tizimdan chiqib ketish bunda siz tizimdan chiqib ketasiz
    lekin ma'lumotlaringiz o'chib ketmaydi"""

    @staticmethod
    def log_out():
        exit()

    """delete_account qismi bu qismda sizning barcha ma'lumotlaringiz o'chirib tashlanadi"""
    def delete_account(self):
        self.mycursor.execute(f'DELETE FROM login WHERE login="{self.list_login_and_password[0]}"')
        self.mydb.commit()
        exit()

    @staticmethod
    def clear_console():
        os.system("clear")


user = User()
user.choose()
