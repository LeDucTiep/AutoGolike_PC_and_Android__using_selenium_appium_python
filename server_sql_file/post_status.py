



import pyodbc
import threading

conn =pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-00A9GG2\LEDUCTIEP;'
                      'Database=jobsgolike;'
                      'Trusted_Connection=yes;')

def post(fb_id, loai_job, link_fb, status):
    with conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE BANGJOBS SET [status]="+str(status)+" WHERE fb_id = '"+fb_id+"' AND loai_job = N'"+loai_job+"' AND link_fb = '"+link_fb+"'")

def post_status(fb_id, loai_job, link_fb, status):
    x = threading.Thread(target=post, args=(fb_id, loai_job, link_fb, status))
    x.start()
    x.join()

post_status('100076681864851',	'TĂNG LIKE CHO BÀI VIẾT',	'https://www.facebook.com/325375386360597', 1)