import matplotlib.pyplot as plt
#import numpy as np

def createLineSegments(): 
    #   
    lines_segments = []
    twoPoints = [] 

    def onclick(event):
        #
        nonlocal twoPoints
        ex, ey = event.xdata, event.ydata 

        ax.plot(ex, ey, marker='o', linestyle='-', color='b')
        plt.show()

        twoPoints.append( (ex, ey) )

        if len(twoPoints) == 2: 
            ax.plot( [ex, twoPoints[0][0]], [ey, twoPoints[0][1]], c = "brown" )
            
            if twoPoints[0][0] < twoPoints[1][0]:
                lines_segments.append( (twoPoints[0], twoPoints[1]) )
            else:
                lines_segments.append( (twoPoints[1], twoPoints[0]) )
            
            twoPoints = [] 

            fig.canvas.draw()     
        # end 'if' clause
    #end procedure onclick()
    
    fig, ax = plt.subplots()
    ax.set_xlim((-20,20))
    ax.set_ylim((-20,20))
    ax.set_title("Draw segments")
    
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    
    return lines_segments
#end procedure drawPolygon()

