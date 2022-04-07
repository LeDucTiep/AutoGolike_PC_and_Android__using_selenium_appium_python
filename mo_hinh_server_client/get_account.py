import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-00A9GG2\LEDUCTIEP;'
                      'Database=jobsgolike;'
                      'Trusted_Connection=yes;')


def lay_taikhoan_matkhau():
    with conn:
        cursor = conn.cursor()
        cursor.execute('''  
                            select top(1) taikhoan, matkhau from TaiKhoanMatKhau
                        ''')
        for i in cursor:
            return i
print(lay_taikhoan_matkhau())