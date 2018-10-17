import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert
import time
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:/Users/lg/AppData/Local/Google/Chrome/User Data")
brower = webdriver.Chrome(chrome_options=options)
brower.maximize_window()
wait = WebDriverWait(brower, 10)
def loginToWeb():
	try:
		brower.get('http://gzife.njcedu.com/')
		submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.jc_top_bg > div.top_bg > input')))
		submit.click()
		loginId = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#loginId")))
		loginId.clear()
		loginId.send_keys('gzife-20150108020129')
		passWord = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#password")))
		passWord.clear()
		passWord.send_keys('123456')
		login = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#loginBtn')))
		login.click()
		print('登录成功...')
	except TimeoutException:
		return loginToWeb()

def get_detail():
	try:
		detail = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.s_con > ul.s_con_l > div:nth-child(2) > ul > li > a.xx_a')))
		if detail:
			detail.click()
			print('进入课程列表...')
		else:
			loadError()
			return get_detail()
	except TimeoutException:
		return get_detail()

def get_video_duration(offset):
	try:
		duration = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#courseTable > tbody > tr:nth-child(%s) > td:nth-child(2)'%str(offset))))
		return duration.text
	except TimeoutException:
		return get_video_duration(offset)

def searchClass(offset):
	try:
		print('点击观看...')
		play = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#courseTable > tbody > tr:nth-child(%s) > td:nth-child(4) > a:nth-child(1)'%str(offset))))
		play.click()
		handles = brower.window_handles
		print('所有窗口句柄：',handles)
		handle = handles[-1]
		print('切换到句柄: ',handle)
		brower.switch_to.window(handle)
		print('当前窗口句柄：',brower.current_window_handle)
	except TimeoutException:
		return searchClass(offset)

def playvideo(vlong):
	try:
		stadying = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.cen_js > ul.cen_js_r > div > a > input')))
		if stadying:
			stadying.click()
			head1 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.top_kc')))
			make_video_play()
			print('视频播放中...')
			time.sleep(vlong)
			change_to_index()
		else:
			loadError()
			return playvideo(vlong)
	except TimeoutException:
		return playvideo(vlong)

def make_video_play():
	time.sleep(3)
	handles = brower.window_handles
	indexwindow = handles[0]
	playerwindow = handles[-1]
	brower.switch_to.window(indexwindow)
	time.sleep(1)
	brower.switch_to.window(playerwindow)
	print('点击播放视频...')

def change_to_index():
	time.sleep(3)
	print('切换到主页...')
	handles = brower.window_handles
	indexwindow = handles[0]
	playerwindow = handles[1]
	print('关闭当前播放页面...')
	brower.close()
	brower.switch_to.window(indexwindow)

def loadError():
	reload = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#reload-button')))
	if reload:
		reload.click()

def main():
	try:
		loginToWeb()
		get_detail()
		for i in range(35,39):
			duration = get_video_duration(i)
			pattern = re.compile('(\d+) / (\d+)')
			time1 = pattern.search(duration).group(1)
			time2 = pattern.search(duration).group(2)
			vlong = (int(time2) - int(time1) + 0.5)*60
			searchClass(i)
			print('准备播放第' + str(i) + '个视频！')
			print('视频时长：',str(vlong) + '秒！')
			playvideo(vlong)
			print('准备播放下一个视频...')
		time.sleep(10)
	except Exception as error:
		print('出错: ',error)
	finally:
		print('视频播放完毕！！！')
		brower.quit()

if __name__ == '__main__':
	main()













