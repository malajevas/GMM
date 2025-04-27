import cv2
import numpy as np
import os
import argparse

def get_video(video_path):
    if video_path == '':
        video_files = [f for f in os.listdir('.') if f.endswith(('.mp4', '.avi', '.mov'))]
        if not video_files:
            raise ValueError("No video files found in the current directory.")
        video_path = video_files[0]
    
    print(f"Using video file: {video_path}")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file")
        exit(1)
    return cap

def extract_best_frames(video_path, req_frames):
    # Find and Open video
    cap = get_video(video_path)
    
    # Get video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Video has {total_frames} frames at {fps} FPS")
    
    if total_frames <= req_frames:
        print(f"Video has fewer frames ({total_frames}) than requested ({req_frames})")
        req_frames = total_frames
    
    # Calculate the approximate step size to get evenly distributed frames
    step = total_frames // (req_frames * 3)  # We'll analyze 3x more frames than needed
    if step < 1:
        step = 1
    
    # Track frame info
    frame_scores = []
    prev_frame = None
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Only process every 'step' frames to save time
        if frame_count % step == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Calculate blur score | higher is better/sharper
            blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Calculate difference from previous frame | higher is better
            diff_score = 0
            if prev_frame is not None:
                diff = cv2.absdiff(prev_frame, gray)
                diff_score = np.sum(diff)

            diff_score = diff_score / (gray.shape[0] * gray.shape[1])
                        
            frame_scores.append((blur_score, diff_score, frame_count, frame))
            prev_frame = gray
        
        frame_count += 1
    
    cap.release()
    
    blur_scores = [score[0] for score in frame_scores]
    diff_scores = [score[1] for score in frame_scores]
    # Normalize scores
    blur_scores = (blur_scores - np.min(blur_scores)) / (np.max(blur_scores) - np.min(blur_scores))
    diff_scores = (diff_scores - np.min(diff_scores)) / (np.max(diff_scores) - np.min(diff_scores))

    # Combine scores into a single score
    # blurry is worse than diff
    combined_scores = 5*blur_scores + diff_scores
    frame_scores = [(combined_scores[i], frame_scores[i][2], frame_scores[i][3]) for i in range(len(frame_scores))]

    for f in frame_scores:
        print(f"Frame {f[1]}: Score: {f[0]:.2f}")

    # Sort frames by score (highest scores first)
    frame_scores.sort(reverse=True)
    
    # select first req_frames frames
    selected_frames = frame_scores[:req_frames]
    
    return selected_frames

def save_frames(frames, output_dir):
    frames = sorted(frames, key=lambda x: x[1])
    os.makedirs(output_dir, exist_ok=True)
    
    for i, frame in enumerate(frames):
        output_path = os.path.join(output_dir, f"image{i:03d}.png")
        cv2.imwrite(output_path, frame[2])
        print(f"Saved {output_path}")


def main():
    # Argument parsing stuff
    parser = argparse.ArgumentParser(description="Extract and extract least blurred frames from a video file.")

    parser.add_argument("-v", "--video", type=str, default='', help="Path to the input video file (default: first video in directory).")
    parser.add_argument("-o", "--output", type=str, default='images', help="Directory to save the output frames (default './images').")
    parser.add_argument("-s", "--select_top", type=int, default=20, help="Number of least blurred frames to save (default 20).")

    args = parser.parse_args()

    save_frames(extract_best_frames(args.video, args.select_top), args.output)

# Example usage
if __name__ == "__main__":
    main()
