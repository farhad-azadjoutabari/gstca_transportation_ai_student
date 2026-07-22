'''This example demonstrates how to read and display data from the QCar Lidar
'''
import time
import matplotlib.pyplot as plt
from pal.products.qcar import QCarLidar
# from pal.utilities.lidar import Lidar

# polar plot object for displaying LIDAR data later on
ax = plt.subplot(111, projection='polar')
plt.show(block=False)

runTime = 10.0 # seconds
# Lidar settings
numMeasurements 	 = 1000	# Points
lidarMeasurementMode 	 = 2
lidarInterpolationMode = 0

# LIDAR initialization and measurement buffers
myLidar = QCarLidar(
	numMeasurements=numMeasurements,
	rangingDistanceMode=lidarMeasurementMode,
	interpolationMode=lidarInterpolationMode
)


t0 = time.time()
try:
    # Run loop until runTime expires OR user closes the plot window
    while (time.time() - t0 < runTime) and plt.fignum_exists(fig.number):
        plt.cla()

        # Capture LIDAR data
        myLidar.read()

        ax.scatter(myLidar.angles, myLidar.distances, marker='.')
        ax.set_theta_zero_location("W")
        ax.set_theta_direction(-1)

        # Allows Matplotlib GUI events to process
        plt.pause(0.01)  # Dropped from 0.1 to 0.01 for better GUI responsiveness

except KeyboardInterrupt:
    print("\nProgram interrupted by user (Ctrl+C). Cleaning up...")

finally:
    # ALWAYS executed on normal exit, Ctrl+C, or window close
    print("Terminating LiDAR hardware connection...")
    myLidar.terminate()
    plt.close('all')
    print("LiDAR safely terminated.")

