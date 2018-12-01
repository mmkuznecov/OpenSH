import face_recognition
import cv2
import os
import json
import datetime
import time
from PIL import Image
import ftplib
with open('document.json') as f:
    data = f.read()
    fgh = json.loads(data)

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
'''obama_image = face_recognition.load_image_file('C:\\Python27\\obama.jpg')
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("C:\\Python27\\biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

misha_image = face_recognition.load_image_file("C:\\Python27\\misha.jpg")
misha_face_encoding = face_recognition.face_encodings(misha_image)[0]'''
faces_images=[]
for i in os.listdir('/home/mikhail/Faces'):
    faces_images.append(face_recognition.load_image_file('/home/mikhail/Faces/'+i))
known_face_encodings=[]
for i in faces_images:
    known_face_encodings.append(face_recognition.face_encodings(i)[0])
known_face_names=[]
for i in os.listdir('/home/mikhail/Faces'):
    i=i.split('.')[0]
    known_face_names.append(i)

#faces_images=[i for i in os.listdir i=face_recognition.load_image_file('C:\\Faces\\'+i)]

# Create arrays of known face encodings and their names
'''known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    misha_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Joe Biden",
    'Misha'
]'''

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

            frame_for_save=frame[:, :, ::-1]
            frame_for_save=Image.fromarray(frame_for_save)
            now=datetime.datetime.now()
            mil=str(round(time.time()*1000))
            date=('/home/mikhail/Visits/'+mil+'_'+fgh['users'][int(name)][name][0]['name']+'.jpg')
            frame_for_save.save(date)
            session = ftplib.FTP('rudy.zzz.com.ua','ondrey','Freefree0')
            session.cwd("ondrey.zzz.com.ua/peephole")
            file = open(date,'rb')                  # file to send
            session.storbinary('STOR '+mil+'_'+fgh['users'][int(name)][name][0]['name']+'.jpg', file)     # send the file
            file.close()                                    # close file and FTP
            session.quit()



    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

        # Draw a label with a name below the face
        #cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        if name=='Unknown':
            #cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        else:
            #cv2.rectangle(frame, (right+100, bottom), (right, top), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, 'Name: '+fgh['users'][int(name)][name][0]['name'], (left + 6, bottom - 6), font, 0.7, (255, 255, 255), 1)
            #cv2.putText(frame, 'Sex: '+fgh['users'][int(name)][name][0]['sex'], (right + 6, top + 24*3), font, 0.7, (255, 255, 255), 1)
            #cv2.putText(frame, 'Age: '+str(fgh['users'][int(name)][name][0]['age']), (right + 6, top + 36*3), font, 0.7, (255, 255, 255), 1)
            #cv2.putText(frame, 'City: '+fgh['users'][int(name)][name][0]['adress'], (right + 6, top + 48*3), font, 0.7, (255, 255, 255), 1)


        #print('Name: '+fgh['users'][int(name)][name][0]['name'])
        #print('Sex: '+fgh['users'][int(name)][name][0]['sex'])
        #print('Age: '+str(fgh['users'][int(name)][name][0]['age']))
        #print('City: '+fgh['users'][int(name)][name][0]['adress'])

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
