import cv2
import os

videos = [f for f in os.listdir('dataset') if f.endswith('.mp4')]
print(videos)
for video in videos:
    output_dir = os.path.join("dataset",f"{video}_frames" )
    print(output_dir)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    video_path = os.path.join('dataset', video)
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video.")
        exit()

    frame_count = 0
    while True: 
        ret, frame = cap.read()
        if not ret:
            break
        header = video.split(".")[0]
        frame_filename = os.path.join(output_dir, f'{header}_frame_{frame_count:04d}.jpg')

        cv2.imwrite(frame_filename, frame)

        frame_count += 1

    cap.release()

    print(f"Extracted {frame_count} frames from the video.")