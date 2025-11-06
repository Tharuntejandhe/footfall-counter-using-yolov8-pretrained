from collections import deque

class FootfallCounterLogic:
    def __init__(self, entry_line_y, exit_line_y):
        self.entry_line_y = entry_line_y
        self.exit_line_y = exit_line_y
        self.centroids = {}
        self.counted_ids = {}
        self.entry_count = 0
        self.exit_count = 0
    
    def check_line_crossing(self, track_id, new_centroid):
        if track_id not in self.centroids:
            self.centroids[track_id] = deque(maxlen=5)
            self.centroids[track_id].append(new_centroid)
            return None
        
        self.centroids[track_id].append(new_centroid)
        
        if len(self.centroids[track_id]) < 2:
            return None
        
        if track_id in self.counted_ids:
            return None
        
        prev_y = self.centroids[track_id][-2][1]
        curr_y = new_centroid[1]
        
        # Cross entry line from above to below => entry
        if prev_y < self.entry_line_y and curr_y >= self.entry_line_y:
            self.counted_ids[track_id] = 'entry'
            self.entry_count += 1
            return 'entry'
        
        # Cross exit line from below to above => exit
        elif prev_y > self.exit_line_y and curr_y <= self.exit_line_y:
            self.counted_ids[track_id] = 'exit'
            self.exit_count += 1
            return 'exit'
        
        return None
    