from tkinter import *
import sys
import os

from Facial_Detection import Facial_Monitor
import cv2

from Screen_Monitor import Screen_Monitor

import speech_recognition as sr

import multiprocessing as mp
try:
    if sys.platform.startswith('win'):
        import multiprocessing.popen_spawn_win32 as forking
    else:
        import multiprocessing.popen_fork as forking
except ImportError:
    import multiprocessing.forking as forking



def facial_func(d, face, eye):
    cap = cv2.VideoCapture(0)

    face_warnings = {0: "NO FACE", 1: "OKAY", 2: "MANY FACES"}
    eye_warnings = {0: "NOT FOCUS", 1: "OKAY"}

    while cap.isOpened():
        _, img = cap.read()
        Face = Facial_Monitor(img)
        Face.face_detection()
        d[face] = str(face_warnings[Face.facewarning])

        Eye = Facial_Monitor(img)
        Eye.eyegaze_detection()
        if Face.facewarning == 0:
            d[eye] = "NO EYES"
        else:
            d[eye] = str(eye_warnings[Eye.eyewarning])


def screen_func(d, screen):
    while True:
        Screen = Screen_Monitor()
        d[screen] = Screen.all_processes


def audio_func(d, audio):
    while True:
        r = sr.Recognizer()

        with sr.Microphone() as source:
            Audio = r.listen(source)
            try:
                d[audio] += str(r.recognize_google(Audio, language='en-us', show_all=False)+"\n")
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                d[audio] += str("Could not request results from Google Speech Recognition service; {0}".format(e))


def update_string_vars(d, *variables):
    for var in variables:
        value = d[str(var)]
        if value is not None:
            if var == screen_text:
                if type(value[-1]) is dict:
                    apps_text.set(str(value[:-1]))
                    tabs_text.set(str(value[-1]))
                else:
                    apps_text.set(str(value))
                    tabs_text.set("")
            else:
                var.set(str(value))
    window.after(40, update_string_vars, d, *variables)


def terminate_processes(*processes):
    for p in processes:
        p.terminate()


if sys.platform.startswith('win'):
    class _Popen(forking.Popen):
        def __init__(self, *args, **kw):
            if hasattr(sys, 'frozen'):
                os.putenv('_MEIPASS2', sys._MEIPASS)
            try:
                super(_Popen, self).__init__(*args, **kw)
            finally:
                if hasattr(sys, 'frozen'):
                    if hasattr(os, 'unsetenv'):
                        os.unsetenv('_MEIPASS2')
                    else:
                        os.putenv('_MEIPASS2', '')

    class Process(mp.Process):
        forking.Popen = _Popen


if __name__ == "__main__":
    mp.freeze_support()

    if getattr(sys, 'frozen', False):
        folder_path = os.path.dirname(sys.executable)
    else:
        folder_path = os.path.dirname(__file__)

    window = Tk()
    window.title("Exam Virtual Invigilator")
    icon = PhotoImage(file=os.path.join(folder_path, "Images/icon.png"))
    window.iconphoto(False, icon)
    window.geometry("1440x1024")
    window.resizable(False, False)
    window.configure(bg="#d1f4ff")
    window.bind('<Destroy>', lambda _: terminate_processes(facial_process, audio_process, screen_process))

    face_text = StringVar()
    eye_text = StringVar()
    audio_text = StringVar()
    screen_text = StringVar()
    apps_text = StringVar()
    tabs_text = StringVar()

    canvas = Canvas(
        window,
        bg="#d1f4ff",
        height=1024,
        width=1440,
        bd=0,
        highlightthickness=0,
        relief="ridge")
    canvas.place(x=0, y=0)

    logo_path = os.path.join(folder_path, "Images/logo.png")
    logo_pic = PhotoImage(file=logo_path)
    logo = canvas.create_image(
        360, 200,
        image=logo_pic)

    entry0_path = os.path.join(folder_path, "Images/img_textBox0.png")
    entry0_img = PhotoImage(file=entry0_path)
    entry0_bg = canvas.create_image(
        903.5, 332.5,
        image=entry0_img)

    entry0 = Label(
        textvariable=apps_text,
        bd=0,
        bg="#fff4f4",
        highlightthickness=0,
        font=("OpenSans-Regular", int(15.0)),
        wraplength=260,
        state=DISABLED)

    entry0.place(
        x=769.0, y=177,
        width=269.0,
        height=309)

    entry1_path = os.path.join(folder_path, "Images/img_textBox1.png")
    entry1_img = PhotoImage(file=entry1_path)
    entry1_bg = canvas.create_image(
        1251.5, 332.5,
        image=entry1_img)

    entry1 = Label(
        textvariable=tabs_text,
        bd=0,
        bg="#f4fcff",
        highlightthickness=0,
        font=("OpenSans-Regular", int(15.0)),
        wraplength=260,
        state=DISABLED)

    entry1.place(
        x=1117.0, y=177,
        width=269.0,
        height=309)

    entry2_path = os.path.join(folder_path, "Images/img_textBox2.png")
    entry2_img = PhotoImage(file=entry2_path)
    entry2_bg = canvas.create_image(
        1079.0, 810.5,
        image=entry2_img)

    entry2 = Label(
        textvariable=audio_text,
        bd=0,
        bg="#f2fff3",
        highlightthickness=0,
        font=("OpenSans-Regular", int(15.0)),
        wraplength=770,
        state=DISABLED)

    entry2.place(
        x=780.0, y=640,
        width=598.0,
        height=339)

    background_path = os.path.join(folder_path, "Images/background.png")
    background_img = PhotoImage(file=background_path)
    background = canvas.create_image(
        796.5, 512.0,
        image=background_img)

    face_label = Label(
        window,
        textvariable=face_text,
        fg="#000000",
        font=("OpenSans-Regular", int(48.0)))

    face_label.place(x=160, y=635)

    eye_label = Label(
        window,
        textvariable=eye_text,
        fg="#000000",
        font=("OpenSans-Regular", int(48.0)))

    eye_label.place(x=160, y=835)

    manager = mp.Manager()

    process_dict = manager.dict({str(face_text): None,
                                 str(eye_text): None,
                                 str(screen_text): None,
                                 str(audio_text): ""})

    facial_process = Process(
        target=facial_func, args=(process_dict, str(face_text), str(eye_text))
    )
    screen_process = Process(
        target=screen_func, args=(process_dict, str(screen_text))
    )
    audio_process = Process(
        target=audio_func, args=(process_dict, str(audio_text))
    )

    facial_process.start()
    screen_process.start()
    audio_process.start()

    update_string_vars(process_dict, face_text, eye_text, screen_text, audio_text)

    window.mainloop()
    os._exit(0)
