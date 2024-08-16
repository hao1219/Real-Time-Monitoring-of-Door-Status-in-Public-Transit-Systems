import os
import json
from thresholding import MY_YOLO5


def guess_door_opening(opening_frame = 100):
    print('opening frame ', opening_frame)
    return int(opening_frame)  

def guess_door_closing(closing_frame = 100):
    print('closing frame ', closing_frame)
    return int(closing_frame)

def Gen_States_Dict(my_yolo:MY_YOLO5):
    states_dict = []
    for i in range(min(len(my_yolo.opening_frame), len(my_yolo.closing_frame))):
        open_dict = {
                        "state_id": i*2+1,
                        "description": "Opening",
                        "guessed_frame": guess_door_opening(my_yolo.opening_frame[i])  
                    }
        close_dict = {
                        "state_id": i*2+2,
                        "description": "Closing",
                        "guessed_frame": guess_door_closing(my_yolo.closing_frame[i])  
                    }
        states_dict.append(open_dict)
        states_dict.append(close_dict)

    return states_dict



def scan_videos(directory):
    """Scan the specified directory for MP4 files and generate JSON annotations."""
    video_files_ori = [f for f in os.listdir(directory) if f.endswith('.mp4')]
    video_files = [os.path.join(directory, i) for i in video_files_ori]
    print(video_files)
    videos_info = []
    my_yolo = MY_YOLO5()

    for idx, video_file in enumerate(video_files):
        my_yolo.main(video_file)
        Sates_dict = Gen_States_Dict(my_yolo)
        videos_info.append({
            "video_filename": video_files_ori[idx],
            "annotations": [
                {
                    "object": "Door",
                    "states": Sates_dict
                }
            ]
        })

    return videos_info

def generate_json(output_filename, videos_info):
    """Generate a JSON file with the provided video information."""
    with open(output_filename, 'w') as file:
        json.dump({"videos": videos_info}, file, indent=4)

def main():
    # Specify the directory to scan
    ########################################################
    directory = "Tests"  
    # directory = "../Samples"
    #########################################################

    output_filename = "output.json"  # Output JSON file name

    videos_info = scan_videos(directory)
    generate_json(output_filename, videos_info)
    print(f"Generated JSON file '{output_filename}' with video annotations.")

if __name__ == "__main__":
    main()
