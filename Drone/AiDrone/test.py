import torch
import cv2

# Model
blank_model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/best.pt', force_reload=True)
person_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# Images
img1 = 'data/test.png'  # or file, Path, PIL, OpenCV, numpy, list
# img = 'https://ultralytics.com/images/zidane.jpg'
img = cv2.imread('data/root2.png')
# Inference
# result1 = blank_model(img1)
# result2 = person_model(img2)

# Results
# results.print()  # or .show(), .save(), .crop(), .pandas(), etc.
# print(result1.pandas().xyxy[0])
# result1.show()

# df_blank = blankresult.pandas().xyxy[0]
# for i in range(len(df_blank)):
#     print((df_blank.loc[i]['xmin'], df_blank.loc[i]['ymin']), (df_blank.loc[i]['xmax'], df_blank.loc[i]['ymax']))
#     cv2.rectangle(img, (int(df_blank.loc[i]['xmin']), int(df_blank.loc[i]['ymin'])),
#                   (int(df_blank.loc[i]['xmax']), int(df_blank.loc[i]['ymax'])), (0, 255, 0), 3)
#
# cv2.imshow('frame', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# xmin = result1.pandas().xyxy[0].loc[0]['xmin']
# print(xmin)
# print(len(result1.pandas().xyxy[0]))

personresult = person_model(img)
print(personresult.pandas().xyxy[0])

df_person = personresult.pandas().xyxy[0]
df_person = df_person[df_person['name'] == 'person']

for i in range(len(df_person)):
            print((df_person.loc[i]['xmin'], df_person.loc[i]['ymin']), (df_person.loc[i]['xmax'], df_person.loc[i]['ymax']))
            cv2.rectangle(img, (int(df_person.loc[i]['xmin']), int(df_person.loc[i]['ymin'])),
                          (int(df_person.loc[i]['xmax']), int(df_person.loc[i]['ymax'])), (255, 0, 0), 3)

cv2.imshow('frame', img)
cv2.waitKey(0)
cv2.destroyAllWindows()