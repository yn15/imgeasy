import tkinter as tk
from tkinter import filedialog, messagebox
import os
import ocr

window = tk.Tk()
entry = tk.Entry(window)

window.title("동주의 이미지 텍스트 판별기")

window.resizable(False, False);

window.file = None
window.file_s = None


def file_find():
    window.file = filedialog.askopenfile(
        initialdir=f'{os.getcwd()}',
        title='파일 선택',
        filetypes=(('xls files', '*.xls'), ('all files', '*.*'))
    )

    if window.file is None:
        return

    label2.configure(text=window.file.name)

    window.file.close()


def file_save():
    window.file_s = filedialog.asksaveasfile(
        mode='w',
        defaultextension=".xls"
    )

    if window.file_s is None:
        return

    label4.configure(text=window.file_s.name)

    window.file_s.close()


def run_ocr():
    run_type = None
    if radVar.get() == 1:
        run_type = False
    elif radVar.get() == 2:
        run_type = True

    if window.file is None or \
            window.file_s is None or \
            run_type is None or entry.get() == '':
        tk.messagebox.showwarning("동주의 경고", "내용 다 채워라")
        return

    label6.grid(row=7, column=0, padx=30, sticky='w')
    label7.grid(row=7, column=1, padx=30, pady=30, sticky='')

    button1.configure(state="disabled")
    button2.configure(state="disabled")
    button3.configure(state="disabled")
    entry.configure(state="disabled")
    radio1.configure(state="disabled")
    radio2.configure(state="disabled")

    ocr.run(window.file.name, entry.get(), window.file_s.name, run_type, label7)
    # ocr.run(window.file.name, entry.get(), 'save', run_type, label7)

label1 = tk.Label(window, text='파일 경로(S) : ')
label1.grid(row=1, column=0, padx=30, pady=(30, 0), sticky='w')

label2 = tk.Label(window, text='')
label2.grid(row=1, column=1, padx=(0, 30), pady=(30, 0))

button1 = tk.Button(window, text='파일 찾기', command=file_find)
button1.grid(row=1, column=2, padx=(0, 30), pady=(30, 0), sticky='e')

label3 = tk.Label(window, text='파일 저장(S) : ')
label3.grid(row=2, column=0, padx=30, pady=30, sticky='w')

label4 = tk.Label(window, text='')
label4.grid(row=2, column=1, padx=(0, 30), pady=30)

button2 = tk.Button(window, text='파일 저장', command=file_save)
button2.grid(row=2, column=2, padx=(0, 30), pady=30, sticky='e')

label5 = tk.Label(window, text='분석 열 이름(S) : ')
label5.grid(row=3, column=0, padx=30, pady=(0, 30), sticky='w')

entry.grid(row=3, column=1, padx=(0, 30), pady=(0, 30), columnspan=2, sticky='w')

label6 = tk.Label(window, text='CPU / GPU : ')
label6.grid(row=4, column=0, padx=30, sticky='w')

radVar = tk.IntVar()

radio1 = tk.Radiobutton(window, text='CPU', variable=radVar, value=1)
radio1.grid(row=4, column=1, padx=(0, 30), sticky='w')

radio2 = tk.Radiobutton(window, text='GPU', variable=radVar, value=2)
radio2.grid(row=5, column=1, padx=(0, 30), pady=(0, 30), sticky='w')

button3 = tk.Button(window, text='실행', command=run_ocr)
button3.grid(row=6, column=0, columnspan=3, padx=30, pady=(0, 30), sticky='w,n,e,s')

label6 = tk.Label(window, text='진행도 : ')

label7 = tk.Label(window, text='')

window.mainloop()
