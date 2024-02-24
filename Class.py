import re

import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="chtdttt"
)

#lấy và xử lý dữ liệu
class ConvertData:
    
    def __init__(self):
        self.benh = []
        self.trieuchung = []
        self.dicFc = [] #lưu trữ các bệnh có cùng trieu chung (suy diễn tiến)
        self.dicBc = [] #lưu trữ các triệu chứng cùng 1 bệnh (suy diễn lùi)
        self.dicTc = [] #lưu trữ các triệu chứng theo bệnh
    
    #  Lấy dữ liệu bảng bệnh
    def convertbenh(self):
        db_benh = mydb.cursor()
        db_benh.execute("SELECT * FROM chtdttt.benh")
        out_benh = db_benh.fetchall()
        dic_benh = {}
        for i in out_benh:
            dic_benh['idBenh'] = i[0]
            dic_benh['tenBenh'] = i[1]
            dic_benh['moTa'] = i[2]
            dic_benh["nguyenNhan"] = i[3]
            dic_benh['loiKhuyen'] = i[4]
            self.benh.append(dic_benh)
            dic_benh = {}

    # Lấy dữ liệu từ bảng trieuchung
    def converttrieuchung(self):
        db_trieuchung = mydb.cursor()
        db_trieuchung.execute("SELECT * FROM chtdttt.trieuchung;")
        out_trieuchung = db_trieuchung.fetchall()
        dic_trieuchung = {}
        for i in out_trieuchung:
            dic_trieuchung['idTrieuChung'] = i[0]
            dic_trieuchung['noiDung'] = i[1]
            self.trieuchung.append(dic_trieuchung)
            dic_trieuchung = {}

    # lấy dữ liệu các bệnh có cùng triệu chứng 
    def getfc(self):
        db_fc = mydb.cursor()
        db_fc.execute(
            "select idsuydien, luat.idluat, idtrieuchung, idbenh, trangThai from suydien, luat where suydien.idluat=luat.idluat and trangThai='1' order by idtrieuchung")
        fc = db_fc.fetchall()
        s = [] #lưu triệu chứng
        d = [] #lưu bệnh
        for i in range(len(fc)):
            s.append(fc[i][2])
            d.append(fc[i][3])

        tc = s[0]
        benh = []
        dic_fc = {}
        for i in range(len(s)):
            if s[i] == tc:
                benh.append(d[i])
            else:
                dic_fc['trieuchung'] = tc
                dic_fc['benh'] = benh
                tc = s[i]
                self.dicFc.append(dic_fc)
                benh = []
                benh.append(d[i])
                dic_fc = {}
    
    def groupfc(self):
        res = []
        for i in self.dicFc:
            for j in range(len(i['benh'])):
                res.append([i['benh'][j], i['trieuchung']])
        return res
    
    #lưu trữ các triệu chứng cùng 1 bệnh
    def getbc(self):
        db_bc = mydb.cursor()
        db_bc.execute("select idsuydien, luat.idluat, idtrieuchung, idbenh, trangthai from suydien, luat where suydien.idluat=luat.idluat and trangThai='0' order by idbenh")
        fc = db_bc.fetchall()
        rule = []#luật
        s = []#triệu chứng
        d = []#bệnh
        for i in range(len(fc)):
            rule.append(fc[i][1])
            s.append(fc[i][2])
            d.append(fc[i][3])
        
        vtrule = rule[0]
        tc = []
        benh = None
    
        dicbc = {}
        for i in range(len(rule)):
            if rule[i] == vtrule:
                tc.append(s[i])
                benh = d[i]
            else:
                dicbc['rule'] = vtrule
                dicbc['benh'] = benh
                dicbc['trieuchung'] = tc
                vtrule = rule[i]
                self.dicBc.append(dicbc)
                benh = d[i]
                tc = []
                tc.append(s[i])
                dicbc = {}

    def groupbc(self):
        temp = []
        for i in self.dicBc:
            t = []
            t.append(i['benh'])
            for j in i['trieuchung']:
                t.append(j)
            temp.append(t)
        return temp

    # lưu trữ các triệu chứng trong bệnh
    def gettrieuchung(self):
        db_trieuchung=mydb.cursor()
        db_trieuchung.execute("SELECT * FROM chtdttt.suydien order by idbenh")
        dttc=db_trieuchung.fetchall()
        benh=[]
        tc=[]
        rule=[]
        for i in dttc:
            benh.append(i[1])
            tc.append(i[3])
            rule.append(i[2])
        vtbenh=benh[0]
        lstc=[]
        dirtc={}
        
        for i in range(len(benh)):
            if benh[i]==vtbenh:
                lstc.append(tc[i])
            else:
                dirtc[vtbenh]=sorted(set(lstc))
                lstc=[]
                vtbenh=benh[i]
                lstc.append(tc[i])
        dirtc[vtbenh]=sorted(set(lstc))
        self.dicTc=dirtc
        return self.dicTc
    
    #Tìm bệnh dựa trên id
    def get_benh_by_id(self, id_benh):
        for i in self.benh:
            if i["idBenh"] == id_benh:
                return i
        return 0
    
    #tìm triệu chứng dựa trên id
    def get_trieuchung_by_id(self, id_trieuchung):
        for i in self.trieuchung:
            if i["idTrieuChung"] == id_trieuchung:
                return i
        return 0

#kiểm soát đầu vào
class Validate:
    def __init__(self) -> None:
        pass

    def validate_input_number_form(self,value):
        while (1):
            valueGetRidOfSpace = ''.join(value.split(' '))
            check = valueGetRidOfSpace.isnumeric()
            if (check):
                return valueGetRidOfSpace
            else:
                print("*Bot: Bạn vui lòng nhập một số nhé!")
                value = input('*User: ')

    def validate_phonenumber(self,value):
        while (1):
            valueGetRidOfSpace = ''.join(value.split(' '))
            check = valueGetRidOfSpace.isnumeric()
            if (check and len(value)==10):
                return valueGetRidOfSpace
            else:
                print("*Bot: Số điện thoại chưa đúng định dạng. Bạn vui lòng nhập số điện thoại!")
                value = input("*User: ")


    def validate_email(self, email):
        while (1):
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

            if (re.fullmatch(regex, email)):
                # print("Chatbot:Tôi đã nhận được thông tin Email của bạn")
                return email

            else:
                print("*Bot: Email chưa đúng định dạng. Bạn vui lòng nhập lại email!")
                email = input("*User: ")

    def validate_name(self, value):
        while (1):
            valueGetRidOfSpace = ''.join(value.split(' '))

            check = valueGetRidOfSpace.isalpha()
            if (check):
                # print("Tôi đã nhận được thông tin Tên của bạn")
                return value
            else:
                print("*Bot: Tên chưa được nhập đúng định dạng. Bạn vui lòng nhập lại tên ! ")
                value = input("*User:")

    def validate_binary_answer(self, value):
        acceptance_answer_lst = ['1', 'y', 'yes', 'co', 'có']
        decline_answer_lst = ['0', 'n', 'no', 'khong', 'không']
        value = value+''
        while (1):
            if (value) in acceptance_answer_lst:
                return True
            elif value in decline_answer_lst:
                return False
            else:
                print(
                    "*Bot: Câu trả lời không hợp lệ. Bạn vui lòng nhập lại câu trả lời")
                value = input("*User: ")


class User:
    def __init__(self, name, phoneNumber, email):
        self.name = name
        self.phoneNumber = phoneNumber
        self.email = email

    def __str__(self):
        return f"{self.name} - {self.phoneNumber} - {self.email}"

        
# Tìm vị trí các rule có bệnh là goal
def searchindexrule(rule,goal):
    index=[]
    for r in range(len(rule)):
        if rule[r][0]==goal:
            index.append(r)
    return index
# Lấy các triệu chứng theo sự suy diễn để giảm thiểu câu hỏi
# và  đánh dấu các luật đã được duyệt qua để bỏ qua những luật có cùng câu hỏi vào
def get_s_in_d(answer,goal,rule,d,flag):
    result=[]
    index=[]
    if flag==1:
        for i in range(len(rule)):
            if (rule[i][0]==goal) and (answer in rule[i]) and (i in d):
                for j in rule[i]:
                    if j[0]=='S':
                        result.append(j)
                        # result=set()
    else:
        for i in range(len(rule)):
            if (rule[i][0]==goal) and (answer in rule[i]): index.append(i)
            if (rule[i][0]==goal) and (answer not in rule[i]) and (i in d):
                for j in rule[i]:
                    if j[0]=='S':
                        result.append(j)        

    return sorted(set(result)),index

