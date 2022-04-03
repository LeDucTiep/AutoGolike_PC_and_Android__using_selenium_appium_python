import pyodbc
import threading

conn =pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-00A9GG2\LEDUCTIEP;'
                      'Database=jobsgolike;'
                      'Trusted_Connection=yes;')


def post(fb_id, loai_job, link_fb, noi_dung_comment):
    with conn:
        cursor = conn.cursor()
        if(noi_dung_comment):
            cursor.execute("insert into BANGJOBS(fb_id, loai_job, link_fb, noi_dung_comment, status) values ('"+fb_id+"', N'"+loai_job+"', N'"+link_fb+"', N'"+noi_dung_comment+"', 0)")
        else:
            cursor.execute("insert into BANGJOBS(fb_id, loai_job, link_fb, status) values ('"+fb_id+"', N'"+loai_job+"', N'"+link_fb+"', 0)")

def post_job(fb_id, loai_job, link_fb, noi_dung_comment = None):
    x = threading.Thread(target=post, args=(fb_id, loai_job, link_fb, noi_dung_comment))
    x.start()
    x.join()

post_job('100076379839853', 'TĂNG HAHA CHO BÀI VIẾT', 'https://www.facebook.com/702885711124789')