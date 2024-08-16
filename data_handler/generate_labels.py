import os
import shutil
all_files = os.listdir()
mp4_files = [file for file in all_files if file.endswith('.mp4')]

os.makedirs('images', exist_ok=True)
os.makedirs('labels', exist_ok=True)

#this means that the first 106 frames are closed, the next 105 frames are open, and the last 424 frames are closed
event = {'01.mp4': [(0,106),(106,211),(211,635)],
         '02.mp4': [(0,1379),(1380,2182),(2183,3058)],
         '03.mp4': [(0,46),(47,147),(148,456)],
        } 

#bb_pos indicates the bounding box position for each frame in the video. The format is "class_id x_center y_center width height" for each frame.
bb_pos = {"01.mp4": ["0 0.5015625 0.21953125 0.99296875 0.43671875","1 0.503125 0.28671875 0.99375 0.565625"],
                 "02.mp4":["0 0.5 0.6890625 1 0.58125","1 0.5 0.7390625 1 0.521875"],
                 "03.mp4":["0 0.5 0.23671875 0.99765625 0.46328125","1 0.50078125 0.60078125 0.9984375 0.77734375"],
                }
                

for video, events in event.items():
    print(video, events)

    frame_folder = os.path.join('dataset',f"{video}_frames")
    frame_head = video.split(".")[0]

    for i in range(0,3):

        start_frame = events[i][0]
        end_frame = events[i][1]
    
        if i == 0:
            bb_position = bb_pos[video][0]
        elif i == 1:
            bb_position = bb_pos[video][1]
        else:
            bb_position = bb_pos[video][0]

        
        for frame_num in range(start_frame, end_frame + 1):
          
            frame_filename = frame_head + f'_frame_{frame_num:04d}.jpg'
        
            frame_filename_label = frame_head + f'_frame_{frame_num:04d}.txt'

            shutil.copy(os.path.join(frame_folder, frame_filename), 'images')
            with open(os.path.join('labels', frame_filename_label), 'w') as f:
                f.write(bb_position)