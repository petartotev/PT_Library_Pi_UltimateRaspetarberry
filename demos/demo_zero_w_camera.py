""""Python Script implements Camera Demo"""

from time import sleep
import sys
sys.path.append("../libraries")
import piLibCamera

def get_directory(type_media):
    """Get Directory"""
    if type_media == 'photo':
        return "/home/pi/Desktop/MyDocuments/MyPhotos/"
    if type_media == 'video':
        return "/home/pi/Desktop/MyDocuments/MyVideos"
    raise ValueError('Path input is invalid!')

if __name__ == "__main__":
    try:
        piLibCamera.takeShot(get_directory("photo"))
        sleep(5)
        piLibCamera.takeShot(get_directory("photo"), 600, 600)
        sleep(5)
        piLibCamera.takeShotPerMinute(get_directory("photo"), 3)
        sleep(5)
        piLibCamera.takeShotPerMinute(get_directory("photo"), 3, 300, 900)
        sleep(5)
        piLibCamera.takeVideo(get_directory("video"), 20)
        sleep(5)
        piLibCamera.takeVideo(get_directory("video"), 10, 300, 300)
        sleep(5)
        piLibCamera.takeShot(get_directory("wrong"))
    except Exception:
        print("Error!")
    finally:
        print("Exit!")
