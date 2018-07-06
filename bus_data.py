import requests as req
import time

def req_page(str_url):
	try:
		resp=req.request(method='GET',url=str_url)
		return(resp.text)
	except:
		return("ERROR")		#error while requesting data from the page

def make_files():
	for i in range(1020):		#rnnning the code for 17 hours London Time:-6am to 11pm ,Singapore Time:- 1pm to 6am
		get_data=req_page("https://api.tfl.gov.uk/line/354/arrivals")  #route number 1
	
		if(get_data!="ERROR"):
			temp="file_"+str(i)+".txt"
			fout=open(temp,"w")
			fout.write(get_data)
			fout.close()
			time.sleep(60) 	#retrieving data after every 60 seconds
		else:
			print("An error occured at "+str(i+1)+"th request")

make_files()

