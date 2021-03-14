#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Nyan~Cat~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
from tkinter import *
import time, winsound

def Play(sound):
    winsound.PlaySound(sound,winsound.SND_ASYNC)
def StopAll():
    winsound.PlaySound(None,winsound.SND_ASYNC)

window = Tk()
window.title("Nyan Cat")
height = window.winfo_screenheight()
width = window.winfo_screenwidth()
window.overrideredirect(1)
#window.wm_attributes('-fullscreen','true')
if(width > height):
    size = width
else:
    size = height
canvas = Canvas(bg="black",height=height,width=width)
canvas.pack()

turn = 0
Play("Nyan.wav")
playSound = "true"
startTime = time.time()

while(True):
    canvas.create_arc(-0.5*width,-0.5*height,1.5*width,1.5*height,style="pieslice",start=turn,fill="purple",outline="",extent=60)
    canvas.create_arc(-0.5*width,-0.5*height,1.5*width,1.5*height,style="pieslice",start=turn+60,fill="red",outline="",extent=60)
    canvas.create_arc(-0.5*width,-0.5*height,1.5*width,1.5*height,style="pieslice",start=turn+120,fill="orange",outline="",extent=60)
    canvas.create_arc(-0.5*width,-0.5*height,1.5*width,1.5*height,style="pieslice",start=turn+180,fill="yellow",outline="",extent=60)
    canvas.create_arc(-0.5*width,-0.5*height,1.5*width,1.5*height,style="pieslice",start=turn+240,fill="green",outline="",extent=60)
    canvas.create_arc(-0.5*width,-0.5*height,1.5*width,1.5*height,style="pieslice",start=turn+300,fill="blue",outline="",extent=60)
    if turn == 360:
        turn = 0
    else:
        turn = turn + 5

    def StopMusic(key):
        if (playSound == "true"):
            StopAll()
            playSound = "false"
        elif (playSound == "false"):
            Play("Nyan.wav")
    window.bind("<s>",StopMusic)
    
    NyanImage = PhotoImage(file="Picture1.gif")
    canvas.create_image(width/2,height/2,image=NyanImage)

    window.update()
    canvas.delete(ALL)

    if (playSound == "true"):
        if(round(time.time()) > (startTime + 216)):
            Play("Nyan.wav")
            startTime = time.time()

window.mainloop()
