import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style

import matplotlib 

#define function to draw graph based
#on the given data in list current_data
def draw_graph(data):
    #Declare x and y plot data
    x1 = []
    
    y1 = []
    y2 = []
    y3 = []

    for row in data:
        temp_date = row[0] + '\n' + row [1]
        x1.append(temp_date)
        
        y1.append(row[2])
        y2.append(row[3])
        y3.append(row[4])

#Graph using plt   
    plt.subplot(3, 1, 1, autoscale_on = True, xmargin = -0.4)
    matplotlib.pyplot.subplots_adjust(hspace=1.25)
    plt.plot(x1, y1, 'o-')
    plt.title('pH Analysis')
    plt.xlabel('time (s)')
    plt.ylabel('pH')

    ax = plt.gca()
    plt.xticks(rotation=90)
    for label in ax.get_xaxis().get_ticklabels()[::2]:
        label.set_visible(False)


    plt.subplot(3, 1, 2, autoscale_on = True, xmargin = -0.4)
    matplotlib.pyplot.subplots_adjust(hspace=1.25)
    plt.plot(x1, y2, '.-')
    plt.title('temperature Analysis')
    plt.xlabel('time (s)')
    plt.ylabel('degree Celcius(C)')
    
    ax = plt.gca()
    plt.xticks(rotation=90)
    for label in ax.get_xaxis().get_ticklabels()[::2]:
        label.set_visible(False)

    plt.subplot(3, 1, 3, autoscale_on = True, xmargin = -0.4)
    matplotlib.pyplot.subplots_adjust(hspace=1.25)
    plt.plot(x1, y3, 'o-')
    plt.title('moisture Analysis')
    plt.xlabel('time (s)')
    plt.ylabel('percentage(%)')
    
    ax = plt.gca()
    plt.xticks(rotation=90)
    for label in ax.get_xaxis().get_ticklabels()[::2]:
        label.set_visible(False)

    #Zoom window
    wm = plt.get_current_fig_manager()
    wm.window.state('iconic')
    plt.show()
