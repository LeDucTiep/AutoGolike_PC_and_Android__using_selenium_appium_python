import time
import random
import subprocess
import pyodbc
from datetime import datetime
from appium import webdriver as appium_webdriver
from selenium.webdriver.common.by import By
from threading import Thread
# from multiprocessing import Pool
import sys

SO_JOB_MOI_NICK = 5
DELAY_FOR_EACH_ELEMENT = 5
TOI_DA_SO_LUONG_JOB_KHONG_LOAD_DUOC_THI_CO_KHA_NANG_LOI = 10
LINK_CHROMEDRIVER_98 = r"D:\ChromeDriver\chrome_ver98\chromedriver.exe"
LINK_CHROMEDRIVER_100 = r"D:\ChromeDriver\chrome_ver100\chromedriver.exe"
LINK_CHROMEDRIVER_101 = r"D:\ChromeDriver\chrome_ver101\chromedriver.exe"
bo_qua_jobs_theo_doi = True


id_device = ('AMD00232309', 'X9C1932014491', 'SKW4NNN7LJDQAYZS')

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-00A9GG2\LEDUCTIEP;'
                      'Database=jobsgolike;'
                      'Trusted_Connection=yes;')


def lay_id_account():
    id = None
    with conn:
        cursor = conn.cursor()
        cursor.execute('''  
                            SELECT top(1)
                                id_fb
                            FROM taikhoan
                            WHERE dang_lam = (SELECT min(dang_lam)
                                FROM taikhoan where day(getdate()) != day(ngay_lam_xong))
                            and day(getdate()) != day(ngay_lam_xong)
                        ''')
        for i in cursor:
            id = i[0]

        if(id == None):
            input(">>> BÁO ĐỘNG: HẾT NICK RỒI THÊM VÀO CHO TAO LÀM NHANH LÊN!!!!!!")
            exit()

        cursor = conn.cursor()
        cursor.execute('''  
                            UPDATE taikhoan 
                            SET dang_lam += 1
                            WHERE id_fb = ''' + id
                       )
    return id


def set_id_account_du_100_jobs(id):
    with conn:
        cursor = conn.cursor()
        cursor.execute('''
                            UPDATE taikhoan 
                            SET ngay_lam_xong = GETDATE()
                            where id_fb = '''+str(id)
                       )

def lay_taikhoan_matkhau():
    with conn:
        cursor = conn.cursor()
        cursor.execute('''  
                            select top(1) taikhoan, matkhau from TaiKhoanMatKhau
                        ''')
        for i in cursor:
            return i

ten_dang_nhap, mat_khau = lay_taikhoan_matkhau()


def sleep13():
    time.sleep(random.randint(55, 65)/10)


def delay():
    time.sleep(random.randint(2, 3) + 0.9)


def dang_o_chi_tiet_job(driver):
    current_link = driver.current_url
    result = current_link.find('job-detail') != -1
    return result


def dang_o_load_job(driver):
    current_link = driver.current_url
    result = current_link.find('load_job') != -1
    return result


def doi_load(driver):
    try:
        while(driver.find_elements(By.TAG_NAME, "img")[6].get_attribute("style") == 'display: none;'):
            pass
    except:
        return True


def nhan_ok(driver):
    try:
        driver.execute_script(
            "document.getElementsByClassName('swal2-confirm swal2-styled')[0].click()")  # nhan ok
    except:
        print(">>>KHONG NHAN OK DUOC")


class Client:
    driver = None
    golike_tab = None
    id_account_is_doing_in_golike = None
    id_will_give_to_server_facebook = None
    so_jobs_can_lam = SO_JOB_MOI_NICK
    so_lan_thu_hoan_thanh_lai = 0
    # Nếu load 10 lần mà ko dc thì có j đó sai sai r
    so_lan_load_ma_khong_co_job = 0
    SO_THU_TU_THIET_BI_CAN_CHAY = None

    def __init__(self, stt):
        self.SO_THU_TU_THIET_BI_CAN_CHAY = stt
        self.THONG_TIN_THIET_BI = {
            'platformName': 'Android',
            'platformVersion': '10',
            'browserName': 'chrome',
            'appium:chromedriverExecutable': LINK_CHROMEDRIVER_100,
            'udid': id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY],
            'newCommandTimeout': '86400',
        }, {
            'platformName': 'Android',
            'platformVersion': '9',
            'browserName': 'chrome',
            # 'appium:chromedriverExecutable': LINK_CHROMEDRIVER_98,
            'udid': id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY],
            'newCommandTimeout': '86400'
        }, {
            'platformName': 'Android',
            'platformVersion': '11',
            'browserName': 'chrome',
            # "noReset": 'true',
            # 'fullReset': True,
            # 'appium:chromedriverExecutable': LINK_CHROMEDRIVER_100,
            'udid': id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY],
            'newCommandTimeout': '86400'
        }
        # appium --allow-insecure chromedriver_autodownload

        self.id_will_give_to_server_facebook = lay_id_account()
        self.driver = self.connect_mobile()
        self.login(ten_dang_nhap, mat_khau)
        self.stack_can_chuyen_nick = 0

    def connect_mobile(self) -> appium_webdriver:
        capabilities = self.THONG_TIN_THIET_BI[self.SO_THU_TU_THIET_BI_CAN_CHAY]
        driver = appium_webdriver.Remote(
            'http://127.0.0.1:4723/wd/hub', capabilities, keep_alive=True)
        driver.implicitly_wait(DELAY_FOR_EACH_ELEMENT)
        return driver

    def scroll_down(self):
        subprocess.call(
            'adb -s '+id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input swipe 200 900 200 300')
        subprocess.call(
            'adb -s '+id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input swipe 200 900 200 300')
        

    def doi_ip(self):
        print("-------------------------------DANG DOI IP MANG---------------------------------------------------")
        subprocess.call(
            'adb -s '+id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY]+' shell svc wifi disable')
        if(id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY] == 'X9C1932014491'):
            subprocess.call('adb -s '+id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input swipe 500 0 500 1000')
            time.sleep(0.01)
            subprocess.call('adb -s '+id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input swipe 500 0 500 1000')
            time.sleep(0.01)
            subprocess.call('adb -s '+id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input tap 140 550')
            time.sleep(1)
            subprocess.call('adb -s '+id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input tap 140 550')
            time.sleep(0.01)
            subprocess.call('adb -s '+id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input swipe 500 1000 500 0')
            subprocess.call('adb -s '+id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input swipe 500 1000 500 0')
        else:
            subprocess.call('adb -s '+id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input swipe 500 0 500 1000')
            time.sleep(0.01)
            subprocess.call('adb -s '+id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input tap 606 266')
            time.sleep(1)
            subprocess.call('adb -s '+id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input tap 606 266')
            time.sleep(0.01)
            subprocess.call('adb -s '+id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input swipe 500 1000 500 0')
            subprocess.call('adb -s '+id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input swipe 500 1000 500 0')

    def login(self, userName, passWord):
        # secs = 10
        # self.driver.background_app({"seconds": secs})
        if (self.driver != None):
            self.driver.get("https://app.golike.net/")
            # input("-->KHÓA ỨNG DỤNG LẠI, RỒI NHẤN ENTER!")
            print("The web is loaded!")
            self.golike_tab = self.driver.window_handles[0]
            # lưu lại tab này, ta sẽ cần nó để phân biệt tab nào không nên tắt
            div = self.driver.find_elements(
                By.CSS_SELECTOR, "input.form-control")
            div[0].send_keys(userName)
            div[1].send_keys(passWord)
            time.sleep(1.5)
            self.driver.find_element(By.TAG_NAME, "button").click()
            time.sleep(3)
            # if(self.captcha_co_dang_hien_thi_khong()):
            #     self.doi_ip()
            #     self.login(userName, passWord)
            #     return
            input()
            self.driver.find_element(
                By.XPATH, "//*[@id=\"cheatModal\"]/div/div/div/div/div/button").click()
            print("Login successful!")
        else:
            input("Chrome in not open yet!")

    def doi_taikhoan_lamviec(self):
        print("doing     : ", self.id_account_is_doing_in_golike)
        print("account_id: ", self.id_will_give_to_server_facebook)
        # đổi đến tài khoản chưa làm xong
        if((self.id_account_is_doing_in_golike != None) and (self.id_account_is_doing_in_golike == self.id_will_give_to_server_facebook)):
            print("Vẫn đang làm account: ", self.id_account_is_doing_in_golike)
            return
        # lần đầu tiên đăng nhập thì ko đổi ip, những lần sau đó thì có
        if(self.id_account_is_doing_in_golike != None):
            self.doi_ip()
        self.driver.execute_script(
            r"{let all=document.getElementsByClassName('card shadow-200 mt-1');for(var i=0;i<all.length;++i){if(all[i].getAttribute('id')=='"+self.id_will_give_to_server_facebook+"'){all[i].click();break;}}}")
        print("==================================================DOI ACCOUNT=====================================================")
        self.id_account_is_doing_in_golike = self.id_will_give_to_server_facebook
        print("--> Dang lam account: ", self.id_account_is_doing_in_golike)

    def kiem_tra_dung_tai_khoan(self):

        nick_dang_lam = self.driver.execute_script(
            "return document.getElementsByClassName('card shadow-200 mt-1 bg-b100')[0].id")
        dk = int(nick_dang_lam) == int(self.id_account_is_doing_in_golike)
        if (not dk):
            print(nick_dang_lam, self.id_account_is_doing_in_golike)
        return dk
    def close_tab_2(self):
        for window in self.driver.window_handles:
            if(window != self.golike_tab):
                self.driver.switch_to.window(window)
                self.driver.close()
        self.driver.switch_to.window(self.golike_tab)
        if(len(self.driver.window_handles) > 1):
            self.close_tab_2()
    def lay_thong_tin_job(self):
        # Ta cần trắc trắn không có thông báo nào hiện lên
        self.xet_cap_cha()
        self.close_tab_2()
        if((not dang_o_load_job(self.driver)) and (not dang_o_chi_tiet_job(self.driver))):
            # Vào phần chọn kênh kiếm tiền: - lệnh này có lỗi khi đang ở Chi tiết và web tự chuyển hướng sang trang load job
            try:
                self.driver.execute_script(
                    "document.getElementsByClassName('font-20 d-block mb-1 icon-wallet')[0].click()")
            except:
                pass
            time.sleep(2)
        if((not dang_o_load_job(self.driver)) and (not dang_o_chi_tiet_job(self.driver))):
            try:
                self.driver.execute_script(
                    "document.getElementsByClassName('btn btn-outline-light')[1].click()")
            except:
                pass
            time.sleep(2)
        else:
            print("--> ĐANG LOADING JOBS")
        # cần làm được: biết nick nào chưa làm xong của ngày hôm nay. -> chuyển đến nick chưa làm xong - solved
        try:
            self.doi_taikhoan_lamviec()
        except:
            print("* Không đổi được tài khoản làm việc.")
        while(1):
            try:
                if(dang_o_load_job(self.driver)):
                    self.scroll_down()
                    # CÓ THỂ LỖI KHI CÓ THÔNG BÁO HIỂN THỊ
                    job = self.driver.find_elements(
                        By.CSS_SELECTOR, 'div.card.mb-2.hand')
                    if(not self.kiem_tra_dung_tai_khoan()):
                        self.doi_taikhoan_lamviec()
                    if((job != None)):
                        # click có thể lỗi nếu có thông báo hiển thị
                        dem = -1
                        for i in job:
                            dem += 1
                            print(i.text)
                            if(i.text.find('LIKE') != -1):
                                break
                        job[dem].click()
                        print("-->ĐÃ TÌM THẤY JOB")
                        self.stack_can_chuyen_nick = 0
                        break
                elif(dang_o_chi_tiet_job(self.driver)):
                    self.hoan_thanh()
                    self.so_lan_load_ma_khong_co_job += 1
                    if(self.so_lan_load_ma_khong_co_job == TOI_DA_SO_LUONG_JOB_KHONG_LOAD_DUOC_THI_CO_KHA_NANG_LOI):
                        self.so_lan_load_ma_khong_co_job = 0
                    self.driver.get('https://app.golike.net/')
                    return self.lay_thong_tin_job()
                else:
                    return self.lay_thong_tin_job()
            except:
                self.so_lan_load_ma_khong_co_job += 1
                if(self.so_lan_load_ma_khong_co_job == TOI_DA_SO_LUONG_JOB_KHONG_LOAD_DUOC_THI_CO_KHA_NANG_LOI):
                    self.so_lan_load_ma_khong_co_job = 0
                    self.id_will_give_to_server_facebook = lay_id_account()
                    try:
                        print(">>> Đổi tài khoản làm việc do load hết hơi không dc job nào...")
                        self.doi_taikhoan_lamviec()
                    except:
                        print("*Khong khoi duoc tai khoan id: ", self.id_will_give_to_server_facebook)
                        self.driver.get('https://app.golike.net/')
                    return self.lay_thong_tin_job()
                print(">>> LỖI KHÔNG TÌM THẤY JOB!!!")
                self.xet_cap_cha()
                # scroll xuong vi mot so thiet bi man hinh nho khong nhin thay ben duoi
                if(dang_o_load_job(self.driver)):
                    self.scroll_down()
                elif(dang_o_chi_tiet_job(self.driver)):
                    self.xet_cap_cha()
                else:
                    return self.lay_thong_tin_job()

        try:
            # stale element reference: element is not attached to the page document
            ten_job = self.driver.find_elements(By.TAG_NAME, 'span')[5].text
        except:
            self.driver.get('https://app.golike.net/')
            return self.lay_thong_tin_job()
        print(ten_job, datetime.now().hour, "giờ", datetime.now().minute,
              "phút", datetime.now().second, "giây")
        # chưa xác định được nguyên nhân tại sao đôi lúc ở đoạn này lại có 2 tab
        # ***
        if(bo_qua_jobs_theo_doi):
            try:
                if(ten_job == "TĂNG LƯỢT THEO DÕI"):
                    self.huy_job()
                    return self.lay_thong_tin_job()
            except:
                pass
        comment = None
        if(ten_job.find("TĂNG COMMENT") != -1):
            self.huy_job()
            return self.lay_thong_tin_job()
            # nick chưa đủ trâu để làm job kiểu này 
            # try:
            #     self.driver.execute_script(
            #         "document.getElementsByTagName('u')[0].click()")  # nhan copy
            #     self.driver.execute_script(
            #         "document.getElementsByTagName('u')[0].click()")  # nhan copy
            # except:
            #     print("--> CÓ LỖI ẤN COPY NỘI DUNG COMMENT")
            # comment = self.driver.find_elements(By.TAG_NAME, "span")[7].text
            # print(">>> NỘI DUNG COMMENT: ", comment)

        # đột nhiên job đủ số lượng, golike đẩy mk về điểm xuất phát.
        try:
            link = self.get_link_job()
        except:
            return self.lay_thong_tin_job()
        self.so_lan_load_ma_khong_co_job = 0
        return self.id_account_is_doing_in_golike, ten_job, link, comment

    def nhan_lam_viec(self):
        # Từng sảy ra lỗi do mất kết nối mạng ko mở dc job
        self.su_ly_nut_lam_viec()

    def get_link_job(self):
        mbasic1 = self.driver.find_elements(By.TAG_NAME, "h6")
        dem = 0
        for mb1 in mbasic1:
            if(mb1.text.lower() == "facebook"):
                return self.driver.execute_script(
                    "return document.getElementsByTagName('h6')["+str(dem)+"]").find_element(By.XPATH, '..').find_element(By.XPATH, '..').get_attribute('href')
            dem += 1
        return None

    def vo_hieu_hoa_link(self):
        mbasic1 = self.driver.find_elements(By.TAG_NAME, "h6")
        dem = 0
        for mb1 in mbasic1:
            if(mb1.text.lower() == "facebook"):
                try:
                    self.driver.execute_script(
                        "document.getElementsByTagName('h6')["+str(dem)+"].parentElement.parentElement.href = 'file:///storage/emulated/0/Downloads/index.html';")
                except Exception as e:
                    print("*Lỗi link", e)
                print(">> Đã vô hiệu hóa link!")
                self.driver.find_element(
                    By.CSS_SELECTOR, "a.row.align-items-center").click()
                print(">> Đã nhấn link!")
                return
            dem += 1

    def su_ly_nut_lam_viec(self):
        # Vô hiệu hóa đường link
        try:
            self.vo_hieu_hoa_link()
        except Exception as e:
            print("Lỗi vô hiện hóa đường link", e)

    def huy_job(self):
        # đang không ở trang chi tiết job
        if(not dang_o_chi_tiet_job(self.driver)):
            return
        self.scroll_down()
        print("đang tố cáo")
        try:
            # nhấn báo lỗi
            tocao = self.driver.find_elements(By.TAG_NAME, "h6")
            dem = 0
            for mb1 in tocao:
                if(mb1.text.lower() == "báo lỗi"):
                    self.driver.execute_script(
                        "document.getElementsByTagName('h6')["+str(dem)+"].click()")
                    break
                dem += 1
            time.sleep(1)
            dem = 0
            for mb1 in tocao:
                if(mb1.text == "Tôi đã làm Job này rồi"):
                    self.driver.execute_script(
                        "document.getElementsByTagName('h6')["+str(dem)+"].click()")
                    break
                dem += 1
        # nhấn gửi
            self.driver.execute_script(
                "document.getElementsByClassName('btn btn-primary btn-sm form-control mt-3')[0].click()")
            doi_load(self.driver)
        except:
            print("Khong nhan to cao duoc")
    # An unknown server-side error occurred while processing the command. Original error: disconnected: received Inspector.detached event
    # [debug] [W3C] Matched W3C error code 'disconnected' to UnknownError
    # [HTTP] <-- POST /wd/hub/session/298b5a7c-50f1-448b-bed5-6837197525d5/elements 500 10 ms - 1120
    # [HTTP]

    def hoan_thanh(self):
        # có thể bị đẩy ra gây lỗi
        doi_load(self.driver)
        try:
            mbasic1 = self.driver.find_elements(By.TAG_NAME, "h6")
            dem = 0
            for mb1 in mbasic1:
                if(mb1.text.lower() == "hoàn thành"):
                    self.driver.execute_script(
                        "document.getElementsByTagName('h6')["+str(dem)+"].click()")
                    doi_load(self.driver)
                    return True
                dem += 1
            return False
        except Exception as e:
            print("Lỗi hoàn thành", e)
    # cần biết:
    # - có captcha không - solved
    # - có giải được captcha không
    # - có bị google chặn không

    # captcha xuất hiện khi đang ở trong phần Chi tiết.
    # nếu không ở trong phần này thì không cần sử lý captcha -> sử lý cái thông báo hiện lên là xong - solved
    # ngược lại:
    # - hãy xét xem có iframe nào đang visible không
    # - nếu không thì ngon rồi lượn thôi
    # - nếu có thì SOS ta cần giải captcha -> sau đó sẽ làm tiếp (nhấn hoàn thành là xong rồi)

    def xet_cap_cha(self):
        # đang ở phần chi tiết job thì có khả năng là có captcha
        if(dang_o_chi_tiet_job(self.driver) or dang_o_load_job(self.driver)):
            self.captcha_co_dang_hien_thi_khong()
        else:
            print("Khong co captcha")

        try:
            thong_bao = self.driver.execute_script(
                "return document.getElementById('swal2-content')").text
        except:
            # khong co thong bao
            return

        if(thong_bao == ""):
            return

        print(thong_bao)
        for i in ('phân phối', 'đảm bảo công bằng'):
            if(thong_bao.find(i) != -1):
                print('* ĐỢi 30s nhé.')
                time.sleep(30)
                break
            
        fb_bi_khoa = False
        can_huy_job = False
        can_load_lai = False
        can_lam_tiep = False
        can_chuyen_nick = False
        chi_nhan_ok = False
        # Các kiểu thông báo
        not_recognized_yet = False

        if(not not_recognized_yet):
            not_recognized_yet = fb_bi_khoa = thong_bao.find(
                'tài khoản Facebook bị khóa') != -1

        for i in ('Bài viết đã đủ số lượng', 'chưa thực hiện thao tác', 'đã bị ẩn', 'hết hạn hoàn thành'):
            if(not not_recognized_yet):
                not_recognized_yet = can_huy_job = thong_bao.find(i) != -1
            else:
                break
        for i in ('cập nhật phiên', 'phân phối', 'đảm bảo công bằng', 'hông tải được'):
            if(not not_recognized_yet):
                not_recognized_yet = can_load_lai = thong_bao.find(i) != -1
            else:
                break
        for i in ('chưa làm việc', 'thử lại sau ít phút', 'Error', 'quá nhanh'):
            if(not not_recognized_yet):
                not_recognized_yet = can_lam_tiep = thong_bao.find(i) != -1
            else:
                break
        for i in ('quá 100 jobs', 'quay lại vào ngày'):
            if(not not_recognized_yet):
                not_recognized_yet = can_chuyen_nick = thong_bao.find(i) != -1
            else:
                break
        for i in ('đã làm', 'lên hệ thống xét duyệt', 'gửi báo cáo lên hệ thống'):
            if(not not_recognized_yet):
                not_recognized_yet = chi_nhan_ok = thong_bao.find(i) != -1
            else:
                break

        new_message = not(
            fb_bi_khoa or can_huy_job or can_load_lai or can_lam_tiep or can_chuyen_nick or chi_nhan_ok)
        if(new_message):
            print(fb_bi_khoa, can_huy_job, can_load_lai,
                  can_lam_tiep, can_chuyen_nick, chi_nhan_ok)
            input("SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS \n -----> TOANG RỒI.!!!!")

        # kiểu j cũng phải nhấn tắt thông báo đi
        nhan_ok(self.driver)
        if(chi_nhan_ok):
            self.so_jobs_can_lam -= 1
            # Đã làm đủ số jobs cần lầm
            if(self.so_jobs_can_lam == 0):
                self.id_will_give_to_server_facebook = lay_id_account()
                self.doi_taikhoan_lamviec()
                self.so_jobs_can_lam = SO_JOB_MOI_NICK
            return
        if(fb_bi_khoa):
            # Bất lực
            input("SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS \n -----> TOANG RỒI. KHÓA NICK!!!!")

        if((self.so_lan_thu_hoan_thanh_lai == 3) or can_load_lai):
            self.so_lan_thu_hoan_thanh_lai = 0
            self.doi_ip()
            self.driver.get('https://app.golike.net/')
            return
        if(can_lam_tiep):
            self.so_lan_thu_hoan_thanh_lai += 1
            time.sleep(1)
            self.su_ly_nut_lam_viec()

            self.hoan_thanh()
            return True
        if(can_huy_job):
            self.huy_job()
            return True
        if(can_chuyen_nick):
            self.stack_can_chuyen_nick += 1
            if(self.stack_can_chuyen_nick == 2):
                self.stack_can_chuyen_nick = 0
                print(
                    "=============================Bạn đã làm quá 100 jobs ============================")
                set_id_account_du_100_jobs(self.id_account_is_doing_in_golike)
                self.id_will_give_to_server_facebook = lay_id_account()
                self.doi_taikhoan_lamviec()
            else: 
                self.doi_ip()
                self.driver.get('https://app.golike.net/')
    def captcha_co_dang_hien_thi_khong(self):
        self.driver.switch_to.default_content()
        frames = self.driver.find_elements(By.TAG_NAME, "iframe")
        for i in range(0, len(frames)):
            try:
                style = frames[i].find_element(By.XPATH, "..").find_element(
                    By.XPATH, "..").get_attribute("style")
                dk = (style != None) and (
                    style.find("visibility: visible;") != -1)
                if(dk):
                    # self.giai_captcha(i)
                    print(">>>>>>>>CÓ CAPTCHA!!!")
                    self.doi_ip()
                    self.driver.get('https://app.golike.net/')
                    return True
            except:
                # print("mã lỗi 137")
                pass
        self.driver.switch_to.default_content()
        return False

# ========================================================================================================================================================================================================================================


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
    cursor.execute("select top(1) status from BANGJOBS where fb_id = '" +
                   fb_id+"' and loai_job = N'"+loai_job+"' and link_fb = N'"+link_fb+"'")
    for i in cursor:
        return i[0]


def get_status_request(fb_id, loai_job, link_fb) -> int:
    while(1):
        x = ThreadWithReturnValue(
            target=doi_server_lam_xong, args=(fb_id, loai_job, link_fb))
        x.start()
        status = x.join()
        # *** LỖI: STATUS CÓ THỂ BẰNG NONE, CHƯA BIẾT NGUYÊN NHÂN, PHỎNG ĐOÁN LÀ CÓ LUỒNG KHÁC NHANH HƠN ĐÃ XÓA MẤT
        if(status == None):
            return 1
        if(int(status)):
            return status
        # print(result)
        time.sleep(0.6)


def create_post_job(fb_id, loai_job, link_fb, noi_dung_comment):
    print(">>> POST: ", fb_id, loai_job, link_fb, noi_dung_comment)
    with conn:
        cursor = conn.cursor()
        if(noi_dung_comment):
            cursor.execute("insert into BANGJOBS(fb_id, loai_job, link_fb, noi_dung_comment, status) values ('" +
                           fb_id+"', N'"+loai_job+"', N'"+link_fb+"', N'"+noi_dung_comment+"', 0)")
        else:
            cursor.execute("insert into BANGJOBS(fb_id, loai_job, link_fb, status) values ('" +
                           fb_id+"', N'"+loai_job+"', N'"+link_fb+"', 0)")


def post_job(fb_id, loai_job, link_fb, noi_dung_comment=None):
    x = Thread(target=create_post_job, args=(
        fb_id, loai_job, link_fb, noi_dung_comment))
    x.start()
    x.join()


def create_post_delete(fb_id, loai_job, link_fb):
    with conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM BANGJOBS WHERE  fb_id = '"+fb_id +
                       "' and loai_job = N'"+loai_job+"' and link_fb = N'"+link_fb+"'")


def post_delete_job(fb_id, loai_job, link_fb):
    x = Thread(target=create_post_delete, args=(fb_id, loai_job, link_fb))
    x.start()
    x.join()


def run_app(so_thu_tu_mobile):
    client = Client(so_thu_tu_mobile)
    # server = Server_facebook()
    # bắt các Exception có thể biết được nếu như mobile bị die
    while(1):
        # client lấy thông tin job về
        info_job = client.lay_thong_tin_job()
        # KIỂM TRA GIÁ TRỊ None TRƯỚC KHI GỬI LÊN DATABASE
        if(not(info_job[0] and info_job[1] and info_job[2])):
            continue
        # gửi job lên database
        post_job(info_job[0], info_job[1], info_job[2], info_job[3])
        # Nhấn làm việc
        client.nhan_lam_viec()
        time.sleep(2)
        # lấy kêts quả phản hồi của server từ database
        status_of_current_job = get_status_request(
            info_job[0], info_job[1], info_job[2])
        post_delete_job(info_job[0], info_job[1], info_job[2])
        # client báo cáo job
        if(status_of_current_job == 1):
            # Đã làm xong
            print("Hoan thanh: ", client.hoan_thanh(), datetime.now().hour, "giờ", datetime.now().minute,
                  "phút", datetime.now().second, "giây")
        elif(status_of_current_job == 2):
            print("Huy job: ", client.huy_job())
        else:
            print("SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS SOS \n-> status_of_current_job:", status_of_current_job)
            input()
        # xét xem nếu có captcha hiện lên
        client.xet_cap_cha()

# def aa ():
#	Pool(sonick).map(minimain, range(0 + batdautu , sonick + batdautu))


if __name__ == '__main__':

    # Pool(2).map(run_app, (0, 1))
    run_app(int(sys.argv[1]))
    # run_app()
