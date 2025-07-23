import cv2
import numpy as np

def background_subtraction(video_source=0, sensitivity=0.5, min_box_size_ratio=0.01):
    """
    Perform background subtraction on video source to detect moving objects.
    
    Parameters:
    - video_source: Camera index (0 for default) or video file path
    - sensitivity: Value between 0-1, where 0 is less sensitive and 1 is very sensitive
    - min_box_size_ratio: Minimum size of bounding box as a ratio of image size
    
    Returns:
    None (displays video windows)
    """
    # Initialize video capture
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print("Error: Could not open video source.")
        return
    
    # Get video properties
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        return
    
    height, width = frame.shape[:2]
    min_box_area = int(height * width * min_box_size_ratio)
    
    # Create background subtractor
    # Convert sensitivity (0-1) to the appropriate values for the parameters
    history = 500
    var_threshold = int(40 * (1 - sensitivity) + 16 * sensitivity)  # Maps sensitivity to 16-40 range (higher sensitivity = lower threshold)
    detect_shadows = True
    
    bg_subtractor = cv2.createBackgroundSubtractorMOG2(
        history=history, 
        varThreshold=var_threshold, 
        detectShadows=detect_shadows
    )
    
    # Custom variables for additional processing
    kernel_size = max(1, int(min(height, width) * 0.01))  # Dynamic kernel size based on image dimensions
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    min_contour_area = min_box_area
    
    while True:
        # Read frame
        ret, frame = cap.read()
        if not ret:
            print("Video ended or error reading frame.")
            break
        
        # Make a copy of the original frame
        original = frame.copy()
        
        # Apply background subtractor
        fg_mask = bg_subtractor.apply(frame)
        
        # Remove shadows (convert gray shadows to black)
        _, fg_mask_binary = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
        
        # Noise removal with morphological operations
        fg_mask_processed = cv2.morphologyEx(fg_mask_binary, cv2.MORPH_OPEN, kernel)
        fg_mask_processed = cv2.morphologyEx(fg_mask_processed, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(fg_mask_processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Create final result frame
        result = original.copy()
        
        # Draw rectangles around detected objects
        for contour in contours:
            area = cv2.contourArea(contour)
            if area >= min_contour_area:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Optionally add text label
                cv2.putText(result, f"Area: {area:.0f}", (x, y - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                print(f"Area: {area:.0f}")
        # Display results
        cv2.imshow("Original", original)
        
        # Create a colored foreground for better visualization
        fg_display = cv2.cvtColor(fg_mask_processed, cv2.COLOR_GRAY2BGR)
        cv2.imshow("Foreground", fg_display)
        
        cv2.imshow("Motion Detection", result)
        
        # Exit on 'q' key
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()

def main():
    """
    Main function to run background subtraction with user parameters.
    """
    # Set parameters
    source = 0  # 0 for webcam, or provide a file path like "video.mp4"
    sensitivity = 0.5  # Adjust between 0-1 (0: less sensitive, 1: very sensitive)
    min_box_size_ratio = 0.0001  # Minimum box size ratio of the image
    
    print("Starting background subtraction...")
    print("Press 'q' to quit.")
    
    # Run background subtraction
    background_subtraction(
        video_source=source,
        sensitivity=sensitivity,
        min_box_size_ratio=min_box_size_ratio
    )

if __name__ == "__main__":
    main()