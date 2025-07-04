# animation.py

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import Video, clear_output, display
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


# ===================================================================
# NEW FUNCTION for Multi-Particle Simulation
# ===================================================================
def create_multiparticle_animation(full_trajectory, radii, colors, box_size, video_filename='multi_particle_animation.mp4'):
    """
    Creates an animation for a system of multiple interacting particles.
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.set_xlim(0, box_size)
    ax.set_ylim(0, box_size)
    ax.set_title("Multi-Particle Simulation")

    sizes = (radii * 150)**2
    scatter = ax.scatter(full_trajectory[0][:, 0], full_trajectory[0][:, 1], s=sizes, c=colors)

    def animate_frame(frame_number):
        positions_at_frame = full_trajectory[frame_number]
        scatter.set_offsets(positions_at_frame)
        return scatter,

    ani = FuncAnimation(fig, animate_frame, frames=len(full_trajectory), blit=True)
    
    print(f"Creating video file: {video_filename}...")
    ani.save(video_filename, writer='ffmpeg', dpi=100)
    plt.close(fig)
    print("Video created successfully!")
    return Video(video_filename)


# ===================================================================
# NEW FUNCTION for Multi-Particle Simulation
# ===================================================================
def run_live_simulation(simulation, n_steps):
    """
    Takes a simulation object and runs it for n_steps, displaying a live animation
    in a Jupyter Notebook.

    Args:
        simulation: An object that has attributes `positions`, `radius`, `box_size`
                    and a method `update_step()`.
        n_steps (int): The number of steps to run the simulation for.
    """
    
    # Create the plot figure and axes
    fig, ax = plt.subplots(figsize=(8, 8))

    # This is the main simulation loop
    for step in range(n_steps):
        # 1. Run one step of the simulation's physics
        simulation.update_step()
        
        # 2. Draw the current state of the simulation
        
        # Set the size and color for all balls
        sizes = (simulation.radius * 150)**2
        color = 'dodgerblue'
        
        # Create the scatter plot of all ball positions
        ax.scatter(simulation.positions[:, 0], simulation.positions[:, 1], s=sizes, c=color)
        
        # Configure the plot appearance
        ax.set_ylim((0, simulation.box_size))
        ax.set_xlim((0, simulation.box_size))
        ax.text(0.4 * simulation.box_size, 0.9 * simulation.box_size, 'step ' + str(step),
                     bbox={'facecolor':'white', 'alpha':0.5, 'pad':7})
        ax.set_aspect('equal', adjustable='box')
        
        # Use IPython display tools for live animation
        clear_output(True)
        display(fig)
        
        # Clear the axes for the next drawing
        ax.cla()
        
    # Close the plot at the very end
    plt.close(fig)




def run_live_simulation_c(simulation, n_steps):
    """
    Takes a simulation object and runs it for n_steps, displaying a live animation.
    This version is updated to handle particles with individual colors and radii.
    """
    
    fig, ax = plt.subplots(figsize=(8, 8))

    for step in range(n_steps):
        # 1. Run one step of the simulation's physics
        simulation.update_step()
        
        # 2. Draw the current state
        
        # Get sizes and colors directly from the simulation object
        sizes = (simulation.radii * 150)**2
        colors = simulation.colors
        
        ax.scatter(simulation.positions[:, 0], simulation.positions[:, 1], s=sizes, c=colors)
        
        # Configure plot appearance
        ax.set_ylim((0, simulation.box_size))
        ax.set_xlim((0, simulation.box_size))
        ax.text(0.4 * simulation.box_size, 0.9 * simulation.box_size, 'step ' + str(step),
                     bbox={'facecolor':'white', 'alpha':0.5, 'pad':7})
        ax.set_aspect('equal', adjustable='box')
        
        # Use IPython display tools for live animation
        clear_output(True)
        display(fig)
        
        # Clear the axes for the next drawing
        ax.cla()
        
    plt.close(fig)
    
