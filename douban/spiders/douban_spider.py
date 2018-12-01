import scrapy, os, time, re
from scrapy.http import Request, FormRequest
import urllib.request
from PIL import Image
from selenium import webdriver
from douban.items import DoubanItem

class DoubanSpider(scrapy.Spider):
	name = "douban"
	allowed_domains = ['douban.com']

	def start_requests(self):
		login_url = 'https://accounts.douban.com/login'
		return [Request(login_url, callback=self.login, meta={'cookiejar':1})]

	def login(self, response):
		data = {
			"source":"movie",
			"redir":"https://movie.douban.com/",
			"form_email":"******",
			"form_password":"******",
			"login":"登录"
			}
		img_path = '/Users/shawn/Downloads/check.png'
		if os.path.exists(img_path):
			os.remove(img_path)
		img_url = response.xpath('//*[@id="captcha_image"]/@src').extract_first()
		if img_url != None:
			img_id = img_url.split("id=")[1].split('&')[0]
			urllib.request.urlretrieve(img_url, filename=img_path)
			img = Image.open(img_path)
			img.show()
			check_input = input("Input the check:")
			data["captcha-id"] = img_id
			data["captcha-solution"] = check_input
			return FormRequest.from_response(response, meta={'cookiejar':response.meta['cookiejar']},formdata=data, callback=self.parge_main)
		else:
			return FormRequest.from_response(response, meta={'cookiejar':response.meta['cookiejar']}, formdata=data, callback=self.parge_main)

	def parge_main(self, response):
		movie_name = input("Input movie name: ")
		search_url = response.urljoin("subject_search?search_text=%s&cat=1002"%movie_name)
		browser = webdriver.Chrome("/Users/shawn/Downloads/chromedriver")
		browser.get(search_url)
		time.sleep(1)
		movie_info = browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div[1]/a')
		movie_info.click()
		time.sleep(1)
		content_info = browser.find_element_by_xpath('//*[@id="comments-section"]/div[1]/h2/span/a')
		content_info.click()
		time.sleep(1)
		content_url = browser.current_url
		return Request(content_url, callback=self.parse, meta={'cookiejar':response.meta['cookiejar']})

	def parse(self, response):
		item = DoubanItem()
		all_person_comments = response.xpath('//div[contains(@class,"comment-item")]')
		for person_comment in all_person_comments:
			username = person_comment.xpath('./div[2]/h3/span[2]/a/text()').extract_first()
			comment = person_comment.xpath('./div[2]/p/span/text()').extract_first()
			score_flag = (person_comment.xpath('./div[2]/h3/span[2]/span[2]').extract_first()).split("title")[0]
			score_list = (re.findall('\d+', score_flag))
			if len(score_list) != 0:
				score = score_list[0]
			else:
				score = str(0)
			item["user"] = username
			item["score"] = score
			item["comment"] = comment
			yield item

		next_url = response.xpath('//*[@id="paginator"]/a[last()]/@href').extract_first()
		next_page_url = response.urljoin(next_url)
		yield Request(url=next_page_url, callback=self.parse, meta={'cookiejar':response.meta['cookiejar']})
