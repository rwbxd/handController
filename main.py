import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
import colors as mp_drawing_styles
mp_hands = mp.solutions.hands
from KeyPresses import sendKey, holdDown, letUp
from WindowSetup import get_application

#app = get_application("notepad.exe")
app = get_application()

# starting positions are unpressed
rightPressed = False
leftPressed = False
upPressed = False
downPressed = False

# key values to send to game
rightKey = "d"
leftKey = "a"
downKey = "s"
upKey = "w"

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:

  if cap.isOpened():
      height, width, channels = cap.read()[1].shape
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:

      control_hand = results.multi_hand_landmarks[-1]

      # do controls here

      # up/down
      if control_hand.landmark[12].y < .1: # up
          if not upPressed:
              holdDown(app, upKey)
              upPressed = True
      else:
          if upPressed:
              letUp(app, upKey)
              upPressed = False

          if control_hand.landmark[9].y > .8: # down
              if not downPressed:
                  holdDown(app, downKey)
                  downPressed = True
          else:
              if downPressed:
                  letUp(app, downKey)
                  downPressed = False

      # right/left
      if control_hand.landmark[9].x < .2: # right
          if not rightPressed:
              holdDown(app, rightKey)
              rightPressed = True
      else:
          if rightPressed:
              letUp(app, rightKey)
              rightPressed = False

          if control_hand.landmark[9].x > .8: # left
              if not leftPressed:
                  holdDown(app, leftKey)
                  leftPressed = True
          else:
              if leftPressed:
                  letUp(app, leftKey)
                  leftPressed = False


      mp_drawing.draw_landmarks(
          image,
          control_hand,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style())

    if results.multi_hand_landmarks and len(results.multi_hand_landmarks) > 1:
      for hand_landmarks in results.multi_hand_landmarks[:-1]:
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_faded_hand_landmarks_style(),
            mp_drawing_styles.get_faded_hand_connections_style())

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
