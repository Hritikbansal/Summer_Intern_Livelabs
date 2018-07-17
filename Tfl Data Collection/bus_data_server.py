#Code to extract bus data for different bus routes on a particular day
import requests as req
import time

def req_page(str_url):
	try:
		resp=req.request(method='GET',url=str_url)
		#print(resp.text)
		return(resp.text)
	except:
		return("ERROR")		#error while requesting data from the page


def make_files():

	f1=open("file_route_25.txt","a")
	f2=open("file_route_17.txt","a")
	f3=open("file_route_145.txt","a")
	f4=open("file_route_12.txt","a")
	f5=open("file_route_326.txt","a")
	f6=open("file_route_111.txt","a")

	

	for i in range(480): #Time for which data needs to be retrieved
		
		print(i)
		get_data_25=req_page("https://api.tfl.gov.uk/line/25/arrivals")  #route number 25
		get_data_17=req_page("https://api.tfl.gov.uk/line/17/arrivals")  
		get_data_145=req_page("https://api.tfl.gov.uk/line/145/arrivals")  
		get_data_12=req_page("https://api.tfl.gov.uk/line/12/arrivals")  
		get_data_326=req_page("https://api.tfl.gov.uk/line/326/arrivals")  
		get_data_111=req_page("https://api.tfl.gov.uk/line/111/arrivals")  

		if(get_data_25!="ERROR"):
			if(i==0):
				get_data_25=get_data_25[:(len(get_data_25)-1)]
				f1.write(get_data_25)
				
			elif(i==479):
				get_data_25=","+get_data_25[1:(len(get_data_25))]
				f1.write(get_data_25)
	
			else:
				get_data_25=","+get_data_25[1:(len(get_data_25)-1)]
				f1.write(get_data_25)
		else:
			print("An error occurred at "+str(i+1)+"th request in 25th route")

		if(get_data_17!="ERROR"):
			if(i==0):
				get_data_17=get_data_17[:(len(get_data_17)-1)]
				f2.write(get_data_17)
			elif(i==479):
				get_data_17=","+get_data_17[1:(len(get_data_17))]
				f2.write(get_data_17)
			else:
				get_data_17=","+get_data_17[1:(len(get_data_17)-1)]
				f2.write(get_data_17)
		else:
			print("An error occurred at "+str(i+1)+"th request in 17th route")

		if(get_data_145!="ERROR"):
			if(i==0):
				get_data_145=get_data_145[:(len(get_data_145)-1)]
				f3.write(get_data_145)
			elif(i==479):
				get_data_145=","+get_data_145[1:(len(get_data_145))]
				f3.write(get_data_145)
			else:
				get_data_145=","+get_data_145[1:(len(get_data_145)-1)]
				f3.write(get_data_145)
		else:
			print("An error occurred at "+str(i+1)+"th request in 145th route")

		if(get_data_12!="ERROR"):
			if(i==0):
				get_data_12=get_data_12[:(len(get_data_12)-1)]
				f4.write(get_data_12)
			elif(i==479):
				get_data_12=","+get_data_12[1:(len(get_data_12))]
				f4.write(get_data_12)
			else:
				get_data_12=","+get_data_12[1:(len(get_data_12)-1)]
				f4.write(get_data_12)
		else:
			print("An error occurred at "+str(i+1)+"th request in 12th route")

		if(get_data_326!="ERROR"):
			if(i==0):
				get_data_326=get_data_326[:(len(get_data_326)-1)]
				f5.write(get_data_326)
			elif(i==479):
				get_data_326=","+get_data_326[1:(len(get_data_326))]
				f5.write(get_data_326)
			else:
				get_data_326=","+get_data_326[1:(len(get_data_326)-1)]
				f5.write(get_data_326)
		else:
			print("An error occurred at "+str(i+1)+"th request in 326th route")

		if(get_data_111!="ERROR"):
			if(i==0):
				get_data_111=get_data_111[:(len(get_data_111)-1)]
				f6.write(get_data_111)
			elif(i==479):
				get_data_111=","+get_data_111[1:(len(get_data_111))]
				f6.write(get_data_111)
			else:
				get_data_111=","+get_data_111[1:(len(get_data_111)-1)]
				f6.write(get_data_111)
		else:
			print("An error occurred at "+str(i+1)+"th request in 111th route")

		time.sleep(30)  #time elapsed after each call


	f1.close()
	f2.close()
	f3.close()
	f4.close()
	f5.close()
	f6.close()
	
make_files()

