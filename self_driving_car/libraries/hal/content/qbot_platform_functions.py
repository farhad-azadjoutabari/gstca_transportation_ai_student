import numpy as np
import cv2

from pal.products.qbot_platform import QBotPlatformDriver
from pal.utilities.math import Calculus
from scipy.ndimage import median_filter
from pal.utilities.math import Calculus
from pal.utilities.stream import BasicStream
from quanser.common import Timeout
from quanser.image_processing import Lidar2DMatchScansGrid 

class QBPMovement():
    """ This class contains the functions for the QBot Platform such as
    Forward/Inverse Differential Drive Kinematics etc. """

    def __init__(self):
        self.WHEEL_RADIUS = QBotPlatformDriver.WHEEL_RADIUS      # radius of the wheel (meters)
        self.WHEEL_BASE = QBotPlatformDriver.WHEEL_BASE          # distance between wheel contact points on the ground (meters)
        self.WHEEL_WIDTH = QBotPlatformDriver.WHEEL_WIDTH        # thickness of the wheel (meters)
        self.ENCODER_COUNTS = QBotPlatformDriver.ENCODER_COUNTS  # encoder counts per channel
        self.ENCODER_MODE = QBotPlatformDriver.ENCODER_MODE      # multiplier for a quadrature encoder

    def diff_drive_inverse_velocity_kinematics(self, forSpd, turnSpd):
        """This function is for the differential drive inverse velocity
        kinematics for the QBot Platform. It converts provided body speeds
        (forward speed in m/s and turn speed in rad/s) into corresponding
        wheel speeds (rad/s)."""

        vL = forSpd - (turnSpd*self.WHEEL_BASE) / 2
        vR = forSpd + (turnSpd*self.WHEEL_BASE) / 2

        wL = vL/ self.WHEEL_RADIUS
        wR = vR/ self.WHEEL_RADIUS

        return wL, wR

    def diff_drive_forward_velocity_kinematics(self, wL, wR):
        """This function is for the differential drive forward velocity
        kinematics for the QBot Platform. It converts provided wheel speeds
        (rad/s) into corresponding body speeds (forward speed in m/s and
        turn speed in rad/s)."""

        vL = wL * self.WHEEL_RADIUS
        vR = wR * self.WHEEL_RADIUS

        # Converts directly to final velocity instead of left and right linear
        # velocities first
        forSpd = (vR+vL)/2
        turnSpd = (vR-vL)/self.WHEEL_BASE

        return forSpd, turnSpd

class QBPVision():
    def __init__(self):
        self.imageCriteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    def undistort_img(self,distImgs,cameraMatrix,distCoefficients):
        """
        This function undistorts a general camera, given the camera matrix and
        coefficients.
        """

        undist = cv2.undistort(distImgs,
                               cameraMatrix,
                               distCoefficients,
                               None,
                               cameraMatrix)
        return undist

    def df_camera_undistort(self, image):
        """
        This function undistorts the downward camera using the camera
        intrinsics and coefficients."""
        CSICamIntrinsics = np.array([[419.36179672, 0, 292.01381114],
                                     [0, 420.30767196, 201.61650657],
                                     [0, 0, 1]])
        CSIDistParam = np.array([-7.42983302e-01,
                                 9.24162996e-01,
                                 -2.39593372e-04,
                                 1.66230745e-02,
                                 -5.27787439e-01])
        undistortedImage = self.undistort_img(
                                                image,
                                                CSICamIntrinsics,
                                                CSIDistParam
                                                )

        return undistortedImage

    def subselect_and_threshold(self, image, rowStart, rowEnd, minThreshold, maxThreshold):
        """
        This function subselects a horizontal slice of the input image from
        rowStart to rowEnd for all columns, and then thresholds it based on the
        provided min and max thresholds. Returns the binary output from
        thresholding."""

        subImage = image[rowStart:rowEnd,:] # subsection of image we are interested in
        _, binary = cv2.threshold(subImage, minThreshold, maxThreshold, cv2.THRESH_BINARY)

        return binary

    def image_find_objects(self, image, connectivity, minArea, maxArea):
        """
        This function implements connected component labeling on the provided
        image with the desired connectivity. From the list of blobs detected,
        it returns the first blob that fits the desired area criteria based
        on minArea and maxArea provided. Returns the column and row location
        of the blob centroid, as well as the blob's area. """

        col = 0
        row = 0
        area = 0

        analysis = cv2.connectedComponentsWithStats(image, connectivity=connectivity, ltype=cv2.CV_32S)
        (labels, ids, values, centroids) = analysis

        for idx, val in enumerate(values):
            if val[4]>minArea and val[4] < maxArea:
                value = val
                centroid = centroids[idx]
                col = centroid[0]
                row = centroid[1]
                area = value[4]
                break
            else:
                col = None
                row = None
                area = None

        return col, row, area

    def line_to_speed_map(self, sampleRate, saturation):

        integrator   = Calculus().integrator(dt = sampleRate, saturation=saturation)
        derivative   = Calculus().differentiator(dt = sampleRate)
        next(integrator)
        next(derivative)
        forSpd, turnSpd = 0, 0
        offset = 0

        while True:
            col, kP, kD = yield forSpd, turnSpd

            if col is not None:
                error = 160 - col + offset # where you want the line to be at
                angle = np.arctan2(error, 125) # error angle w.r.t. image center at bottom row
                turnSpd = kP * angle + kD * derivative.send(angle) # turn spd command
                forSpd = 0.35*np.cos(angle) # forward spd command
                offset = integrator.send(25*turnSpd)

class QBPRanging():
    def __init__(self):
        pass

    def adjust_and_subsample(self, ranges, angles,end=-1,step=4):

        # correct angles data
        angles_corrected = -1*angles + np.pi/2
        # return every 4th sample
        return ranges[0:end:step], angles_corrected[0:end:step]

    def correct_lidar(self, lidarPosition, ranges, angles):

        # Convert lidar data from polar into cartesian, and add lidar position
        x = ranges*np.cos(angles) + lidarPosition[0]
        y = ranges*np.sin(angles) + lidarPosition[1]

        # Convert back into polar coordinates
        ranges_c = np.sqrt(x**2 + y**2)
        angles_c = np.arctan2(y, x)

        return ranges_c, angles_c

    def detect_obstacle(self, ranges, angles, forSpd, forSpeedGain, turnSpd, turnSpeedGain, minThreshold, obstacleNumPoints):

        halfNumPoints = 205
        quarterNumPoints = round(halfNumPoints/2)

        # Grab the first half of ranges and angles representing 180 degrees
        frontRanges = ranges[0:halfNumPoints]
        frontAngles = angles[0:halfNumPoints]

        # Starting index in top half          1     West
        # Mid point in west quadrant         51     North-west
        # Center index in top half          102     North
        # Mid point in east quadrant     51+102     North-east
        # Ending index in top half          205     East

        # Normalize turn speed from -1 to 1
        normalizedTurnSpeed = turnSpd/3.564

        # Find starting index to select quarterNumPoints
        startingIndex = int(quarterNumPoints/2) -  int((halfNumPoints/8)*turnSpeedGain*normalizedTurnSpeed)
        if startingIndex < 0:
            startingIndex = 0
        elif startingIndex > 102:
            startingIndex = 102

        normalizedForSpeed = forSpd/0.35
        safetyThreshold=normalizedForSpeed*forSpeedGain

        if safetyThreshold>2:
            safetyThreshold=2
        elif safetyThreshold <0.3:
            safetyThreshold=0.3
        # Pick quarterNumPoints in ranges and angles from the front half
        # this will be the region you monitor for obstacles
        monitorRanges = frontRanges[startingIndex:startingIndex+quarterNumPoints]
        monitorAngles = frontAngles[startingIndex:startingIndex+quarterNumPoints]

        # At angles corresponding to monitorAngles, pick uniform ranges based on
        # a safety threshold
        safetyAngles = monitorAngles
        safetyRanges = safetyThreshold*monitorRanges/monitorRanges

        # Total number of obstacles detected between
        # minThreshold & safetyThreshold
        totalObstaclePoints = ((monitorRanges < safetyThreshold)*(monitorRanges > minThreshold)).sum()
        if totalObstaclePoints > obstacleNumPoints:
            obstacleFlag = 1
        else:
            obstacleFlag = 0

        # Lidar Ranges and Angles for plotting (both scan & safety zone)
        plottingRanges = np.append(monitorRanges, safetyRanges)
        plottingAngles = np.append(monitorAngles, safetyAngles)

        return plottingRanges, plottingAngles, obstacleFlag
    
class QBPLocalization():
    """ This class contains the functions for the QBot Platform 
        for localization using lidar data """
    def __init__(self, resolution=20, max_range=5):
        self.lidarScanMatch = Lidar2DMatchScansGrid(resolution=resolution, max_range=max_range)
        self.pose = np.array([0.0,0.0,0.0],dtype=np.float32)
        self.score = np.array([0.0],dtype=np.float32)
        self.covariance = np.eye(3,dtype=np.float32)
        self.prevPose =  np.array([0.0,0.0,0.0],dtype=np.float32)

        self.refRanges = None
        self.refAngles = None
        self.refXY = None
        self.refSaved = False # flag for whether reference scan has been saved 
    
    def save_ref(self, rangesIn, anglesIn):
        """ This function saves input LiDAR data as a reference scan"""
        self.refSaved = False

        if rangesIn is not None and anglesIn is not None:
            
            # save reference scan
            self.refRanges = rangesIn
            self.refAngles = anglesIn

            # set flag 
            self.refSaved = True

            # initialize generator that converts each scan point to Cartesian  
            self.refXY = self.polar_to_cartesian(self.refRanges, self.refAngles)

        return self.refSaved
        
    def polar_to_cartesian(self, rangesIn, anglesIn):
        """ This generator converts polar coordinates
            to Cartesian """
        idx = 0
        while True:
            yield [rangesIn[idx]*np.cos(anglesIn[idx]), 
                   rangesIn[idx]*np.sin(anglesIn[idx])]
            idx = (idx+4)%len(rangesIn)

    def scan_match(self, ranges, angles, transRange=(3.0, 3.0), rotRange=2*np.pi ):
        """ This function checks for a saved reference scan and then runs
            the match method to find the transformation between the current scan"""
        if not self.refSaved:
            return False
        else:
            newMatch = self.lidarScanMatch.match(ref_ranges=self.refRanges, 
                                            ref_angles=self.refAngles, 
                                            num_ref_points = len(self.refRanges),
                                            ranges = ranges, 
                                            angles = angles, 
                                            num_points = len(ranges),
                                            initial_pose = self.prevPose, 
                                            translation_search_range = np.array(transRange, dtype=np.float32), 
                                            rotation_search_range = rotRange,
                                            pose=self.pose, 
                                            score=self.score, 
                                            covariance=self.covariance)
            self.prevPose = self.pose

            # update the next point in the reference scan
            self.refX, self.refY = next(self.refXY)
    
    def terminate(self):
        self.lidarScanMatch.close()


        

    

