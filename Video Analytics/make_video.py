# Capturing video to test it on the proposed algorithm

import cv2
import numpy as np
import time

t0=time.time() #start time in seconds


cap=cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('occlusion.avi',fourcc, 30.0, (640,480),True)


while(True):
	ret,frame=cap.read()
	out.write(frame)
	#cv2.imshow('frame',frame)
	
	t1=time.time()
	diff=t1-t0
	if(diff>30):  		#Making a video of 30 seconds 
		break
	
	if(cv2.waitKey(1)&0xFF==ord('q')):
		break

cap.release()
out.release()
cv2.destroyAllWindows()


	

