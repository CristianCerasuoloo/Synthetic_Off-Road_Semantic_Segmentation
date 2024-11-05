# Take a video file and unpack it into a series of images

import cv2
import os
import sys
import tqdm

def unpack_video(video_path, output_dir):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file")
        return

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read the video frame by frame
    frame_num = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Save the frame as an image
        image_path = os.path.join(output_dir, f"{frame_num:06d}.png")
        cv2.imwrite(image_path, frame)

        frame_num += 1

    cap.release()

if __name__ == "__main__":
    # video_folder = "/Users/cristiancerasuolo/Library/CloudStorage/GoogleDrive-c.cerasuolo2@studenti.unisa.it/Il mio Drive/Magistrale/Tesi/Video Scenari/Bozza3/Bozza3/AVI"
    # output_dir = "/Users/cristiancerasuolo/Library/CloudStorage/GoogleDrive-c.cerasuolo2@studenti.unisa.it/Il mio Drive/Magistrale/Tesi/Video Scenari/Bozza3/Bozza3/Frames"
    video_folder = "/Users/cristiancerasuolo/Desktop/Bozza4/Video"
    output_dir = "/Users/cristiancerasuolo/Desktop/Bozza4/Frames"


    for video_file in tqdm.tqdm(os.listdir(video_folder)):
        if video_file == ".DS_Store":
            continue


        video_path = os.path.join(video_folder, video_file)

        if os.path.exists(os.path.join(output_dir, video_file.split(".")[0])):
            print(f"Already unpacked {video_file}")
            continue
        unpack_video(video_path, os.path.join(output_dir, video_file.split(".")[0]))
        print(f"Unpacked {video_file} into {output_dir}")