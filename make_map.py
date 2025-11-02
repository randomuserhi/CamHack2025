from PIL import Image
import numpy as np
import cv2
import os
import pickle

x = 54
y = 30
score = []
done = {}

def process_video_frames(video_path):
    """
    Opens a video file and iterates through all its frames.
    """
    # Check if the video file exists.
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        print("Please run 'create_dummy_video.py' first to generate it.")
        return

    print(f"Opening video file: {video_path}")
    
    # 1. Open the video file using VideoCapture
    cap = cv2.VideoCapture(video_path)

    # 2. Check if the video opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open video file at {video_path}")
        return

    # Get video properties (optional, but good for info)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Video properties: {total_frames} total frames, {fps:.2f} FPS")

    frame_count = 0

    # 3. Loop as long as the video is opened
    while cap.isOpened():
        # 4. Read one frame from the video
        # 'ret' is a boolean: True if a frame was read, False if at end of video
        # 'frame' is the actual image data (as a NumPy array)
        ret, frame = cap.read()
        if (video_path in done and done[video_path] >= frame_count):
            frame_count += 1
            continue
        # 5. Check if a frame was successfully read
        if not ret:
            # If 'ret' is False, we've reached the end of the video
            print("\nEnd of video reached.")
            break

        # 6. --- YOUR PROCESSING LOGIC GOES HERE ---
        #
        # 'frame' is a NumPy array representing the image.
        # You can analyze it, modify it, run ML models on it, etc.
        #
        # Example: Just print a message every 30 frames

        frame = downscale_image(frame, y, x)
        avg = np.zeros(shape=[3])
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                avg += frame[i][j] / (frame.shape[0] * frame.shape[1])

        score.append((video_path, frame_count, avg))

        if frame_count % 30 == 0:
            print(f"  Processing frame number {frame_count}...")
        
        done[video_path] = frame_count
        frame_count += 1

        # (Optional) To display the frame in a window:
        # cv2.imshow('Video Frame', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     # Break the loop if 'q' is pressed
        #     break

    # 7. When the loop is finished, release the video capture object
    print(f"\nFinished processing.")
    print(f"Total frames read: {frame_count}")
    cap.release()

    # (Optional) If you used cv2.imshow(), close all windows
    # cv2.destroyAllWindows()

def extract_frame(video_path, frame_number):
    """
    Extracts a specific frame from a video file and returns it as a numpy array.

    Args:
        video_path (str): The path to the video file.
        frame_number (int): The index of the frame to extract (0-based).
    
    Returns:
        numpy.ndarray: The extracted frame as a NumPy array, or None if an error occurred.
    """
    
    # Check if the video file exists
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at '{video_path}'")
        return None

    # Open the video file
    video_capture = cv2.VideoCapture(video_path)

    if not video_capture.isOpened():
        print(f"Error: Could not open video file '{video_path}'")
        return None

    # Get the total number of frames in the video
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

    # Check if the requested frame number is valid
    frame_number %= total_frames
    if frame_number < 0 or frame_number >= total_frames:
        print(f"Error: Invalid frame number. Frame {frame_number} is out of range.")
        print(f"The video has {total_frames} frames (indexed 0 to {total_frames - 1}).")
        video_capture.release()
        return None

    # Set the video capture to the specific frame
    # CAP_PROP_POS_FRAMES is the 0-based index of the frame to be decoded/captured next.
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    # Read the frame
    success, frame = video_capture.read()

    if not success:
        print(f"Error: Failed to read frame {frame_number}.")
        video_capture.release()
        return None

    # Release the video capture object
    video_capture.release()
    
    # Return the extracted frame
    return frame

def downscale_image(image_array: np.ndarray, target_width: int, target_height: int) -> np.ndarray:
    """
    Downscales an image (represented as a NumPy array) to target dimensions.

    Args:
        image_array: The input image as a NumPy array (e.g., shape HxWx3 or HxW).
        target_width: The desired output width.
        target_height: The desired output height.

    Returns:
        The downscaled image as a NumPy array.
    """
    
    # --- Input Validation (Optional but Recommended) ---
    if not isinstance(image_array, np.ndarray):
        raise TypeError("Input 'image_array' must be a NumPy array.")
    if image_array.ndim < 2 or image_array.ndim > 4:
         raise ValueError(f"Input 'image_array' has an unexpected number of dimensions: {image_array.ndim}")
    if target_width <= 0 or target_height <= 0:
        raise ValueError("Target width and height must be positive integers.")
        
    original_height, original_width = image_array.shape[:2]
    
    if target_width > original_width or target_height > original_height:
        print(f"Warning: Target dimensions ({target_width}w x {target_height}h) "
              f"are larger than original ({original_width}w x {original_height}h). "
              "This function will upscale. For downscaling, ensure target dimensions are smaller.")

    # cv2.resize expects the target dimensions in (width, height) format.
    target_dimensions = (target_width, target_height)

    # cv2.INTER_AREA is the recommended interpolation method for shrinking an image (downscaling).
    # For enlarging (upscaling), cv2.INTER_CUBIC or cv2.INTER_LINEAR are usually preferred.
    downscaled_array = cv2.resize(
        image_array, 
        target_dimensions, 
        interpolation=cv2.INTER_AREA
    )

    return cv2.cvtColor(downscaled_array, cv2.COLOR_BGR2RGB)

img = Image.open("palate.png").convert("RGB")

# Convert to NumPy array
palate = np.array(img)

"""
Iterates through all files and directories in the given path.

Args:
    directory_path (str): The absolute or relative path to the directory.
"""

if os.path.exists('my_data.pkl'):
    with open('my_data.pkl', 'rb') as f:
        # 2. Use pickle.load to read the object from the file
        score = pickle.load(f)

for item in score:
    done[item[0]] = item[1]

cnt = 0
directory_path = "videos"
for entry in os.listdir(directory_path):
    if (cnt >= 5):
        break

    cnt += 1
    print(cnt)

with open('my_data.pkl', 'wb') as f:
    # 3. Use pickle.dump to write the list to the file
    pickle.dump(score, f)

amt = 5
best = [[[("", -1)] * 16 for _ in range(16)] for idk in range(amt)]
mp = {}
for i in range(16):
    for j in range(16):
        target = palate[i * 16][j * 16]

        def compare(a):
            cost = 0
            cost += sum((target - a[2]) ** 2)
            return cost
        
        score.sort(key=compare)
        seen = 0
        k = 0
        while seen < amt:
            if (score[k][0] not in mp):
                best[seen][i][j] = (score[k][0], score[k][1])
                mp[score[k][0]] = True
                seen += 1
            k += 1
        print(i * 16 + j)


total_frames = (6, 6)
copies = 4

for idk in range(copies):
    for c in range(amt):
        out = np.zeros(shape=(x * 16 * total_frames[0], y * 16 * total_frames[1], 3), dtype=np.uint8)

        for i in range(16):
            for j in range(16):
                path, frame = best[c][i][j]
                try:
                    for k in range(total_frames[0] * total_frames[1]):
                        tl = k // total_frames[0]
                        tr = k % total_frames[1]

                        img = np.array(extract_frame(path, frame + idk * total_frames[0] * total_frames[1] + k))
                        img2 = downscale_image(img, y, x)
                        coord_x = tl * x * 16 + i * x
                        coord_y = tr * y * 16 + j * y
                        out[coord_x: coord_x + x, coord_y: coord_y + y] = img2
                except:
                    continue
        print(idk * amt + c)
        img = Image.fromarray(out)
        img.save(f"output{idk},{c}.png")

quit()
out = out.astype(np.uint8)
for i in range(copies):
    for j in range(amt):
        img = Image.fromarray(out[i][j])
        img.save(f"output{i},{j}.png")