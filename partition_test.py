# 2022-08-25
# Zhenshiyi Tian

import numpy as np

from trajCluster.partition import approximate_trajectory_partitioning, segment_mdl_comp, rdp_trajectory_partitioning
from trajCluster.point import Point
from trajCluster.cluster import line_segment_clustering, representative_trajectory_generation

from matplotlib import pyplot as plt


ts1 = [142.0, 9.9, 141.0, 9.7, 140.0, 9.5, 138.7, 9.6, 137.4, 9.7, 136.2, 9.8, 135.0, 10.0, 133.9, 10.1, 132.8, 10.3, 132.0, 10.7, 130.9, 11.1, 129.6, 11.3, 128.3, 11.5, 127.2, 11.6, 126.1, 11.4, 125.4, 10.9, 124.8, 10.7, 124.4, 10.9, 123.7, 10.8, 122.3, 10.8, 121.7, 12.0, 122.8, 13.2, 124.0, 14.3, 124.7, 15.2, 125.3, 15.9, 126.0, 16.2, 127.1, 16.3, 128.1, 16.1, 129.1, 15.9, 130.0, 15.5, 130.8, 15.3, 131.4, 15.0, 132.0, 14.7, 132.6, 14.3, 133.1, 13.8]
ts2 = [137.2, 11.0, 136.0, 10.9, 134.9, 10.8, 133.8, 10.8, 132.8, 10.8, 131.8, 10.8, 130.8, 10.9, 129.8, 10.9, 128.6, 11.0, 127.4, 11.3, 126.2, 11.9, 125.0, 12.5, 123.6, 13.2, 122.0, 14.1, 120.4, 14.8, 118.7, 15.8, 116.8, 16.8, 115.3, 17.8, 114.0, 18.5, 113.0, 19.2, 111.9, 20.1, 111.3, 20.9, 111.0, 21.9, 109.9, 22.3, 109.2, 22.5, 108.4, 22.6, 107.5, 22.3]
ts3 = [150.5, 9.5, 150.0, 9.6, 149.5, 9.8, 149.1, 9.9, 148.6, 10.0, 148.0, 10.0, 147.2, 10.0, 146.3, 10.1, 145.5, 10.2, 144.6, 10.3, 143.7, 10.4, 142.8, 10.8, 142.0, 11.2, 141.4, 11.7, 141.1, 12.1, 140.6, 12.6, 139.9, 13.2, 139.2, 14.1, 138.7, 14.8, 137.8, 15.4, 137.2, 16.0, 136.3, 16.8, 135.4, 17.3, 134.6, 17.4, 134.2, 17.6, 133.7, 17.8, 133.2, 18.0, 133.0, 18.2, 132.8, 18.3, 132.6, 18.3, 132.5, 18.1, 132.5, 18.0, 132.6, 17.9, 133.1, 18.2, 133.7, 18.7, 134.3, 19.2, 134.9, 19.8, 135.3, 20.4, 135.7, 20.8, 135.8, 21.0, 135.6, 21.1, 135.1, 21.1, 134.8, 20.9, 135.1, 20.8, 135.1, 21.2, 134.9, 21.6, 134.8, 21.8, 134.5, 22.2, 134.2, 22.7, 133.8, 23.0, 133.8, 23.3, 133.9, 23.5, 133.9, 23.8, 134.1, 24.2, 134.2, 24.9, 134.4, 25.6, 134.3, 26.3, 134.0, 26.8, 133.2, 27.3, 132.6, 27.7, 131.8, 28.1, 130.6, 28.3, 129.5, 28.7, 128.9, 28.8, 128.1, 28.9, 127.4, 28.8, 126.9, 28.5, 126.6, 28.2, 126.0, 27.9, 125.5, 27.5, 125.2, 26.7, 125.1, 26.1, 125.2, 25.6, 125.4, 25.2, 125.9, 25.1, 126.5, 25.2, 126.9, 25.6, 127.2, 26.1, 127.6, 26.8, 127.8, 27.5, 128.0, 28.2, 127.7, 29.2, 126.8, 30.6, 126.0, 32.0, 125.4, 33.8, 123.1, 36.8, 120.6, 38.1, 119.2, 38.8, 117.5, 38.9, 116.6, 39.9, 114.2, 40.7, 112.1, 41.9, 110.3, 42.5, 109.7, 43.3, 110.1, 44.0, 111.0, 44.7, 111.7, 45.5, 112.8, 46.3, 114.1, 46.7, 115.8, 47.2, 117.6, 48.0]
ts4 = [128.2, 14.2, 127.4, 14.4, 126.7, 14.7, 125.9, 15.2, 125.2, 15.9, 124.4, 16.5, 123.8, 16.8, 122.8, 17.0, 122.0, 17.1, 120.5, 17.3, 119.4, 17.4, 118.5, 17.8, 118.0, 18.4, 117.9, 18.7, 117.7, 19.1, 117.2, 19.2, 116.8, 19.4, 116.4, 19.6, 116.3, 19.8, 116.2, 19.9, 116.1, 20.0, 116.1, 20.1, 116.0, 20.2, 115.8, 20.6, 116.0, 21.0, 116.4, 21.5, 116.9, 21.8, 117.1, 22.0, 117.2, 22.3, 117.1, 22.5, 116.8, 22.6, 116.5, 22.7, 116.2, 22.4, 116.3, 22.2, 116.5, 22.1, 116.8, 22.0, 117.2, 22.0, 117.6, 22.2, 118.4, 22.9, 118.9, 23.8, 119.1, 24.9, 117.1, 27.0, 116.5, 28.1, 115.9, 29.0, 115.5, 29.5, 115.0, 30.0, 114.5, 30.5, 113.5, 31.3, 113.0, 32.2]
ts5 = [157.4, 8.7, 157.0, 8.8, 156.5, 8.9, 156.0, 9.2, 155.6, 9.4, 155.3, 9.8, 155.0, 10.3, 154.8, 10.8, 154.8, 11.2, 155.1, 11.8, 154.7, 12.3, 154.5, 12.9, 154.4, 13.1, 154.3, 13.2, 154.2, 13.2, 154.1, 13.3, 154.0, 13.6, 154.0, 13.8, 154.1, 14.2, 154.0, 15.1, 153.8, 15.8, 153.5, 16.6, 152.3, 17.8, 151.7, 19.2, 149.6, 20.8, 147.8, 21.7, 146.5, 22.5, 144.7, 23.8, 143.3, 24.7, 141.9, 25.8, 140.7, 27.3, 139.4, 28.6, 138.6, 29.5, 138.1, 30.3, 137.5, 31.5, 136.8, 33.0, 136.6, 34.8, 137.3, 37.7, 137.3, 38.8]

traj1 = [Point(ts1[i:i+2][0], ts1[i:i+2][1]) for i in range(0, len(ts1), 2)]
traj2 = [Point(ts2[i:i+2][0], ts2[i:i+2][1]) for i in range(0, len(ts2), 2)]
traj3 = [Point(ts3[i:i+2][0], ts3[i:i+2][1]) for i in range(0, len(ts3), 2)]
traj4 = [Point(ts4[i:i+2][0], ts4[i:i+2][1]) for i in range(0, len(ts4), 2)]
traj5 = [Point(ts5[i:i+2][0], ts5[i:i+2][1]) for i in range(0, len(ts5), 2)]

# part 1: partition
part1 = approximate_trajectory_partitioning(traj1, theta=6.0, traj_id=1)
part2 = approximate_trajectory_partitioning(traj2, theta=6.0, traj_id=2)
part3 = approximate_trajectory_partitioning(traj3, theta=6.0, traj_id=3)
part4 = approximate_trajectory_partitioning(traj4, theta=6.0, traj_id=4)
part5 = approximate_trajectory_partitioning(traj5, theta=6.0, traj_id=5)

all_segs = part1 + part2 + part3 + part4 + part5
print(len(all_segs))
norm_cluster, remove_cluster = line_segment_clustering(all_segs, min_lines=3, epsilon=20.0)
for k, v in remove_cluster.items():
    print("remove cluster: the cluster %d, the segment number %d" % (k, len(v)))

cluster_s_x, cluster_s_y = [], []
for k, v in norm_cluster.items():
    cluster_s_x.extend([s.start.x for s in v])
    cluster_s_x.extend([s.end.x for s in v])

    cluster_s_y.extend([s.start.y for s in v])
    cluster_s_y.extend([s.end.y for s in v])
    print("using cluster: the cluster %d, the segment number %d" % (k, len(v)))

source_line_x_1 = [p.x for p in traj1]
source_line_y_1 = [p.y for p in traj1]

source_line_x_2 = [p.x for p in traj2]
source_line_y_2 = [p.y for p in traj2]

source_line_x_3 = [p.x for p in traj3]
source_line_y_3 = [p.y for p in traj3]

source_line_x_4 = [p.x for p in traj4]
source_line_y_4 = [p.y for p in traj4]

source_line_x_5 = [p.x for p in traj5]
source_line_y_5 = [p.y for p in traj5]


fig = plt.figure(figsize=(9, 6))
ax = fig.add_subplot(111)
ax.plot(source_line_x_1, source_line_y_1, 'g--', lw=2.0, label="trajectory 1")
ax.scatter(source_line_x_1, source_line_y_1, c='g', alpha=0.5)
ax.plot(source_line_x_2, source_line_y_2, 'r--', lw=2.0, label="trajectory 2")
ax.scatter(source_line_x_2, source_line_y_2, c='r', alpha=0.5)
ax.plot(source_line_x_3, source_line_y_3, 'b--', lw=2.0, label="trajectory 3")
ax.scatter(source_line_x_3, source_line_y_3, c='b', alpha=0.5)
ax.plot(source_line_x_4, source_line_y_4, 'y--', lw=2.0, label="trajectory 4")
ax.scatter(source_line_x_4, source_line_y_4, c='y', alpha=0.5)
ax.plot(source_line_x_5, source_line_y_5, 'y--', lw=2.0, label="trajectory 5")
ax.scatter(source_line_x_5, source_line_y_5, c='y', alpha=0.5)

for k, v in norm_cluster.items():
    for s in v:
        _x = [s.start.x, s.end.x]
        _y = [s.start.y, s.end.y]
        if s.traj_id == 1:
            ax.plot(_x, _y, c='k', lw=3.0, alpha=0.7)
        elif s.traj_id == 2:
            ax.plot(_x, _y, c='c', lw=3.0, alpha=0.7)
        elif s.traj_id == 3:
            ax.plot(_x, _y, c='m', lw=3.0, alpha=0.7)
        else:
            ax.plot(_x, _y, c='r', lw=3.0, alpha=0.7)
ax.scatter(cluster_s_x, cluster_s_y, c='k', alpha=0.5, s=80, label="cluster")

main_traj_dict = representative_trajectory_generation(norm_cluster, min_lines=2, min_dist=1.0)
for c, v in main_traj_dict.items():
    v_x = [p.x for p in v]
    v_y = [p.y for p in v]
    ax.plot(v_x, v_y, 'r-', lw=4.0, label="cluster_%d_main_trajectory" % c)

ax.legend()
plt.savefig("./figures/trajectory-major.png", dpi=400)
plt.show()



