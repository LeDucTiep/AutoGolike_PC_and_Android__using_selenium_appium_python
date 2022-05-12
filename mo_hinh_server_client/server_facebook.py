from concurrent.futures import thread
from selenium import webdriver as selenium_webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from threading import Thread
from datetime import datetime
import time
import docx
import random
import pyodbc
import sys

SO_DRIVER_MO_CUNG_LUC = 2
LINK_CHROMEDRIVER = r"D:\ChromeDriver\chrome_ver101\chromedriver.exe"
LINK_FOLDER_CHROMEPROFILE = "D:\\AutoGolike_PC_and_Android\\browser_profiles\\"

input_form_system = sys.argv
if(len(input_form_system) == 2):
    IS_HEADLESS = bool(int(sys.argv[1]))
else:
    IS_HEADLESS = 1


class Do_tich_cuc_hoat_dong_cua_driver:
    def __init__(self):
        self.lich_su_hoat_dong = {}

    def hoat_dong(self, id):
        self.lich_su_hoat_dong[str(id)] = datetime.now(
        ).month*1000 + datetime.now().day*24*60 + datetime.now().hour*60*60 + datetime.now().minute*60 + datetime.now().second

    def xoa_driver(self):
        delete_id = min(self.lich_su_hoat_dong, key=self.lich_su_hoat_dong.get)
        self.lich_su_hoat_dong.pop(delete_id)
        return delete_id


driver_list = {}


class Server_facebook:
    current_fb = None
    link_facebook = None
    comment_data = None
    type_of_job = None
    done_job = None
    dang_nuoi = {}

    def __init__(self):
        self.lich_su_hoat_dong = Do_tich_cuc_hoat_dong_cua_driver()

    def do(self, id_facebook, type_of_job, link_facebook, comment_data):
        print(">>> GET: ", id_facebook,
              type_of_job.lower(), link_facebook, comment_data)
        self.current_fb = id_facebook
        self.start_driver()
        self.link_facebook = link_facebook
        self.comment_data = comment_data
        self.type_of_job = type_of_job
        # kiểm tra xem sẽ làm điều gì
        self.like_share_comment_follow()
        return self.done_job
    # Giải quyết link

    def load_link(self):
        link = self.link_facebook
        vt = link.find('facebook')
        # Message: no such window: target window already closed
        driver_list[self.current_fb].switch_to.window(
            driver_list[self.current_fb].window_handles[0])
        driver_list[self.current_fb].get("https://mbasic."+link[vt:len(link)])

    def start_driver(self):
        self.lich_su_hoat_dong.hoat_dong(self.current_fb)
        # nếu là fb đã mở sẵn rồi
        try:
            if(driver_list[self.current_fb] != None):
                return
        except:
            pass
        # NẾU MỞ 2 CHROME RỒI THÌ PHẢI LÀM SAO????
        if(len(driver_list) == SO_DRIVER_MO_CUNG_LUC):
            id_bi_xoa = self.lich_su_hoat_dong.xoa_driver()
            driver_list[id_bi_xoa].quit()
            driver_list.pop(id_bi_xoa)

        # chrome chưa mở
        options = selenium_webdriver.ChromeOptions()
        options.add_argument(
            r'user-data-dir=' + LINK_FOLDER_CHROMEPROFILE + self.current_fb)
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.headless = IS_HEADLESS
        prefs = {
            "profile.managed_default_content_settings.images": 2
        }
        options.add_experimental_option("prefs", prefs)
        driver_list[self.current_fb] = selenium_webdriver.Chrome(service=Service(
            LINK_CHROMEDRIVER), options=options)

    def like_share_comment_follow(self):
        # có đôi lúc tự động mở thêm 1 cửa sổ quảng cáo mà ko biết lý do
        try:
            driver_list[self.current_fb].switch_to.window(
                driver_list[self.current_fb].window_handles[1])
            driver_list[self.current_fb].close()
            driver_list[self.current_fb].switch_to.window(
                driver_list[self.current_fb].window_handles[0])
        except:
            pass
        # ngắt luồng nuôi fb
        self.dang_nuoi[self.current_fb] = False
        self.load_link()
        self.done_job = False
        if (self.type_of_job == 'TĂNG LIKE CHO FANPAGE' or self.type_of_job == 'TĂNG LIKE_PAGE_CORONA_0 CHO BÀI VIẾT'):
            self.like_fage()
        elif(self.type_of_job == 'TĂNG LIKE CHO BÀI VIẾT' or self.type_of_job == 'TĂNG LIKE_CORONA_0 CHO BÀI VIẾT'):
            self.baytocamxuc(0)
        elif(self.type_of_job == 'TĂNG THƯƠNG THƯƠNG CHO BÀI VIẾT'):
            self.baytocamxuc(2)
        elif(self.type_of_job == 'TĂNG LOVE CHO BÀI VIẾT'):
            self.baytocamxuc(1)
        elif(self.type_of_job == 'TĂNG HAHA CHO BÀI VIẾT'):
            self.baytocamxuc(3)
        elif(self.type_of_job == 'TĂNG WOW CHO BÀI VIẾT'):
            self.baytocamxuc(4)
        elif(self.type_of_job == 'TĂNG SAD CHO BÀI VIẾT'):
            self.baytocamxuc(5)
        elif(self.type_of_job == 'TĂNG ANGRY CHO BÀI VIẾT'):
            self.baytocamxuc(6)
        elif(self.type_of_job == 'TĂNG COMMENT CHO BÀI VIẾT'):
            self.tang_comment()
        elif(self.type_of_job == 'TĂNG LƯỢT THEO DÕI' or self.type_of_job == 'TĂNG FOLLOW_CORONA_0 CHO BÀI VIẾT'):
            # self.to_cao(0)
            self.theo_doi()
        elif(self.type_of_job == 'TĂNG LIKE CHO ALBUM'):
            self.baytocamxuc(0)
        elif(self.type_of_job == 'TĂNG LIKE_COMMENT CHO BÀI VIẾT'):
            self.like_comment(0)

        elif(self.type_of_job == 'TĂNG CHIA SẺ CHO BÀI VIẾT'):
            # playsound("C:\withpython\gun1.mp3",block=True)
            self.chia_se()
        else:
            f = open("D:\\warnning.txt")
            f.write(self.type_of_job)
            f.write(self.link_facebook)
            f.close()
            input(">>> SERVER KHÔNG BIẾT ĐÂY LÀ JOB GÌ!!!!")

    def baytocamxuc(self, abc):
        # Đoạn này để xác định xem đã bày tỏ cảm xúc trc đó chưa
        result = driver_list[self.current_fb].execute_script(r'''const the_span = document.getElementsByTagName('span');
                                                            let result_cua_Tiep = -1;
                                                            for(let i = 0; i < the_span.length; i++){
                                                                if(the_span[i].innerHTML == 'Bày tỏ cảm xúc' || the_span[i].innerHTML == 'React')
                                                                {result_cua_Tiep = i;break;};}
                                                            return result_cua_Tiep
                                                            ''')
        print("*****************", result)
        if(result == -1):
            # ĐÃ BÀY TỎ CẢM XÚC TRƯỚC ĐÓ
            cai_nao_da_an = self.xet_cai_nao_da_an()
            # da nhan dung cai can nhan
            if(cai_nao_da_an == abc):
                self.done_job = True
            else:
                print("-> Đã ", cai_nao_da_an, " nhưng lại yêu cầu ", abc)
                print(
                    "*Lỗi do có thg Hấp mua 2 loại cảm xúc cho một bài, hủy đi thôi chứ làm kiểu gì bây giờ.")
            return
        else:  # nếu chưa nhấn
            time.sleep(random.randint(0, 1) + 0.8)
            driver_list[self.current_fb].execute_script(
                r"const the_span = document.getElementsByTagName('span');for(let i = 0; i < the_span.length; i++){if(the_span[i].innerHTML == 'Bày tỏ cảm xúc' || the_span[i].innerHTML == 'React'){the_span[i].click();break;};}")
            time.sleep(random.randint(0, 1) + 0.8)
            nhan = driver_list[self.current_fb].find_elements(
                By.TAG_NAME, 'li')
            nhan[abc].click()
            self.done_job = True
            return

    def xet_cai_nao_da_an(self):
        cam_xuc_da_an = int(driver_list[self.current_fb].execute_script(
            r'''const the_span = document.getElementsByTagName('span');
            let result_cua_Tiep = -1;
            for(let i = 0; i < the_span.length; i++){
                if(the_span[i].innerHTML == 'Like' || the_span[i].innerHTML == 'Thích')
                    {result_cua_Tiep = 0;break;};
                if(the_span[i].innerHTML == 'Love' || the_span[i].innerHTML == 'Yêu thích')
                    {result_cua_Tiep = 1;break;};
                if(the_span[i].innerHTML == 'Care' || the_span[i].innerHTML == 'Thương thương')
                    {result_cua_Tiep = 2;break;};
                if(the_span[i].innerHTML == 'Haha')
                    {result_cua_Tiep = 3;break;};
                if(the_span[i].innerHTML == 'Wow')
                    {result_cua_Tiep = 4;break;};
                if(the_span[i].innerHTML == 'Sad' || the_span[i].innerHTML == 'Buồn')
                    {result_cua_Tiep = 5;break;};
                if(the_span[i].innerHTML == 'Angry' || the_span[i].innerHTML == 'Phẫn nộ')
                    {result_cua_Tiep = 6;break;};
            }
            return result_cua_Tiep
            '''))
        return cam_xuc_da_an

    def like_comment(self, abc):
        try:
            time.sleep(random.randint(0, 1) + 0.8)
            nhan = driver_list[self.current_fb].find_elements(
                By.TAG_NAME, 'li')
            nhan[abc].click()
            time.sleep(random.randint(0, 1) + 0.8)
            self.done_job = True
        except:
            print("Khong nhan link comment duoc")

    def theo_doi(self):
        time.sleep(random.randint(0, 1) + 0.8)
        driver_list[self.current_fb].execute_script(
            "const the_span = document.getElementsByTagName('a');for(let i = 0; i < the_span.length; i++){if(the_span[i].innerHTML == 'Follow' || the_span[i].innerHTML == 'Theo dõi'){the_span[i].click();break;};};")
        time.sleep(random.randint(0, 1) + 0.8)
        # chỉ có thể là đã theo dõi hoặc chưa theo dõi
        self.done_job = True

    def tang_comment(self):
        try:
            time.sleep(random.randint(0, 1) + 0.8)
            driver_list[self.current_fb].find_element(By.NAME,
                                                      "comment_text").send_keys(self.comment_data)
            time.sleep(random.randint(0, 1) + 0.8)
            inp = driver_list[self.current_fb].find_elements(
                By.TAG_NAME, "input")
            time.sleep(1)
            for ip in inp:
                if(ip.get_attribute("value") == 'Bình luận' or ip.get_attribute("value") == 'Comment'):
                    ip.click()
                    break
            time.sleep(random.randint(0, 1) + 0.8)
            self.done_job = True
        except:
            print("khong binh luan duoc")

    def like_fage(self):
        try:
            driver_list[self.current_fb].execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randint(0, 1) + 0.8)
            driver_list[self.current_fb].execute_script(
                "window.scrollTo(0, 0);")
            time.sleep(random.randint(0, 1) + 0.8)
            driver_list[self.current_fb].execute_script(
                r"{let the_span = document.getElementsByTagName('span');for(let i = 0; i < the_span.length; i++){if(the_span[i].innerHTML == 'Thích' || the_span[i].innerHTML == 'Like'){the_span[i].click();};}}")  # nhanlikefage
            time.sleep(random.randint(0, 1) + 0.8)
            self.done_job = True
        except:
            print("Khong nhan like page duoc")

    def chia_se(self):

        time.sleep(random.randint(0, 1) + 0.8)
        driver_list[self.current_fb].execute_script(
            "const the_span = document.getElementsByTagName('span');for(let i = 0; i < the_span.length; i++){if(the_span[i].innerHTML == 'Chia sẻ' || the_span[i].innerHTML == 'Share'){the_span[i].click();break;};}")
        time.sleep(random.randint(0, 1) + 0.8)
        driver_list[self.current_fb].execute_script(
            "document.getElementsByName('view_post')[0].click()")
        time.sleep(random.randint(0, 1) + 0.8)
        self.done_job = True
    # Giả vờ lướt lướt như vô tội

    def gia_vo_nhu_vo_toi(self):
        nuoi = Thread(target=self.nuoi_facebook)
        nuoi.start()

    def nuoi_facebook(self):
        try:
            id_nuoi = self.current_fb
            self.dang_nuoi[id_nuoi] = True
            n = random.randint(1, 8)
            w = random.randint(1, 99)
            time.sleep(random.randint(2, 4))
            if (n == 1):
                if(self.dang_nuoi[id_nuoi] == False):
                    return
                driver_list[id_nuoi].get(
                    'https://mbasic.facebook.com/')  # trang chủ
                time.sleep(random.randint(10, 12)/10)
                # if(w < 30):
                #     doc = docx.Document(
                #         r"D:\MyImportantData\dang_trang_thai_fb.docx")
                #     all_paras = doc.paragraphs
                #     e = len(all_paras)
                #     trang_thai = all_paras[random.randint(0, e-1)].text
                #     print(">>> ĐĂNG TRẠNG THÁI: ", trang_thai)
                #     if(self.dang_nuoi[id_nuoi] == False):
                #         return
                #     driver_list[id_nuoi].find_element_by_name(
                #         "xc_message").send_keys(trang_thai)
                #     time.sleep(random.randint(1, 2))
                #     if(self.dang_nuoi[id_nuoi] == False):
                #         return
                #     driver_list[id_nuoi].find_element_by_name(
                #         "view_post").click()
                self.dang_nuoi[id_nuoi] = False
                driver_list[id_nuoi].execute_script(
                    "javascript:setInterval(function(){window.scrollBy(0,(Math.floor((Math.random() * 1) + 0)+1)*window.innerHeight);}, Math.floor((Math.random() * 5000) + 1000));")
                    
                return

            elif (n == 2):
                if(self.dang_nuoi[id_nuoi] == False):
                    return
                driver_list[id_nuoi].get(
                    r'https://mbasic.facebook.com/profile.php?=58842' + str(w))  # trang cá nhân : none
                time.sleep(random.randint(10, 12)/10)
                driver_list[id_nuoi].execute_script(
                    "javascript:setInterval(function(){window.scrollBy(0,(Math.floor((Math.random() * 1) + 0)+1)*window.innerHeight);}, Math.floor((Math.random() * 5000) + 1000));")
                self.dang_nuoi[id_nuoi] = False
                
                return

            elif (n == 3):
                if(self.dang_nuoi[id_nuoi] == False):
                    return
                driver_list[id_nuoi].get(
                    r'https://mbasic.facebook.com/messages/?ref_component=mbasic_home_header&ref_page=%2Fwap%2Fprofile_timeline.php&refid=' + str(w))  # tin nhắn
                time.sleep(random.randint(10, 12)/10)
                driver_list[id_nuoi].execute_script(
                    "javascript:setInterval(function(){window.scrollBy(0,(Math.floor((Math.random() * 1) + 0)+1)*window.innerHeight);}, Math.floor((Math.random() * 5000) + 1000));")
                self.dang_nuoi[id_nuoi] = False
                
                return

            elif (n == 4):
                if(self.dang_nuoi[id_nuoi] == False):
                    return
                driver_list[id_nuoi].get(
                    r'https://mbasic.facebook.com/notifications.php?ref_component=mbasic_home_header&ref_page=MNotificationsController&refid=' + str(w))  # thông báo
                time.sleep(random.randint(10, 12)/10)
                driver_list[id_nuoi].execute_script(
                    "javascript:setInterval(function(){window.scrollBy(0,(Math.floor((Math.random() * 1) + 0)+1)*window.innerHeight);}, Math.floor((Math.random() * 5000) + 1000));")
                self.dang_nuoi[id_nuoi] = False
                
                return

            elif (n == 5):
                if(self.dang_nuoi[id_nuoi] == False):
                    return
                driver_list[id_nuoi].get(
                    r'https://mbasic.facebook.com/buddylist.php?ref_component=mbasic_home_header&ref_page=MMessagingThreadlistController&refid=' + str(w))  # chat
                time.sleep(random.randint(10, 12)/10)
                driver_list[id_nuoi].execute_script(
                    "javascript:setInterval(function(){window.scrollBy(0,(Math.floor((Math.random() * 1) + 0)+1)*window.innerHeight);}, Math.floor((Math.random() * 5000) + 1000));")
                self.dang_nuoi[id_nuoi] = False
                
                return

            elif (n == 6):
                if(self.dang_nuoi[id_nuoi] == False):
                    return
                driver_list[id_nuoi].get(
                    r'https://mbasic.facebook.com/friends/center/mbasic/?fb_ref=tn&sr=1&ref_component=mbasic_home_header&ref_page=MChatBuddyListController')  # bạn bè
                time.sleep(random.randint(1, 2))
                try:
                    if(self.dang_nuoi[id_nuoi] == False):
                        return
                    driver_list[id_nuoi].find_elements_by_link_text("Xác nhận")[random.randint(
                        0, len(driver_list[id_nuoi].find_elements_by_link_text("Xác nhận"))-1)].click()
                    time.sleep(random.randint(1, 2))
                    if(w > 50):
                        if(self.dang_nuoi[id_nuoi] == False):
                            return
                        driver_list[id_nuoi].find_elements_by_link_text("Thêm bạn bè")[random.randint(
                            0, len(driver_list[id_nuoi].find_elements_by_link_text("Thêm bạn bè"))-1)].click()
                except:
                    print(
                        "khong xac nhan duoc ket ban ---------------------------------------------------------------------------------")
                self.dang_nuoi[id_nuoi] = False
                return

            elif (n == 7):
                if(self.dang_nuoi[id_nuoi] == False):
                    return
                driver_list[id_nuoi].get(
                    r'https://mbasic.facebook.com/pages/?ref_component=mbasic_home_header&ref_page=XPagesBrowserController')  # trang
                time.sleep(random.randint(10, 12)/10)
                driver_list[id_nuoi].execute_script(
                    "javascript:setInterval(function(){window.scrollBy(0,(Math.floor((Math.random() * 1) + 0)+1)*window.innerHeight);}, Math.floor((Math.random() * 5000) + 1000));")
                self.dang_nuoi[id_nuoi] = False
                
                return

            else:
                if(self.dang_nuoi[id_nuoi] == False):
                    return
                driver_list[id_nuoi].get(
                    r'https://mbasic.facebook.com/groups/?category=membership&ref_component=mbasic_home_header&ref_page=XGroupBrowseController&refid=' + str(w))  # nhóm
                time.sleep(random.randint(10, 12)/10)
                driver_list[id_nuoi].execute_script(
                    "javascript:setInterval(function(){window.scrollBy(0,(Math.floor((Math.random() * 1) + 0)+1)*window.innerHeight);}, Math.floor((Math.random() * 5000) + 1000));")
                self.dang_nuoi[id_nuoi] = False
                
                return
        except Exception as e:
            print(">>> HÌNH NHƯ DRIVER BỊ ĐÓNG: ", id_nuoi)
            print(e)


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
    cursor.execute(
        "select top(1) fb_id, loai_job, link_fb,noi_dung_comment FROM BANGJOBS WHERE [status] = 0")
    for i in cursor:
        return i
    return None


def get_job():
    x = ThreadWithReturnValue(target=get)
    x.start()
    return x.join()


def post(fb_id, loai_job, link_fb, status):
    print(">>> POST: ", fb_id, loai_job, link_fb, status)
    print('\n\n')
    with conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE BANGJOBS SET [status]="+str(status)+" WHERE fb_id = '" +
                       fb_id+"' AND loai_job = N'"+loai_job+"' AND link_fb = '"+link_fb+"'")


def post_status(fb_id, loai_job, link_fb, status):
    x = Thread(target=post, args=(fb_id, loai_job, link_fb, status))
    x.start()
    x.join()


if __name__ == '__main__':
    server = Server_facebook()
    # bắt các Exception có thể biết được nếu như mobile bị die
    while(1):
        # lấy job về
        info_job = get_job()
        if(info_job == None):
            # print('khong co job')
            time.sleep(1)
            continue
        # server thực hiện
        done_thao_tac = server.do(
            info_job[0], info_job[1], info_job[2], info_job[3])
        # client báo cáo job
        if(done_thao_tac):
            post_status(info_job[0], info_job[1], info_job[2], 1)
        else:
            post_status(info_job[0], info_job[1], info_job[2], 2)
        server.gia_vo_nhu_vo_toi()
