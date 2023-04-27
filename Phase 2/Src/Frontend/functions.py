from tkinter import *
from tkinter import filedialog
import subprocess

def raise_frame(frame):
    frame.tkraise()

def reset_txt():
    reg=open('register.txt', "w")
    for i in range(32):
        reg.write(f"0x{hex(i)} 0x0\n")
    reg.close()
    mem=open('memory.txt', "w")
    for i in range(0,1024,4):
        mem.write(f"0x{hex(i)} 0x0\n")
    mem.close()


def nxt_func(nxt, line, text, registers, mem):
    idx=float(line[0])
    idx2=float(line[1])
    print(idx, idx2)
    if idx2!=0.0:
        text.tag_remove("here", idx2, idx2+1)
        text.tag_add("there", idx2, idx2+1)
        text.tag_config("there", background="blue")
        
    text.tag_add("here", idx, idx+1)
    text.tag_remove("there", idx, idx+1)
    text.tag_config("here", background="yellow")
    
    args=text.get(idx,idx+1).split(' ')
    print(args)
    # terminal=subprocess.run(['gcc', 'myRISCVdebug.c', '-o', 'debug', '&&', 'debug', args[0], args[1]],stdout=subprocess.PIPE, shell=True)
    terminal=subprocess.run(['debug', args[0], args[1]],stdout=subprocess.PIPE, shell=True)

    pc=int(terminal.stdout.decode(), 16)
    print(pc)
    if(pc!=(0xffffffff)):
        line[1]=line[0]
        line[0]=pc/4+1
    reg=open("register.txt", "r")
    regVals=reg.read()
    reg.close()
    registers.insert(1.0, regVals)
    memory=open("memory.txt", "r")
    memVals=memory.read()
    memory.close()
    mem.insert(1.0, memVals)
    

def run_func(content,args):
    reset_txt()
    lst=['g++', '../Backend/main.cpp', '-o', 'run', '&&', 'run']
    lst.append(args[0])
    if(args[1].get()==1):
        lst.append('-p')
    if(args[2].get()==1):
        lst.append('-f')
    if(args[3].get()==1 or args[4].get()==1):
        lst.append('-v')
        if(args[3].get()==1):
            lst.append('p')
        if(args[4].get()==1):
            lst.append('r')
    print(lst)
    subprocess.run(lst, shell=True)
    runwindow=Toplevel(bg="#262626")
    runwindow.geometry('900x750')

    buttonframe = Frame(runwindow,width=100)

    runwindow.title(' RUN')
    frame = Frame(runwindow,padx=10,pady=10,relief=SUNKEN,bg="#262626")
    frame.grid(row=0,column=0,rowspan=8,padx=20,pady=10)
    Code = Label(frame,bg="#262626",fg="white",font=("Comic Sans MS",14),anchor="center",text="CODE").pack()

    # Create a scrollbar for the frame
    scrollbar = Scrollbar(frame,bg="#262626")

    # Create a canvas within the frame and attach the scrollbar to it
    canvas = Canvas(frame, yscrollcommand=scrollbar.set,bg="#262626")
    canvas.pack(side=LEFT,anchor="center", fill=NONE, expand=True)

    # Create a frame within the canvas to hold the text
    text_frame = Frame(canvas,bg="#262626",pady=10,padx=10)
    canvas.create_window((0,0), window=text_frame, anchor='center')

    # Add each element of the array to the text frame

    text = ''.join(content)
    # label = Label(scrollbar,text=text,font=("Comic Sans MS",12),fg="white",pady=20,bg="#262626")
    label = Label(text_frame,text=text,anchor="e",padx=30,font=("Comic Sans MS",13),border = 10,fg="white",bg="#262626")
    label.pack(expand=NO)
    scrollbar.pack(side=RIGHT, fill=Y)
    scrollbar.config(command=canvas.yview)
    

    # Update the canvas and scroll region
    text_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


    registers = Frame(runwindow,width=30,height=300,bg="#262626")
    # Create a canvas widget
    text_reg = Label(registers,text = "REGISTERS" ,justify="center",anchor="center",fg="white",bg='#262626',font=("Comic Sans MS",12)).pack(anchor="center",expand=TRUE,fill="both")
    canvas = Canvas(registers, background="#262626")
    canvas.pack(side="left", fill="both", expand=True)

    # Add a scrollbar to the canvas
    scrollbar = Scrollbar(registers, orient="vertical", command=canvas.yview,bg="#202020")
    scrollbar.pack(side="right", fill="y")

    # Configure the canvas to work with the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame to hold the text
    frame = Frame(canvas, background="#282828",bg="#262626")
    canvas.create_window((0, 0), window=frame, anchor="center")

    # Open the text file and add its contents to the frame
    with open("register.txt") as f:
        text = f.read()
        label = Label(frame, text=text, justify="left", wraplength=500, padx=30,pady=10,fg='white',bg="#262626", font=("Comic Sans MS", 12),anchor="center")
        label.pack()

    # Resize the canvas scrollable area to match the frame's size
    frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

    registers.grid(column=2,row=0,rowspan=8)
    
    
    clock_frame = Frame(runwindow,width = 30,height=5,bg="white",relief=SUNKEN)
    clock_frame.grid(row=14,column=0)
    text2 = Label(clock_frame,relief=RAISED,font=("Comic Sans MS", 13),padx=30,bg="#262626",fg="white",border =3,pady=10,text="Clock ",anchor="center").pack()
    with open("clock.txt") as f:
        text = f.read()
        label = Label(clock_frame, text=text, wraplength=500,fg='#262626',bg="white",border=3, font=("Comic Sans MS", 12),anchor="center")
        label.pack()

    mem = Frame(runwindow,width=50,height=200,bg="#262626")
    mem.grid(row=10,column=2,rowspan=8)
    canvas = Canvas(mem, borderwidth=0, background="#262626")
    text_mem = Label(mem,text= "MEMORY" ,anchor="center",font=("Comic Sans MS", 12),bg="#262626",fg="white").pack(side="top")
    canvas.pack(side="left", fill="both", expand=True)

    # Add a scrollbar to the canvas
    scrollbar = Scrollbar(mem, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configure the canvas to work with the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame to hold the text
    frame = Frame(canvas, background="#202020")
    canvas.create_window((0, 0), window=frame, anchor="center")

    # Open the text file and add its contents to the frame
    with open("memory.txt") as f:
        text = f.read()
        label = Label(frame, text=text, justify="left", wraplength=500,padx= 30, bg="#262626", font=("Comic Sans MS", 12),fg="white")
        label.pack()

    # Resize the canvas scrollable area to match the frame's size
    frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))



    ####   LINES   ######

    ## Bottom of code
    line_frame2=Frame(runwindow,bg="#282828") ## Right of code
    textline=Label(line_frame2,text="hello",bg="#282828",fg="white",font=("Comic Sans MS",16))
    # textline.pack(anchor="center",side="left")
    textline=Label(line_frame2,text="_____________________________",anchor="center",bg="#282828",fg="white",font=("Comic Sans MS",16)).pack()
    line_frame2.grid(column=0,row=8,columnspan=1)
    
    ## Bottom of registers
    line_frame3=Frame(runwindow,bg="#282828") ## Right of code
    textline=Label(line_frame3,text="hello",bg="#282828",fg="white",font=("Comic Sans MS",16))
    # textline.pack(anchor="center",side="left")
    textline=Label(line_frame3,text="   __________________________",anchor="center",bg="#282828",fg="white",font=("Comic Sans MS",16)).pack()
    line_frame3.grid(column=2,row=8,columnspan=1)


def debug_func(content, root,location,contentmain,locationmain,args):
    reset_txt()
    subprocess.run(['g++', '../Backend/debug.cpp', '-o', 'debug'], shell=True)
    line=[1, 0]

    debugwindow=Toplevel(bg='#282828')
    debugwindow.attributes("-fullscreen", True)

    debugwindow.title('Debugging')

    ##########   REGISTERS    #########

    regi = Frame(debugwindow,bg="#282828",width=70)
    regi_text = Label(regi,bg="#282828",anchor="center",text = "REGISTERS", fg="white", font=("Comic Sans MS",14))
    regi_text.pack(side="top",fill="both",)
    canvas = Canvas(regi, background="#181818")
    canvas.pack(side="left", fill="both", expand=True,padx=10)

    # Add a scrollbar to the canvas
    scrollbar = Scrollbar(regi, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configure the canvas to work with the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame to hold the text
    frame = Frame(canvas, background="#181818",height=800,relief=SUNKEN,width=70)
    canvas.create_window((0, 0), window=frame, anchor="center",)
    # regi_text = Label(regi,text = "regiORY",bg="#282828", fg="white", font=("Comic Sans MS",12),anchor="center",pady=3).pack(side="top")

    # Open the text file and add its contents to the frame
    with open("register.txt") as f:
        text = f.read()
        label = Label(frame, text=text, justify="left", wraplength=300, bg="#181818",padx=20, fg="white", font=("Comic Sans MS",12))
        label.pack()

    # Resize the canvas scrollable area to match the frame's size
    frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

    regi.grid(row=6,column=3,columnspan=1,rowspan=4)

    #######    Memory Grid       #######

    # mem.grid(row=1,column=3,columnspan=1,rowspan=4)
    mem = Frame(debugwindow,bg="#282828",width=70)
    mem_text = Label(mem,bg="#282828",anchor="center",text = "MEMORY", fg="white", font=("Comic Sans MS",14))
    mem_text.pack(side="top",fill="both",)
    canvas = Canvas(mem, background="#181818")
    canvas.pack(side="left", fill="both", expand=True,padx=10)

    # Add a scrollbar to the canvas
    scrollbar = Scrollbar(mem, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configure the canvas to work with the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame to hold the text
    frame = Frame(canvas, background="#181818",height=800,relief=SUNKEN,width=70)
    canvas.create_window((0, 0), window=frame, anchor="center",)
    # mem_text = Label(mem,text = "MEMORY",bg="#282828", fg="white", font=("Comic Sans MS",12),anchor="center",pady=3).pack(side="top")

    # Open the text file and add its contents to the frame
    with open("memory.txt") as f:
        text = f.read()
        label = Label(frame, text=text, justify="left", wraplength=300, bg="#181818",padx=20, fg="white", font=("Comic Sans MS",12))
        label.pack()

    # Resize the canvas scrollable area to match the frame's size
    frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

    mem.grid(row=1,column=3,columnspan=1,rowspan=4)


    #######    Stages Grid       #######

    stage = Frame(debugwindow,bg="#282828",width=70)
    stage_txt = Label(stage,text="PILELINE STAGES",bg="#282828",anchor="center", fg="white", font=("Comic Sans MS",14)).pack(side="top",fill="both")

    with open('stages.txt', 'r') as f:
    # Read the entire file as a string and split it into a list of values
        values = f.read().split()
        
        # Convert the list of values to a NumPy array of integers
        import numpy as np
        A = np.array(values, dtype=int)


    count = A.shape[0]/6
    name = Frame(stage,padx=20,bg="#282828",border=3)
    name.pack(side=TOP, fill=BOTH, expand=True)

    colors = ['red', 'green', 'blue', 'orange', 'purple', 'pink']
    name1 = Label(name,text="C",padx=18,pady=4, bg=colors[0],font=("Comic Sans MS",14)).grid(row=0, column=0, sticky='nsew')
    name2 = Label(name,text="F",padx=18,pady=4, bg=colors[1],font=("Comic Sans MS",12)).grid(row=0, column=1, sticky='nsew')
    name3 = Label(name,text="D",padx=18,pady=4, bg=colors[2],font=("Comic Sans MS",12)).grid(row=0, column=2, sticky='nsew')
    name4 = Label(name,text="E",padx=18,pady=4, bg=colors[3],font=("Comic Sans MS",12)).grid(row=0, column=3, sticky='nsew')
    name5 = Label(name,text="M",padx=18,pady=4, bg=colors[4],font=("Comic Sans MS",12)).grid(row=0, column=4, sticky='nsew')
    name6 = Label(name,text="W",padx=18,pady=4, bg=colors[5],font=("Comic Sans MS",12)).grid(row=0, column=5, sticky='nsew')
        

    class GridFrame(Frame):
        def __init__(self, master, values):
            super().__init__(master)
            
            # Create a Canvas widget to contain the grid
            canvas = Canvas(self,bg="#181818",height=300)
            canvas.pack(side=LEFT, fill=BOTH, expand=True)

            # Create a Frame widget to hold the grid elements
            self.grid_frame = Frame(canvas,padx=20,bg="#181818")
            self.grid_frame.pack(side=TOP, fill=BOTH, expand=True)

            # Attach the Frame to the Canvas
            canvas.create_window((0,0), window=self.grid_frame, anchor=NW)

            # Configure the scrollbar to control the Canvas
            self.scrollbar = Scrollbar(self, orient=VERTICAL, command=canvas.yview)
            self.scrollbar.pack(side=RIGHT, fill=Y)
            canvas.configure(yscrollcommand=self.scrollbar.set,bg="#181818")

            # Populate the grid with the values
            num_rows = int(count)
            num_cols = 6

            for r in range(num_rows):
                for c in range(num_cols):
                    value = values[r*num_cols+c]
                    label = Label(self.grid_frame, text=value,padx=18,pady=2, bg=colors[c],font=("Comic Sans MS",12))
                    label.grid(row=r+1, column=c, sticky='nsew')

            # Configure the grid to stretch with the window
            for r in range(num_rows):
                self.grid_rowconfigure(r, weight=1)
            for c in range(num_cols):
                self.grid_columnconfigure(c, weight=1)

            # Bind the Canvas to mouse events to enable scrolling
            def on_canvas_mousewheel(event):
                canvas.yview_scroll(-1*int(event.delta/120), "units")
            canvas.bind_all("<MouseWheel>", on_canvas_mousewheel)
            
    # Read the values from the input file
    values = []
    with open('stages.txt', 'r') as f:
        for line in f:
            values.extend([int(x) for x in line.strip().split()])


  

    # Create the GridFrame and pack it into the root window
    grid_frame = GridFrame(stage, values)
    grid_frame.pack(side=TOP, fill=BOTH, expand=True)

    stage.grid(row=1,column=5,columnspan=1,rowspan=5)


    ##########      Inserting code      #############

    codeframe = Frame(debugwindow,width=70,height=190,padx=20,bg="#282828",border=3)
    code_head=Label(codeframe,text="CODE",anchor="center",fg="white", font=("Comic Sans MS",14),bg="#282828").pack(side="top")
    code=Text(codeframe, height=20, width=25,padx=20, pady=5,bg="#181818",border=10,fg="white", font=("Comic Sans MS",12))
    code.insert(1.0, content)
    code.pack()
    codeframe.grid(row=1,column=0,columnspan=2,rowspan=7)

    #OUT TEXT CLOCK, Hazard
    text_frame=Frame(debugwindow,width=70,padx=20,pady=2,bg="#282828")
    with open("hazard.txt") as f:
        text = f.read()
        label = Label(text_frame, text=text, justify="center", wraplength=300,width=20, bg="white",fg="black", font=("Comic Sans MS",15))
        label.pack()
    text_frame.grid(row=7,column=5,columnspan=2)

    #Lines
    line_frame1=Frame(debugwindow,bg="#282828") ## Right of code
    textline=Label(line_frame1,text="hello",bg="#282828",fg="white",padx=10,font=("Comic Sans MS",16))
    # textline.pack(anchor="center",side="left")
    textline=Label(line_frame1,text="|  \n|  \n|  \n|  \n|  \n|  \n|  \n|  \n|  \n|  \n|  \n|  \n|  \n|  \n|  \n|  \n|  \n|  \n|  \n|  \n|  \n|  \n|  \n",anchor="center",bg="#282828",fg="white",font=("Comic Sans MS",16)).pack()
    line_frame1.grid(column=2,row=1,rowspan=20)

    ## Bottom of code
    line_frame2=Frame(debugwindow,bg="#282828") ## Right of code
    textline=Label(line_frame2,text="hello",bg="#282828",fg="white",font=("Comic Sans MS",16))
    # textline.pack(anchor="center",side="left")
    textline=Label(line_frame2,text="______________________",anchor="center",bg="#282828",fg="white",font=("Comic Sans MS",16)).pack()
    line_frame2.grid(column=0,row=8,columnspan=2)
    
    ## Bottom of registers
    line_frame3=Frame(debugwindow,bg="#282828") ## Right of code
    textline=Label(line_frame3,text="hello",bg="#282828",fg="white",font=("Comic Sans MS",16))
    # textline.pack(anchor="center",side="left")
    textline=Label(line_frame3,text="____________________________            ",anchor="center",bg="#282828",fg="white",font=("Comic Sans MS",16)).pack()
    line_frame3.grid(column=3,row=5,columnspan=2)
    
    ## Bottom Pipeline
    line_frame3=Frame(debugwindow,bg="#282828") ## Right of code
    textline=Label(line_frame3,text="hello",bg="#282828",fg="white",font=("Comic Sans MS",16))
    # textline.pack(anchor="center",side="left")
    textline=Label(line_frame3,text="____________________________            ",anchor="center",bg="#282828",fg="white",font=("Comic Sans MS",16)).pack()
    line_frame3.grid(column=5,row=6,columnspan=2)

    ##########     Left of memory   ##########

    line_frame4=Frame(debugwindow,bg="#282828") ## Right of code
    textline=Label(line_frame4,text="hello",bg="#282828",fg="white",padx=10,font=("Comic Sans MS",16))
    # textline.pack(anchor="center",side="left")
    textline=Label(line_frame4,text="     |     \n     |     \n     |     \n     |     \n     |     \n     |     \n     |     \n     |     \n     |     \n     |     \n     |     \n     |     \n     |     \n     |     \n     |     \n     |     \n     |     \n     |     \n     |     \n     |     \n     |     \n     |     \n     |     \n",anchor="center",bg="#282828",fg="white",font=("Comic Sans MS",16)).pack()
    line_frame4.grid(column=4,row=1,rowspan=20)


    # Button Frame ###   Creating buttons
    buttonframe = Frame(debugwindow,width=70,bg="#282828")
    btn_run=Button(buttonframe, text="Run",font=("Comic Sans MS",12), padx=10,bg='#181818',relief=SUNKEN,fg="white", command=lambda: run_func_debug(args,content,debugwindow))
    btn_run.pack(anchor="center",padx=5,side="left",pady=20)
    btn_nxt=Button(buttonframe, text="Step",width=8, padx=10,font=("Comic Sans MS",12),fg="white",bg="#181818", command=lambda: nxt_func(btn_nxt, line, code, regi, mem))
    btn_nxt.pack(anchor="center",padx=5,side="left",pady=20)
    btn_reset=Button(buttonframe, text="Reset",width=8, padx=10,font=("Comic Sans MS",12),fg="white",bg="#181818", command=lambda: reset_func(debugwindow,root,contentmain,locationmain))
    btn_reset.pack(anchor="center",padx=5,side="left",pady=20)
    buttonframe.grid(row=0,column=0,columnspan=2)

    print('debugging')


def run_func_debug(args,content,debugwindow):
    debugwindow.after(100,debugwindow.destroy)
    run_func(content, args)

#ef debug_func(content, root,location,contentmain,locationmain):
def reset_func(debug,root,contentmain,locationmain):
    debug.after(100,debug.destroy)
    debug_func(contentmain, root,locationmain,contentmain,locationmain)   


def func_upload(root, f2):
    raise_frame(root)
    #Opens the file
    root.filename=filedialog.askopenfilename(initialdir="c:/Desktop/", title="select a dumpfile (.mc)", filetypes=[("dump files", "*.mc")])
    location=root.filename

    #Loads the file
    f=open(location, "r")
    content=f.read()
    f.close()


    #Making the Frame to hold
    above=Frame(root,bg='#282828')
    above.grid(column=0,row=100,columnspan=2,rowspan=1000)
    below=Frame(root,bg='#282828',pady=7)
    below.grid(column=0,row=0,columnspan=2)
    below.configure()

    # Adding text
    code=Text(below, height=10, width=18, pady=20,font=("Comic Sans MS",10))

    #check box

    var_pileline = IntVar()
    var_forwarding = IntVar()
    var_pp = IntVar()
    var_pr = IntVar()
    box = Frame(below,bg="#282828",pady=10)

    c_pipeline = Checkbutton(box,width=16,text = "Pipeline",font=("Comic Sans MS",9),variable=var_pileline,onvalue=1,offvalue=0)
    c_pipeline.pack()
    c_forwarding = Checkbutton(box,width=16,text = "Forwarding",font=("Comic Sans MS",9),variable=var_forwarding,onvalue=1,offvalue=0)
    c_forwarding.pack()
    c_pp = Checkbutton(box,width=16,text = "Print Pipelines",font=("Comic Sans MS",9),variable=var_pp,onvalue=1,offvalue=0)
    c_pp.pack()
    c_pr = Checkbutton(box,width=16,text = "Print Registers",font=("Comic Sans MS",9),variable=var_pr,onvalue=1,offvalue=0)
    c_pr.pack()


    box.grid(row=1,column=0,columnspan=2,rowspan=2)

    args = [location,var_pileline, var_forwarding, var_pp, var_pr]

    #Making Button
    btn_run=Button(below, text="Run",anchor="center",font=("Comic Sans MS",12), padx=15,border=3, bg='#151515',fg="white", command=lambda: run_func(content,args))
    temptext = Label(below,text="CODE",fg="white",anchor="center",bg='#282828',font=("Comic Sans MS",14)).grid(row=3,column=0,columnspan=2)
    texttemp = Label(below,text=" \n\n\n\n\n\n",bg='#282828').grid(row=11,rowspan=20,column=0)

    #Making Button
    btn_debug=Button(below, text="Debug",anchor="center",font=("Comic Sans MS",12),border=3,bg='#151515',fg="white", padx=15, command=lambda: debug_func(content,f2,location,content,location, args))
    code.insert(1.0, content)
    code.grid(row=4,column=0,columnspan=2)
    btn_run.grid(row=0, column=0)
    btn_debug.grid(row=0, column=1)
