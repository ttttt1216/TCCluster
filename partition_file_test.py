from trajCluster.partition import approximate_trajectory_partitioning, segment_mdl_comp, rdp_trajectory_partitioning
from trajCluster.point import Point
from trajCluster.cluster import line_segment_clustering, representative_trajectory_generation

from matplotlib import pyplot as plt


def plot_traj(traj_list,label_name="test"):
    source_line_x = [p.x for p in traj_list]
    source_line_y = [p.y for p in traj_list]
    ax.plot(source_line_x, source_line_y, 'r--', lw=0.5, label="trajectory"+label_name)
    # ax.scatter(source_line_x, source_line_y, c='c', alpha=0.5)


if __name__ == "__main__":
    ts = {}
    traj = {}
    ts_number = []
    with open(r'G:/1TianZhenshiyi/myCode/_coordination.txt', "r") as f:
        for key in range(1, 244, 1):
            ts_number.append(key)
            header = f.readline().split()
            ts[key] = list(map(float, header))
    for key in ts_number:
        traj[key] = [Point(ts[key][i:i + 2][0], ts[key][i:i + 2][1]) for i in range(0, len(ts[key]), 2)]

    # 展示台风轨迹
    fig1 = plt.figure(1,figsize=(9, 6))
    ax = fig1.add_subplot(111)
    for key in ts_number:
        plot_traj(traj[key],label_name = str(key))

    # part 1: partition及展示部分
    all_segs = []
    for key in ts_number:
        all_segs += approximate_trajectory_partitioning(traj[key], theta=35, traj_id=key)

    for s in all_segs:
        _x = [s.start.x, s.end.x]
        _y = [s.start.y, s.end.y]
        ax.plot(_x, _y, c='c', lw=1.0, alpha=0.5)

    cluster_s_x, cluster_s_y = [], []
    cluster_s_x.extend([s.start.x for s in all_segs])
    cluster_s_x.extend([s.end.x for s in all_segs])
    cluster_s_y.extend([s.start.y for s in all_segs])
    cluster_s_y.extend([s.end.y for s in all_segs])
    ax.scatter(cluster_s_x, cluster_s_y, c='k', alpha=1, s=10, label="cluster")

    # ax.legend()
    plt.savefig("./figures/trajectory-major.png", dpi=400)
    plt.show()