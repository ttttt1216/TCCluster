# 2022-08-25
# Zhenshiyi Tian

import numpy as np

from trajCluster.partition import approximate_trajectory_partitioning, segment_mdl_comp, rdp_trajectory_partitioning
from trajCluster.point import Point
from trajCluster.cluster import line_segment_clustering, representative_trajectory_generation

from matplotlib import pyplot as plt

if __name__ == '__main__':
    ts = {}
    traj = {}
    ts_number = []
    with open(r'../_coordination.txt', "r") as f:
        for key in range(1, 1164, 1):
            ts_number.append(key)
            header = f.readline().split()
            ts[key] = list(map(float, header))
    for key in ts_number:
        traj[key] = [Point(ts[key][i:i + 2][0], ts[key][i:i + 2][1]) for i in range(0, len(ts[key]), 2)]

    # part 1: partition
    all_segs = []
    for key in ts_number:
        # 如果两个点重合，就会报错??? 但是去掉之后还是会报错QAQ
        print(key)
        print(traj[key])
        if key == 225 :
            continue
        all_segs += approximate_trajectory_partitioning(traj[key], theta=6.0, traj_id=key)

    norm_cluster, remove_cluster = line_segment_clustering(all_segs, min_lines=2, epsilon=15.0)
    for k, v in remove_cluster.items():
        print("remove cluster: the cluster %d, the segment number %d" % (k, len(v)))

    cluster_s_x, cluster_s_y = [], []
    for k, v in norm_cluster.items():
        cluster_s_x.extend([s.start.x for s in v])
        cluster_s_x.extend([s.end.x for s in v])

        cluster_s_y.extend([s.start.y for s in v])
        cluster_s_y.extend([s.end.y for s in v])
        print("using cluster: the cluster %d, the segment number %d" % (k, len(v)))

    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_subplot(111)

    main_traj_dict = representative_trajectory_generation(norm_cluster, min_lines=2, min_dist=1.0)
    for c, v in main_traj_dict.items():
        v_x = [p.x for p in v]
        v_y = [p.y for p in v]
        ax.plot(v_x, v_y, lw=4.0, label="cluster_%d_main_trajectory" % c)

    ax.legend()
    plt.savefig("./figures/trajectory-major.png", dpi=400)
    plt.show()
