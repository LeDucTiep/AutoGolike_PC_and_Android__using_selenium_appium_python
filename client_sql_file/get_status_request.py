import time
import pyodbc
from threading import Thread

conn =pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-00A9GG2\LEDUCTIEP;'
                      'Database=jobsgolike;'
                      'Trusted_Connection=yes;')

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        # print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def doi_server_lam_xong(fb_id, loai_job, link_fb):
    cursor = conn.cursor()
    cursor.execute("select top(1) status from BANGJOBS where fb_id = '"+fb_id+"' and loai_job = N'"+loai_job+"' and link_fb = N'"+link_fb+"'")
    for i in cursor:
        return i[0]

def get_status_request(fb_id, loai_job, link_fb) -> int:
    while(1):
        x = ThreadWithReturnValue(target=doi_server_lam_xong, args=(fb_id, loai_job, link_fb))
        x.start()
        status = x.join()
        if(int(status)):return status
        # print(result)
        time.sleep(0.6)


print(get_status_request('100076681864851',	'TĂNG LIKE CHO BÀI VIẾT',	'https://www.facebook.com/325375386360597'))