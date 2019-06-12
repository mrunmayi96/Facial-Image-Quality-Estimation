# Facial-Image-Quality-Estimation

We propose a framework for facial image quality estimation in order to address the limitation of real-time applicability of facial recognition. This framework determines whether an image is suitable for facial recognition. We first exploit machine learning algorithms to map the relationship between image quality features and performance of facial recognition. We extract a variety of features (like focus measure, brightness, obscured face) and study their influence on the accuracy of face recognition. After examining the results of this approach, we then used deep learning to build a binary classifier which accepts or rejects images before sending them for actual facial recognition. This decision is taken based on the probability of the facial recognition framework correctly matching a face from the image. We used images from the Chokepoint dataset, and OpenFace- an open source facial recognition software, for building our framework.


Based on the paper - Towards Designing an Adaptive Framework for Facial Image Quality Estimation at Edge
https://ieeexplore.ieee.org/document/8529475

