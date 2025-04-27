# Papuga Project
Rough outline of the pipeline: (The steps in the outline are a continuous subject of discussion.)

1. Video =ffmpeg=> Images (DONE)
2. Images =nezinau=> non blurry images (DONE)
3. NBI =OpenCV=> NBI + Camera positions
4. NBI + CAM =TensoRF/OG NERF/Gaussian-something/BakedSDF?(idk) => Point cloud/mesh/gaussian
5. PC/M/G =our own code or some library=> blender

Each part of the pipeline should do roughly one thing and have one corresponding .py file. <br/>
f.ex: video_to_img.py takes by default 20 best frames (least blurred, most different) of a video in the same directory and saves them in ./images folder

later these will be combined into exe file with libraries, no need to do anything with libraries for now, just install them in your env

Libs needed so far:
pip install opencv-python