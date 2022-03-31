from selenium import webdriver as selenium_webdriver
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from selenium.webdriver.common.by import By
import time
import random
# input: id_facebook, type_of_job, link_facebook, comment_data
# cần mở chrome mong muốn với id
# - nếu đang mở chrome khác thì giải quyết: tắt nó
# - bằng cách nào có thể phân biệt chrome là của id nào

LINK_CHROMEDRIVER_99 = "D:\\ChromeDriver\\chromedriver.exe"
LINK_FOLDER_CHROMEPROFILE = "D:\\ChromeDriver\\A-N VLOG\\"


class Server_facebook:
    present_id = None
    driver = None
    link_facebook = None
    comment_data = None
    type_of_job = None
    done_job = None

    def do(self, id_facebook, type_of_job, link_facebook, comment_data):
        print(">>>>>>>SERVER ĐANG LÀM: ", id_facebook)
        self.start_driver(id_facebook)
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
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.get("https://mbasic."+link[vt:len(link)])

    # Giải quyết id
    def id_to_profile(self, id_facebook):
        if(id_facebook == '100076681864851'):
            return 'profile ' + '1'
        if(id_facebook == '100076630237844'):
            return 'profile ' + '2'
        if(id_facebook == '100076621927821'):
            return 'profile ' + '3'
        if(id_facebook == '100076609088552'):
            return 'profile ' + '4'
        if(id_facebook == '100076560130796'):
            return 'profile ' + '5'
        if(id_facebook == '100076487174292'):
            return 'profile ' + '6'
        if(id_facebook == '100076469834611'):
            return 'profile ' + '7'
        if(id_facebook == '100076469265711'):
            return 'profile ' + '8'
        if(id_facebook == '100076379839853'):
            return 'profile ' + '9'
        if(id_facebook == '100012962526153'):
            return 'profile ' + '10'

    def start_driver(self, id_facebook):
        # nếu là fb đã mở sẵn rồi
        if(id_facebook == self.present_id):
            return
        # ngược lại và nếu đang mở chrome
        if(self.driver != None):
            self.driver.quit()
        options = selenium_webdriver.ChromeOptions()
        options.add_argument(
            r'user-data-dir=' + LINK_FOLDER_CHROMEPROFILE + self.id_to_profile(id_facebook))
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        # options.headless = True
        prefs = {
            "profile.managed_default_content_settings.images": 2
        }
        options.add_experimental_option("prefs", prefs)
        self.driver = selenium_webdriver.Chrome(service=Service(
            LINK_CHROMEDRIVER_99), options=options)
        self.present_id = id_facebook

    def like_share_comment_follow(self):
        # có đôi lúc tự động mở thêm 1 cửa sổ quảng cáo mà ko biết lý do 
        try:
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        except:pass
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
        try:
            if(self.driver.find_element(By.LINK_TEXT, "Bày tỏ cảm xúc").get_attribute("class") == ""):
                dk = True
            else:
                dk = False
        except:
            dk = True
        if (dk):  # đã nhấn bay to cam xuc
            cai_nao_da_an = self.xet_cai_nao_da_an()
            # da nhan dung cai can nhan
            if(cai_nao_da_an == abc):
                self.done_job = True
            return
        else:  # nếu chưa nhấn
            time.sleep(random.randint(0, 1) + 0.8)
            self.driver.find_element(By.LINK_TEXT, "Bày tỏ cảm xúc").click()
            time.sleep(random.randint(0, 1) + 0.8)
            nhan = self.driver.find_elements_by_tag_name('li')
            nhan[abc].click()
            self.done_job = True
            return

    def xet_cai_nao_da_an(self):
        try:
            if(self.driver.find_element_by_link_text("Thích").get_attribute("class") != ""):
                return 0
        except:
            pass
        try:
            if(self.driver.find_element_by_link_text("Yêu thích").get_attribute("class") != ""):
                return 1
        except:
            pass
        try:
            if(self.driver.find_element_by_link_text("Thương thương").get_attribute("class") != ""):
                return 2
        except:
            pass
        try:
            if(self.driver.find_element_by_link_text("Haha").get_attribute("class") != ""):
                return 3
        except:
            pass
        try:
            if(self.driver.find_element_by_link_text("Wow").get_attribute("class") != ""):
                return 4
        except:
            pass
        try:
            if(self.driver.find_element_by_link_text("Buồn").get_attribute("class") != ""):
                return 5
        except:
            pass
        # if(self.driver.find_element_by_link_text("Phẫn nộ").get_attribute("class") != ""):
        return 6

    def like_comment(self, abc):
        try:
            time.sleep(random.randint(0, 1) + 0.8)
            nhan = self.driver.find_elements_by_tag_name('li')
            nhan[abc].click()
            time.sleep(random.randint(0, 1) + 0.8)
            self.done_job = True
        except:
            print("Khong nhan link comment duoc")

    def theo_doi(self):
        try:
            time.sleep(random.randint(0, 1) + 0.8)
            self.driver.find_element_by_link_text("Theo dõi").click()
            time.sleep(random.randint(0, 1) + 0.8)
        except:
            print("Khong nhan duoc theo doi")
        # chỉ có thể là đã theo dõi hoặc chưa theo dõi
        self.done_job = True

    def tang_comment(self):
        try:
            time.sleep(random.randint(0, 1) + 0.8)
            self.driver.find_element_by_name(
                "comment_text").send_keys(self.comment_data)
            time.sleep(random.randint(0, 1) + 0.8)
            inp = self.driver.find_elements_by_tag_name("input")
            time.sleep(1)
            for ip in inp:
                if(ip.get_attribute("value") == 'Bình luận'):
                    ip.click()
                    break
            time.sleep(random.randint(0, 1) + 0.8)
            self.done_job = True
        except:
            print("khong binh luan duoc")

    def like_fage(self):
        try:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randint(0, 1) + 0.8)
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(random.randint(0, 1) + 0.8)
            self.driver.execute_script(
                r"{let the_span = document.getElementsByTagName('span');for(let i = 0; i < the_span.length; i++){if(the_span[i].innerHTML == 'Thích' || the_span[i].innerHTML == 'Like'){the_span[i].click();};}}")  # nhanlikefage
            time.sleep(random.randint(0, 1) + 0.8)
            self.done_job = True
        except:
            print("Khong nhan like page duoc")

    def chia_se(self):
        try:
            time.sleep(random.randint(0, 1) + 0.8)
            self.driver.find_element_by_link_text("Chia sẻ").click()
            time.sleep(random.randint(0, 1) + 0.8)
            self.driver.execute_script(
                "document.getElementsByClassName('bh cq cr cs ct')[0].click()")
            time.sleep(random.randint(0, 1) + 0.8)
            self.done_job = True
        except:
            print("Khong nhan duoc chia se")
