import cv2
import numpy as np
import glob

# Import everything needed to edit/save/watch video clips
from moviepy.editor import VideoFileClip

from src.calibrate import Calibrator
from src.transform import Transform
from src.color import color
from src.lines import lines
from src.curvature import curvature
from src.position import position

def main():
    transform_src = np.float32([[580, 450], [700, 450], [1070, 675], [240, 675]])

    # Set up camera callibration
    calibrator = Calibrator('../camera_cal/calibration*.jpg')
    transformer = Transform(transform_src)

    images = glob.glob("../test_images/**")



    def process(img):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        # # Undistort the image
        calibrated = calibrator.undistort(img)
        #
        # # Warp
        transformed = transformer.warp(calibrated)
        #
        # # Color transforms
        colored = color(transformed)
        #
        # # Find Lane Lines
        left_fit, right_fit, colored_img = lines(colored)

        # Draw the lane space on the original image
        unwarped = transformer.unwarp(colored_img)
        result = cv2.addWeighted(calibrated, 1, unwarped, 0.5, 0)

        curv = curvature(left_fit, right_fit)
        pos = position(left_fit, right_fit, colored_img)
        direction = "left" if pos < 0 else "right"

        cv2.putText(result, "Curvature: {} meters".format(int(curv)), (300, 50), 0, 1, (255, 255,0), 3)
        cv2.putText(result, "Position: {} meters {}".format(abs(pos), direction), (300, 100), 0, 1, (255, 255, 0), 3)

        result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

        return result


    # Video
    video_output = '../output_videos/result.mp4'
    clip1 = VideoFileClip("../project_video.mp4")
    white_clip = clip1.fl_image(process)
    white_clip.write_videofile(video_output, audio=False)




if __name__ == '__main__':
    main()