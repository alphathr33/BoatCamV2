import pyrealsense2 as rs
import numpy as np
import cv2

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        #np.savetxt('depthImageData.txt', depth_image)
        color_image = np.asanyarray(color_frame.get_data())


        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap1 = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_INFERNO)
        cv2.imshow('colormap',depth_colormap1)
        depth_colormap = cv2.blur(depth_colormap1, (5,5))

        processed_depth = depth_colormap
        processed_depth = cv2.Canny(processed_depth, 80, 120)


        depth_colormap = cv2.cvtColor(depth_colormap, cv2.COLOR_BGR2GRAY)
        depth_colormap1 = cv2.cvtColor(depth_colormap1, cv2.COLOR_BGR2GRAY)
        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        # If depth and color resolutions are different, resize color image to match depth image for display
        if processed_depth.shape != depth_colormap_dim:
            resized_depth_image = cv2.resize(depth_colormap, dsize=(processed_depth[1], processed_depth[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_depth_image, processed_depth))
        else:
            images = np.hstack((depth_colormap1, depth_colormap, processed_depth))

        # Show images
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', images)
        cv2.waitKey(1)

finally:

    # Stop streaming
    pipeline.stop()