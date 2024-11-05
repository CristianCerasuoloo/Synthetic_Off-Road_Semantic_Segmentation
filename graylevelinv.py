
import cv2
import os

def invert_grayscale_video(input_path, output_path):
    # Check if the input path exists
    if not os.path.exists(input_path):
        print(f"Error: The input file '{input_path}' does not exist.")
        return

    # Open the video file
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file '{input_path}'")
        return

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    codec = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for mp4 format

    # Create a VideoWriter object to save the output video
    out = cv2.VideoWriter(output_path, codec, fps, (width, height), isColor=False)

    while True:
        # Read each frame
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Perform gray-level inversion
        inverted_frame = 255 - gray_frame

        # Write the inverted frame to the output video
        out.write(inverted_frame)

    # Release resources
    cap.release()
    out.release()
    print(f"Inverted video saved as '{output_path}'")

# Usage example
# invert_grayscale_video("input_video.mp4", "output_video.mp4")

if __name__ == "__main__":
    input_video = "/Users/cristiancerasuolo/Downloads/WL0.mp4"
    output_video = "/Users/cristiancerasuolo/Downloads/WL0_inv.mp4"

    invert_grayscale_video(input_video, output_video)

