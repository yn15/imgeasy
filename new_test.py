import easyocr
import numpy as np
import requests
import cv2
import pandas as pd
import gc
import torch


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
        denoised_image = cv2.medianBlur(binary_image, 3)

        scale_data.append(denoised_image)

    except Exception as e:
        print('Image scale error')
        print(e)
        print(image_url)
        scale_data.append([])
        return False


def is_text_in_image(data_arg, reader):
    try:
        result = reader.readtext(data_arg, detail=0)
        if not result:
            return False
        else:
            return True
    except Exception as e:
        print('Image OCR error')
        print(e)
        return False
    # gc.collect()
    # torch.cuda.empty_cache()
    # del reader


def run(file_name, col_name, save_file, run_type, label7):
    df1 = pd.read_excel(file_name, engine='xlrd')
    data = df1.loc[1:]['목록 이미지*'].to_list()

    df2 = pd.DataFrame()

    print("scale start")

    scale_data = []

    for i in range(len(data)):
        img_scale(data[i], scale_data)

    # for i in data:
    #     img_scale(i, scale_data)

    print("scale end")

    reader = easyocr.Reader(['ko', 'en'], gpu=run_type)  # this needs to run only once to load the model into memory

    for i in range(len(scale_data)):
        if len(scale_data) == 0:
            print(data[i])
            df2 = pd.concat([df2, df1.loc[[i + 1]]])
            continue

        if is_text_in_image(data[i], reader):
            df2 = pd.concat([df2, df1.loc[[i + 1]]])
        # label7.configure(text=str(i + 1) + ' / ' + str(len(data)))
        print(i)

    writer = pd.ExcelWriter(save_file, mode='w', engine='xlsxwriter')
    df2.to_excel(writer, index=False)
    writer.close()


run('C:/Users/ehdwn/PycharmProjects/imgeasy/cou.xls',
    '1',
    'C:/Users/ehdwn/PycharmProjects/imgeasy/a.xls',
    True,
    '1')
