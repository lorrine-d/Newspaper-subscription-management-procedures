import hashlib
from DBConnect import Database
from rich import print

'''
DROP TABLE IF EXISTS `User`;
CREATE TABLE `User` (
  `Uuid` varchar(255)  NOT NULL,
  `Name` varchar(255)  NOT NULL,
  `Admin` int  NOT NULL,
  PRIMARY KEY ( `Uuid` )
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''

class Sign(object):
    def __init__(self):
        conf = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'pw': 'dd20001102',
            'db': 'book'
        }
        self.db = Database(conf=conf)

    def salted_password(self,password):
        salt = "12345"
        def md5hex(ascii_str):
            return hashlib.md5(ascii_str.encode('ascii')).hexdigest()
        # 普通加密
        hash1 = md5hex(password)
        # 加盐加密
        hash2 = md5hex(hash1 + salt)
        return hash2

    def Login(self, login_obj):
      try:
        info = self.db.select_more_old('User', ' Name="%s" ;'%(login_obj["Name"]))
        if len(info) != 0 :
          if str(login_obj['Passwd']) == info[0]['password']:
             print('Login In!')
             self.db.close()
             return True
          else :
            print('Passwd Wrong!')
            self.db.close()
            return False
        else :
          print('No such User name!')
          self.db.close()
          return False
      except Exception as e:
        print(e)
        self.db.close()
        
    def Rigister(self, rigister_obj):
      try :
        info  = self.db.select_more_old('User', ' Name="%s" ;'%(rigister_obj["Name"]))
        if len(info) == 0:
          item = {}
          item['Name'] = rigister_obj["Name"]
          item['hpassword'] = self.salted_password(rigister_obj['Passwd'])
          item['password'] = rigister_obj['Passwd']
          item['Admin'] = str(0)  #默认不是Admin用户
          res = self.db.insert('User', item)
          if res == 0:
            print('[INFO]Rigister: ' + str(res))
            return True
          else :
            print('[ERROR]Rigister: ' + str(res))
            print('Rigister Failed')
            return False
        else :
          print('User Repeat!')
          return False
      except Exception as e:
        print(e)

if __name__ == "__main__":
    s = Sign()
    item = {
      'Name' : 'a',
      'Passwd' : '2333'
    }
    s.Rigister(item)
    item = {
      'Name' : 'mec',
      'Passwd' : '2333'
    }
    s.Login(item)