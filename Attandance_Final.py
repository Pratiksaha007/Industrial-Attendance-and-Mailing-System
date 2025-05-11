import cv2
import face_recognition
import csv
import os
import datetime
import numpy as np
import pyttsx3
import student_roll_no
import smtplib
import email_details01
import email_dict01
import content
import student_names01

eng = pyttsx3.init()

def speak(text):
    eng.say(text)
    eng.runAndWait()

def send_email(to, content):
    try:
        a = email_details01.details.get("email_id")
        b = email_details01.details.get("password")
        
        if not a or not b:
            raise ValueError("Email ID or password not provided in email_details01.")
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(a, b)
        
        message = f"Subject: Attendance Notification\n\n{content}"
        server.sendmail(a, to, message)
        server.close()
        
        print("Email sent successfully!")
        speak("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
        # speak("SMTP error occurred.")
    except Exception as e:
        print(f"An error occurred: {e}")
        # speak("An error occurred.")

def Image_file_path(path):
    all_files = os.listdir(path)
    image_paths=[]
    for file in all_files:
        image_paths.append(os.path.join(path,file))
    return image_paths

def load_encode_faces(image_paths):
    encoded_faces = []
    for path in image_paths:
        image = face_recognition.load_image_file(path)
        face_encodings = face_recognition.face_encodings(image)
        if face_encodings:  # Check if any faces are found
            encoded_faces.append(face_encodings[0])  # Append the first face encoding found
        else:
            print(f"No faces found in image: {path}")
    return encoded_faces
    
student_names=student_names01.names()
student=student_names.copy()

def create_csv(name):
    now = datetime.datetime.now()
    current_date = now.strftime("%d-%m-%Y")
    current_time = now.strftime("%H-%M-%S")
    for names1 in student_roll_no.Roll_no:
        if name == names1:
            roll=student_roll_no.Roll_no[names1]
    
    filename = f"{current_date}.csv"
    
    # Check if the file exists to determine if the header should be written
    file_exists = False
    try:
        with open(filename, "r", newline="") as f:
            file_exists = True
    except FileNotFoundError:
        pass
    
    with open(filename, "a", newline="") as f:
        lnwriter = csv.writer(f)
        # Write the header only if the file does not already exist
        if not file_exists:
            lnwriter.writerow(["Name","Roll No.","In-Time"])
            
        lnwriter.writerow([name,roll,current_time])


face_locations = []
face_encodings = []

def attendance(path):
    image_paths_01=Image_file_path(path)
    encoded_faces = load_encode_faces(image_paths_01)
    name=""
    vid_capture = cv2.VideoCapture(0)
    while True:
        ret,frame = vid_capture.read()
        if not ret:
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)  #CHANGING THE INPUT SIZE OF THE WEBCAM TO 1/4 FOR FASTER PROCESSING 

        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)     #BGR TO RGB CHANGE
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
      
        for (top, right, bottom, left),face_encoding in zip (face_locations,face_encodings):
            cv2.rectangle(frame, (left*4, top*4), (right*4, bottom*4), (0, 0, 255), 2)
            matches = face_recognition.compare_faces(encoded_faces, face_encoding)
            face_distance = face_recognition.face_distance(encoded_faces,face_encoding)
            best_match_index = np.argmin(face_distance)
            txt = "Attendance Marked !"
            # txt1 = "Email sent successfully !"
            content2 = content.content1

            if True in matches:
                if matches[best_match_index]:
                    name = student_names[best_match_index]
                    cv2.rectangle(frame, (left*4, top*4), (right*4, bottom*4), (0, 255, 0), 2)
                    cv2.imshow('Video', frame)

            if name in student_names:
                if name in student:
                    student.remove(name)
                    print(student)
                    create_csv(name)
                    print(txt)
                    speak(txt)
                    try:
                        for names2 in email_dict01.email:
                            if name == names2:
                                to=email_dict01.email[names2]
                                send_email(to,content2)
                                # print(txt1)
                                # speak(txt1)
                    except:
                        err2 = "email can`t be sent"
                        print(err2)
                        speak(err2)


        if cv2.waitKey(1) & 0xFF == ord('a'):
            break
    
    vid_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    path= r"C:\Users\PRATIK SAHA\OneDrive\Desktop\project1\Successful proj\Attendance_project\Student pics"
    attendance(path)

