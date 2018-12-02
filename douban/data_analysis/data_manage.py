import pymongo
import wordcloud
import os

class Analysis():
	def __init__(self):
		client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
		db_name = client["douban"]
		collection = db_name["comments"]
		self.results = collection.find({},{"score":1,"comment":1})
		self.filepath = "/Users/shawn/Downloads/result.txt"

	def fileIsExists(self):		
		if os.path.exists(self.filepath):
			os.remove(self.filepath)

	def writefile(self):
		for data in self.results:
			comment = data["comment"]
			with open(self.filepath,"a") as f1:
				f1.write(comment + "\n")

	def makewordcloud(self):
		f2 = open(self.filepath).read()
		fontfile = "/Users/shawn/Downloads/font.ttf"
		wordcd = wordcloud.WordCloud(background_color="white",font_path=fontfile,width=1000,height=860,margin=2,max_words=2000).generate(f2)
		wordcd.to_file("/Users/shawn/Downloads/result.png")

if __name__ == '__main__':
	ana = Analysis()
	ana.fileIsExists()
	ana.writefile()
	ana.makewordcloud()