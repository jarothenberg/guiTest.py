import csv

import mpl_toolkits.mplot3d.axes3d as p3
import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt

fig = plt.figure()  # defines the figure as a plot
ax = p3.Axes3D(fig, auto_add_to_figure=False)  # defines 3D axes for the figure
fig.add_axes(ax)  # adds the 3D axes to the figure

fileName = 'FistRelax-200205-01'  # the name of the file and data to be plotted
with open('C:/Users/Jacka/Desktop/Research/3D Model/Data/CSVs/Formatted/' + fileName + '-Trig.csv') as csv_file:
    trigs = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)  # variable trigs is CSV data
    trig = False  # boolean indicating whether a trigger value has been hit, default to false
    trig_indexes = []  # an array of the frames in which a trigger value is present
    for row in trigs:
        if not trig and row[1] < -0.2:  # detects if a trigger value is hit
            trig_indexes.append(row[0])  # adds the current frame to the array
            trig = True  # sets the boolean trig indicator to true
        elif trig and row[1] > -0.2:  # if not a trigger
            trig = False  # sets the boolean trig indicator to false

with open('C:/Users/Jacka/Desktop/Research/3D Model/Data/CSVs/Formatted/' + fileName + '-Mocap.csv') as csv_file:
    coords = csv.reader(csv_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)  # variable coords is CSV data
    x_coords = []  # a 2D array holding the x values of every point in 1D arrays for every frame
    y_coords = []  # a 2D array holding the y values of every point in 1D arrays for every frame
    z_coords = []  # a 2D array holding the z values of every point in 1D arrays for every frame
    rowNum = 0  # a counter for the row being the frame number in the coords CSV data
    for row in coords:
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
        rowNum += 1  # add one to the counter, showing we are now analyzing the next row

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

    if frameNum + (skipNum - 1) > len(trig_indexes):  # checks if we are out of bounds of the frames
        frameNum = 1  # resets the frame number so we don't go out of bounds and can repeat

    print(str(frameNum) + "/" + str(len(trig_indexes)))  # prints the current frame out of the total
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


ani = animation.FuncAnimation(fig, update_plot, interval=30, frames=len(trig_indexes), repeat=False,
                              fargs=(x, y, z, points, lines, fingers))  # animates the figure with all trigger frames
plt.show()  # shows the plot as an interactable 3D animation
ani.save(fileName + '.gif')  # saves the animation as a gif file
