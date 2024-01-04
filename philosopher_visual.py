import matplotlib
import matplotlib.pyplot as plt
import time


def draw(phil_status, t):  # creates image for each time t
    plt.cla()
    plt.axis('off')

    ax1.set_xlim([-50, 50])
    ax1.set_ylim([-50, 50])
    circle = plt.Circle((0, 0), 15, fc='grey', ec='black')  # table
    plt.gca().add_patch(circle)

    ax1.text(-45, -45, "t=")
    ax1.text(-38, -45, t)

    #chopsticks on table
    chop_pos_table = [[[0, 0], [10, 15]], [[-10, -14], [3, 5]], [[-6, -9], [-8, -12]], [[6, 9], [-8, -12]], [[10, 14], [3, 5]]]
    for i in range(5):
        plt.plot(chop_pos_table[i][0], chop_pos_table[i][1], color='black')

    # coordinates for chopsticks next to philosophers
    # chop_pos_phil[i][j][k] where i is the philosopher index, j is 0 for left and 1 for right, k is 0 for x and 1 for y
    chop_pos_phil = [[[[-6.8, -8.8], [15.7, 20.3]], [[-13.2, -17.2], [11, 13.8]]],
                     [[[-16.7, -21.6], [-3.1, -3.7]], [[-13.3, -17.4], [-10.5, -13.4]]],
                     [[[-4.1, -5.3], [-16.5, -21.5]], [[4.1, 5.3], [-16.5, -21.5]]],
                     [[[13.3, 17.4], [-10.5, -13.4]], [[16.7, 21.6], [-3.1, -3.7]]],
                     [[[13.2, 17.2], [11, 13.8]], [[6.8, 8.8], [15.7, 20.3]]]]

    phil_pos = [[-12, 16], [-18.5, -8], [0, -20], [18.5, -8], [12, 16]]
    phil_status_pos = [[-12, 22], [-32, -8], [0, -26], [32, -8], [12, 22]]

    for i in range(5):
        ax1.text(phil_pos[i][0], phil_pos[i][1], f"P{i}", ha="center", va="center")  # philosopher
        ax1.text(phil_status_pos[i][0], phil_status_pos[i][1], phil_status[i],  ha="center", va="center")  # status

        # colored circle and moving chopsticks
        if phil_status[i] == "Eating" or phil_status[i] == "Cleaning":
            plt.plot(chop_pos_table[i][0], chop_pos_table[i][1], color='grey')  # left chopstick not on table
            plt.plot(chop_pos_table[(i + 1) % 5][0], chop_pos_table[(i + 1) % 5][1],
                     color='grey')  # right chopstick not on table
            plt.plot(chop_pos_phil[i][0][0], chop_pos_phil[i][0][1], color='black')  # left chopstick next to phil
            plt.plot(chop_pos_phil[i][1][0], chop_pos_phil[i][1][1], color='black')  # right chopstick next to phil
        elif phil_status[i] == "Right":
            plt.plot(chop_pos_table[i][0], chop_pos_table[i][1], color='grey')  # left chopstick not on table
            plt.plot(chop_pos_phil[i][0][0], chop_pos_phil[i][0][1], color='black')  # left chopstick next to phil

        color = 'white'
        if phil_status[i] == "Meditating":
            color = 'green'
        elif phil_status[i] == "Left" or phil_status[i] == "Right" or phil_status[i] == "Return":
            color = 'blue'
        elif phil_status[i] == "Eating":
            color = 'red'
        elif phil_status[i] == "Cleaning":
            color = 'yellow'

        circle = plt.Circle((phil_pos[i][0], phil_pos[i][1]), 4, fc=color, ec='black')
        plt.gca().add_patch(circle)
        ax1.figure.canvas.draw()
    plt.pause(1)
    plt.ion()


if __name__ == "__main__":
    matplotlib.use('TkAgg')

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')
    ax1.set_xlim([-50, 50])
    ax1.set_ylim([-50, 50])

    lines = []
    content = []
    status = ["", "", "", "", "", ""]

    # open each file and add to content
    for i in range(5):
        with open(f"philosopher{i}.csv") as f:
            content.append([x.strip() for x in f.readlines()])

    # print(content)
    timer = 0

    print("start")
    print(content[1][0].split(',')[0])
    indices = [0, 0, 0, 0, 0]  # line in philosopher i
    flag = [1, 1, 1, 1, 1]  # philosopher still doing smt
    while flag != [0, 0, 0, 0, 0]:
        plt.gca()
        print(timer)

        # check status of philosopher at time t
        for i in range(5):
            if indices[i] >= len(content[i]):
                flag[i] = 0
                continue
            if int(content[i][indices[i]].split(',')[1]) == timer:  # is something happening at time t?
                while indices[i] < len(content[i]) and int(content[i][indices[i]].split(',')[1]) == timer:
                    indices[i] += 1
                status[i] = content[i][indices[i] - 1].split(',')[0]

        print(indices)
        draw(status, timer)

        time.sleep(1)
        timer += 1
