from tkinter import *
from tkinter.filedialog import askopenfilename
import csv
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation
from matplotlib import pyplot as plt
import tkinter
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import numpy as np


def confirmExit():
    if tkinter.messagebox.askokcancel("Notice", "Are you sure you want to exit?"):
        window.destroy()
        quit()


def trigFileSelect():
    global trigFile
    trigFile = askopenfilename()
    if str(trigFile) == "":
        trigFile = "Trigger Data File Path"
    trigLabel.config(text=trigFile)
    if posLabel.cget("text") != "Position Data File Path" and trigLabel.cget("text") != "Trigger Data File Path":
        prcssButton.config(cursor="hand2", state="normal", bg="#fff")
    else:
        prcssButton.config(cursor="arrow", state="disabled", bg="#ccc")


def posFileSelect():
    global posFile
    posFile = askopenfilename()
    if str(posFile) == "":
        posFile = "Position Data File Path"
    posLabel.config(text=posFile)
    if posLabel.cget("text") != "Position Data File Path" and trigLabel.cget("text") != "Trigger Data File Path":
        prcssButton.config(cursor="hand2", state="normal", bg="#fff")
    else:
        prcssButton.config(cursor="arrow", state="disabled", bg="#ccc")


def quitAni():
    canvas.get_tk_widget().pack_forget()
    canvas.figure.clear()
    ani.pause()
    framesLabel.config(text="Frame # / Total Frames")
    prcssButton.config(cursor="hand2", state="normal", bg="#fff")
    trigButton.config(cursor="hand2", state="normal", bg="#fff")
    posButton.config(cursor="hand2", state="normal", bg="#fff")
    quitButton.config(cursor="arrow", state="disabled", bg="#ccc")
    saveButton.config(cursor="arrow", state="disabled", bg="#ccc")


def saveAniWindow():
    saveWindow = Tk()
    saveWindow.resizable(0, 0)
    saveWindow.title("Saving GUI")
    saveFrame = Frame(saveWindow, width=312, height=272.5, bg="grey")
    saveFrame.pack()
    saveTitleLabel = Label(saveFrame, text="Enter Filename to Save As (.gif) : ")
    saveTitleLabel.grid(row=0, column=0)
    textBox = Entry(saveFrame)
    textBox.grid(row=0, column=1)
    confirmButton = Button(saveWindow, text="Confirm and Save", width=20, height=3, bd=0, bg="#fff",
                           cursor="hand2", command=lambda: saveAni(textBox.get(), saveWindow))
    confirmButton.pack()


def saveAni(fileName, saveWindow):
    ani.save(fileName + '.gif')
    saveWindow.destroy()


def process():
    global ani
    global trigFile
    global posFile
    global canvas
    if prcssButton["state"] == "normal":
        fig = plt.figure()  # defines the figure as a plot
        ax = p3.Axes3D(fig, auto_add_to_figure=False)  # defines 3D axes for the figure
        ax.set_xlabel('$X$')
        ax.set_ylabel('$Y$')
        ax.set_zlabel('$Z$')
        pltTitle = str(posFile).split("/")
        pltTitle = pltTitle[len(pltTitle)-1]
        ax.text2D(0.05, 0.95, pltTitle, transform=ax.transAxes)
        fig.add_axes(ax)  # adds the 3D axes to the figure
        canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        with open(trigFile, encoding='utf-8-sig') as csv_file:
            trigs = list(csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC))  # csv data as list
            trigs = sorted(trigs,key=lambda x: x[1])
            trig_indexes = []
            for row in trigs:
                if row[1] > 1 and row[0] not in trig_indexes and row[0]+1 not in trig_indexes and row[0]-1 not in trig_indexes:
                    trig_indexes.append(row[0])
            trig_indexes = sorted(trig_indexes)

        with open(posFile, encoding='utf-8-sig') as csv_file:
            coords = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)  # variable coords is CSV data
            x_coords = []  # a 2D array holding the x values of every point in 1D arrays for every frame
            y_coords = []  # a 2D array holding the y values of every point in 1D arrays for every frame
            z_coords = []  # a 2D array holding the z values of every point in 1D arrays for every frame
            rowNum = 0  # a counter for the row being the frame number in the coords CSV data
            for row in coords:
                rowNum += 1  # add one to the counter, showing we are now analyzing the next row
                if rowNum in trig_indexes:  # checks if the current frame being analyzed is in the trig_indexes array
                    coordCount = 1  # a counter for each coordinate in each row of the coords variable
                    x_row = []  # a 1D array holding all of the x values in this row from the CSV data
                    y_row = []  # a 1D array holding all of the y values in this row from the CSV data
                    z_row = []  # a 1D array holding all of the z values in this row from the CSV data
                    for num in row:
                        if coordCount % 3 == 1:  # checks if the current number is a x coordinate
                            x_row.append(num)  # adds the coordinate to the x_row array
                        elif coordCount % 3 == 2:  # checks if the current number is a y coordinate
                            y_row.append(num)  # adds the coordinate to the y_row array
                        else:  # anything else is a z coordinate
                            z_row.append(num)  # adds the coordinate to the z_row array
                        coordCount += 1  # add one to the counter, showing we are now analyzing the next number in the row
                    x_coords.append(x_row)  # adds the x coordinates from this frame to the 2D array
                    y_coords.append(y_row)  # adds the y coordinates from this frame to the 2D array
                    z_coords.append(z_row)  # adds the z coordinates from this frame to the 2D array

        global frameNum  # the number of the current frame being displayed

        frameNum = 1  # sets the first frame to 1
        x = np.array(x_coords[frameNum - 1])  # gets the x coordinates for the first frame
        y = np.array(y_coords[frameNum - 1])  # gets the y coordinates for the first frame
        z = np.array(z_coords[frameNum - 1])  # gets the z coordinates for the first frame

        points, = ax.plot(x, y, z, '*')  # plots the points in 3D space
        lines, = ax.plot(x, y, z, 'none')  # plots the lines connecting the points in 3D space

        fingersColor = 'r-'  # sets the line color of the individual fingers
        thumb, = ax.plot(x[0:4], y[0:4], z[0:4], fingersColor)  # plots the lines for the thumb
        pointer, = ax.plot(x[4:8], y[4:8], z[4:8], fingersColor)  # plots the lines for the pointer finger
        middle, = ax.plot(x[8:12], y[8:12], z[8:12], fingersColor)  # plots the lines for the middle finger
        ring, = ax.plot(x[12:16], y[12:16], z[12:16], fingersColor)  # plots the lines for the ring finger
        pinky, = ax.plot(x[16:20], y[16:20], z[16:20], fingersColor)  # plots the lines for the pinky finger
        fingers = [thumb, pointer, middle, ring, pinky]  # an array of the lines of the different fingers

        def update_plot(num, x, y, z, points, lines, fingers):  # a method made to update the plot
            global frameNum  # redeclaration of the frameNum so it can be used locally
            skipNum = 1  # the number in which we look at frames (if 2, we plot every 2 frames)

            frameNum += skipNum  # adds the number in which we are plotting frames to the current frame number

            if frameNum + (skipNum-1) > len(trig_indexes):  # checks if we are out of bounds of the frames
                frameNum = 1  # resets the frame number so we don't go out of bounds and can repeat

            framesLabel.config(text="Current frame: " + str(frameNum) + " out of " + str(
                len(trig_indexes)))  # prints the current frame out of the total
            new_x = np.array(x_coords[frameNum - 1])  # sets the new x coordinates to those from the current frame
            new_y = np.array(y_coords[frameNum - 1])  # sets the new y coordinates to those from the current frame
            new_z = np.array(z_coords[frameNum - 1])  # sets the new z coordinates to those from the current frame

            points.set_data(new_x, new_y)  # sets the new x and y coordinates for all the points with the new frame
            points.set_3d_properties(new_z, 'z')  # sets the new z coordinates for all the points with the new frame
            lines.set_data(new_x, new_y)  # sets the new x and y coordinates for all the lines with the new frame
            lines.set_3d_properties(new_z, 'z')  # sets the new z coordinates for all the points with the new frame

            pointCount = 0  # a counter representing the number given to each of the points to look at the fingers individually
            for finger in fingers:
                # sets the new x and y coordinates for all the finger lines with the new frame
                finger.set_data(new_x[pointCount:pointCount + 4], new_y[pointCount:pointCount + 4])
                # sets the new z coordinates for all the finger lines with the new frame
                finger.set_3d_properties(new_z[pointCount:pointCount + 4], 'z')
                pointCount += 4  # adds to get to the points of the next finger

        ani = animation.FuncAnimation(fig, update_plot, interval=30, frames=len(trig_indexes), repeat=True,
                                      fargs=(
                                          x, y, z, points, lines,
                                          fingers))  # animates the figure with all trigger frames

        canvas.draw()
        prcssButton.config(cursor="arrow", state="disabled", bg="#ccc")
        trigButton.config(cursor="arrow", state="disabled", bg="#ccc")
        posButton.config(cursor="arrow", state="disabled", bg="#ccc")
        quitButton.config(cursor="hand2", state="normal", bg="#fff")
        saveButton.config(cursor="hand2", state="normal", bg="#fff")


window = Tk()
window.resizable(0, 0)
window.title("Button GUI")
titleLabel = Label(window, text="Welcome to Jack's animation GUI")
titleLabel.pack()

btnsFrame = Frame(window, width=312, height=272.5, bg="grey")
btnsFrame.pack()

trigLabel = Label(btnsFrame, text="Trigger Date File Path")
trigLabel.grid(row=0, column=1, padx=1, pady=1)
trigButton = Button(btnsFrame, text="Select Trigger Data File", width=20, height=3, bd=0, bg="#fff",
                    cursor="hand2", command=lambda: trigFileSelect())
trigButton.grid(row=0, column=0, padx=1, pady=1)
posLabel = Label(btnsFrame, text="Position Data File Path")
posLabel.grid(row=1, column=1, padx=1, pady=1)
posButton = Button(btnsFrame, text="Select Position Data File", width=20, height=3, bd=0, bg="#fff",
                   cursor="hand2", command=lambda: posFileSelect())
posButton.grid(row=1, column=0, padx=1, pady=1)
prcssButton = Button(btnsFrame, text="Process Animation", width=20, height=3, bd=0, bg="#ccc",
                     cursor="arrow", command=lambda: process(), state="disabled")
prcssButton.grid(row=2, column=0, padx=1, pady=1)
framesLabel = Label(btnsFrame, text="Frame # / Total Frames")
framesLabel.grid(row=2, column=1, padx=1, pady=1)
quitButton = Button(btnsFrame, text="Stop Animation", width=20, height=3, bd=0, bg="#ccc",
                    cursor="arrow", command=lambda: quitAni(), state="disabled")
quitButton.grid(row=3, column=0, padx=1, pady=1)
saveButton = Button(btnsFrame, text="Save Animation", width=20, height=3, bd=0, bg="#ccc",
                    cursor="arrow", command=lambda: saveAniWindow(), state="disabled")
saveButton.grid(row=3, column=1, padx=1, pady=1)
window.protocol("WM_DELETE_WINDOW", confirmExit)
window.mainloop()