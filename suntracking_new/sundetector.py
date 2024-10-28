import cv2
import numpy as np

class SunDetector:
    def __init__(self, frame=None):
        if frame is not None:
            self.set_frame(frame)
        else:
            self.frame = None
        
        self.sun_center = []
        self.frame_center = []

    # Setter methods
    def set_frame(self,frame):
        self.frame = frame

    def set_frame_from_mat(self, frame):
        self.frame = frame

    def set_sun_center(self, center):
        self.sun_center = [int(center[0]), int(center[1])]

    def set_frame_center(self):
        if self.frame is not None:
            self.frame_center = [self.frame.shape[1] // 2, self.frame.shape[0] // 2]

    # Getter methods
    def get_frame(self):
        return self.frame

    def get_sun_center(self):
        return self.sun_center

    def get_frame_center(self):
        return self.frame_center

    def get_frame_width(self):
        return self.frame.shape[1] if self.frame is not None else 0

    def get_frame_height(self):
        return self.frame.shape[0] if self.frame is not None else 0

    # Method to find sun
    def find_sun(self):
        if self.frame is None:
            print("No frame set.")
            return

        print(f"Frame size: {self.frame.shape[1]} x {self.frame.shape[0]}")
        
        # Set frame center
        self.set_frame_center()
        
        # Convert image to grayscale
        gray_img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur
        blurred_image = cv2.GaussianBlur(gray_img, (51, 51), 0)

        # Convert grayscale to binary image
        _, threshold_img = cv2.threshold(blurred_image, 252, 255, cv2.THRESH_BINARY)

        # Find moments of the image
        moments = cv2.moments(threshold_img, True)
        if moments['m00'] != 0:  # Prevent division by zero
            center_x = int(moments['m10'] / moments['m00'])
            center_y = int(moments['m01'] / moments['m00'])
            center = (center_x, center_y)
            self.set_sun_center(center)
            print(f"Sun Detected at: {self.sun_center[0]}, {self.sun_center[1]}")
        else:
            print("No sun detected.")

    # Video management
    def start_video(self):
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.video = cv2.VideoWriter("Solar_Tracker_outVideo.avi", fourcc, 25, (self.get_frame_width(), self.get_frame_height()))

    def end_video(self):
        if hasattr(self, 'video'):
            self.video.release()

    def display(self, action):
        if hasattr(self, 'video'):
            # Print the command on the image
            cv2.putText(self.frame, action, (30, 30), cv2.FONT_HERSHEY_DUPLEX, 0.9, (200, 50, 200), 1)

            # Draw centers
            center = self.get_sun_center()
            frame_center = self.get_frame_center()
            #cv2.circle(self.frame, (center[0], center[1]), 30, (0, 255, 0), 3)
            cv2.circle(self.frame, (frame_center[0], frame_center[1]), 5, (0, 0, 130), 10)

            # Show frame
            cv2.imshow("Image with center", self.frame)
            cv2.waitKey(1)  # Display for a brief moment
