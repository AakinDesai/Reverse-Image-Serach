# Reverse Image Search

## Summary

Image search engines that quantify the contents of an image are called Content-Based Image Retrieval(CBIR) systems. 

### Four Steps of Any CBIR System

1. **Define image descriptor:** Image descriptor is an alogrithm which is used to describe an image. Three different type of image descriptors (Color Histogram, Region Adjacency Graphs and Structural Similarity Index) are used for this project.
2. **Index dataset:** Image descriptor to each image in dataset is applied, features are extracted, and are wrote to storage (ex. CSV file, RDBMS, Redis, etc.) so that they can be later compared for similarity.
3. **Define similarity metric:** Chi-squared distance for Histogram method and Hausdorff’s distance for RAG features are used.
4. **Searching:** Features from the image are extracted and then similarity function is applied to compare the image features to the features already indexed. 

### Result

Method | Precision | Recall | F1-score | SSIM 
--- | --- | --- | --- | ---
Global Color Histogram | 0.714 | 0.5 | 0.588 | 0.53 
Regional Color Histogram | 0.67 | 0.8 | 0.729 | 0.57 
RAG based description | 0.375 | 0.3 | 0.33 | 0.63 
