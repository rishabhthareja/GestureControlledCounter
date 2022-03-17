# GestureControlledCounter
The code is written to detect face and control the on screen counter using thumb position.
If the thumb of user in frame is pointng upward the on-screen counter will start up counting and vice-versa.

The libraries used for face detection and hand landmark detection are:
1. mediapipe 
2. openCV

How code is working:
The code identifies the face using mediapipe inbuild CNN based algorithm.
For detecting the thumb direction and thumbs up gesture recognition:
1. Algorithm first figure out if all the fingers are curled and inside the palm, that is computed
   using the inter landmark distance of each finger.
2. After verifying if fingers are closed then check if thumb is in up or down postion by calculating the landmark position
   of each landmark of thumb on Y-axis.
3. Check if the fingers are closed but thumb is not up or down or when there is just fist is present in the frame. 
   this is called thumb neutral position. This is computed by check thumb landmark position on X-axis.

COnditions:
Up count:
1. When all the firngers are curled in and thumb is up.

Down count 
1. All fingers are curled in and thumb is pointing down.

Neither up or down count.
1. When fingers are not curled in palm.
2. If thumb is pointing up or down but fingers are not curled in.
3. If fingers are curled inside palm and thumb is not pointing up or down or when there will be fist gesture in frame.


https://user-images.githubusercontent.com/36872855/158835130-729a1634-d1c3-4452-ab82-1c5166723adb.mp4

