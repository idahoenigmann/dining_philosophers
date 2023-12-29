import matplotlib.pyplot as plt
import time
import math

fig1 = plt.figure()
ax1 = fig1.add_subplot(111, aspect='equal')
ax1.set_xlim([-50, 50])
ax1.set_ylim([-50, 50])

lines = []
content = []
# open each file and add to content
with open("philosopher0.csv") as f1:
    content1 = f1.readlines()
content1 = [x.strip() for x in content1]
content.append(content1)

with open("philosopher1.csv") as f2:
    content2 = f2.readlines()
content2 = [x.strip() for x in content2]
content.append(content2)

with open("philosopher2.csv") as f3:
    content3 = f3.readlines()
content3 = [x.strip() for x in content3]
content.append(content3)

with open("philosopher3.csv") as f4:
    content4 = f4.readlines()
content4 = [x.strip() for x in content4]
content.append(content4)

with open("philosopher4.csv") as f5:
    content5 = f5.readlines()
content5 = [x.strip() for x in content5]
content.append(content5)

print(content)
timer = 0
status = ["", "", "", "", ""]


def draw(a, b, c, d, e, t):  # creates image for each time t
    plt.cla()
    plt.axis('off')

    ax1.set_xlim([-50, 50])
    ax1.set_ylim([-50, 50])
    circle = plt.Circle((0, 0), 15, fc='grey', ec='black')  # table
    plt.gca().add_patch(circle)

    ax1.text(-45, -45, "t=")
    ax1.text(-38, -45, t)

    #chopsticks on table
    x1 = [0, 0]
    y1 = [10, 15]
    plt.plot(x1, y1, color='black')

    x2 = [-10, -14]
    y2 = [3, 5]
    plt.plot(x2, y2, color='black')

    x3 = [-6, -9]
    y3 = [-8, -12]
    plt.plot(x3, y3, color='black')

    x4 = [6, 9]
    y4 = [-8, -12]
    plt.plot(x4, y4, color='black')

    x5 = [10, 14]
    y5 = [3, 5]
    plt.plot(x5, y5, color='black')

    # coordinates for chopsticks next to philosophers
    x1_l = [-6.8, -8.8]
    y1_l = [15.7, 20.3]
    x1_r = [-13.2, -17.2]
    y1_r = [11, 13.8]

    x2_l = [-16.7, -21.6]
    y2_l = [-3.1, -3.7]
    x2_r = [-13.3, -17.4]
    y2_r = [-10.5, -13.4]

    x3_l = [-4.1, -5.3]
    y3_l = [-16.5, -21.5]
    x3_r = [4.1, 5.3]
    y3_r = [-16.5, -21.5]

    x4_l = [13.3, 17.4]
    y4_l = [-10.5, -13.4]
    x4_r = [16.7, 21.6]
    y4_r = [-3.1, -3.7]

    x5_l = [13.2, 17.2]
    y5_l = [11, 13.8]
    x5_r = [6.8, 8.8]
    y5_r = [15.7, 20.3]


    # P1
    ax1.text(-12, 16, "P1", ha="center", va="center")  # philosopher
    ax1.text(-12, 22, a,  ha="center", va="center")  # status

    # colored circle and moving chopsticks
    c_1 = 'black'
    if a == "Eating":
        c_1 = 'red'  # color change
        plt.plot(x1, y1, color='grey')  # left chopstick not on table
        plt.plot(x2, y2, color='grey')  # right chopstick not on table
        plt.plot(x1_l, y1_l, color='black')  # left chopstick next to P1
        plt.plot(x1_r, y1_r, color='black')  # right chopstick next to P1

    if a == "Left" or a == "Return":
        c_1 = 'blue'  # color change

    if a == "Right":
        c_1 = 'blue'  # color change
        plt.plot(x1, y1, color='grey')  # left chopstick not on table
        plt.plot(x1_l, y1_l, color='black') # left chopstick next to P1

    if a == "Meditating":
        c_1 = 'green'  # color change
    circle = plt.Circle((-12, 16), 4, fc=c_1, ec='black')
    plt.gca().add_patch(circle)
    ax1.figure.canvas.draw()

# repeat for all philosophers

    # P2
    ax1.text(-18.5, -8, "P2", ha="center", va="center")
    ax1.text(-32, -8, b, ha="center", va="center")

    c_2 = 'black'
    if b == "Eating":
        c_2 = 'red'
        plt.plot(x2, y2, color='grey')  # left chopstick not on table
        plt.plot(x3, y3, color='grey')  # right chopstick not on table
        plt.plot(x2_l, y2_l, color='black')  # left chopstick next to P2
        plt.plot(x2_r, y2_r, color='black')  # right chopstick next to P2

    if b == "Left" or b == "Return":
        c_2 = 'blue'

    if b == "Right":
        c_2 = 'blue'
        plt.plot(x2, y2, color='grey')  # left chopstick not on table
        plt.plot(x2_l, y2_l, color='black')  # left chopstick next to P2

    if b == "Meditating":
        c_2 = 'green'
    circle = plt.Circle((-18.5, -8), 4, fc=c_2, ec='black')
    plt.gca().add_patch(circle)
    ax1.figure.canvas.draw()

    # P3
    ax1.text(0, -20, "P3", ha="center", va="center")
    ax1.text(0, -26, c, ha="center", va="center")

    c_3 = 'black'
    if c == "Eating":
        c_3 = 'red'
        plt.plot(x3, y3, color='grey')  # left chopstick not on table
        plt.plot(x4, y4, color='grey')  # right chopstick not on table
        plt.plot(x3_l, y3_l, color='black')  # left chopstick next to P3
        plt.plot(x3_r, y3_r, color='black')  # right chopstick next to P3

    if c == "Left" or c == "Return":
        c_3 = 'blue'

    if c == "Right":
        c_3 = 'blue'
        plt.plot(x3, y3, color='grey')  # left chopstick not on table
        plt.plot(x3_l, y3_l, color='black')  # left chopstick next to P3

    if c == "Meditating":
        c_3 = 'green'
    circle = plt.Circle((0, -20), 4, fc=c_3, ec='black')
    plt.gca().add_patch(circle)
    ax1.figure.canvas.draw()

    # P4
    ax1.text(18.5, -8, "P4", ha="center", va="center")
    ax1.text(32, -8, d, ha="center", va="center")

    c_4 = 'black'
    if d == "Eating":
        c_4 = 'red'
        plt.plot(x4, y4, color='grey')  # left chopstick not on table
        plt.plot(x5, y5, color='grey')  # right chopstick not on table
        plt.plot(x4_l, y4_l, color='black')  # left chopstick next to P4
        plt.plot(x4_r, y4_r, color='black')  # right chopstick next to P4

    if d == "Left" or d == "Return":
        c_4 = 'blue'

    if d == "Right":
        c_4 = 'blue'
        plt.plot(x4, y4, color='grey')  # left chopstick not on table
        plt.plot(x4_l, y4_l, color='black')  # left chopstick next to P4

    if d == "Meditating":
        c_4 = 'green'
    circle = plt.Circle((18.5, -8), 4, fc=c_4, ec='black')
    plt.gca().add_patch(circle)
    ax1.figure.canvas.draw()

    # P5
    ax1.text(12, 16, "P5", ha="center", va="center")
    ax1.text(12, 22, e, ha="center", va="center")

    c_5 = 'black'
    if e == "Eating":
        c_5 = 'red'
        plt.plot(x5, y5, color='grey')  # left chopstick not on table
        plt.plot(x1, y1, color='grey')  # right chopstick not on table
        plt.plot(x5_l, y5_l, color='black')  # left chopstick next to P5
        plt.plot(x5_r, y5_r, color='black')  # right chopstick next to P5

    if e == "Left" or e == "Right" or e == "Return":
        c_5 = 'blue'

    if e == "Right":
        c_5 = 'blue'
        plt.plot(x5, y5, color='grey')  # left chopstick not on table
        plt.plot(x5_l, y5_l, color='black')  # left chopstick next to P5

    if e == "Meditating":
        c_5 = 'green'
    circle = plt.Circle((12, 16), 4, fc=c_5, ec='black')
    plt.gca().add_patch(circle)
    ax1.figure.canvas.draw()
    plt.pause(1)
    plt.ion()


print("start")
print(content[1][0].split(',')[0])
iterators = [0, 0, 0, 0, 0]  # line in philosopher i
while True:
    flag = [1, 1, 1, 1, 1]  # philosopher still doing smt
    plt.gca()
    print(timer)
    # check status of philosopher 1 at time t
    if iterators[0] == len(content[0]):  # last line?
        flag[0] = 0
        status[0] = " done"

    elif int(content[0][iterators[0]].split(',')[1]) == timer:  # is something happening at time t?
        while int(content[0][iterators[0]].split(',')[1]) == timer:
            iterators[0] += 1
        iterators[0] -= 1
        status[0] = content[0][iterators[0]].split(',')[0]
        iterators[0] += 1
# repeat for all philosophers
    # p2
    if iterators[1] == len(content[1]):
        flag[1] = 0
        status[1] = " done"
    elif int(content[1][iterators[1]].split(',')[1]) == timer:
        while int(content[1][iterators[1]].split(',')[1]) == timer:
            iterators[1] += 1
        iterators[1] -= 1
        status[1] = content[1][iterators[1]].split(',')[0]
        iterators[1] += 1
    # p3
    if iterators[2] == len(content[2]):
        flag[2] = 0
        status[2] = " done"
    elif int(content[2][iterators[2]].split(',')[1]) == timer:
        while int(content[2][iterators[2]].split(',')[1]) == timer:
            iterators[2] += 1
        iterators[2] -= 1
        status[2] = content[2][iterators[2]].split(',')[0]
        iterators[2] += 1
    # p4
    if iterators[3] == len(content[3]):
        flag[3] = 0
        status[3] = " done"
    elif int(content[3][iterators[3]].split(',')[1]) == timer:
        while int(content[3][iterators[3]].split(',')[1]) == timer:
            iterators[3] += 1
        iterators[3] -= 1
        status[3] = content[3][iterators[3]].split(',')[0]
        iterators[3] += 1
    # p5
    if iterators[4] == len(content[4]):
        flag[4] = 0
        status[4] = " done"
    elif int(content[4][iterators[4]].split(',')[1]) == timer:
        while int(content[4][iterators[4]].split(',')[1]) == timer:
            iterators[4] += 1
        iterators[4] -= 1
        status[4] = content[4][iterators[4]].split(',')[0]
        iterators[4] += 1

    print(iterators)
    draw(status[0], status[1], status[2], status[3], status[4], timer)

    if flag[0] == 0 and flag[1] == 0 and flag[2] == 0 and flag[3] == 0 and flag[4] == 0:
        break
    time.sleep(1)
    timer += 1
