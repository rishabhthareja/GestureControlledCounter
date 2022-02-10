import cv2
import mediapipe as mp
import time
NUM_FACE = 2
model_selection = 0
min_detection_confidence = 0.5

class FaceThumbDetect():
    def __init__(self, model_selection = 0, min_detection_confidence = 0.5, max_num_hands=1, min_detection_confidenceHand=0.7):
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFace = mp.solutions.face_detection
        self.face = self.mpFace.FaceDetection(model_selection=model_selection,
                                              min_detection_confidence=min_detection_confidence)
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands=max_num_hands, min_detection_confidence=min_detection_confidenceHand)
        self.finger_tips = [8, 12, 16, 20]
        self.thumb_tip = 4

    # Function to detect face and  computing thumb position using hand landmarks.
    def findFaceLandmark(self, img):
        #count = 0
        self.imgRGB = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
        #self.results = self.faceMesh.process(self.imgRGB)
        self.imgRGB.flags.writeable = False
        self.resultFace = self.face.process(self.imgRGB)
        self.imgRGB.flags.writeable = True
        self.imgRGB = cv2.cvtColor(self.imgRGB, cv2.COLOR_RGB2BGR)
        self.thumb_status = 0

        # Face detection and creating bounding box around it.
        if self.resultFace.detections:
            for detection in self.resultFace.detections:
                self.mpDraw.draw_detection(self.imgRGB , detection)

        self.resultHand = self.hands.process(self.imgRGB)

        # Hand detection and creating connecting lines between landmarks.

        if self.resultHand.multi_hand_landmarks:

            # Identifying the hand type , means finding the hand in frame is left or right.
            for handtype in self.resultHand.multi_handedness:
                hand_type = handtype.classification[0].label
                #print(hand_type)

            for handslms in self.resultHand.multi_hand_landmarks:

                landmarks = []
                for id, lm in enumerate(handslms.landmark):
                    # print(id, lm
                    h, w, c = self.imgRGB.shape

                    lmx = int(lm.x * w)
                    lmy = int(lm.y * h)

                    landmarks.append(lm)
                    leftHand_fold_status = []
                    rightHand_fold_status = []

                for tip in self.finger_tips:
                    #print(tip)
                    x, y = int(landmarks[tip].x * w), int(landmarks[tip].y * h)
                    cv2.circle(self.imgRGB, (x, y), 15, (0, 0, 255), cv2.FILLED)
                    xthumb, ythumb = int(landmarks[self.thumb_tip].x * w), int(landmarks[self.thumb_tip].y * h)
                    cv2.circle(self.imgRGB, (xthumb, ythumb), 15, (0, 0, 255), cv2.FILLED)

                    # Checking if the fingers of right hand are closed and inside the palm
                    if (landmarks[tip].x > landmarks[tip - 2].x) and hand_type == "Right":

                        # and hand_type == "Left":
                        cv2.circle(self.imgRGB, (x, y), 15, (0, 255, 0), cv2.FILLED)
                        rightHand_fold_status.append(True)

                        # print("left_hand")
                    else:
                        rightHand_fold_status.append(False)

                    # Checking if the fingers of left hand are closed and inside the palm
                    if (landmarks[tip].x < landmarks[tip - 2].x and hand_type == "Left"):
                        # and hand_type == "Left":
                        cv2.circle(self.imgRGB, (x, y), 15, (0, 255, 0), cv2.FILLED)
                        leftHand_fold_status.append(True)

                        # print("left_hand")
                    else:
                        leftHand_fold_status.append(False)

                # Checking the if thumb is upright by computing the distance comparison of thumb landmarks.
                if (landmarks[self.thumb_tip].y * h < landmarks[self.thumb_tip - 1].y * h < landmarks[self.thumb_tip - 2].y * h):
                    if all(leftHand_fold_status) == True or all(rightHand_fold_status) == True:
                        xthumb, ythumb = int(landmarks[self.thumb_tip].x * w), int(landmarks[self.thumb_tip].y * h)
                        cv2.circle(self.imgRGB, (xthumb, ythumb), 15, (0, 255, 0), cv2.FILLED)
                        #print("Thumbsup")
                        self.thumb_status = "UP"
                    else:
                        print("")

                # Checking if the thumb is horizontal and not pointing up or down
                elif (landmarks[self.thumb_tip].x * h > landmarks[self.thumb_tip - 1].x * h > landmarks[
                    self.thumb_tip - 2].x * h):
                    if all(leftHand_fold_status) == True or all(rightHand_fold_status) == True:
                        #print("Thumbs Neutral")
                        self.thumb_status = "NEUTRAL"
                    else:
                        print("")
                else:
                    print("")

                # Checking the if thumb is pointing down by computing the distance comparison of thumb landmarks.
                if (landmarks[self.thumb_tip].y * h > landmarks[self.thumb_tip - 1].y * h > landmarks[self.thumb_tip - 2].y * h):
                    if all(leftHand_fold_status) == True or all(rightHand_fold_status) == True:
                        #count -= 1
                        #print("Thumbs Down")
                        self.thumb_status = "DOWN"
                    else:
                        print("")

                elif (landmarks[self.thumb_tip].x * h < landmarks[self.thumb_tip - 1].x * h < landmarks[
                    self.thumb_tip - 2].x * h):
                    if all(leftHand_fold_status) == True or all(rightHand_fold_status) == True:
                        print("Thumbs Neutral")
                        self.thumb_status = "NEUTRAL"
                    else:
                        print("")
                else:
                    print("")

                # Drawing the interconnection lines between all the points on the hand.
                self.mpDraw.draw_landmarks(self.imgRGB, handslms, self.mpHands.HAND_CONNECTIONS)


        return self.imgRGB, self.thumb_status


# Opening a webcam video feed
cap = cv2.VideoCapture(0)
count = 0
detector = FaceThumbDetect()

while cap.isOpened():
    success, img = cap.read()
    if not success:
        print("Ignoring empty camera frame")
        continue
    # Calling face and thumb detection function
    imgOut, status = detector.findFaceLandmark(img)

    # Checking the status of the thumb and controlling counter and overlaying the counter status
    # and thumb position on the frame.
    if status == "UP":
        time.sleep(0.2)
        count += 1
        cv2.putText(imgOut, "Thumb "+ str(status)+" : "+str(count), (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2, cv2.LINE_AA)
    elif status == "DOWN":
        time.sleep(0.2)
        count -= 1
        cv2.putText(imgOut, "Thumb "+ str(status) + " : " + str(count), (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2, cv2.LINE_AA)

    elif status == "NEUTRAL":
        time.sleep(0.2)
        count =  count
        cv2.putText(imgOut, "Thumb " + str(status) + " : " + str(count), (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2, cv2.LINE_AA)

    else:
        count = count
        cv2.putText(imgOut, str("No thumb up gesture") + " : " + str(count), (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2, cv2.LINE_AA)
    # printing the thumb position and counter status for verification purpose.
    print("Thumb Position", status,)
    print("Counter status", count, )
    cv2.imshow('Face Detection', imgOut)

    if cv2.waitKey(5) & 0xFF == 27:
        break

# release the webcam and destroy all active windows
cap.release()


