import time
import random
import subprocess
import pyodbc
from datetime import datetime
from appium import webdriver as appium_webdriver
from selenium.webdriver.common.by import By
from threading import Thread
from multiprocessing import Pool
import sys

SO_JOB_MOI_NICK = 10
DELAY_FOR_EACH_ELEMENT = 5
# FILE_LUU_SO_THU_TU_JOB_LAM_DAU_TIEN = "D:\AutoGolike_PC_and_Android\so_account_da_lam_xong.txt"
LINK_CHROMEDRIVER_99 = "D:\\ChromeDriver\\chromedriver.exe"
LINK_CHROMEDRIVER_98 = r"D:\ChromeDriver\chrome_ver98\chromedriver.exe"
ten_dang_nhap = "tieple247"
mat_khau = "lananhvu2701"
id_device = ('AMD00232309', 'X9C1932014491')

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-00A9GG2\LEDUCTIEP;'
                      'Database=jobsgolike;'
                      'Trusted_Connection=yes;')


def lay_so_account_da_lam() -> int:
    cursor = conn.cursor()
    cursor.execute("SELECT soacc FROM SoAccountDaLam")
    for i in cursor:
        return i[0]


def sua_so_account_da_lam(so_acc):
    with conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE SoAccountDaLam SET soacc = "+str(so_acc))


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
    present_id = None
    fb_id = ('100076681864851',
             '100076630237844',
             '100076621927821',
             '100076609088552',
             '100076560130796',
             '100076487174292',
             '100076469834611',
             '100076469265711',
             '100076379839853',
             '100012962526153')
    so_account_da_lam = None
    so_jobs_can_lam = SO_JOB_MOI_NICK
    so_lan_thu_hoan_thanh_lai = 0
    SO_THU_TU_THIET_BI_CAN_CHAY = None

    def __init__(self, stt):
        self.SO_THU_TU_THIET_BI_CAN_CHAY = stt
        self.THONG_TIN_THIET_BI = {
            'platformName': 'Android',
            'platformVersion': '10',
            'browserName': 'chrome',
            'appium:chromedriverExecutable': LINK_CHROMEDRIVER_99,
            'udid': id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY],
            'newCommandTimeout': '86400'
        }, {
            'platformName': 'Android',
            'platformVersion': '9',
            'browserName': 'chrome',
            'appium:chromedriverExecutable': LINK_CHROMEDRIVER_98,
            'udid': id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY],
            'newCommandTimeout': '86400'
        }
        self.so_account_da_lam = lay_so_account_da_lam()
        self.tang_so_account_da_lam()
        self.driver = self.connect_mobile()
        # test(self.driver)
        self.login(ten_dang_nhap, mat_khau)

    def connect_mobile(self) -> appium_webdriver:
        capabilities = self.THONG_TIN_THIET_BI[self.SO_THU_TU_THIET_BI_CAN_CHAY]
        driver = appium_webdriver.Remote(
            'http://127.0.0.1:4723/wd/hub', capabilities, keep_alive=True)
        driver.implicitly_wait(DELAY_FOR_EACH_ELEMENT)
        return driver

    def tang_so_account_da_lam(self):
        self.so_account_da_lam += 1
        if(self.so_account_da_lam == len(self.fb_id)):
            self.so_account_da_lam = 0
        sua_so_account_da_lam(self.so_account_da_lam)

    def doi_ip(self):
        print("-------------------------------DANG DOI IP MANG---------------------------------------------------")
        subprocess.call(
            'adb -s '+id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY]+' shell svc wifi disable')
        subprocess.call(
            'adb -s '+id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY]+' shell svc data disable')
        subprocess.call(
            'adb -s '+id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY]+' shell svc data enable')
        time.sleep(0.5)
        subprocess.call(
            'adb -s '+id_device[self.SO_THU_TU_THIET_BI_CAN_CHAY]+' shell svc data enable')

    def login(self, userName, passWord):
        if (self.driver != None):
            self.driver.get("https://app.golike.net/")
            # input("-->KHÓA ỨNG DỤNG LẠI, RỒI NHẤN ENTER!")
            print("The web is loaded!")
            # lưu lại tab này, ta sẽ cần nó để phân biệt tab nào không nên tắt
            self.golike_tab = self.driver.window_handles[0]
            div = self.driver.find_elements(
                By.CSS_SELECTOR, "input.form-control")
            div[0].send_keys(userName)
            div[1].send_keys(passWord)
            time.sleep(1.5)
            self.driver.find_element(By.TAG_NAME, "button").click()
            time.sleep(1.5)
            self.driver.find_element(
                By.XPATH, "//*[@id=\"cheatModal\"]/div/div/div/div/div/button").click()
            print("Login successful!")
            
        else:
            print("Chrome in not open yet!")

    def doi_taikhoan_lamviec(self):
        print(" ", self.present_id, "\n", self.fb_id[self.so_account_da_lam])
        # đổi đến tài khoản chưa làm xong
        if((self.present_id != None) and (self.present_id == self.fb_id[self.so_account_da_lam])):
            print("Vẫn đang làm account: ", self.present_id)
            return
        if(self.present_id != None):
            self.doi_ip()
        self.driver.execute_script(
            r"{let all=document.getElementsByClassName('card shadow-200 mt-1');for(var i=0;i<all.length;++i){if(all[i].getAttribute('id')=='"+self.fb_id[self.so_account_da_lam]+"'){all[i].click();break;}}}")
        print("==================================================DOI ACCOUNT=====================================================")
        self.present_id = self.fb_id[self.so_account_da_lam]
        print("--> Dang lam account: ", self.present_id)

    def kiem_tra_dung_tai_khoan(self):
        nick_dang_lam = self.driver.execute_script(
            "return document.getElementsByClassName('card shadow-200 mt-1 bg-b100')[0].id")
        return nick_dang_lam == self.present_id

    def lay_jobs(self):
        self.close_tab_2()
        # Ta cần trắc trắn không có thông báo nào hiện lên
        self.xet_cap_cha()

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
        self.doi_taikhoan_lamviec()

        while(1):
            try:
                # CÓ THỂ LỖI KHI CÓ THÔNG BÁO HIỂN THỊ
                job = self.driver.find_elements(
                    By.CSS_SELECTOR, 'div.card.mb-2.hand')
                if(not self.kiem_tra_dung_tai_khoan()):
                    input("----------------------------------lech tai khoan: ")
                if((job != None)):
                    # click có thể lỗi nếu có thông báo hiển thị
                    job[0].click()
                    print("-->ĐÃ TÌM THẤY JOB")
                    break
            except:
                self.xet_cap_cha()
                # scroll xuong vi mot so thiet bi man hinh nho khong nhin thay ben duoi
                try:
                    self.driver.execute_script(
                        "document.getElementsByClassName('b200 mb-2 mt-2')[0].scrollIntoView()")
                except:
                    self.doi_ip()
                    self.driver.get('https://app.golike.net/')
                    return self.lay_jobs()
                print(">>> LỖI KHÔNG TÌM THẤY JOB!!!")
        try:
            # stale element reference: element is not attached to the page document
            ten_job = self.driver.find_elements(By.TAG_NAME, 'span')[5].text
        except:
            self.driver.get('https://app.golike.net/')
            return self.lay_jobs()
        print(ten_job, datetime.now().hour, "giờ", datetime.now().minute,
              "phút", datetime.now().second, "giây")
        try:
            if(ten_job == "TĂNG LƯỢT THEO DÕI"):
                self.huy_job()
                return self.lay_jobs()
        except:
            pass
        comment = None
        if(ten_job.find("TĂNG COMMENT") != -1):
            try:
                self.driver.execute_script(
                    "document.getElementsByTagName('u')[0].click()")  # nhan copy
                self.driver.execute_script(
                    "document.getElementsByTagName('u')[0].click()")  # nhan copy
            except:
                print("--> CÓ LỖI ẤN COPY NỘI DUNG COMMENT")
            comment = self.driver.find_elements(By.TAG_NAME, "span")[7].text
        # đột nhiên job đủ số lượng, golike đẩy mk về điểm xuất phát.
        try:
            link = self.driver.execute_script("return document.getElementsByTagName('h6')[2]").find_element(By.XPATH,
                                                                                                            '..').find_element(By.XPATH, '..').get_attribute('href')
        except:
            self.close_tab_2()
            self.driver.get('https://app.golike.net/')
            return self.lay_jobs()
        try:
            # Từng sảy ra lỗi do mất kết nối mạng ko mở dc job
            self.su_ly_nut_lam_viec()
        except:
            self.close_tab_2()
            self.doi_ip()
            self.driver.get('https://app.golike.net/')
            return self.lay_jobs()
        print(link)
        return self.present_id, ten_job, link, comment

    def close_tab_2(self):
        for window in self.driver.window_handles:
            if(window != self.golike_tab):
                self.driver.switch_to.window(window)
                self.driver.close()
        self.driver.switch_to.window(self.golike_tab)
        if(len(self.driver.window_handles) > 1):
            self.close_tab_2()

    def su_ly_nut_lam_viec(self):
        # trang web tự dưng bị ngắt, tab thứ 2 vẫn còn
        self.close_tab_2()
        # Vô hiệu hóa đường link
        self.driver.execute_script(
            "document.getElementsByTagName('h6')[2].parentElement.parentElement.href = 'javascript:void(0)';document.getElementsByTagName('h6')[2].click();")

        # sẽ có 1 đường link 'vớ vẩn' hiện lên và ta cần đóng nó lại
        self.close_tab_2()
        return

    def huy_job(self):
        # đang không ở trang chi tiết job
        if(not dang_o_chi_tiet_job(self.driver)):
            return
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
        # Tôi không muốn làm Job này
            time.sleep(3)
            dem = 0
            for mb1 in tocao:
                if(mb1.text == "Tôi không muốn làm Job này"):
                    self.driver.execute_script(
                        "document.getElementsByTagName('h6')["+str(dem)+"].click()")
                    break
                dem += 1
        # nhấn gửi
            self.driver.execute_script(
                "document.getElementsByClassName('btn btn-primary btn-sm form-control mt-3')[0].click()")
        except:
            print("Khong nhan to cao duoc")
    # An unknown server-side error occurred while processing the command. Original error: disconnected: received Inspector.detached event
    # [debug] [W3C] Matched W3C error code 'disconnected' to UnknownError
    # [HTTP] <-- POST /wd/hub/session/298b5a7c-50f1-448b-bed5-6837197525d5/elements 500 10 ms - 1120
    # [HTTP]

    def hoan_thanh(self):
        doi_load(self.driver)
        mbasic1 = self.driver.find_elements(By.TAG_NAME, "h6")
        dem = 0
        for mb1 in mbasic1:
            if(mb1.text.lower() == "hoàn thành"):
                self.driver.execute_script(
                    "document.getElementsByTagName('h6')["+str(dem)+"].click()")
                return True
            dem += 1
        return False

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
            self.xac_dinh_captcha_dang_hien_thi()
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
            if(self.so_jobs_can_lam == 0):
                self.tang_so_account_da_lam()
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
            try:
                self.su_ly_nut_lam_viec()
            except:
                pass
            self.hoan_thanh()
            return True
        if(can_huy_job):
            self.huy_job()
            return True
        if(can_chuyen_nick):
            print(
                "=============================Bạn đã làm quá 100 jobs ============================")
            self.tang_so_account_da_lam()
            self.doi_taikhoan_lamviec()

    def xac_dinh_captcha_dang_hien_thi(self):
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
                    break
            except:
                # print("mã lỗi 137")
                pass

        self.driver.switch_to.default_content()


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
        # client lấy job về
        info_job = client.lay_jobs()
        # server thực hiện
        # KIỂM TRA GIÁ TRỊ None TRƯỚC KHI GỬI LÊN DATABASE
        if(not(info_job[0] and info_job[1] and info_job[2])):
            continue
        # gửi job lên database
        post_job(info_job[0], info_job[1], info_job[2], info_job[3])
        time.sleep(0.6)
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
