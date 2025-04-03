# Papuga Project
Rough outline of the pipeline: (The steps in the outline are a continuous subject of discussion.)

1. Video =ffmpeg=> Images
2. Images =nezinau=> non blurry images
3. NBI =OpenCV=> NBI + Camera positions
4. NBI + CAM =TensoRF/OG NERF/Gaussian-something/BakedSDF?(idk) => Point cloud/mesh/gaussian
5. PC/M/G =our own code or some library=> blender

Each part of the pipeline should do exactly ONE thing and have one corresponding .py file. <br/>
E.g.: <br/>
**video_to_img.py** should take the first .mp4(or some other) file in the same directory and use ffmpeg to transform it into a collection of images and put them into a folder /data, such that the the image paths are /data/img001.jpg /data/img002.jpg and so on. 

**delete_blurry.py** should read through each image in /data and delete those that are blurry.

If the .py file requires to use a non-standard library, either make the .py file download the libraries before running the main code, or add the library files to the commit at /src/lib.py or something like that.
