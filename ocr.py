import easyocr
import numpy as np
import requests
import cv2
import pandas as pd


def is_text_in_image(image_url, reader):

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
        denoised_image = cv2.GaussianBlur(binary_image, (1, 1), 0)

        result = reader.readtext(denoised_image, detail=0)

        # 이미지 텍스트 출력
        print(image_url)
        print(result)

        if not result:
            return False
        else:
            return True
    except Exception as e:
        print('예외 발생')
        print(e)
        print(image_url)
        return False


def run(file_name, col_name, save_file, run_type, label7):
    reader = easyocr.Reader(['ko', 'en'], gpu=run_type)  # this needs to run only once to load the model into memory

    print(file_name)
    df1 = pd.read_excel(file_name, engine='xlrd')
    data = df1.loc[1:]['목록 이미지*'].to_list()

    df2 = pd.DataFrame()
    print('start')

    for i in range(len(data)):
        if is_text_in_image(data[i], reader):
            df2 = pd.concat([df2, df1.loc[[i]]])
        # label7.configure(text=str(i + 1) + ' / ' + str(len(data)))

    # is_text_in_image('https://i.pinimg.com/736x/19/97/cb/1997cbad0289f8313f0e1af86524b19d.jpg', reader)

    writer = pd.ExcelWriter(save_file, mode='w', engine='xlsxwriter')
    df2.to_excel(writer, index=False)
    writer.close()

run('C:/Users/ehdwn/PycharmProjects/imgeasy/cou.xls',
    '1',
    'C:/Users/ehdwn/PycharmProjects/imgeasy/a.xls',
    True,
    '1')

