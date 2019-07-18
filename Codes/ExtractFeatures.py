import json
from pprint import pprint
import os
import pandas as pd
import boto3


s3 = boto3.resource('s3')
b = s3.Bucket('chokealuoct')
count_image = 0
df = pd.DataFrame()

for img_file in b.objects.all():
	path = str(img_file.key)
 	path, img = path.split('/')
	
	if img != "":
		name, ext = img.split('.') 	
		cmd  = "aws rekognition detect-faces --image \'{\"S3Object\":{\"Bucket\":\"chokealuoct\",\"Name\":\""+path+"/"+img+"\"}}\' --attributes \"ALL\" --region us-west-2 > /home/ubuntu/choke_json/out_"+name+".json"
		
	
		os.system(cmd)

		with open('/home/ubuntu/choke_json/out_'+name+'.json') as data_file:
			data = json.load(data_file)
			
		if (len(data['FaceDetails']) == 0 or len(data['FaceDetails'][0]) < 15):
			row = [ img, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]


			data = [row]


			df_temp = pd.DataFrame(data, columns=['Name', 'Confidence', 'Brightness', 'Face Area', 'Left Eye X', 'Left Eye Y', 'Right Eye X','Right Eye Y', 'Nose X','Nose Y', 'Mouth Left X', 'Mouth Left Y', 'Mouth Right X', 'Mouth Right Y', 'Age low', 'Age high', 'Sunglass Confidence', 'Sunglass Value', 'Eyeglass Confidence', 'Eyeglass Value', 'Gender Confidence', 'Gender Value', 'Eyes Open Confidence', 'Eyes Open Value', 'Smile Confidence', 'Smile Value', 'Moustache Confidence', 'Moustache Value', 'Beard Confidence', 'Beard Value' ], dtype = float)

	
			df = df.append(df_temp)

			
		else:
			#Features
			confidence = data['FaceDetails'][0]['Confidence']

			sunglasses_confidence = data['FaceDetails'][0]['Sunglasses']['Confidence']
			sunglasses_value = data['FaceDetails'][0]['Sunglasses']['Value']

			eyeglasses_confidence = data['FaceDetails'][0]['Eyeglasses']['Confidence']
			eyeglasses_value = data['FaceDetails'][0]['Eyeglasses']['Value']

			gender_value = data['FaceDetails'][0]['Gender']['Value']
			gender_confidence = data['FaceDetails'][0]['Gender']['Confidence']

			eye_left_X = data['FaceDetails'][0]['Landmarks'][0]['X']
			eye_left_Y = data['FaceDetails'][0]['Landmarks'][0]['Y']

			eye_right_X = data['FaceDetails'][0]['Landmarks'][1]['X']
			eye_right_Y = data['FaceDetails'][0]['Landmarks'][1]['Y']

			nose_X = data['FaceDetails'][0]['Landmarks'][2]['X']
			nose_Y = data['FaceDetails'][0]['Landmarks'][2]['Y']

			mouthLeft_X = data['FaceDetails'][0]['Landmarks'][3]['X']
			mouthLeft_Y = data['FaceDetails'][0]['Landmarks'][3]['Y']

			mouthRight_X = data['FaceDetails'][0]['Landmarks'][4]['X']
			mouthRight_Y = data['FaceDetails'][0]['Landmarks'][4]['Y']

			ageRange_low = data['FaceDetails'][0]['AgeRange']['Low']
			ageRange_high = data['FaceDetails'][0]['AgeRange']['High']

			eyesOpen_value = data['FaceDetails'][0]['EyesOpen']['Value']
			eyesOpen_confidence = data['FaceDetails'][0]['EyesOpen']['Confidence']

			smile_confidence = data['FaceDetails'][0]['Smile']['Confidence']
			smile_value = data['FaceDetails'][0]['Smile']['Value']

			brightness = data['FaceDetails'][0]['Quality']['Brightness']

			moustache_confidence = data['FaceDetails'][0]['Mustache']['Confidence']
			moustache_value = data['FaceDetails'][0]['Mustache']['Value']

			beard_confidence = data['FaceDetails'][0]['Beard']['Confidence']
			beard_value = data['FaceDetails'][0]['Beard']['Value']
			
			bb_w = data['FaceDetails'][0]['BoundingBox']['Width']
			bb_h = data['FaceDetails'][0]['BoundingBox']['Height']
			
			face_area = bb_w * bb_h

	
			row = [ img, confidence, brightness, face_area, eye_left_X, eye_left_Y, eye_right_X, eye_right_Y, nose_X, nose_Y, mouthLeft_X, mouthLeft_Y, mouthRight_X, mouthRight_Y, ageRange_low, ageRange_high, sunglasses_confidence, sunglasses_value, eyeglasses_confidence, eyeglasses_value, gender_confidence, gender_value, eyesOpen_confidence, eyesOpen_value, smile_confidence, smile_value, moustache_confidence, moustache_value, beard_confidence, beard_value ]


			data = [row]


			df_temp = pd.DataFrame(data, columns=['Name', 'Confidence', 'Brightness', 'Face Area', 'Left Eye X', 'Left Eye Y', 'Right Eye X','Right Eye Y', 'Nose X','Nose Y', 'Mouth Left X', 'Mouth Left Y', 'Mouth Right X', 'Mouth Right Y', 'Age low', 'Age high', 'Sunglass Confidence', 'Sunglass Value', 'Eyeglass Confidence', 'Eyeglass Value', 'Gender Confidence', 'Gender Value', 'Eyes Open Confidence', 'Eyes Open Value', 'Smile Confidence', 'Smile Value', 'Moustache Confidence', 'Moustache Value', 'Beard Confidence', 'Beard Value' ], dtype = float)

	
			df = df.append(df_temp)
			df.to_csv('AWSFeatures_ChokePoint.csv')
			count_image = count_image + 1
			if count_image % 10 == 0:
				print "Number of Images Done= " + str(count_image)

#after for loop


