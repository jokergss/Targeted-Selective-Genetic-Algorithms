import random
from calculation import *
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

# 随机生成任务
def gettask():
    task = []
    for i in range(10):
        task.append(random.randint(5, 20))
    return task

# 全部本地计算
def full_local_compute(t=[]):
    test_task = t
    total_cost=0
    if test_task == []:
        # print("no task,please check")
        return 0
    for i in range(10):
        a=test_task[i]
        total_cost= total_cost+compute_cost(0,a)
    return total_cost


# 随机卸载
# 取随机数函数
def p_random(arr1,arr2):
    assert len(arr1) == len(arr2), "Length does not match."
    assert sum(arr2) == 1 , "Total rate is not 1."

    sup_list = [len(str(i).split(".")[-1]) for i in arr2]
    top = 10 ** max(sup_list)
    new_rate = [int(i*top) for i in arr2]
    rate_arr = []
    for i in range(1,len(new_rate)+1):
        rate_arr.append(sum(new_rate[:i]))
    rand = random.randint(1,top)
    data = None
    for i in range(len(rate_arr)):
        if rand <= rate_arr[i]:
            data = arr1[i]
            break
    return data

# 随机生成一个策略
def make_random_strategy():
    plist = []
    for i in range(10):
        plist.append( p_random([0,1,2],[1/3,1/3,1/3]))
# print(plist)
    return plist

# 判断策略是否符合规则
def judge_strategy(list=[]):
    judge_list=list
    if judge_list == []:
        # print("no strategy!remake a new one")
        return 0
    one_num = 0
    two_num = 0
    for i in range(10):
        if judge_list[i]==1:
            one_num+=1
        if judge_list[i]==2:
            two_num+=1
    if one_num>4 or two_num>4:
        # print("over the MAX NUM,please remake")
        return 0
    return 1

# 当有策略list和任务list时，可以直接调用这个函数求出总体的cost值
def has_strategy_compute(strategy=[],task=[]):
    test_task = task
    test_strategy=strategy
    total_cost = 0
    if test_task == []:
        # print("no task,please check")
        return 0
    if test_strategy == []:
        # print("no task,please check")
        return 0
    for i in range(10):
        a = test_strategy[i]
        b = test_task[i]
        total_cost = total_cost + compute_cost(a, b)
    return total_cost


#遗传算法相关
# 原版的单断点式交叉生成新染色体
def crossover(F_chromosome = [],M_chromosome = []):
    if F_chromosome==[] or M_chromosome==[]:
        return F_chromosome
    new_chromosome=[]
    is_bad_chromosome=0
    cycle_times = 0
    while is_bad_chromosome == 0:
        cycle_times += 1
        if(cycle_times>20):
            return F_chromosome
        place=random.randint(1,8)
        # print(place)
        for i in range(place):
            new_chromosome.append(F_chromosome[i])
        for i in range(10-place):
            new_chromosome.append(M_chromosome[place+i])
        is_bad_chromosome = judge_strategy(new_chromosome)
    return new_chromosome

# 在染色体的某一处发生变异，但发生变异后要保证仍为好染色体
def mutation ( chromosome = [] ):
    if chromosome==[]:
        return chromosome
    become_bad = 0
    cycle_times = 0
    while become_bad==0:
        cycle_times+=1
        if cycle_times >20 :
            return chromosome
        place = random.randint(0, 9)
        # state = random.randint(0,2)
        # print(place,state)
        origin_num = chromosome[place]
        if origin_num == 0:
            state = p_random([1, 2], [0.5, 0.5])
        elif origin_num == 1:
            state = p_random([0, 2], [0.5, 0.5])
        elif origin_num == 2:
            state = p_random([0, 1], [0.5, 0.5])
        chromosome[place] = state
        become_bad = judge_strategy(chromosome)
        if become_bad ==0:
            chromosome[place] = origin_num
    return chromosome

# 原版的遗传算法
def Genetic_algorithms (task=[]):
    if task == []:
        return 0
    chromosome_list = []
    max_cost = 0
    max_index = 0
    min_cost = 0
    min_index = 0
    fitness_list = []
    cycle_num = 0
    total_fitness = 0
    for i in range(50):
        zhuangtian = []
        while judge_strategy(zhuangtian) == 0:
            zhuangtian = make_random_strategy()
        chromosome_list.append(zhuangtian)
    for i in range(50):
        if max_cost == 0:
            max_cost = has_strategy_compute(chromosome_list[i], task)
            max_index = i
        elif max_cost < has_strategy_compute(chromosome_list[i], task):
            max_cost = has_strategy_compute(chromosome_list[i], task)
            max_index = i
        if min_cost == 0:
            min_cost = has_strategy_compute(chromosome_list[i], task)
            min_index = i
        elif min_cost > has_strategy_compute(chromosome_list[i], task):
            min_cost = has_strategy_compute(chromosome_list[i], task)
            min_index = i
    while cycle_num < 200:
        for i in range(50):
            test_cost = 0
            test_fitness = 0
            test_cost = has_strategy_compute(chromosome_list[i], task)
            test_fitness = compute_fitness(test_cost)
            fitness_list.append(test_fitness)
        total_fitness = sum(fitness_list)

        num = 0
        chouqu_fitness = 0
        mutate = 0

        mom_chromosome_index = 0
        num = random.randint(0, 100)
        chouqu_fitness = total_fitness * num * 0.01
        for i in range(50):
            chouqu_fitness = chouqu_fitness - fitness_list[i]
            if chouqu_fitness <= 0:
                mom_chromosome_index = i
                break
        dad_chromosome_index = 0
        num = random.randint(0, 100)
        chouqu_fitness = total_fitness * num * 0.01
        for i in range(50):
            chouqu_fitness = chouqu_fitness - fitness_list[i]
            if chouqu_fitness <= 0:
                dad_chromosome_index = i
                break

        probability = 0
        son_chromosome = []
        probability = random.randint(0,100)
        if probability <= 80:
            son_cost = 0
            son_index = 0
            son_chromosome = crossover(chromosome_list[dad_chromosome_index],chromosome_list[mom_chromosome_index])
            mutate = random.randint(0,100)
            if mutate <= 3:
                son_chromosome = mutation(son_chromosome)
            son_cost = has_strategy_compute(son_chromosome,task)
            if son_cost < max_cost :
                chromosome_list.pop(max_index)
                chromosome_list.insert(max_index,son_chromosome)
                son_index = max_index
                max_cost = 0
                max_index = 0
                if son_cost < min_cost :
                    min_cost = son_cost
                    min_index = son_index

            for i in range(50):
                if max_cost == 0:
                    max_cost = has_strategy_compute(chromosome_list[i], task)
                    max_index = i
                elif max_cost < has_strategy_compute(chromosome_list[i], task):
                    max_cost = has_strategy_compute(chromosome_list[i], task)
                    max_index = i
        cycle_num += 1
    # print(chromosome_list[min_index],min_cost)

    # print(chromosome_list[min_index],"\n")
    return min_cost
