import time
import pyodbc
from threading import Thread

conn = pyodbc.connect('Driver={SQL Server};'
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


def get():
    cursor = conn.cursor()
    cursor.execute("select top(1) fb_id, loai_job, link_fb,noi_dung_comment FROM BANGJOBS WHERE [status] = 0")
    for i in cursor:
        return i
    return None
def get_job():
    x = ThreadWithReturnValue(target=get)
    x.start() 
    return x.join()

result = get_job()


if(result != None):
    for i in result:
        print(i)
else:
    print('khong co job')
input()