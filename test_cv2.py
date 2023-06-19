import cv2
import numpy as np
import dlib

# cap = cv2.VideoCapture("dataset/1min/20230409_102445_NR.mp4")
cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("dataset/shape_predictor_68_face_landmarks.dat")

# Set the desired display resolution
display_width = 800
display_height = 600

def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)

def euclidean_distance(p1, p2):
    distance = ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
    return distance

def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bot = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
    ver_line = cv2.line(frame, center_top, center_bot, (0, 255, 0), 2)

    hor_line_length = euclidean_distance(left_point, right_point)
    ver_line_length = euclidean_distance(center_top, center_bot)

    ratio = hor_line_length/ver_line_length
    return ratio

count_blink = 0
prev_ratio_left = 0
prev_ratio_right = 0
phase = ""

while True:
    # Read a frame from the video
    ret, frame = cap.read()

    # Break the loop if the video is over or not successfully read
    if not ret:
        break
    
    frame_height, frame_width, _ = frame.shape
    
    # Resize the frame while maintaining the aspect ratio
    aspect_ratio = frame_width / frame_height
    if aspect_ratio > display_width / display_height:
        new_width = display_width
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = display_height
        new_width = int(new_height * aspect_ratio)
    
    frame = cv2.resize(frame, (new_width, new_height))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = detector(gray)
    
    for face in faces:
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()    
        if x < frame.shape[1] // 2:
            # cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)
            
            landmarks = predictor(gray, face)
            
            # LEFT EYE
            left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
            
            # RIGHT EYE
            right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
            
            # if left_eye_ratio > 6 and right_eye_ratio > 6:
            #     if prev_ratio_left < 6 and prev_ratio_right < 6:
            #         count_blink += 1
            # if left_eye_ratio > 6 and right_eye_ratio > 6:
            #     if 4 < prev_ratio_left < 6 and 4 < prev_ratio_right < 6:
            #         # closing
            #         cv2.putText(frame, f"closing phase", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            #         print("closing")
            #     else:
            #         #closed
            #         cv2.putText(frame, f"closed phase", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            #         print("closed")
            # elif 4 < left_eye_ratio < 6 and 4 < right_eye_ratio < 6:
            #     if prev_ratio_left > 6 and prev_ratio_right > 6:
            #         #reopening
            #         cv2.putText(frame, f"reopening phase", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            #         print("reopening")
            if left_eye_ratio > 5.5 and right_eye_ratio > 5.5:
                #closed
                print("closed")
            elif left_eye_ratio > prev_ratio_left and right_eye_ratio > prev_ratio_right and left_eye_ratio > 4 and right_eye_ratio > 4:
                # closing
                print("closing")
            elif left_eye_ratio <= prev_ratio_left and right_eye_ratio <= prev_ratio_right and left_eye_ratio > 4 and right_eye_ratio > 4:
                # opening
                print("reopening")
                                  
            prev_ratio_left = left_eye_ratio
            prev_ratio_right = right_eye_ratio
            
    # Display the number of detected faces
    cv2.putText(frame, f"left, right: {left_eye_ratio, right_eye_ratio}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    # if (5 < left_eye_ratio < 6 and 5 < right_eye_ratio < 6):
    #     cv2.putText(frame, f"closing phase", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    # elif (left_eye_ratio > 6 and right_eye_ratio > 6):
    #     cv2.putText(frame, f"closed phase", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    # else:
    #     cv2.putText(frame, f"reopening phase", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Create a black background image with the desired display resolution
    display_frame = np.zeros((display_height, display_width, 3), dtype=np.uint8)
    x_offset = (display_width - new_width) // 2
    y_offset = (display_height - new_height) // 2
    
    # Overlay the resized frame onto the black background
    display_frame[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = frame
    
    cv2.imshow("Frame", display_frame)
    
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
