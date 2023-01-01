import cv2
import torch
import os
dst = cv2.imread('./capture', cv2.IMREAD_COLOR)

print('Load Model ...')
blank_model = torch.load('weights/best_blank.pt')
person_model = torch.load('weights/best_person.pt')

for i in os.listdir('./capture/'):
    path = './capture/' + i

    img = cv2.imread(path, cv2.IMREAD_COLOR)

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
            print((df_blank.iloc[i]['xmin'], df_blank.iloc[i]['ymin']),
                  (df_blank.iloc[i]['xmax'], df_blank.iloc[i]['ymax']))
            cv2.rectangle(img, (int(df_blank.iloc[i]['xmin']), int(df_blank.iloc[i]['ymin'])),
                          (int(df_blank.iloc[i]['xmax']), int(df_blank.iloc[i]['ymax'])), (0, 255, 0), 3)
            cv2.putText(img, df_blank.iloc[i]['name'],
                        (int(df_blank.iloc[i]['xmin']), int(df_blank.iloc[i]['ymin'] - 6)), cv2.FONT_ITALIC, 1,
                        (0, 255, 0), 2)

        sendimg = cv2.resize(img, (960, 960))
        # server.splitFrame(sendimg)

    if df_person is not None:
        for i in range(len(df_person)):
            print((df_person.iloc[i]['xmin'], df_person.iloc[i]['ymin']),
                  (df_person.iloc[i]['xmax'], df_person.iloc[i]['ymax']))
            cv2.rectangle(img, (int(df_person.iloc[i]['xmin']), int(df_person.iloc[i]['ymin'])),
                          (int(df_person.iloc[i]['xmax']), int(df_person.iloc[i]['ymax'])), (255, 0, 0), 3)
            cv2.putText(img, df_person.iloc[i]['name'],
                        (int(df_person.iloc[i]['xmin']), int(df_person.iloc[i]['ymin'] - 6)), cv2.FONT_ITALIC, 1,
                        (255, 0, 0), 2)

    cv2.imshow("Drone view", img)
    cv2.waitKey(0)