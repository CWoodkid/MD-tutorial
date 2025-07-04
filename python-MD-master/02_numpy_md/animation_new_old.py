# animation.py

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import Video
import numpy as np

# Use a non-interactive backend to ensure the script runs without needing a display window.
import matplotlib
matplotlib.use('Agg')

def create_animation_video(trajectory, xlims, ylims, video_filename='animation.mp4'):
    """
    Handles all steps of creating an animation from a trajectory.
    - Creates the plot and animation object.
    - Saves the animation to a video file using ffmpeg.
    - Returns an IPython Video object that can be displayed directly in a notebook.
    """
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlim(xlims)
    ax.set_ylim(ylims)
    ax.set_title("Projectile Motion")
    ax.set_xlabel("x position (m)")
    ax.set_ylabel("y position (m)")

    # The objects we will be animating: a point for the ball and a line for its trail.
    head, = ax.plot([], [], marker='o', color='gold', markersize=12)
    trace, = ax.plot([], [], lw=1, color='orange', linestyle='--')

    # This function sets up the first frame
    def init():
        head.set_data([], [])
        trace.set_data([], [])
        return head, trace

    # This function is called for every frame to update the plot
    def animate_frame(frame_number):
        # Get the path data up to the current frame
        path_so_far = np.array(trajectory[:frame_number+1])

        # Update the head to the current position
        # THE FIX IS HERE: We wrap the single x and y values in lists.
        head.set_data([path_so_far[-1, 0]], [path_so_far[-1, 1]])

        # Update the trace to show the entire path so far
        trace.set_data(path_so_far[:, 0], path_so_far[:, 1])
        return head, trace

    # Create the animation object
    ani = FuncAnimation(
        fig,
        animate_frame,
        frames=len(trajectory),
        init_func=init,
        blit=True
    )

    # Save the animation to a file. This is the most reliable rendering method.
    print(f"Creating video file: {video_filename}...")
    ani.save(video_filename, writer='ffmpeg', dpi=100)

    # Close the plot figure to free up memory
    plt.close(fig)

    print("Video created successfully!")
    # Return an object that Jupyter can display automatically
    return Video(video_filename)


def plot_trajectory_and_error(trajectory_time, trajectory_numerical, trajectory_analytical, error):
    """
    This is the original plot function from your file, preserved for later use.
    It creates two subplots: one for the trajectories and one for the error over time.
    """
    fig = plt.figure(figsize=(8, 10))

    # Trajectory plot
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.set_title("Trajectory Comparison")
    ax1.plot(np.array(trajectory_numerical)[:, 0], np.array(trajectory_numerical)[:, 1], label="Numerical")
    ax1.plot(np.array(trajectory_analytical)[:, 0], np.array(trajectory_analytical)[:, 1], label="Analytical", linestyle='--')
    ax1.legend()
    ax1.set_ylabel("y position (m)")
    ax1.set_xlabel("x position (m)")
    ax1.grid(True)

    # Error plot
    ax2 = fig.add_subplot(2, 1, 2)
    ax2.set_title("Error Over Time")
    ax2.plot(trajectory_time, np.array(error)[:, 0], label="Error in x")
    ax2.plot(trajectory_time, np.array(error)[:, 1], label="Error in y")
    ax2.legend()
    ax2.set_ylabel("Error (m)")
    ax2.set_xlabel("Time (s)")
    ax2.grid(True)

    fig.tight_layout(pad=3.0)
    plt.show()
