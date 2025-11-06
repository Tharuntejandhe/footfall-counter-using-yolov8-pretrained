# Footfall Counter - Computer Vision Project (Updated)

This AI-powered people counting system uses YOLOv8 medium and centroid-based tracking to accurately count entries and exits through two ROI lines. It also visualizes movement trajectories and generates a motion heatmap.

---

## 🏆 Features

- Real-time person detection using YOLOv8m
- Centroid-based tracking with robust ID management
- Two distinct ROI lines for entry and exit counting
- Visualization of bounding boxes, IDs, trajectories, and ROI lines
- Heatmap of movement intensity generated after processing
- Final total entry, exit, and net footfall counts displayed
- Easy-to-use Tkinter GUI for video file selection
- Cross-platform support (macOS with MPS, CUDA, or CPU)

---

## 🛠️ Technologies

- Python 3.8+
- Ultralytics YOLOv8
- OpenCV for video processing and visualization
- SciPy for Euclidean distance calculation
- Tkinter GUI
- Numpy for numerical operations
- PyTorch backend for hardware acceleration support

---

## 🌐 Installation

Install dependencies via pip from the provided requirements.txt:

pip3 install -r requirements.txt

text

---

## 🚀 Usage

To start the GUI and select a video file:

python3 gui_runner.py

text

Select your mp4 video from the file dialog. The program will process the video, display the annotated frames, save an output video with bounding boxes, IDs, entry and exit lines, trajectory paths, and generate a heatmap image file.

Press `Q` in the video window to stop processing early if needed.

---

## 📝 Output Files

- `<input_video_name>_footfall_output.mp4`: The output video with overlays.
- `motion_heatmap.png`: Heatmap visualization of overall movement.

---

## 🔧 Configuration

- **Entry Line Y:** Default at 1/3rd height of video frame.
- **Exit Line Y:** Default at 2/3rd height of video frame.
- **Maximum centroid matching distance:** 50 pixels.
- **Track max age before removing:** 20 frames.

These parameters can be modified in `gui_runner.py` in the `run_footfall_counter()` function.

---

## 📊 Results Displayed

- Entry count (people crossing entry line top-to-bottom)
- Exit count (people crossing exit line bottom-to-top)
- Net footfall (entry - exit)
- Active tracks count during processing
- Total counts printed on console after processing

---

## ⚠️ Troubleshooting

- If OpenCV window is unresponsive, ensure it has keyboard focus.
- For Mac users: install Python/Tkinter properly for GUI support.
- Use compatible mp4 videos.
- Lower resolution videos ensure better framerate.
- If GPU is not detected, it will automatically fall back to CPU.

---

## 📁 Project Structure

footfall_counter_project/
├── detection.py
├── tracking.py
├── counting.py
├── visualization.py
├── gui_runner.py
├── requirements.txt
└── README.md

text

---

## 📚 References

- YOLOv8 Documentation: https://docs.ultralytics.com
- OpenCV Documentation: https://docs.opencv.org
- SciPy Spatial Distance: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.euclidean.html
- Tkinter Documentation: https://docs.python.org/3/library/tkinter.html

---

## 🧑‍💻 Author

Andhe Tharun Tej
---

## MIT License

Free to use and modify for personal and commercial purposes.
