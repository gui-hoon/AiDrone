import cv2
import torch

cap1 = cv2.VideoCapture('data/test5.mp4')
cap2 = cv2.VideoCapture('data/root3.mp4')

blank_model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/best.pt', force_reload=True)
person_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

while(cap1.isOpened()):
    ret, img = cap1.read()
    if ret:
        img = cv2.rotate(img, cv2.ROTATE_180)

        blankresult = blank_model(img)
        personresult = person_model(img)

        df_blank = blankresult.pandas().xyxy[0]
        df_blank = df_blank[df_blank['confidence'] > 0.7]
        # print(f"df_blank = {df_blank}")

        df_person = personresult.pandas().xyxy[0]
        df_person = df_person[df_person['name'] == 'person']
        df_person = df_person[df_person['confidence'] > 0.8]
        # print(f"df_person = {df_person}")

        if df_blank is not None:
            for i in range(len(df_blank)):
                # print((df_blank.loc[i]['xmin'], df_blank.loc[i]['ymin']), (df_blank.loc[i]['xmax'], df_blank.loc[i]['ymax']))
                cv2.rectangle(img, (int(df_blank.loc[i]['xmin']), int(df_blank.loc[i]['ymin'])),
                              (int(df_blank.loc[i]['xmax']), int(df_blank.loc[i]['ymax'])), (0, 255, 0), 3)

        if df_person is not None:
            for i in range(len(df_person)):
                # print((df_person.iloc[i]['xmin'], df_person.iloc[i]['ymin']), (df_person.iloc[i]['xmax'], df_person.iloc[i]['ymax']))
                cv2.rectangle(img, (int(df_person.iloc[i]['xmin']), int(df_person.iloc[i]['ymin'])),
                              (int(df_person.iloc[i]['xmax']), int(df_person.iloc[i]['ymax'])), (255, 0, 0), 3)

        cv2.imshow('test', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap1.release()
cv2.destroyAllWindows()