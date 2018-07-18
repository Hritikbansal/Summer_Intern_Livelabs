# Summer_Intern_SMU
Tfl Bus Data Collection and Video Analytics


Detailed Documentation can be found at:

https://docs.google.com/document/d/1tDaomsvD9iYBNnc_bVxJDLeGC3CN9RRyQGKF70ALqiw/edit


Usage in Video Analytics Project(Not real time):

1.Capture a video using make_video.py
2.Detection happens using NCS connected to the PC(Rpi) and ncsdk/ncappzoo
3.live-object-detector.py in live-object-detector app of ncappzoo is made to run on captured video.
4.Result video and result file are generated.
5.Result file is converted into framelist file using convert_to_framelist.py
6.framelist file and result video are used by trackncount.py to calculate the number of people 
  who have moved left to right/right to left across the screen.
  
 Results for the above procedure are present in the google doc attached above.
