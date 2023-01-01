import cv2
import torch
import time

cap = cv2.VideoCapture('data/test5.mp4')
# cap = cv2.VideoCapture('data/root3.mp4')

prev_time = 0
fps = 5

# blank_model_ori = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/best.pt', force_reload=True)
# person_model_ori = torch.hub.load('ultralytics/yolov5', 'yolov5s')
#
# torch.save(blank_model_ori, './best_blank.pt')
# torch.save(person_model_ori, './best_person.pt')

print('save model')
blank_model = torch.load('best_blank.pt')
person_model = torch.load('best_person.pt')

while(cap.isOpened()):
    ret, img = cap.read()
    current_time = time.time() - prev_time

    if (ret is True) & (current_time > 1./ fps):
        prev_time = time.time()

        img = cv2.rotate(img, cv2.ROTATE_180)
        blankresult = blank_model(img)
        personresult = person_model(img)

        df_blank = blankresult.pandas().xyxy[0]
        df_blank = df_blank[df_blank['confidence'] > 0.7]
        print(f"df_blank = {df_blank}")

        df_person = personresult.pandas().xyxy[0]
        df_person = df_person[df_person['name'] == 'person']
        df_person = df_person[df_person['confidence'] > 0.8]
        print(f"df_person = {df_person}")

        if df_blank is not None:
            for i in range(len(df_blank)):
                print((df_blank.iloc[i]['xmin'], df_blank.iloc[i]['ymin']), (df_blank.iloc[i]['xmax'], df_blank.iloc[i]['ymax']))
                cv2.rectangle(img, (int(df_blank.iloc[i]['xmin']), int(df_blank.iloc[i]['ymin'])),
                              (int(df_blank.iloc[i]['xmax']), int(df_blank.iloc[i]['ymax'])), (0, 255, 0), 3)
                cv2.putText(img, df_blank.iloc[i]['name'], (int(df_blank.iloc[i]['xmin']), int(df_blank.iloc[i]['ymin']-6)), cv2.FONT_ITALIC, 1, (0,255,0),2)

        if df_person is not None:
            for i in range(len(df_person)):
                print((df_person.iloc[i]['xmin'], df_person.iloc[i]['ymin']), (df_person.iloc[i]['xmax'], df_person.iloc[i]['ymax']))
                cv2.rectangle(img, (int(df_person.iloc[i]['xmin']), int(df_person.iloc[i]['ymin'])),
                              (int(df_person.iloc[i]['xmax']), int(df_person.iloc[i]['ymax'])), (255, 0, 0), 3)
                cv2.putText(img, df_person.iloc[i]['name'], (int(df_person.iloc[i]['xmin']), int(df_person.iloc[i]['ymin']-6)), cv2.FONT_ITALIC, 1, (255, 0, 0), 2)

        cv2.imshow('Drone View', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()