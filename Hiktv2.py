import cv2
import numpy as np  
import time
import multiprocessing as mp

"""
Source: Yonv1943 2018-06-17
https://github.com/Yonv1943/Python/tree/master/Demo
"""

fps = 0
size = (0,0)

def image_collect(queue_list, camera_name):

    """show in single opencv-imshow window"""
    window_name = camera_name[0]
    cv2.namedWindow(window_name, flags=cv2.WINDOW_FREERATIO)
    while True:
        imgs = [q.get() for q in queue_list]
        imgs = np.concatenate(imgs, axis=1)
        cv2.imshow(window_name, imgs)
        cv2.waitKey(1)



def image_put(q, ip):
    #通过cv2中的类获取视频流操作对象cap
    cap = cv2.VideoCapture(ip)
    #调用cv2方法获取cap的视频帧（帧：每秒多少张图片）
    global fps
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)
    #获取cap视频流的每帧大小
    global size
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print(size)


    if cap.isOpened():
        print('HIKVISION')

    while True:
        q.put(cap.read()[1])
        q.get() if q.qsize() > 1 else time.sleep(0.01)

def image_get(q, window_name):
    tol = 1
    cv2.namedWindow(window_name, flags=cv2.WINDOW_FREERATIO)
    fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')
    #定义视频文件输入对象
    fps = 25.0
    size = (704,576)
    name = time.strftime("%a_%b_%d_%H_%Y", time.localtime())
    name = window_name+'/'+name+'.avi'
    outVideo = cv2.VideoWriter(name,fourcc,fps,size)
    while True:
        frame = q.get()

        tol += 1
        # 86400*25 定时更换文件名
        if(tol%2160000==0):
            print('change', window_name)
            name = window_name+'/'+time.strftime("%a_%b_%d_%H_%S_%Y", time.localtime())+'.avi'
            outVideo.release()
            outVideo = cv2.VideoWriter(name,fourcc,fps,size)
        cv2.imshow(window_name, frame)
        outVideo.write(frame)
        cv2.waitKey(1)

    outVideo.release()
    cv2.destroyAllWindows()


def run_multi_camera():
    # user_name, user_pwd = "admin", "password"
    camera_ip_l = [
        "rtmp://？？" ,
        "rtmp://？？"
        # 把你的摄像头的地址放到这里，如果是ipv6，那么需要加一个中括号。
    ]

    camera_name_l = [
        "6857",
        "6858"
    ]


    # mp.set_start_method(method='spawn')  # init
    queues = [mp.Queue(maxsize=4) for _ in camera_ip_l]
    processes = []
    # processes.append(mp.Process(target=image_collect, args=(queues, camera_name_l))) # 同屏显示
    for queue, camera_ip, camera_name in zip(queues, camera_ip_l,camera_name_l):
        processes.append(mp.Process(target=image_put, args=(queue,camera_ip)))
        processes.append(mp.Process(target=image_get, args=(queue, camera_name)))
        




    for process in processes:
        process.daemon = True
        process.start()
    for process in processes:
        process.join()

if __name__ == '__main__':
    run_multi_camera()
