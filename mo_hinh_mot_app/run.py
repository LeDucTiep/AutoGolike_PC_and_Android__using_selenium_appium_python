from client_android_mobile import Client
from server_facebook import Server_facebook
from datetime import datetime

if __name__ == '__main__':
    client = Client(1)
    server = Server_facebook()
    # bắt các Exception có thể biết được nếu như mobile bị die 
    while(1):
        # client lấy job về
        info_job = client.lay_jobs()
        # server thực hiện
        done_thao_tac = server.do(
            info_job[0], info_job[1], info_job[2], info_job[3])
        # client báo cáo job
        if(done_thao_tac):
            print("Hoan thanh: ", client.hoan_thanh(), datetime.now().hour, "giờ", datetime.now().minute,
                  "phút", datetime.now().second, "giây")
        else:
            print("Huy job: ", client.huy_job())
        # xét xem nếu có captcha hiện lên
        client.xet_cap_cha()
