import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-00A9GG2\LEDUCTIEP;'
                      'Database=jobsgolike;'
                      'Trusted_Connection=yes;')


with conn:
    cursor = conn.cursor()
    cursor.execute('''  
                        UPDATE taikhoan set dang_lam = 0
                    ''')
