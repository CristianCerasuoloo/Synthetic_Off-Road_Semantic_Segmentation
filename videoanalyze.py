import cv2

def analyze_video(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    # Get video properties
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps
    
    print(f"Video Path: {video_path}")
    print(f"Frame Count: {frame_count}")
    print(f"FPS: {fps}")
    print(f"Width: {width}")
    print(f"Height: {height}")
    print(f"Duration: {duration:.2f} seconds")
    
    cap.release()

if __name__ == "__main__":
    video_path = input("Enter the path to the video file: ")
    analyze_video(video_path)