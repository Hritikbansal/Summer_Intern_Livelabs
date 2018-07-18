#Capture video using make_video.py
#Get detected video using MobileDet with NCS plugged in
#Convert the text file into framelist list with frames which have person in them
#Run trackncount.py to find the number of people in the captured video

#Multiple object tracking
import cv2
import numpy as np


cap=cv2.VideoCapture("result_exp_8.avi")
a=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
##print(a)
b=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
##print(b)
v_line_l2r=int(a*(0.65))  #to the right side of the screen
#print("virtual line 1= "+str(v_line_l2r))

v_line_r2l=int(a*(0.35)) #to the left side of the screen
#print("virtual line 2= "+str(v_line_r2l))

#Tackling a simpler problem where people 
#are moving one after another..rather than
#multiple people entering a place at the same
#time
#loading the file which has all the frames

def reached_vline_l2r(x1,x2):
	#for an object moving from left to right
	if(x2>v_line_l2r and x1<v_line_l2r):
		return True
	return False

def reached_vline_r2l(x1,x2):
	#for an object moving from left to right
	if(x2>v_line_r2l and x1<v_line_r2l):
		return True
	return False

def crossed_vline_l2r(x1,x2):
	if(x2>v_line_l2r and x1>=v_line_l2r):
		return True
	return False

def crossed_vline_r2l(x1,x2):
	if(v_line_r2l>=x2 and v_line_r2l>x1):
		return True
	return False

def find_ind(li,tup):  
	for i in range(len(li)):
		#f0.write(str((li[i],tup)))
		#f0.write("\n")
		if li[i]==tup:
			return i


def present_in_next_frame_l2r(li1,li2,x1,x2,y1,y2):#li2 is the next frame of li1
	##print(li1,(str(y1),str(x1),str(y2),str(x2)))
	ind=find_ind(li1,(str(y1),str(x1),str(y2),str(x2)))

	if(len(li2)!=0):#non-empty next frame
		for k in li2:
			if(k!=0):
				#f0.write(str(k))
				#f0.write("\n")
				x11,x22,y11,y22=int(k[1]),int(k[3]),int(k[0]),int(k[2])
				if((x1)<=x11<=(x1+50) and (x2-5)<=x22<=(x2+50)): #Hard constraint on x1
					#print(2)
					li1[ind]=0	#this bounding box has been visited..0 is a flag
					if(crossed_vline_l2r(x11,x22)):
						ind=li2.index(k)
						li2[ind]=0
					return (True,(x11,x22,y11,y22))
				else:
				#if((y1-20)<y11<=(y1+20) or (y2-20)<y22<=(y2+20)):  #Softer Constraint
				#	return (True,(x11,x22,y11,y22))
				#	else:
					#print(3)
					if(k==li2[len(li2)-1]):
						return (False,(x1,x2,y1,y2))
					else:
						continue
			else:
				return(False,(x1,x2,y1,y2))
	else:
		#print(4)
		return(False,(x1,x2,y1,y2)) #this frame has no person detection so we have to send coordinates of initial frame


def present_in_next_frame_r2l(li1,li2,x1,x2,y1,y2):#li2 is the next frame of li1

	ind=find_ind(li1,(str(y1),str(x1),str(y2),str(x2)))
	
	if(len(li2)!=0):#non-empty next frame
		for k in li2:
			if(k!=0):
				#f0.write(str(k))
				#f0.write("\n")
				x11,x22,y11,y22=int(k[1]),int(k[3]),int(k[0]),int(k[2])
				if((x1-50)<=x11<=(x1+5) and (x2-50)<=x22<=(x2)): #hard constraint on x2
					li1[ind]=0
					if(crossed_vline_r2l(x11,x22)):
						ind=li2.index(k)
						li2[ind]=0
					return (True,(x11,x22,y11,y22))
				else:
				#if((y1-20)<y11<=(y1+20) or (y2-20)<y22<=(y2+20)):
				#	return (True,(x11,x22,y11,y22))
				#	else:
					if(k==li2[len(li2)-1]):
						return (False,(x1,x2,y1,y2))
					else:
						continue
			else:
				return(False,(x1,x2,y1,y2))
	else:
		return(False,(x1,x2,y1,y2)) #this frame has no person detection so we have to send coordinates of initial frame



def track_l2r(frame_list,x1,x2,y1,y2):#list of maximum 30 frames

	coor=(x1,x2,y1,y2) #initial coordinates of the bounding box
	j=0
	m=0 #number of detection misses
	#f0.write(str(frame_list))
	#f0.write("\n")
	length=len(frame_list)
	if(length<2):
		return(False,length)
	else:
		while(j in range(length-1)):
			ret,coor=present_in_next_frame_l2r(frame_list[j],frame_list[j+1+m],coor[0],coor[1],coor[2],coor[3])
			#print(1)
			#f0.write(str((frame_list[j],frame_list[j+1+m])))
			#f0.write("\n")
			if(ret==True):
				if(crossed_vline_l2r(coor[0],coor[1])):#the person has crossed the virtual line
					#frame_list[j+1+m]=0 		#this frame has obviously been visited
					#f0.write("crossed "+str(coor))
					#f0.write("\n")
					return (True,j+1+m)
				else:
					if(m!=0):
						j=j+1+m
						m=0
						if(j==length-1):
							#f1.write(str(length-1)+" 1\n")
							return(False,length-1)
					else: #m==0
						j=j+1
						if(j==length-1):
							##f1.write(str(length-1)+" 2\n")
							return(False,length-1)

			else: #the track has been lost of the person 
				m+=1    #number of frames in which the person has not been found
				if(m<5):	
					if(j<=length-2-m):
						#f1.write(str(55)+" 3\n")
						continue
					else:
						#f1.write(str(length)+" 4\n")
						return(False,length)
				else:
					#f1.write(str(j+1)+" 5\n")
					return(False,j+1)

def track_r2l(frame_list,x1,x2,y1,y2):#list of maximum 30 frames

	coor=(x1,x2,y1,y2) #initial coordinates of the bounding box
	j=0
	m=0 #number of detection misses
	#f0.write(str(frame_list))
	#f0.write("\n")
	length=len(frame_list)
	if(length<2):
		return(False,length)
	else:
		while(j in range(length-1)):
			ret,coor=present_in_next_frame_r2l(frame_list[j],frame_list[j+1+m],coor[0],coor[1],coor[2],coor[3])
			#f0.write(str((frame_list[j],frame_list[j+1+m])))
			#f0.write("\n")
			if(ret==True):
				if(crossed_vline_r2l(coor[0],coor[1])):#the person has crossed the virtual line
					#frame_list[j+1+m]=0			#this frame has obviously been visited
					#f0.write("crossed "+str(coor))
					#f0.write("\n")
					return (True,j+1+m)

				else:
					if(m!=0):
						j=j+1+m
						m=0
						if(j==length-1):
							#f2.write(str(length-1)+" 1\n")
							return(False,length-1)
					else: #m==0
						j=j+1
						if(j==length-1):
							#f2.write(str(length-1)+" 2\n")
							return(False,length-1)
			else: #the track has been lost of the person 
				m+=1    #number of frames in which the person has not been found
				if(m<5):	
					if(j<=length-2-m):
						#f2.write(str(55)+" 3\n")
						continue
					else:
						#f2.write(str(length)+" 4\n")
						return(False,length)
				else:
					#f2.write(str(j+1)+" 5\n")
					return(False,j+1)


def count_l2r(frames): 
	i=0
	length=len(frames)
	tot_count_l2r=0  #number of people who have entered the frame from left to right
	
	while(i in range(length)): #within 30 frames(overestimation) the the count needs to be increased 
		#format is (h1,w1,h2,w2)
		#f1.write(str(frames[i])+"\n")

		if(len(frames[i])!=0):
			#Assuming that only one of them will cross the virtual line at a time
			for j in range(len(frames[i])):

				if(frames[i][j]!=0):		#this bounding box in that frame has been tracked/visited before
					x1,x2=int(frames[i][j][1]),int(frames[i][j][3])
					y1,y2=int(frames[i][j][0]),int(frames[i][j][2])
					boolean=reached_vline_l2r(x1,x2)
					if(boolean==True):	
						##print(1)
						#f0.write(str(frames[i][j]))
						#f0.write("\n")			
						if(i<length-30):
							#f1.write(str(6)+"\n")
							ret,ind=track_l2r(frames[i:i+30],x1,x2,y1,y2)
							#f0.write(str(ret))
							#f0.write("\n")
						else:
							#f1.write(str(7)+"\n")
							##print(frames[i])
							##print(frames[i:length])
							ret,ind=track_l2r(frames[i:length],x1,x2,y1,y2)
							#f0.write(str(ret))
							#f0.write("\n")
							#the person crossing the line needs to be tracked within 30 frames
							#ret is the bool which returns True if a person has crossed the virtual line in that window
							#ind is the index of the frame in which the person has crossed the line in the window of 30 frames if ret is true
							#if ret is false then it returns the index from which fresh search should be made
						if(ret==True):
							#f1.write(str(8)+"\n")
							tot_count_l2r+=1
							#k=i+(ind+1)
						
						else:
							##print(2)
							##print(ind)
							#f1.write(str(9)+"\n")
							#k=i+ind
							##print(i,length)

			i=i+1 	#Increment value		
			
		else:
			#nothing detected in this frame
			#f1.write(str(5)+"\n")
			i=i+1

	##print(tot_count_l2r)
	return tot_count_l2r


def count_r2l(frames): 
	i=0
	length=len(frames)
	tot_count_r2l=0  #number of people who have entered the frame from left to right
	
	while(i in range(length)): #within 30 frames(overestimation) the the count needs to be increased 
		#format is (h1,w1,h2,w2)
		#f2.write(str(frames[i])+"\n")
	
		if(len(frames[i])!=0):

			for j in range(len(frames[i])):

				if(frames[i][j]!=0):  #this bounding box in the frame has been visited before

					x1,x2=int(frames[i][j][1]),int(frames[i][j][3])
					y1,y2=int(frames[i][j][0]),int(frames[i][j][2])
					boolean=reached_vline_r2l(x1,x2)

					if(boolean==True):	
						##print(1)
						#f0.write(str(frames[i][j]))		
						#f0.write("\n")		
						if(i<length-30):
							#f2.write(str(6)+"\n")
							ret,ind=track_r2l(frames[i:i+30],x1,x2,y1,y2)
							#f0.write(str(ret))
							#f0.write("\n")
						else:
							#f2.write(str(7)+"\n")
						##print(frames[i])
						##print(frames[i:length])
							ret,ind=track_r2l(frames[i:length],x1,x2,y1,y2)
							#f0.write(str(ret))
							#f0.write("\n")
						#the person crossing the line needs to be tracked within 30 frames
						#ret is the bool which returns True if a person has crossed the virtual line in that window
						#ind is the index of the frame in which the person has crossed the line in the window of 30 frames if ret is true
						#if ret is false then it returns the index from which fresh search should be made
						if(ret==True):
							#f2.write(str(8)+"\n")
							tot_count_r2l+=1
								#break
						else:
						##print(2)
						##print(ind)
							#f2.write(str(9)+"\n")
				   
						##print(i,length)
			i=i+1		
				
		else:
			#nothing detected in this frame
			#f2.write(str(5)+"\n")
			i=i+1

	##print(tot_count_r2l)
	return tot_count_r2l


		
def main():
	
	f1=open("framelist_exp_8.txt","r")
	#framelist has all the frames in the video..only the location of bounding box of a person is present

	frames_l2r=[]
	frames_r2l=[]
	#assuming left to right calculation
	for line in f1:
		#line[-1] because the last element of each string is a breakline character
		# eval is used for considering every line as list rather than a string
		frames_l2r.append(eval(line[:-1]))
		frames_r2l.append(eval(line[:-1])) 	

	##print(frames_l2r)

	tot_l2r=count_l2r(frames_l2r)
	#print(tot_l2r)
	#f0.write("------------------------------------------------")		#differentiate between l2r and r2l..easy to debug
	#f0.write("\n")
	tot_r2l=count_r2l(frames_r2l)

	print("total people l2r is= "+str(tot_l2r))
	print("total people r2l is= "+str(tot_r2l))

main() #this is the main function that will be called in the program