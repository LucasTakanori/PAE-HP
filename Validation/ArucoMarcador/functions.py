import cv2
import numpy as np
import yaml
import math

# Parametres per les funcions de ChArUco
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
board = cv2.aruco.CharucoBoard_create(7,5,.04,.02,aruco_dict)
img = board.draw((600,500))

def read_CharucoBoards(images):
    """
    Charuco base pose estimation.
    """
    print("POSE ESTIMATION STARTS:")
    allCorners = []
    allIds = []
    decimator = 0
    # SUB PIXEL CORNER DETECTION CRITERION
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.00001)

    for im in images:
        print("=> Processing image {0}".format(im))
        frame = cv2.imread(im)
        frame_smooth = cv2.GaussianBlur(frame,(5,5),cv2.BORDER_DEFAULT)
        gray = cv2.cvtColor(frame_smooth, cv2.COLOR_BGR2GRAY)
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, aruco_dict)

        if len(corners)>0:
            # SUB PIXEL DETECTION
            for corner in corners:
                cv2.cornerSubPix(gray, corner,
                                 winSize = (3,3),
                                 zeroZone = (-1,-1),
                                 criteria = criteria)
            res2 = cv2.aruco.interpolateCornersCharuco(corners,ids,gray,board)
            if res2[1] is not None and res2[2] is not None and len(res2[1])>3 and decimator%1==0:
                allCorners.append(res2[1])
                allIds.append(res2[2])

        decimator+=1

    imsize = gray.shape
    return allCorners,allIds,imsize

def calibrate_camera_charuco(allCorners,allIds,imsize):
    """
    Calibrates the camera using the detected corners.
    """
    print("CAMERA CALIBRATION")

    cameraMatrixInit = np.array([[ 1000.,    0., imsize[0]/2.],
                                 [    0., 1000., imsize[1]/2.],
                                 [    0.,    0.,           1.]])

    distCoeffsInit = np.zeros((5,1))
    flags = (cv2.CALIB_USE_INTRINSIC_GUESS + cv2.CALIB_RATIONAL_MODEL + cv2.CALIB_FIX_ASPECT_RATIO)
    #flags = (cv2.CALIB_RATIONAL_MODEL)
    (ret, camera_matrix, distortion_coefficients,
     rotation_vectors, translation_vectors,
     stdDeviationsIntrinsics, stdDeviationsExtrinsics,
     perViewErrors) = cv2.aruco.calibrateCameraCharucoExtended(
                      charucoCorners=allCorners,
                      charucoIds=allIds,
                      board=board,
                      imageSize=imsize,
                      cameraMatrix=cameraMatrixInit,
                      distCoeffs=distCoeffsInit,
                      flags=flags,
                      criteria=(cv2.TERM_CRITERIA_EPS & cv2.TERM_CRITERIA_COUNT, 10000, 1e-9))

    return ret, camera_matrix, distortion_coefficients, rotation_vectors, translation_vectors

def calibrate_camera_chess(images, CHECKERBOARD):

    # stop the iteration when specified
    # accuracy, epsilon, is reached or
    # specified number of iterations are completed.
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Vector for 3D points
    threedpoints = []

    # Vector for 2D points
    twodpoints = []

    # 3D points real world coordinates
    objectp3d = np.zeros((1, CHECKERBOARD[0]
                        * CHECKERBOARD[1],
                        3), np.float32)
    objectp3d[0, :, :2] = np.mgrid[0:CHECKERBOARD[0],
                                0:CHECKERBOARD[1]].T.reshape(-1, 2)
    prev_img_shape = None
    print("POSE ESTIMATION STARTS:")

    for filename in images:
        print("=> Processing image {0}".format(filename))
        image = cv2.imread(filename)
        grayColor = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners, if desired number of corners are
        # found in the image then ret = true
        ret, corners = cv2.findChessboardCorners( grayColor, CHECKERBOARD, flags = cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)

        # If desired number of corners can be detected then,
        # refine the pixel coordinates and display them on the images of checker board
        if ret == True:
            threedpoints.append(objectp3d)

            # Refining pixel coordinates for given 2d points.
            corners2 = cv2.cornerSubPix(
                grayColor, corners, (11, 11), (-1, -1), criteria)

            twodpoints.append(corners2)

            # Draw and display the corners
            image = cv2.drawChessboardCorners(image,
                                            CHECKERBOARD,
                                            corners2, ret)

    cv2.destroyAllWindows()
    imsize = grayColor.shape

    # Perform camera calibration by passing the value of above found out
    # 3D points (threedpoints) and its corresponding pixel coordinates of 
    # the detected corners (twodpoints)
    print("CAMERA CALIBRATION")
    ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(
    	threedpoints, twodpoints, grayColor.shape[::-1], None, None)

    return ret, matrix, distortion, r_vecs, t_vecs, imsize

def saveCameraParams(filename, imageSize, cameraMatrix, distCoeffs, totalAvgErr, rvecs, tvecs):

    # crea diccionari per guardar totes les dades
    data = {'camera_matrix': np.asarray(cameraMatrix).tolist(),
            'dist_coeff': np.asarray(distCoeffs).tolist(),
            'r_vecs' : np.asarray(rvecs).tolist(),
            't_vecs' : np.asarray(tvecs).tolist(),
            'total_avg_error' : np.asarray(totalAvgErr).tolist(),
            'imageSize' : np.asarray(imageSize).tolist() }
    
    # guarda dades al fitxer li hem passat
    with open(filename, "w") as f:
        yaml.dump(data, f)

def readCameraParams(filename):

    with open(filename, 'r') as f:
        # dict = yaml.load(f)  # Treu warning, deprecated
        dict = yaml.load(f, Loader=yaml.SafeLoader)

    cameraMatrix = dict['camera_matrix']
    distCoeffs = dict['dist_coeff']
    rotation_vectors = dict['r_vecs']
    translation_vectors = dict['t_vecs']
    total_avg_error = dict['total_avg_error']
    imageSize = dict['imageSize']

    return imageSize, cameraMatrix, distCoeffs, total_avg_error, rotation_vectors, translation_vectors

def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)) * 180 / math.pi

def rescale_frame(frame, scale):    # works for image, video, live video
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width, height)
    return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)