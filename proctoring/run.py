from proctoring import audio
from proctoring import head_pose
from proctoring import detection
import threading as th
from django.shortcuts import redirect
import cv2

# def run_system():
def main(stop_event, cheat_event, username, quiz_id):
    # main()
    while not stop_event.is_set():
        head_pose_thread = th.Thread(target=head_pose.pose, args=(stop_event, cheat_event, username, quiz_id, ), name="Thread 1")
        # audio_thread = th.Thread(target=audio.sound, args=(stop_event,cheat_event,), name="Thread 2")
        detection_thread = th.Thread(target=detection.run_detection, args=(stop_event, cheat_event, username,), name="Thread 3")

        head_pose_thread.start()
        # audio_thread.start()
        detection_thread.start()

        # while not head_pose.stop_event.is_set():
        #     pass
        head_pose_thread.join()
        # audio_thread.join()
        detection_thread.join()
        # from proctoring.global_var import event_stop
        # if not head_pose_thread.is_alive() and not audio_thread.is_alive() and not detection_thread.is_alive() and event_stop:
        #     print("Value of event_stop in run", event_stop)
        #     return
        if stop_event.is_set():
            print("Run thread closed.")
            break
    detection.CHEAT_COUNT = 0
    detection.FINAL_CHEAT_COUNT = 0
    detection.GLOBAL_CHEAT = 0
    detection.PERCENTAGE_CHEAT = 0
    detection.CHEAT_THRESH = 0.6
    detection.XDATA = list(range(200))
    detection.YDATA = [0] * 200
    print("Hello process next")
    print("Value of stop_event", stop_event.is_set())
    print("Value of cheat_event", cheat_event.is_set())
    return redirect('/app/landingpage2/')

# def running_tester():
#     stop_event = th.Event()
#     run_threads(stop_event)
