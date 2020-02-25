import time
import cv2
from matplotlib import pyplot as plt
import multiprocessing
 
src0 = 'rtmp:url'




def Cap(No,src):
    #通过cv2中的类获取视频流操作对象cap
    cap = cv2.VideoCapture(src)
    #调用cv2方法获取cap的视频帧（帧：每秒多少张图片）
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)
    #获取cap视频流的每帧大小
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print(size)
     
    #定义编码格式mpge-4
    fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', '2')

    name = time.strftime("%a_%b_%d_%H_%Y", time.localtime())
    name = str(No)+'/'+name+'.avi'
    #定义视频文件输入对象
    outVideo = cv2.VideoWriter(name,fourcc,fps,size)
     
    #获取视频流打开状态
    if cap.isOpened():
        rval,frame = cap.read()
        print('ture')
    else:
        rval = False
        print('False')
     
    tot=1
    c=1
    #循环使用cv2的read()方法读取视频帧
    while rval:
        rval,frame = cap.read()
        cv2.imshow('test',frame)
        #每间隔20帧保存一张图像帧,25帧一秒
        # if tot % 20 ==0 :
        #     cv2.imwrite('cut/'+'cut_'+str(c)+'.jpg',frame)
        #     c+=1
        tot+=1
        # print('tot=',tot)
        
        # 24*60*60*25=2160000
        if(tot%2160000==0):
             print('change', No)
             name = str(No) + '/' + name +'.avi'
             outVideo.release() # 释放上一个视频
             outVideo = cv2.VideoWriter(name,fourcc,fps,size)
             
        
        #使用VideoWriter类中的write(frame)方法，将图像帧写入视频文件
        outVideo.write(frame)
        cv2.waitKey(1)
    cap.release()
    outVideo.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Cap(0,src0)
    p0 = multiprocessing.Process(target=Cap,args=(0,src0,))

    p0.start()

