# Exam-Virtual-Invigilator
This project aims to monitor a student's activity during examinations, through webcam, microphone and screen monitoring. It can detect any unfair actions done by students, such as cheating. 

Please find the Executable File of this Software from this github link: https://github.com/Louisljz/Exam-Virtual-Invigilator-EXE

The following are the algorithms used in the 3 different types of activity monitoring:
1. Webcam:
  - Face Monitoring: Detects Whether a single face is always present within the camera frame. If no face, or more than one face is present, then it will mark it as a form of cheating action.
  - Eye Gaze Tracking: The exam taker should continually focus looking on his/her laptop screen. If he/she keeps looking around to the left or right many times, then it will be marked as suspicious activity, and the exam invigilator will receive a notice. 
2. Microphone:
  - Speech Recognition: Through Google speech recognition API, the software can detect any conversations from the microphone, and will translate speech to text, so the invigilator can analyze whether someone is helping the student to do the exam. 
3. Screen:
  - App Monitoring: The software can monitor the list of applications open during the exam. And if there is any unnecessary apps open, then the invigilator will be notified about the title of the opened window. 
  - Browser Tab Monitoring: The software can list down the title of all of the tabs opened in various browsers, not limited to Google Chrome, but also Microsoft Edge and Mozilla Firefox. 
 
All of these different monitoring algorithms will be integrated and implemented into one software with Graphic User Interface (GUI) for people to view and use it easily. 

Note: This Project is still BETA, meaning it's just a prototype, and a server hasn't been implemented to transmit the data from the exam taker client PC into the invigilator's center PC. There is still no infrastructure/pipeline created to do that. 
