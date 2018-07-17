import cv2
import numpy as np

#function to return the coordinates of the bounding box
def loc(string):
	#print(string)	
	l=[]
	for h in range(len(string)):
		if (string[h]=="("):
			for k in range(len(string[h+1:])):
				if((string[h+1:])[k]==")"):		
					l.append((string[h+1:])[:k])
					break
					
	#print(l)
	h1=l[0].split(", ")[0]
	w1=l[0].split(", ")[1]
	h2=l[1].split(", ")[0]
	w2=l[1].split(", ")[1]
	return (h1,w1,h2,w2)	

def check_person(string): #to check if the made detection is of a person or not
	l=string.count("15:")
	if(l!=0):	#the detected object is a person
		return True
	return False


f=open("result_occ.txt","r")

li=f.readlines()



frames=[]
#print(li)

f1=open("framelist_occ.txt","w")
for k in li:
	people=[]
	if(k!="\n"):	#if there are some detections in that frame 
		num_det_frame=k.count("and")
		if(num_det_frame!=0):  
			sp_li=k.split(" and ")	
			for i in range(len(sp_li)):
				if(check_person(sp_li[i])):
					people.append(loc(sp_li[i]))
		else:
			if(check_person(k)):
				people.append(loc(k))

	frames.append(people)
	f1.write(str(people)+"\n")


print(len(frames))
f1.close()
