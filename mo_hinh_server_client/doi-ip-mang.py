import subprocess
import time

id_device = ('AMD00232309', 'X9C1932014491', 'SKW4NNN7LJDQAYZS')
SO_THU_TU_THIET_BI_CAN_CHAY = 1
subprocess.call(
            'adb -s '+id_device[SO_THU_TU_THIET_BI_CAN_CHAY]+' shell svc wifi disable')
if(id_device[ SO_THU_TU_THIET_BI_CAN_CHAY] == 'X9C1932014491'):
	subprocess.call('adb -s '+id_device[ SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input swipe 500 0 500 1000')
	time.sleep(0.01)
	subprocess.call('adb -s '+id_device[ SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input swipe 500 0 500 1000')
	time.sleep(0.01)
	subprocess.call('adb -s '+id_device[ SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input tap 140 550')
	time.sleep(0.1)
	subprocess.call('adb -s '+id_device[ SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input tap 140 550')
	time.sleep(0.01)
	subprocess.call('adb -s '+id_device[ SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input swipe 500 1000 500 0')
	subprocess.call('adb -s '+id_device[ SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input swipe 500 1000 500 0')
else:
	subprocess.call('adb -s '+id_device[ SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input swipe 500 0 500 1000')
	time.sleep(0.01)
	subprocess.call('adb -s '+id_device[ SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input tap 606 266')
	time.sleep(0.1)
	subprocess.call('adb -s '+id_device[ SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input tap 606 266')
	time.sleep(0.01)
	subprocess.call('adb -s '+id_device[ SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input swipe 500 1000 500 0')
	subprocess.call('adb -s '+id_device[ SO_THU_TU_THIET_BI_CAN_CHAY]+' shell input swipe 500 1000 500 0')


