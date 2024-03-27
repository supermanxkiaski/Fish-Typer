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

# List of words to check,
words_to_check = ['bee', 'fly', 'way', 'there', 'islam', 'know', 'laws', 'dove', 'aviation', 'should', 'believe', 'able', 'the', 'america', 'has', 'made', 'make', 'was', 'are', 'our', 'daughter', 'johnny', 'sammy', 
                  'like', 'live', 'life', 'love', 'you', 'jus', 'jude', 'moose', 'goose', 'where', 'plane', 'crash', 'build', 'yeah', 'yes', 'not', 'real', 'juice', 'cheese', 'walrus', 'and', 'then', 'they', 'arm', 'erect',
                   'that', 'have', 'had', 'for', 'with', 'fat', 'dahmer', 'this', 'talk', 'speak', 'speech', 'russia', 'language', 'horse', 'cod', 'fish', 'but', 'his', 'her', 'bossy', 'boy', 'girl',
                    'man', 'women', 'knee', 'push', 'pull', 'suck', 'swallow', 'eat', 'puke', 'barf', 'vomit', 'food', 'war', 'gun', 'shoot', 'shot', 'write', 'right', 'left', 'cup', 'down', 'female', 'dog', 'africa',
                     'tiger', 'lions', 'bird', 'dino', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'twenty', 'thirty', 'fourty', 'fifty', 'hundred', 'thousand', 'million' 
                      'celia', 'giraffe', 'elephant', 'animal', 'worm', 'bug', 'annoy', 'from', 'say', 'she', 'will', 'law', 'rule', 'police', 'ground', 'swear', 'word', 'goin', 'wanna', 'want', 'would', 'japan', 'blind', 'german', 'classic'
                       'sonic', 'wind', 'dirt', 'tear', 'paper', 'rapper', 'gum', 'would', 'could', 'good', 'bad', 'bald', 'phantom', 'ghost', 'shadow', 'picture', 'video', 'photo', 'graph', 'look', 'ever', 'time', 'laugh', 'what', 'out', 'animate', 'who', 'get', 'cosby',
                        'friend', 'enemy', 'guy', 'dead', 'when', 'can', 'door', 'patio', 'radio', 'hear', 'here', 'stand', 'walk', 'mountain', 'puma', 'joke', 'choke', 'breath', 'staff', 'cow', 'owl', 'deer', 'forgot', 'kinda', 'just', 'evil', 'thing', 'body', 'some', 'son', 'sun', 'big', 'small', 'little', 'all', 
                         'huge', 'take', 'took', 'knife', 'blade', 'sword', 'katana', 'color', 'which', 'red', 'blue', 'yellow', 'complain', 'lawn', 'yawn', 'yarn', 'rhino', 'ice', 'now', 'ski', 'pole', 'north', 'south', 'east', 'west', 'wheat', 'feed',
                          'into', 'bend', 'chair', 'cause', 'people', 'person', 'child', 'lid', 'kid', 'bid', 'onto', 'outro', 'intro', 'year', 'day', 'second', 'first', 'third', 'minute', 'hour', 'week', 'weak', 'month', 'jam', 'parrot', 'bear', 'grizzly', 'music', 'song', 
                           'hell', 'heel', 'goes', 'heaven', 'random', 'tube', 'pipe', 'drill', 'saw', 'seen', 'scene', 'delete', 'erase', 'rid', 'jay', 'jet', 'other', 'mom', 'dad', 'only', 'before', 'after', 'during', 'middle', 'school', 'drink', 'eat', 'any', 'fist', 'fight', 'kind',
                            'soldier', 'battle', 'field', 'computer', 'think', 'thought', 'black', 'back', 'eaow', 'use', 'work', 'job', 'employ', 'skin', 'race', 'native', 'culture', 'vine', 'biden', 'joe', 'new', 'old', 'swim', 'suit', 'dive', 'die', 'desert', 'jungle', 'air', 'gas', 'poison', 'mush', 'room', 'bath',
                             'hospital', 'port', 'hang', 'stab', 'thank', 'welcome', 'most', 'least', 'home', 'near', 'deep', 'shallow', 'world', 'exist', 'mean', 'nice', 'water', 'pop', 'doctor', 'pepper', 'soda', 'sew', 'soon', 'asia', 'india', 'narwal', 
                              'uniform', 'badge', 'leg', 'hand', 'finger', 'middle', 'between', 'far', 'hill', 'over', 'done', 'kill', 'aardvark', 'ant', 'land', 'locate', 'location', 'fake', 'eye', 'found', 'part', 'piece', 'brick', 'stick', 'straw', 'cut', 'slice', 
                               'open', 'ready', 'prepare', 'pair', 'case', 'point', 'mark', 'number', 'rain', 'raid', 'military', 'base', 'storm', 'may', 'government', 'town', 'city', 'district', 'hood', 
                                'suprise', 'letter', 'mail', 'pack', 'mouse', 'fact', 'onion', 'power', 'truth', 'phone', 'sister', 'god', 'devil', 'egg', 'eel', 'pot', 'tomato', 'tornado', 'weather', 'strap',
                                 'way', 'group', 'organ', 'car', 'truck', 'aim', 'miss', 'fire', 'depart', 'leave', 'leaf', 'return', 'xray', 'act', 'show', 'present', 'rise', 'set', 'got', 'start', 'half', 'hole', 'full', 'entire', 'egypt', 'rock', 'cloud', 'star',
                                  'possible', ' care', 'space', 'inner', 'foam', 'stare', 'top', 'spot', 'stairs', 'flight', 'trade', 'center', 'murder', 'genocide', 'mass', 'terror', 'speed', 'fast', 'slow', 'flash', 'dull', 'sound', 'night', 'seed'
                                   'oops', 'sorry', 'upset', 'machine', 'vend', 'run', 'jump', 'sit', 'same', 'differ', 'side', 'other', 'teal', 'archer', 'amaze', 'autism', 'cigar', 'smoke', 'noah', 'tree', 'snake', 'orange', 'did'
                                    'let', 'finish', 'negro', 'nword', 'bag', 'apple', 'bae', 'bay', 'off', 'set', 'buy', 'sell', 'hot', 'cold', 'end', 'key', 'pay', 'few', 'age', 'yet', 'box', 'fox', 'sap', 'log', 'frog', 'swam',
                                     'lake', 'pond', 'pound', 'try', 'due', 'ago', 'oil', 'tin', 'hat', 'cap', 'bat', 'act', 'assault', 'rifle', 'test', 'ape', 'art', 'ash', 'ask', 'ate', 'axe', 'ayeaye', 'captain', 'bar', 'snack', 'hollow', 'holland', 'follow', 'foil', 'bed', 'beef', 'beg', 'bell', 
                                      'beer', 'ear', 'ufo', 'saw', 'usa', 'utah', 'wave', 'wig', 'vhs', 'won', 'win', 'wag', 'wet', 'vet', 'why', 'noah', 'boat', 'wood', 'wow', 'toy', 'score', 'tab', 'tap', 'swipe', 
                                       'teddy', 'tell', 'tea', 'tie', 'toad', 'browser', 'tri', 'poloski', 'tug', 'motor', 'team', 'oof', 'oak', 'wizard', 'lizard', 'iguana', 'blizard', 'great', 'orca', 'whale', 'inhale',
                                        'sale', 'sail', 'garage', 'laugh', 'oscar', 'smack', 'chris', 'rock', 'own', 'hawk', 'pacman', 'pan', 'fry', 'pal', 'pass', 'pat', 'head', 'leg', 'foot', 'paw', 'pectopah', 'pen', 'puppy', 
                                         'pet', 'pig', 'pie', 'pink', 'pill', 'pin', 'pit', 'donkey', 'bong', 'pod', 'pop', 'soda', 'poor', 'monkey', 'cat', 'pro', 'pug', 'punch', 'kick', 'put', 'shame', 'jake', 'bloom', 'jar',
                                          'jar', 'jew', 'jog', 'joe', 'joy', 'eddy', 'ivy', 'plant', 'trap', 'venus', 'ian', 'iowa', 'india', 'emu', 'ink', 'info', 'its', 'nut', 'hack', 'rack', 'sack', 'back', 'idaho', 'iam', ]

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

        # Print the letter every 6 seconds
        current_time = time.time()
        if current_time - last_time >= 5.5:
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
    cv2.imshow('Fish Types Words', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
cap.release()
cv2.destroyAllWindows()
