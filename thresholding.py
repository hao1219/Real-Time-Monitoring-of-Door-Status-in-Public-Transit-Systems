import torch
import cv2
import os
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import logging

class MY_YOLO5:
    def __init__(self, weights_path='yolov5/best.pt'):
        # Configure logging
        logging.basicConfig(level=logging.WARNING)  # INFO or DEBUG to show other info
        print("Initializing YOLOv5...")
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = torch.hub.load('yolov5', 'custom', path=weights_path, source='local').to(self.device)
        self.model.conf = 0.1
        self.class_names = self.model.names

        self.closing_frame, self.opening_frame = [100], [100]
        self.real_peak = []
        # Initialize frame data
        self.frame_classes = []
        self.frame_confis = []
        self.closed_frame_confis = []

    def plot_results(self, frame_classes, frame_confis, closed_frame_confis, diff_frame_classes, source_video):
        plt.figure()
        plt.plot(self.frame_classes, label='class')
        #plt.plot(closed_frame_confis, label='closed_frame_confi')
        #plt.plot(diff_frame_classes, label='class_change_diff')
        plt.xlabel('Frame')
        plt.ylabel('Confidence / Class')
        plt.grid()
        plt.legend()
        plt.title('Class and Confidence Changes Over Frames')
        plot_path = os.path.join(f'{source_video}_class_changes.png')
        plt.savefig(plot_path)
        plt.close()

    def open_close_generate(self, frame_classes=[], source_video='', Peak_indices=[]):
    
        diff_frame_classes = np.diff(frame_classes)
        peak_indices = np.where(diff_frame_classes != 0)[0]

        print(f"Initial Peak indices: {peak_indices}")

        def is_valid_peak(frame_classes,index,real_peak_i):
           
            window_size = 10
            if index < window_size or index >= len(frame_classes) - window_size:
                return False 
            
            if real_peak_i % 2 == 0:
               right_window = frame_classes[index + 1:index + 1 + window_size]
               if np.mean(right_window)<0.5:
                   return False
               for i in range(1, window_size + 1):
                   if (index + i) in peak_indices:
                       return False 
            else:  
               left_window = frame_classes[index - window_size:index]   
               if np.mean(left_window)<0.5:
                     return False
               for i in range(1, window_size + 1):
                if (index - i) in peak_indices:
                    return False
            return True

        self.opening_frame, self.closing_frame,self.real_peak= [], [], []
        
        peak_i = 0
        real_peak_i = 0
        while peak_i < len(peak_indices):
            if is_valid_peak(frame_classes,peak_indices[peak_i],real_peak_i):
                self.real_peak.append(peak_indices[peak_i])
                real_peak_i += 1
                peak_i += 1
            else:
                peak_i += 1
        print(f"Real Peak indices: {self.real_peak}")
        for i, peak in enumerate(self.real_peak):
            if i % 2 == 0:
                self.opening_frame.append(peak)
            else:
                self.closing_frame.append(peak)

        print(f'OPENING {self.opening_frame}\nCLOSING {self.closing_frame}')
       
        return 0


    def rotate_frame(self, frame):
        # Rotate frame 90 degrees clockwise and return it
        return cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    def process_video(self, source_video, rotate=False):
        cap = cv2.VideoCapture(source_video)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f'Accept video {source_video}, Total Frames {total_frames}')

        self.frame_classes = []  # Reset class frame list
        self.frame_confis = []   # Reset confidence frame list
        self.closed_frame_confis = []  # Reset closed frame confidence list

        low_confidence_count = 0
        confidence_threshold = 0.1
        confidence_threshold_closed = 0.6

        with tqdm(total=total_frames, desc=f"Processing {source_video}", unit="frame") as pbar:
            for i in range(total_frames):
                ret, frame = cap.read()
                if not ret:
                    break

                # Rotate frame if needed
                if rotate:
                    frame = self.rotate_frame(frame)

                results = self.model(frame)
                if len(results.xyxy[0]) > 0:
                    # Get the highest confidence bounding box
                    max_conf_result = max(results.xyxy[0], key=lambda result: result[4])
                    x1, y1, x2, y2, conf, cls = max_conf_result
                    
                    cls = int(cls)
                    frame_confi = conf.item()
                    self.frame_confis.append(frame_confi)

                    # Set closed frame confidence
                    if cls == 1 or frame_confi < confidence_threshold_closed:
                        closed_frame_confi = 0
                    else:
                        closed_frame_confi = frame_confi
                    self.closed_frame_confis.append(closed_frame_confi)

                    # Count low confidence frames
                    if frame_confi < confidence_threshold:
                        low_confidence_count += 1
                    else:
                        low_confidence_count = 0  # Reset counter if confidence is high
                else:
                    # Default to state 0 if no bounding boxes are detected
                    self.frame_confis.append(0)
                    self.closed_frame_confis.append(0)
                    low_confidence_count += 1

                pbar.update(1)

                # Check if last 50 frames had low confidence
                if low_confidence_count >= 50:
                    cap.release()
                    return False  # Signal to rotate and reprocess

        
        for i in range(len(self.closed_frame_confis)):
            if self.closed_frame_confis[i] == 0:
                self.frame_classes.append(1)
            else:
                self.frame_classes.append(0)

        cap.release()
        return True  # Signal successful processing

    def main(self, source_video, plot=False):
        if not os.path.exists(source_video):
            print(f"File {source_video} does not exist.")
            return

        processed = self.process_video(source_video)

        if not processed:
            print("Rotating video and reprocessing due to low confidence.")
            self.process_video(source_video, rotate=True)

        print(f"Processing of {source_video} complete.")
        frame_classes = torch.tensor(self.frame_classes).cpu().numpy()
        self.open_close_generate(frame_classes, source_video)

        if plot:
            diff_frame_classes = np.diff(frame_classes)
            self.plot_results(frame_classes, self.frame_confis, self.closed_frame_confis, diff_frame_classes, source_video)

        return 0
    
if __name__ == "__main__":
    my_yolo = MY_YOLO5()
    my_yolo.main('your_video.mp4')
