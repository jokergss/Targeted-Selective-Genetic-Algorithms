from math import *
from constant_num import *

time_local_compute = 0
time_edge_upload = 0
time_edge_compute = 0
time_edge_down = 0
time_center_upload = 0
time_center_compute = 0
time_Center_down = 0

# 计算策略和任务对应的时延
def compute_time(state, size):
    if state == 0:
        time = size / Local_CPU_frequency
    else:
        if state == 1:
            time = size / transport_rating + size / Edge_CPU_frequency + 0.1 * size / transport_rating
        else:
            time = size / transport_rating + size / transport_rating + size / Center_CPU_frequency + 0.1 * size / transport_rating + 0.1 * size / transport_rating

    return time

# 本来是想定义几个时间变量的，但后续没用到，不予理会即可
def settime(state,size):
    if state == 0:
        time_local_compute = (size / Local_CPU_frequency)
    else:
        if state == 1:
            time_edge_upload = (size/transport_rating)
            time_edge_compute = (size/Edge_CPU_frequency)
            time_edge_down = (0.1*size/transport_rating)
        else:
            time_center_upload = (size/transport_rating + size/transport_rating)
            time_center_compute = (size / Center_CPU_frequency)
            time_Center_down = (0.1*size/transport_rating + 0.1*size/transport_rating)

# 计算策略和任务对应的能耗
def compute_energy(state, size):
    total_time = compute_time(state,size)
    if state == 0:
        energy = (size / Local_CPU_frequency) * Local_work_consumption + (size / Local_CPU_frequency)*(Edge_freeze_consumption+Center_freeze_consumption)
    else:
        if state == 1:
            energy = (size /transport_rating)*Local_work_consumption + (total_time-(size/transport_rating))*Local_freeze_consumption+ \
                     (size/Edge_CPU_frequency)*Edge_work_consumption + (0.1*size/transport_rating)*Edge_work_consumption + (total_time-(size/Edge_CPU_frequency)-(0.1*size/transport_rating))*Edge_freeze_consumption + \
                     total_time*Center_freeze_consumption
        else:
            energy = (size/transport_rating)*Local_work_consumption + (total_time-size/transport_rating)*Local_freeze_consumption + \
                     (1.1*size /transport_rating)*Edge_work_consumption + (total_time -(1.1*size/transport_rating))*Edge_freeze_consumption + \
                     ((size / Center_CPU_frequency) + 0.1*size/transport_rating)*Center_work_consumption + (total_time-((size / Center_CPU_frequency) + 0.1*size/transport_rating))*Center_freeze_consumption

    return energy/1000  #单位时mW，转换为W对应的单位

# 计算综合的时延和能耗
def compute_cost(state,size):
    testtime = compute_time(state,size)
    testenergy = compute_energy(state,size)
    cost = 0.5*testtime+0.5*testenergy

    return cost

# 计算适应度，为了让适应度稍稍大一点，取了100除以cost的值作为适应度
def compute_fitness(cost):
    if cost != 0 :
        return 100/cost