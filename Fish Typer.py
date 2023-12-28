import cv2
import numpy as np
import string
import time
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize the video capture object
cap = cv2.VideoCapture(0)

# Initialize the background subtractor
back_sub = cv2.createBackgroundSubtractorMOG2()

# Set the zoom factor
zoom_factor = 2.05  # Adjust this value to your preference

# Initialize the contour buffer
contour_buffer = None

# Create a 2D array of letters
letters = np.array(list(string.ascii_uppercase)[:-1]).reshape(5, 5)  # Remove 'Z' and adjust the shape according to your grid size

# Initialize the time counter
last_time = time.time()

# Initialize the word
word = ''

# Initialize the list of chosen words
chosen_words = []

# List of words to check
words_to_check = ['bee', 'fly', 'no', 'way', 'there', 'is', 'to', 'all', 'known', 'laws', 'of', 'aviation', 'should', 'be', 'able']

while True:
    # Capture a video frame
    ret, frame = cap.read()

    if not ret:
        break

    # Get the dimensions of the frame
    height, width = frame.shape[:2]

    # Compute the size of the zoomed frame
    zoomed_height, zoomed_width = int(height * zoom_factor), int(width * zoom_factor)

    # Compute the region of interest
    start_row, start_col = int((zoomed_height - height) / 2), int((zoomed_width - width) / 2)
    end_row, end_col = start_row + height, start_col + width

    # Resize (zoom) the frame
    zoomed_frame = cv2.resize(frame, (zoomed_width, zoomed_height))

    # Crop the frame
    frame = zoomed_frame[start_row:end_row, start_col:end_col]

    # Apply the background subtractor
    fg_mask = back_sub.apply(frame)

    # Apply a binary threshold to the foreground mask
    _, thresh = cv2.threshold(fg_mask, 90, 255, cv2.THRESH_BINARY)

    # Perform morphological operations to reduce noise
    kernel = np.ones((5,5),np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations = 2)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations = 2)

    # Find contours in the threshold image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If contours are detected, update the contour buffer
    if contours:
        contour_buffer = max(contours, key=cv2.contourArea)

    # If no contours are detected, use the contour buffer
    elif contour_buffer is not None:
        contours = [contour_buffer]

    # Draw the largest contour on the frame
    if contours:
        cv2.drawContours(frame, contours, -1, (255,0,0), 3)

        # Get the coordinates of the contour's centroid
        M = cv2.moments(contour_buffer)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # Calculate the grid cell coordinates
        grid_start_x = (width - (width // 5) * 5) // 2
        grid_start_y = (height - (height // 7) * 5) // 2
        cell_x = min((cX - grid_start_x) // (width // 5), letters.shape[1] - 1)  # Adjust this value according to your grid size
        cell_y = min((cY - grid_start_y) // (height // 7), letters.shape[0] - 1)  # Adjust this value according to your grid size

        # Print the letter every 4 seconds
        current_time = time.time()
        if current_time - last_time >= 4:
            letter = letters[cell_y, cell_x]
            print(letter, end='')  # Print the letter next to the previous one without adding a newline
            engine.say(letter)
            engine.runAndWait()
            word += letter.lower()  # Add the letter to the word
            for check_word in words_to_check:  # Check if the word contains any of the chosen words
                if check_word in word:
                    print(f'\nThe word "{check_word}" has been entered.')
                    engine.say(check_word)
                    engine.runAndWait()
                    chosen_words.append(check_word)  # Add the chosen word to the list of chosen words
                    word = word.replace(check_word, '')  # Remove the chosen word from the word
            last_time = current_time

    # Display the chosen words on the video in red text
    for i, chosen_word in enumerate(chosen_words):
        cv2.putText(frame, chosen_word, (10, 30 + i * 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Overlay the grid and letters on the frame
    for i in range(5):
        for j in range(5):
            cv2.rectangle(frame, (j * (width // 5) + grid_start_x, i * (height // 7) + grid_start_y), ((j+1) * (width // 5) + grid_start_x, (i+1) * (height // 7) + grid_start_y), (0, 255, 0), 1)
            cv2.putText(frame, letters[i, j], (j * (width // 5) + 5 + grid_start_x, i * (height // 7) + 15 + grid_start_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    # Display the frame
    cv2.imshow('Fish Types The Bee Movie Script', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()
cv2.destroyAllWindows()
