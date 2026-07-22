import time
import cv2
import numpy as np

from pit.YOLO.nets import YOLOv8
from pit.YOLO.utils import QCar2DepthAligned
from pal.products.qcar import QCar


# ============================================================
# Parameters
# ============================================================

SAMPLE_RATE = 30
SAMPLE_TIME = 1.0 / SAMPLE_RATE

IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480

FORWARD_THROTTLE = 0.10

# Steering is commanded as zero during the entire experiment.
STEERING = 0.00

# Begin the timed forward movement when the sign is within 0.9 m.
DETECTION_DISTANCE = 0.90

# Stop this far before the measured stop-sign position.
# Use 0.0 only if reaching the sign position is physically safe.
STOP_OFFSET = 0.25

STOP_DURATION = 3.0

# Prevent invalid time calculations when the measured speed is too low.
MIN_VALID_SPEED = 0.03

# Prevent an erroneous distance reading from commanding a very long motion.
MAX_ADVANCE_TIME = 3.0

print("Sample Time:", SAMPLE_TIME)


# ============================================================
# Initialize Hardware
# ============================================================

myCar = QCar(
    readMode=1,
    frequency=SAMPLE_RATE
)

myYolo = YOLOv8(
    imageHeight=IMAGE_HEIGHT,
    imageWidth=IMAGE_WIDTH
)

QCarImg = QCar2DepthAligned()

LEDs = np.array([0, 0, 0, 0, 0, 0, 1, 1])


# ============================================================
# State Variables
# ============================================================

state = "DRIVING"

advanceStartTime = 0.0
requiredAdvanceTime = 0.0

stopStartTime = 0.0

detectedDistance = None
measuredSpeedAtDetection = None


# ============================================================
# Initial Safe Command
# ============================================================

# Explicitly command zero steering and zero throttle before motion begins.
myCar.read_write_std(
    throttle=0.0,
    steering=-0.04,
    LEDs=LEDs
)

time.sleep(1.0)

print("System initialized.")
print("Initial steering command: 0.0 rad")
print("State: DRIVING")


# ============================================================
# Main Loop
# ============================================================

try:

    while True:

        loopStart = time.time()

        # ----------------------------------------------------
        # Read RealSense RGB and aligned depth images
        # ----------------------------------------------------

        QCarImg.read()

        rgbProcessed = myYolo.pre_process(QCarImg.rgb)

        myYolo.predict(
            inputImg=rgbProcessed,
            classes=[11],
            confidence=0.30,
            half=True,
            verbose=False
        )

        processedResults = myYolo.post_processing(
            alignedDepth=QCarImg.depth,
            clippingDistance=5
        )

        # ----------------------------------------------------
        # Find the nearest detected stop sign
        # ----------------------------------------------------

        nearestStopDistance = None
        nearestStopConfidence = None

        for obj in processedResults:

            if obj.name == "stop sign":

                distance = float(obj.distance)
                confidence = float(obj.conf)

                if (
                    nearestStopDistance is None
                    or distance < nearestStopDistance
                ):
                    nearestStopDistance = distance
                    nearestStopConfidence = confidence

        if nearestStopDistance is not None:

            print(
                f"STOP SIGN | "
                f"Distance: {nearestStopDistance:.3f} m | "
                f"Confidence: {nearestStopConfidence:.3f} | "
                f"State: {state}"
            )

        # ----------------------------------------------------
        # State Machine
        # ----------------------------------------------------

        if state == "DRIVING":

            throttle = FORWARD_THROTTLE

            if (
                nearestStopDistance is not None
                and nearestStopDistance <= DETECTION_DISTANCE
            ):

                # motorTach is treated as measured linear speed in m/s
                measuredSpeed = abs(float(myCar.motorTach))

                if measuredSpeed < MIN_VALID_SPEED:

                    print(
                        "Stop sign reached the trigger distance, but "
                        f"measured speed is too low: {measuredSpeed:.3f} m/s"
                    )

                    # Stop safely instead of performing an invalid division.
                    throttle = 0.0
                    state = "STOPPED"
                    stopStartTime = time.time()

                else:

                    remainingDistance = max(
                        0.0,
                        nearestStopDistance - STOP_OFFSET
                    )

                    calculatedTime = (
                        remainingDistance / measuredSpeed
                    )

                    requiredAdvanceTime = min(
                        calculatedTime,
                        MAX_ADVANCE_TIME
                    )

                    detectedDistance = nearestStopDistance
                    measuredSpeedAtDetection = measuredSpeed
                    advanceStartTime = time.time()

                    state = "ADVANCING"

                    print("=" * 60)
                    print("STOP SIGN TRIGGERED")
                    print(
                        f"Detected distance: "
                        f"{detectedDistance:.3f} m"
                    )
                    print(
                        f"Desired stopping offset: "
                        f"{STOP_OFFSET:.3f} m"
                    )
                    print(
                        f"Planned travel distance: "
                        f"{remainingDistance:.3f} m"
                    )
                    print(
                        f"Measured vehicle speed: "
                        f"{measuredSpeedAtDetection:.3f} m/s"
                    )
                    print(
                        f"Calculated forward time: "
                        f"{requiredAdvanceTime:.3f} s"
                    )
                    print("=" * 60)

        elif state == "ADVANCING":

            throttle = FORWARD_THROTTLE

            elapsedAdvanceTime = (
                time.time() - advanceStartTime
            )

            remainingTime = max(
                0.0,
                requiredAdvanceTime - elapsedAdvanceTime
            )

            print(
                f"ADVANCING | "
                f"Elapsed: {elapsedAdvanceTime:.2f} s | "
                f"Remaining: {remainingTime:.2f} s"
            )

            if elapsedAdvanceTime >= requiredAdvanceTime:

                throttle = 0.0
                state = "STOPPED"
                stopStartTime = time.time()

                print("Planned forward movement completed.")
                print("Vehicle stopped for 5 seconds.")

        elif state == "STOPPED":

            throttle = 0.0

            elapsedStopTime = time.time() - stopStartTime

            print(
                f"STOPPED | "
                f"Elapsed: {elapsedStopTime:.2f} s"
            )

            if elapsedStopTime >= STOP_DURATION:

                print("Five-second stop completed.")
                print("Second test scenario finished.")
                #break
                state = "DRIVING"

        else:

            throttle = 0.0
            raise RuntimeError(
                f"Unknown vehicle state: {state}"
            )

        # ----------------------------------------------------
        # Send vehicle command
        # ----------------------------------------------------

        # Steering remains exactly zero in every state.
        myCar.read_write_std(
            throttle=throttle,
            steering=STEERING,
            LEDs=LEDs
        )

        # ----------------------------------------------------
        # Display annotated RealSense feed
        # ----------------------------------------------------

        annotatedImg = myYolo.post_process_render(
            showFPS=True
        )

        cv2.imshow(
            "QCar2 Stop Sign Test",
            annotatedImg
        )

        # ----------------------------------------------------
        # Maintain approximate loop rate
        # ----------------------------------------------------

        computationTime = time.time() - loopStart
        waitTime = max(
            0.001,
            SAMPLE_TIME - computationTime
        )

        key = cv2.waitKey(
            max(1, int(waitTime * 1000))
        )

        # ESC key ends the test.
        if key == 27:
            print("ESC pressed.")
            break


except KeyboardInterrupt:

    print("User interrupted the program.")


finally:

    # Always stop the vehicle and return steering to zero.
    try:
        myCar.read_write_std(
            throttle=0.0,
            steering=0.0,
            LEDs=LEDs
        )

        time.sleep(0.25)

    except Exception as error:
        print(
            f"Final stop command failed: {error}"
        )

    QCarImg.terminate()
    myCar.terminate()

    cv2.destroyAllWindows()

    print("Vehicle stopped.")
    print("Steering command returned to zero.")
    print("Program finished.")
