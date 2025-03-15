Real-Time Video Authentication System
This project implements a real-time video authentication system using DeepFace for face recognition and anti-spoofing techniques. The application provides an interactive user interface built with PyQt5 and processes video files to determine if the faces in the video are real or fake.

Features
Login System: Basic user authentication with username (root) and password (kali).
File Upload: Users can upload video files (.mp4, .avi, .mkv) for face authentication analysis.
Real-Time Analysis: The app analyzes video files, detects faces, and provides real-time progress updates through a progress bar.
Dynamic Table: Displays the status of uploaded videos, including file name and analysis status (Real/Fake).
Stop Functionality: Ability to stop the analysis process midway.
Error Handling: Clear error messages if something goes wrong during analysis.
Technologies Used
Python: The primary programming language used to develop the project.
PyQt5: Used to create the graphical user interface (GUI).
DeepFace: Deep learning-based face recognition and anti-spoofing library.
OpenCV: Used for video file handling and frame extraction.
TensorFlow: Backend library for deep learning-based face recognition models.

1. Run the Application
Navigate to the project directory and run the main script:

bash
Kopyala
Düzenle
python main.py
2. Login
Upon starting the application, you will be prompted to log in.

Username: root
Password: kali
3. Upload Video File
After logging in, the home page will appear with an "Upload File" button. Click the button to select a video file (.mp4, .avi, .mkv) to analyze.

4. Video Analysis
The system will start analyzing the uploaded video. You can see the progress in real-time through a progress bar and the status of the analysis in a dynamic table.

5. Stop Functionality
If you want to stop the analysis at any point, click the "Stop" button.

6. View Results
Once the analysis is complete, the table will display whether the faces in the video are "Real" or "Fake".

How It Works
Video Processing: The application extracts frames from the video file and passes them through a pre-trained deep learning model (Xception model) via DeepFace to detect whether the faces are real or fake.
Anti-Spoofing: The application uses anti-spoofing techniques to ensure that the detected faces are not spoofed (e.g., printed images or videos).
Real-Time Updates: A progress bar shows the percentage of video frames processed, and the status of each uploaded video is dynamically updated in a table.

Future Work
Support for More Models: Add support for additional face recognition models.
Video Processing Optimization: Improve the efficiency of video processing for larger files.
Enhanced User Interface: Add drag-and-drop functionality for easier file uploads and other user-friendly features.
Notes
This project demonstrates real-time face authentication for video files using DeepFace's face recognition model. The application can detect if the faces in the video are real or fake using deep learning and anti-spoofing methods. It is built using Python, PyQt5, and DeepFace.

