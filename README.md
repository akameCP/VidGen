# VidGen

The **VidGen** project implements a **real-time video authentication** system using the DeepFace library for face recognition and anti-spoofing techniques. It offers a user interface (GUI) built with PyQt5 and analyzes video files to determine whether the faces in the video are real or fake.

## Features

- **Login System**: Simple authentication with username (root) and password (kali).
- **File Upload**: Users can upload video files in `.mp4`, `.avi`, `.mkv` formats.
- **Real-Time Video Analysis**: The application analyzes the uploaded video files, detects faces, and shows the progress of the analysis with a progress bar.
- **Dynamic Status Table**: Displays the analysis status of uploaded videos, including the file name and whether the faces are "Real" or "Fake" in a dynamic table.
- **Stop/Abort Functionality**: Users can stop the analysis process at any point.

## Technologies Used

- **Python**: The main programming language used to develop the project.
- **PyQt5**: Library used for creating the graphical user interface (GUI).
- **DeepFace**: Deep learning-based face recognition and anti-spoofing library.
- **OpenCV**: Library used for processing video files and extracting frames.
- **TensorFlow**: Backend library used for deep learning-based face recognition models.

## Running the Application

1. To start the project, run the `main.py` script:

```bash
python main.py
