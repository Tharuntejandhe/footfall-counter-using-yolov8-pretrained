import tkinter as tk
from tkinter import filedialog
import os
import cv2
import torch
from detection import PersonDetector
from tracking import CentroidTracker
from counting import FootfallCounterLogic
from visualization import Visualizer, generate_heatmap
from collections import deque

class FootfallApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Select Video for Footfall Counter')
        self.root.geometry('600x150')
        self.create_widgets()
        self.root.mainloop()
    
    def create_widgets(self):
        self.label = tk.Label(self.root, text="Click to select a video file:")
        self.label.pack(pady=10)
        self.select_btn = tk.Button(self.root, text='Select Video', command=self.select_video)
        self.select_btn.pack(pady=10)
        self.status = tk.Label(self.root, text='', fg='green')
        self.status.pack(pady=10)
    
    def select_video(self):
        video_path = filedialog.askopenfilename(
            title='Select video file',
            filetypes=[('MP4 files', '*.mp4'), ('All files', '*.*')])
        if not video_path:
            self.status['text'] = 'No file selected.'
            return
        self.status['text'] = f'Selected: {os.path.basename(video_path)}'
        self.root.update()
        self.run_footfall_counter(video_path)
    
    def run_footfall_counter(self, video_path):
        if torch.cuda.is_available():
            device = 'cuda'
        elif torch.backends.mps.is_available():
            device = 'mps'
        else:
            device = 'cpu'
        
        cap = cv2.VideoCapture(video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        entry_line_y = height // 3
        exit_line_y = 2 * height // 3
        
        detector = PersonDetector(device=device)
        tracker = CentroidTracker(max_distance=50, max_age=20)
        counter = FootfallCounterLogic(entry_line_y=entry_line_y, exit_line_y=exit_line_y)
        visualizer = Visualizer(entry_line_y=entry_line_y, exit_line_y=exit_line_y, width=width, height=height)
        
        out_path = os.path.splitext(video_path)[0] + '_footfall_output.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))
        
        frame_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            boxes = detector.detect_people(frame)
            new_centroids = [tracker.get_centroid(bbox) for bbox in boxes]
            matched_tracks, unmatched_indices = tracker.match_centroids(new_centroids)
            
            detections_to_draw = {}
            
            for track_id, centroid in matched_tracks.items():
                tracker.current_tracks[track_id] = centroid
                crossing = counter.check_line_crossing(track_id, centroid)
                if crossing:
                    print(f"Frame {frame_count}: ID {track_id} - {crossing.upper()}")
                for i, box in enumerate(boxes):
                    if tracker.get_centroid(box) == centroid:
                        detections_to_draw[track_id] = box
                        break
            
            for idx in unmatched_indices:
                tracker.next_id += 1
                track_id = tracker.next_id
                centroid = new_centroids[idx]
                tracker.current_tracks[track_id] = centroid
                tracker.centroids[track_id] = deque(maxlen=5)
                tracker.centroids[track_id].append(centroid)
                detections_to_draw[track_id] = boxes[idx]
            
            for track_id in list(tracker.current_tracks.keys()):
                tracker.track_age[track_id] += 1
            for track_id in detections_to_draw.keys():
                tracker.track_age[track_id] = 0
            tracks_to_remove = []
            for track_id, age in tracker.track_age.items():
                if age > tracker.MAX_AGE:
                    tracks_to_remove.append(track_id)
            for track_id in tracks_to_remove:
                if track_id in tracker.current_tracks:
                    del tracker.current_tracks[track_id]
                if track_id in tracker.centroids:
                    del tracker.centroids[track_id]
                if track_id in tracker.track_age:
                    del tracker.track_age[track_id]
            
            draw_list = {tid: detections_to_draw[tid] for tid in tracker.current_tracks if tid in detections_to_draw}
            frame = visualizer.draw(frame, draw_list, counter.entry_count, counter.exit_count, tracker.current_tracks, centroids_histories=tracker.centroids)
            
            out.write(frame)
            
            cv2.imshow('Footfall Counter - Press Q to quit', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            frame_count += 1
        
        cap.release()
        out.release()
        cv2.destroyAllWindows()

        heatmap_image = generate_heatmap(width, height, tracker.centroids)
        cv2.imwrite('motion_heatmap.png', heatmap_image)

        print("\n" + "="*50)
        print("PROCESSING COMPLETE!")
        print(f"TOTAL ENTRIES: {counter.entry_count}")
        print(f"TOTAL EXITS: {counter.exit_count}")
        print(f"NET FOOTFALL: {counter.entry_count - counter.exit_count}")
        print("="*50 + "\n")
        print(f"Output video saved to: {out_path}")
        print(f"Heatmap image saved to: motion_heatmap.png")


if __name__ == "__main__":
    FootfallApp()
