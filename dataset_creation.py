import cv2
import os
import shutil
import glob

def unpack_video(video_path, output_dir, perc_frames = -1):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Number of frames: {frame_count}")

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

        if perc_frames > 0 and frame_num/frame_count >= perc_frames:
            print(f"Stopped at frame {frame_num} of the video")
            break

    cap.release()

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

if __name__ == "__main__":

    # Step 1: Estrazione Frame
    video_folder = "/Users/cristiancerasuolo/Desktop/Bozza5"
    video_rgb_folder = video_folder + "/RGB"
    video_gt_folder = video_folder + "/GT"

    frame_folder = "/Users/cristiancerasuolo/Desktop/SynthOffRoad"
    frame_images_folder = frame_folder + "/Images"
    frame_gt_folder = frame_folder + "/GT"

    # Per primo step creiamo una grande unica cartella in cui mettere tutti i frame e poi dividiamo in train valid e test
    # Take all the *.avi files in the video folder (there are more levels of folder) with glob
    video_files = glob.glob(video_folder + "/**/*.avi", recursive=True)
    # print("List of videos: ")
    video_files.sort()
    # for video in video_files:
    #     print(video)

    video_files_clean = []

    for video_path in video_files:
        if "Rainy" in video_path:
            print("Skipping ", video_path)
            continue

        if "WL" in video_path and not "inv" in video_path and "GT" in video_path:
            print("Skipping ", video_path)
            continue

        video_files_clean.append(video_path)

        video_files = video_files_clean
        # print("Final list of videos: ")
        # for video in video_files:
        #     print(video)

    for video_path in video_files:
        # Create the destination path
        video_name = video_path.split("/")[-1].split(".")[0]
        if "_inv" in video_name:
            video_name = video_name.replace("_inv", "")
        video_parent = video_path.split("/")[-2]
        
        video_name = video_parent + "_" + video_name

        if "GT" in video_path:
            frame_path = frame_gt_folder + "/" + video_name
        else:
            frame_path = frame_images_folder + "/" + video_name

        frame_path = frame_path.split(".")[0]

        print(video_path + " -> " + frame_path)

        if not os.path.exists(frame_path):
            pass
            unpack_video(video_path, frame_path, perc_frames = 0.01)
        else:
            print("Skipping " + video_path + " Folder already exists")

    # For each folder, check if the elements inside the folder are the same in the folder under GT with same name

    color_folders = glob.glob(frame_images_folder + "/*")
    for folder in color_folders:
        print(folder)

    for color_folder in color_folders:
        gt_folder = color_folder.replace("Images", "GT")
        print(color_folder + " -> " + gt_folder)
        color_files = len(os.listdir(color_folder))
        gt_files = len(os.listdir(gt_folder))

        print(f"{color_folder}: {color_files} color files - {gt_files} gt files")
        
    # For each couple of folder color and gt take the one with few images and remove the images not available in the other folder (with greater id, so)
    for color_folder in color_folders:
        gt_folder = color_folder.replace("Images", "GT")
        print(color_folder + " -> " + gt_folder)

        color_files = glob.glob(color_folder + "/*.png")
        gt_files = glob.glob(gt_folder + "/*.png")
        color_files.sort(reverse = True)
        gt_files.sort(reverse = True)
        print(f"{color_folder}: {len(color_files)} color files - {len(gt_files)} gt files")

        if len(color_files) > len(gt_files):
            for i in range(len(color_files) - len(gt_files)):
                os.remove(color_files[i])
                print("Removed " + color_files[i] + " from color")
        elif len(color_files) < len(gt_files):
            for i in range(len(gt_files) - len(color_files)):
                os.remove(gt_files[i])
                print("Removed " + gt_files[i] + " from GT")

    # For each file in each images folder check that there is one with the same name in the GT folder
    for color_folder in color_folders:
        gt_folder = color_folder.replace("Images", "GT")
        print(color_folder + " -> " + gt_folder)

        color_files = glob.glob(color_folder + "/*.png")

        for color_file in color_files:
            gt_file = color_file.replace("Images", "GT")
            if not os.path.exists(gt_file):
                print("GT file not found for " + color_file)

    # Take the frame files under the "Images" folder
    frame_files = glob.glob(frame_images_folder + "/**/*.png", recursive=True)
    print("Number of frame extracted: " + str(len(frame_files)))

    # Create the folders Train Val and Test under the Images and GT folders
    train_folder = frame_images_folder + "/Train"
    val_folder = frame_images_folder + "/Val"
    test_folder = frame_images_folder + "/Test"

    train_gt_folder = frame_gt_folder + "/Train"
    val_gt_folder = frame_gt_folder + "/Val"
    test_gt_folder = frame_gt_folder + "/Test"

    folder_to_create = [train_folder, val_folder, test_folder, train_gt_folder, val_gt_folder, test_gt_folder]

    for folder in folder_to_create:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # Move FL0 and WL3 to test, FL3 and WL4 to val and the rest to train
    color_folders = glob.glob(frame_images_folder + "/*")
    for folder in color_folders:
        if "FL0" in folder or "WL3" in folder:
            shutil.move(folder, test_folder)
            shutil.move(folder.replace("Images", "GT"), test_gt_folder)
        elif "FL3" in folder or "WL4" in folder:
            shutil.move(folder, val_folder)
            shutil.move(folder.replace("Images", "GT"), val_gt_folder)
        elif "Test" not in folder and "Val" not in folder and "Train" not in folder:
            shutil.move(folder, train_folder)
            shutil.move(folder.replace("Images", "GT"), train_gt_folder)
