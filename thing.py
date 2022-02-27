import cv2
import mediapipe as mp
from Finger import *
from directkeys import PressKey, ReleaseKey, W, A, S, D
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]

            indexFinger = Finger("Index",
            hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
            hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP])

            middleFinger = Finger("Middle",
            hand.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
            hand.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP])

            ringFinger = Finger("Ring",
            hand.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
            hand.landmark[mp_hands.HandLandmark.RING_FINGER_PIP])

            pinkyFinger = Finger("Pinky",
            hand.landmark[mp_hands.HandLandmark.PINKY_TIP],
            hand.landmark[mp_hands.HandLandmark.PINKY_PIP])

            thumb = Thumb("Thumb",
            hand.landmark[mp_hands.HandLandmark.THUMB_TIP],
            hand.landmark[mp_hands.HandLandmark.THUMB_MCP])

            fingers = [indexFinger, middleFinger, ringFinger, pinkyFinger, thumb]

            for fingerObj in fingers:
                fingerObj.raisedCheck()

            for key in [A,S,D]: ReleaseKey(key)
            if pinkyFinger.raised: pass
            elif ringFinger.raised and middleFinger.raised and indexFinger.raised: PressKey(S)
            elif middleFinger.raised and indexFinger.raised: PressKey(D)
            elif indexFinger.raised: PressKey(A)

            if thumb.raised: PressKey(W)
            else: ReleaseKey(W)

            mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
          break
cap.release()
