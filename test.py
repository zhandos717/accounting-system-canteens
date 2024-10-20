import cv2


def list_available_cameras(max_index=10, verbose=False):
    """Lists available cameras by trying to access them."""
    available_cameras = []
    for index in range(max_index):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            available_cameras.append(index)
            cap.release()
        else:
            if verbose:
                print(f"Camera {index} is not available.")
            break  # Stop the loop if the camera is not available

    if not available_cameras:
        print("No cameras detected.")
    else:
        print("Available cameras:")
        for camera in available_cameras:
            print(f"  - Camera {camera}: Available")
    return available_cameras


# Run the function to check for available cameras
list_available_cameras(max_index=10, verbose=True)
