# Facial-Image-Quality-Estimation

## Introduction
We propose a framework for facial image quality estimation in order to address the limitation of real-time applicability of facial recognition. This framework determines whether an image is suitable for facial recognition. We first exploited machine learning algorithms to map the relationship between image quality features and performance of facial recognition. We extract a variety of features (like focus measure, brightness, obscured face) and studied their influence on the accuracy of face recognition. After examining the results of this approach, we then used deep learning to build a binary classifier which accepts or rejects images before sending them for actual facial recognition. This decision is taken based on the probability of the facial recognition framework correctly matching a face from the image. We used images from the Chokepoint dataset, and OpenFace- an open source facial recognition software, for building our framework.

### Running the digits model: 

```
$ nvidia-docker run -d -p 5678:5000 -v /home/$USER/Desktop/BE_Project/datafolder/digits/data/:/data/ -v /home/$USER/Desktop/BE_Project/datafolder/digits/jobs/:/jobs --name digits5 nvidia/digits
```

### Using the model to predict a set of images:
- Can be a single image or a folder of images 
- Nvidia-digits uses the port 5678 
```
curl localhost:5678/models/images/classification/classify_many.json -XPOST -F job_id=20180503-094000-45e6 -F image_list=@/home/$USER/Desktop/BE_Project/datafolder/digits/data/va2.txt > /home/$USER/Desktop/BE_Project/FinalDemo/Data/predictionV2.json
```


### Towards Designing an Adaptive Framework for Facial Image Quality Estimation at Edge
Refer to the following paper describing the work in this project - 
https://ieeexplore.ieee.org/document/8529475

<br>
