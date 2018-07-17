#Code to scrap data from TFL bus API
import requests as req
import time

def req_page(str_url):
	try:
		resp=req.request(method='GET',url=str_url)
		return(resp.text)
	except:
		return("ERROR")		#error while requesting data from the page

def make_files():
	for i in range(1020):		#time for which data needs to be extracted
		get_data=req_page("https://api.tfl.gov.uk/line/354/arrivals")  #
	
		if(get_data!="ERROR"):
			temp="file_"+str(i)+".txt"
			fout=open(temp,"w")
			fout.write(get_data)
			fout.close()
			time.sleep(60) 	#retrieving data after every 60 seconds
		else:
			print("An error occured at "+str(i+1)+"th request")

make_files()

