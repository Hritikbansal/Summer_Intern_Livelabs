#Simple code to convert any json format containing file to csv format
import pandas as pd 
#pd.read_json("filename in json format").to_csv("filename in csv format")
pd.read_json("file_route_12.txt").to_csv("file_route_12.csv")

		
