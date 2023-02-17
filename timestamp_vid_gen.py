from utils import *

def animate3(frame, coral_df, fig, ax, times, plot_title, detection_threshold=0.0):
    
    # animates a single frame
    timestamp = times[frame]
    
    poses = coral_df.loc[coral_df['time']==timestamp]
    
    ax.clear()
    ax.set_title(plot_title)
    for pos in range(len(poses)):
        pose = poses.iloc[pos].to_dict()
    
        width, height = 640, 480
        all_x_coords, all_y_coords, probs = [], [], []
        x_coords, y_coords = [], []

        for kp in keypoints:
            all_x_coords.append(pose[kp][0])
            all_y_coords.append(pose[kp][1])
            probs.append(pose[kp][2])

            if pose[kp][2] > detection_threshold:
                x_coords.append(pose[kp][0])
                y_coords.append(pose[kp][1])
        ax.scatter(x=x_coords, y=y_coords, color='blue')
        ax.text(430.0, 20.0, f"time: {timestamp}")
        for i,j in num_edges:
            if probs[i] > detection_threshold and probs[j] > detection_threshold:
                xs, ys = [all_x_coords[i], all_x_coords[j]], [all_y_coords[i], all_y_coords[j]]
                plt.plot(xs, ys, color='black')
        ax.set_xlim([0, width])
    ax.set_ylim([height, 0])
    
    return ax

def make_vid_of_hour(coral, year, month, day, hour):
    # create dataframe
    hour_df_dir = f'compton-data/{coral}/{year}/{month}/{day}/{hour}'
    hour_df = create_df_from_hour(hour_df_dir)
    hour_df = add_time(hour_df)
    plot_title = f'{month}/{day}/{year}'

    # create animation
    fig, ax = plt.subplots()
    coral_df = hour_df.copy()
    times = coral_df['time'].unique()
    ani = FuncAnimation(fig, 
                        partial(animate3,
                                coral_df=coral_df,
                                fig=fig,
                                ax=ax,
                                times=times,
                                plot_title=plot_title), 
                        frames=len(times)-1,
                        # frames=30
                        )

    # save animation
    f = f"compton-vids/{coral}/{day}_{hour}.mp4"
    writervideo = FFMpegWriter(fps=30)
    ani.save(f, writer=writervideo)

corals = [
            'deft_shrimp', 
            # 'elusive_tang', 
            # 'jumbo_orange'
            ]
days = ['15']
hours = [
        # '0', '1', '2', '3', '4', '5', '6', '7', '8',
        #  '9', '10', '11', '12', '13', '14', '15', 
        '16',
        #  '17', '18', '19', '20', 
        # '21', '22', 
        # '23', '24'
        ]
# hours = ['19', '20']

for c in corals:
    for d in days:
        for h in hours:
            if os.path.exists(f'compton-data/{c}/2023/02/{d}/{h}'):
                make_vid_of_hour(c, '2023', '02', d, h)

# make_vid_of_hour('deft_shrimp', '2023', '02', '04', '19')
# 'compton-data/deft_shrimp/2023/02/04/19'