# Sharingan-AI
This project, Sharingan AI, is a real-time computer vision application that transforms your eyes into the iconic Sharingan from Naruto. Using OpenCV and MediaPipe, it tracks your face through the webcam and dynamically animates glowing Sharingan pupils that follow your head movements.The design includes rotating tomoe patterns, smooth glow effects, and customizable overlays for a realistic anime-inspired look. It’s a fun blend of AI, animation, and augmented reality that brings the Sharingan to life.

# Tech Stack
Here are the 5 main technologies powering this project:
Python – Core programming language
OpenCV (cv2) – Image processing, real-time video capture, and rendering
MediaPipe – Lightweight face detection and tracking library
NumPy – Fast numerical operations for transformations and blending
Math & Time Modules – For calculating smooth rotations and animations

# How It Works
1. Face Detection:
MediaPipe detects your face and calculates a bounding box.
The script computes the relative position of your face from the screen center.
2. Pupil Tracking:
The difference in position (dx, dy) moves the Sharingan pupils naturally.
Movement is clamped to stay inside the sclera region.
3. Sharingan Rendering:
A glowing pupil is drawn using concentric circles.
Rotating tomoe (three black marks) are animated using trigonometric functions.
4. Overlay Application:
A transparent PNG (top.png) is blended onto the background.
Uses alpha blending to preserve smooth edges.
5. Display:
The final image (eye_img) is displayed in real-time with OpenCV.
