# Generate Chart
import matplotlib
matplotlib.use('Agg')  # for threading, you must set matplot backend to 'agg'
# Now you can import as plt
import matplotlib.pyplot as plt
import multiprocessing
import time
import sys
import os

def main_chart(queue):

    while True:
        print ("Generating Chart")
        try:
            otherDir = 'log'  # specify log directory
            origDir = os.getcwd()
            os.chdir(os.path.join(os.path.abspath(sys.path[0]), otherDir)) # switch to other dir
        except OSError:
            print("Error: 'log' directory does not exist.")
            break
        try:
            with open("./srvlogLive.csv", "r") as f:
                lines = f.readlines()
                _online = (len([line for line in lines if "Online" in line]))
                _offline = (len([line for line in lines if "Offline" in line]))
                with open("./svclogLive.csv", "r") as f:
                    lines = f.readlines()
                    _running = (len([line for line in lines if "Running" in line]))
                    _stopped = (len([line for line in lines if "Stopped" in line]))
                    _manual = (len([line for line in lines if "Manual" in line]))
                    plt.ioff()
                    plt.plot([1.6, 2.7])
            
                    # Added to so you can see more color in the graph.
                    # It widens the color slices.
                    # You may want to customize this.
                    _onlineadd  = _online  + 18
                    _offlineadd = _offline + 16
                    _stoppedadd = _stopped + 7
                    _manualadd  = _manual  + 5
                    
                    # Pie chart
                    labels = ['Online', 'Offline', 'Svc Running', 'Svc Stopped', 'Svc Manual']
                    sizes = [_onlineadd, _offlineadd, _running, _stoppedadd, _manualadd]
                    
                    # Other colors you can try:
                    # colors = ['#75D307','#CC3B14','#194FFF','#9F17D6', '#A514CC']
                    colors = ['#159802','#de2242','#729fcf','#fbb610', '#A514CC']
            
                    fig1, ax1 = plt.subplots()
                    
                    # Change color of text
                    plt.rcParams['text.color'] = 'white'
                    
                    ax1.pie(sizes, colors = colors, startangle=90)
                    ax1.set_facecolor("red")
                    
                    #draw circle
                    centre_circle = plt.Circle((0,0),0.70,fc='#2e3436')
                    fig = plt.gcf()
                    fig.patch.set_facecolor('#2e3436')
                    
                    # CHANGE SIZE in inches
                    #fig.set_size_inches(4.9, 2)
                    fig.set_size_inches(5.5, 2.6)
                    fig.gca().add_artist(centre_circle)
                    
                    leg = ax1.legend(labels, loc="right")
                    # SET LEGEND TO TRANSPARENT
                    leg.get_frame().set_alpha(0.0)  # 0.5 is translucent

                    # The equal aspect ration makes sure the pie is drawn as a circle
                    ax1.axis('equal')  
                    plt.tight_layout()
                    
                    fig.savefig('../static/images/main_chart.png', transparent=True)
                    plt.close(fig)
                    os.chdir(origDir) # switch back to original dir
                    time.sleep(10)
        except IOError as e:
            print (e)
            print ("Log is probably missing from 'log' directory.")
            time.sleep(30)

if __name__ == '__main__':

    # for testing
    queue = multiprocessing.Queue()
    main_chart(queue)
