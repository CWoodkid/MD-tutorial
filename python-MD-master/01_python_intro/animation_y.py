# animation.py

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import Video
import matplotlib

# Use a backend that doesn't try to open a window, which is good for scripts.
matplotlib.use('Agg')

def create_and_save_animation_y(trajectory, ball_radius, xlims, ylims, video_filename='Ball Simulation'):
    """
    A general function to create a ball animation.
    - Creates the plot and animation object based on provided limits.
    - Saves the animation to the specified video file.
    - Returns an IPython Video object for display in a notebook.
    """

    # 1. Set up the plot area
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlim(xlims)
    ax.set_ylim(ylims)
    ax.set_title("Ball Simulation")

    # 2. Create the ball object (a circle) that we will animate
    ball_drawing = plt.Circle(trajectory[0], radius=ball_radius, color='dodgerblue')
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
    print(f"Creating video file: {video_filename}...")
    ani.save(video_filename, writer='ffmpeg', dpi=100)

    # Close the plot to free up memory
    plt.close(fig)
    print("Video created successfully!")

    # 6. Return an object that Jupyter knows how to display as a video
    return Video(video_filename)
