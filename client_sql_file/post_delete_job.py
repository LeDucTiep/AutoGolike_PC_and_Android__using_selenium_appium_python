import pyodbc
import threading

conn =pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-00A9GG2\LEDUCTIEP;'
                      'Database=jobsgolike;'
                      'Trusted_Connection=yes;')

def create_post_delete(fb_id, loai_job, link_fb):
    with conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM BANGJOBS WHERE  fb_id = '"+fb_id+"' and loai_job = N'"+loai_job+"' and link_fb = N'"+link_fb+"'")

def post_delete_job(fb_id, loai_job, link_fb):
    x = threading.Thread(target=create_post_delete, args=(fb_id, loai_job, link_fb))
    x.start()
    x.join()

post_delete_job('100076681864851',	'TĂNG LIKE CHO BÀI VIẾT',	'https://www.facebook.com/325375386360597')