import easyocr
import numpy as np
import requests
import cv2
import pandas as pd
import test

import gc
import torch

import time

import threading

from numba import cuda
from multiprocessing import Process, Queue



def img_scale(image_url, scale_data):
    try:
        # 이미지 바이트 배열 변환
        image_nparray = np.asarray(bytearray(requests.get(image_url).content), dtype=np.uint8)

        # 이미지 원형 변환
        image = cv2.imdecode(image_nparray, cv2.IMREAD_COLOR)

        # 이미지 그레이스케일링
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 이미지 이진화
        _, binary_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)

        # 이미지 노이즈 제거
        # denoised_image = cv2.fastNlMeansDenoising(binary_image, None, 10, 7, 21)
        # denoised_image = cv2.GaussianBlur(binary_image, (1, 1), 0)
        denoised_image = cv2.medianBlur(binary_image, 3)

        scale_data.append(denoised_image)

    except Exception as e:
        print('Image scale error')
        print(e)
        return False


def run(file_name, col_name, save_file, run_type, label7):
    # for i in range(0, 10000, 1000):
    #     print(i)

    # list = [0, 1, 2, 3, 4]
    # print(list[0:7])

    df1 = pd.read_excel(file_name, engine='xlrd')
    data = df1.loc[1:]['목록 이미지*'].to_list()

    scale_data = []

    for i in range(0, len(data)):
        img_scale(data[i], scale_data)

    print('scale end')

    # this needs to run only once to load the model into memory

    # df2 = pd.DataFrame()

    for i in range(0, len(scale_data), 1000):
        # reader = easyocr.Reader(['ko', 'en'], gpu=run_type)
        # th = threading.Thread(target=test.is_text_in_image, args=(scale_data[i:i + 100], i))

        th = Process(target=test.is_text_in_image, args=(scale_data[i:i + 1000], i))
        th.start()
        th.join()
        # cuda.get_current_device().reset()
        # time.sleep(30)
        # print(i)
        # if i % 1000 == 0:
        #     gc.collect()
        #     torch.cuda.empty_cache()
        #     time.sleep(30)
        # if is_text_in_image(scale_data[i:i+1000], reader):
        #     continue
        # df2 = pd.concat([df2, df1.loc[[i]]])


if __name__ == '__main__':
    run('C:/Users/ehdwn/PycharmProjects/imgeasy/cou.xls',
        '1',
        'C:/Users/ehdwn/PycharmProjects/imgeasy/a.xls',
        True,
        '1')
