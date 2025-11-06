import cv2
import numpy as np

class Visualizer:
    def __init__(self, entry_line_y, exit_line_y, width, height):
        self.entry_line_y = entry_line_y
        self.exit_line_y = exit_line_y
        self.width = width
        self.height = height
        self.track_colors = {}
    
    def draw(self, frame, detections, entry_count, exit_count, current_tracks, centroids_histories=None):
        # Draw entry line (green)
        cv2.line(frame, (0, self.entry_line_y), (self.width, self.entry_line_y), (0, 255, 0), 3)
        cv2.putText(frame, 'ENTRY LINE', (10, self.entry_line_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        # Draw exit line (red)
        cv2.line(frame, (0, self.exit_line_y), (self.width, self.exit_line_y), (0, 0, 255), 3)
        cv2.putText(frame, 'EXIT LINE', (10, self.exit_line_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Draw bounding boxes and IDs
        for track_id, bbox in detections.items():
            x1, y1, x2, y2 = bbox
            if track_id not in self.track_colors:
                self.track_colors[track_id] = (np.random.randint(0,255),
                                               np.random.randint(0,255),
                                               np.random.randint(0,255))
            color = self.track_colors[track_id]
            cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)
            cv2.putText(frame, f'ID: {track_id}', (x1,y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            cx = (x1+x2)//2
            cy = (y1+y2)//2
            cv2.circle(frame, (cx,cy), 4, color, -1)
        
        # Draw trajectories if centroids history provided
        if centroids_histories is not None:
            for track_id, centroids in centroids_histories.items():
                if len(centroids) < 2:
                    continue
                points = list(centroids)
                for i in range(1, len(points)):
                    cv2.line(frame, points[i-1], points[i], self.track_colors.get(track_id, (0,255,0)), 2)

        # Draw statistics box
        overlay = frame.copy()
        cv2.rectangle(overlay, (5,5), (350, 160), (0,0,0), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)

        cv2.putText(frame, f'ENTRY: {entry_count}', (15,35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)
        cv2.putText(frame, f'EXIT: {exit_count}', (15,70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
        cv2.putText(frame, f'NET: {entry_count - exit_count}', (15,105), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0),2)
        cv2.putText(frame, f'Active Tracks: {len(current_tracks)}', (15,140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0),1)

        return frame


def generate_heatmap(width, height, centroids_histories):
    heatmap = np.zeros((height, width), dtype=np.float32)
    
    for centroids in centroids_histories.values():
        for (x, y) in centroids:
            if 0 <= x < width and 0 <= y < height:
                cv2.circle(heatmap, (x, y), 20, 1, thickness=-1)
    
    heatmap = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX)
    heatmap = heatmap.astype(np.uint8)
    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    
    return heatmap_color
