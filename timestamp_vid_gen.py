from utils import *

def animate3(frame, coral_df, fig, ax, times, plot_title, fps, est_times, detection_threshold=0.0):
    
    # animates a single frame
    timestamp = times[frame]
    est_timestamp = est_times[0] + times[frame][-13:]
    
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
        # ax.text(430.0, 20.0, f"time: {timestamp}")
        ax.text(430.0, 20.0, f"time: {est_timestamp}", color='red')
        ax.text(430.0, 40.0, f'avg fps: {str(fps)[:5]}')
        for i,j in num_edges:
            if probs[i] > detection_threshold and probs[j] > detection_threshold:
                xs, ys = [all_x_coords[i], all_x_coords[j]], [all_y_coords[i], all_y_coords[j]]
                plt.plot(xs, ys, color='black')
        ax.set_xlim([0, width])
    ax.set_ylim([height, 0])
    
    return ax

def make_vid_of_hour(coral, year, month, day, hour):
    # convert from pst to est
    est_hour, est_day = est_to_pst(h, d)

    # create dataframe
    hour_df_dir = f'../COMPTON_DATA_2023/{coral}/{year}/{month}/{day}/{hour}'
    hour_df = create_df_from_hour(hour_df_dir)
    hour_df = add_time(hour_df)
    plot_title = f'{month}/{est_day}/{year}'

    # create animation
    fig, ax = plt.subplots()
    coral_df = hour_df.copy()
    times = coral_df['time'].unique()
    fps = 1/(float(times[11][-9:]) - float(times[10][-9:]))
    ani = FuncAnimation(fig, 
                        partial(animate3,
                                coral_df=coral_df,
                                fig=fig,
                                ax=ax,
                                times=times,
                                plot_title=plot_title,
                                fps = fps,
                                est_times = [est_hour, est_day]), 
                        frames=len(times)-1,
                        # frames=20
                        )

    # save animation
    f = f"../compton-vids/{coral}/{est_day}_{est_hour}.mp4"
    writervideo = FFMpegWriter(fps=int(fps))
    ani.save(f, writer=writervideo)

corals = [
            'deft_shrimp', 
            'elusive_tang', 
            'jumbo_orange'
            ]
days = [
	'04', '05', '06',
	#'07', '08', '09', '10', 
        #'11', '12', '13', '14', '15', '16', '17', '18'
	]
hours = [
        '00', '01', '02', '03', '04', 
        '05', '06', '07', '08', '09', '10', 
        '11', '12', '13', '14', '15', '16', '17', '18', '19', 
        '20', '21', '22', '23', '24'
        ]

for c in corals:
    for d in days:
        for h in hours:
            file_dir = f'../COMPTON_DATA_2023/{c}/2023/02/{d}/{h}'
	    print(file_dir)
            if os.path.exists(file_dir):
                make_vid_of_hour(c, '2023', '02', d, h)


# for c in corals:
#     for d in days:
#         for h in hours:
#             if os.path.exists(f'../COMPTON_DATA_2023/{c}/2023/02/{d}/{h}'):
#                 make_vid_of_hour(c, '2023', '02', d, h)

# make_vid_of_hour('deft_shrimp', '2023', '02', '04', '19')
# 'compton-data/deft_shrimp/2023/02/04/19'
