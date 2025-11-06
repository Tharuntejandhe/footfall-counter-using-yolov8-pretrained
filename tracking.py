from collections import deque, defaultdict
from scipy.spatial import distance as dist
import numpy as np

class CentroidTracker:
    def __init__(self, max_distance=50, max_age=20):
        self.max_distance = max_distance
        self.MAX_AGE = max_age  # <-- Add this line to fix the error
        self.next_id = 1
        self.current_tracks = {}
        self.centroids = {}
        self.track_age = defaultdict(int)

    def get_centroid(self, bbox):
        x1, y1, x2, y2 = bbox
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        return (cx, cy)
    
    def match_centroids(self, new_centroids):
        matched_tracks = {}
        unmatched_indices = set(range(len(new_centroids)))
        if not self.current_tracks:
            return matched_tracks, list(unmatched_indices)
        existing_ids = list(self.current_tracks.keys())
        existing_centroids = [self.current_tracks[id] for id in existing_ids]
        matched_new = set()
        for ex_idx, ex_id in enumerate(existing_ids):
            ex_centroid = existing_centroids[ex_idx]
            min_distance = self.max_distance
            min_idx = -1
            for new_idx, new_centroid in enumerate(new_centroids):
                if new_idx in matched_new:
                    continue
                d = dist.euclidean(ex_centroid, new_centroid)
                if d < min_distance:
                    min_distance = d
                    min_idx = new_idx
            if min_idx != -1:
                matched_tracks[ex_id] = new_centroids[min_idx]
                matched_new.add(min_idx)
                unmatched_indices.discard(min_idx)
        unmatched = [i for i in range(len(new_centroids)) if i in unmatched_indices]
        return matched_tracks, unmatched
