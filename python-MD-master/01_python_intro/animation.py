#import matplotlib.pyplot as plt
#import matplotlib.animation as animation

#def animate(trajectory, speed):
    #fig, ax = plt.subplots()
    #head, = ax.plot([], [], lw=2, marker='o', color='y')
    #trace, = ax.plot([], [], lw=2, color='y')
    #lines = [head, trace]
    #x_data = []
    #y_data = []

    #def init():
        #ax.set_ylim(0, 1)
        #ax.set_xlim(0, 1)
        #fig.canvas.set_window_title('tennis ball simulation')
        #del x_data[:]
        #del y_data[:]
        #for line in lines:
            #line.set_data(x_data, y_data)
        #return lines,

    #def run(data):
        #x, y = data
        #x_data.append(x)
        #y_data.append(y)
        #lines[0].set_data(x_data[-1], y_data[-1])
        #lines[1].set_data(x_data, y_data)
        #return lines
    #ani = animation.FuncAnimation(fig, run, iter(trajectory), blit=False, interval=speed,
                                  #repeat=False, init_func=init)
    #return ani
# animation.py

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import Video
import matplotlib

# Use a backend that doesn't try to open a window
matplotlib.use('Agg')

def create_and_display_animation(trajectory, ball_radius, xlims=(0, 3), ylims=(0, 1.5)):
    """
    Handles all steps of creating and displaying the animation.
    - Creates the plot and animation object.
    - Saves the animation to a video file.
    - Returns an IPython Video object for display in a notebook.
    """

    # 1. Set up the plot area
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlim(xlims)
    ax.set_ylim(ylims)
    ax.set_title("Bouncing Ball Simulation")

    # 2. Create the ball object (a circle) that we will animate
    ball_drawing = plt.Circle(trajectory[0], radius=ball_radius, color='gold')
    ax.add_patch(ball_drawing)

    # 3. Define the function that updates the plot for each frame
    def animate_frame(frame_number):
        position = trajectory[frame_number]
        ball_drawing.center = position
        return ball_drawing,

    # 4. Create the final animation object
    ani = FuncAnimation(
        fig,
        animate_frame,
        frames=len(trajectory),
        blit=True
    )

    # 5. Save the animation as an MP4 video file (requires ffmpeg)
    # This is the most reliable way to render animations.
    video_filename = 'bouncing_ball_animation.mp4'
    ani.save(video_filename, writer='ffmpeg', dpi=150)

    # Close the plot to free up memory
    plt.close(fig)

    # 6. Return an object that Jupyter knows how to display as a video
    return Video(video_filename)
