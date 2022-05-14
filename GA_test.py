from other_algorithm import *
import numpy as np

# 改进过后的交叉函数，根据任务保留最适合的基因，剩余空位在保证好策略的前提下补齐
def ModifiedCrossover(F_chromosome=[],M_chromosome=[],task=[]):
    if F_chromosome == [] or M_chromosome == [] or task == []:
        return F_chromosome
    son_chromosome = [0,0,0,0,0,0,0,0,0,0]
    sort_array = np.array([task[0],task[1],task[2],task[3],task[4],task[5],task[6],task[7],task[8],task[9]])
    sort_index = np.argsort(sort_array)
    sure_index_list = []
    for i in range(10):
        if i <= 1:
            if F_chromosome[sort_index[i]] == 0:
                son_chromosome[sort_index[i]] = 0
                sure_index_list.append(sort_index[i])
        elif i <= 5:
            if F_chromosome[sort_index[i]] == 2:
                son_chromosome[sort_index[i]] = 2
                sure_index_list.append(sort_index[i])
        else:
            if F_chromosome[sort_index[i]] == 1:
                son_chromosome[sort_index[i]] = 1
                sure_index_list.append(sort_index[i])
    for i in range(10):
        if i <= 1:
            if M_chromosome[sort_index[i]] == 0:
                son_chromosome[sort_index[i]] = 0
                sure_index_list.append(sort_index[i])
        elif i <= 5:
            if M_chromosome[sort_index[i]] == 2:
                son_chromosome[sort_index[i]] = 2
                sure_index_list.append(sort_index[i])
        else:
            if M_chromosome[sort_index[i]] == 1:
                son_chromosome[sort_index[i]] = 1
                sure_index_list.append(sort_index[i])
    num_one = 0
    num_two = 0
    for i in range(10):
        if son_chromosome[i] == 1:
            num_one += 1
        if son_chromosome[i] == 2:
            num_two += 1

    for i in range(10):
        is_existed = 0
        for j in range(len(sure_index_list)):
            if i == sure_index_list[j]:
                is_existed = 1
        if is_existed == 1:
            continue
        if num_one < 4 :
            son_chromosome[i] = 1
            num_one += 1
            continue
        elif num_two < 4:
            son_chromosome[i] = 2
            num_two += 1
            continue
        else:
            son_chromosome[i] = 0

    return son_chromosome

# 改进版本遗传算法，通过随机选取一个染色体和cost最小的染色体交叉生成儿子染色体
def ModifiedGA(task = []):
    if task ==[]:
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
        if max_cost < has_strategy_compute(chromosome_list[i],task):
            max_cost = has_strategy_compute(chromosome_list[i],task)
            max_index = i
        if min_cost == 0:
            min_cost = has_strategy_compute(chromosome_list[i],task)
            min_index = i
        elif min_cost > has_strategy_compute(chromosome_list[i],task):
            min_cost = has_strategy_compute(chromosome_list[i],task)
            min_index = i
    # print("初始时最大最小值：",max_cost,max_index,min_cost,min_index)
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

        # 交叉过程，其中有3%的概率生成的儿子染色体变异
        probability = 0
        son_chromosome = []
        probability = random.randint(0,100)
        if probability <= 80:

            son_cost = 0
            son_index = 0
            son_chromosome = ModifiedCrossover(chromosome_list[min_index],chromosome_list[mom_chromosome_index],task)
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
                if max_cost < has_strategy_compute(chromosome_list[i], task):
                    max_cost = has_strategy_compute(chromosome_list[i], task)
                    max_index = i
            # print("son的cost",son_cost,"最大的cost",max_cost,"最小的cost",min_cost,)
            # print("son的序号",son_index,"随后计算的最大cost的序号", max_index,"最小cost的序号", min_index)

        cycle_num += 1
    # print(chromosome_list[min_index],min_cost)
    # print(chromosome_list[min_index],"\n")
    return min_cost


# 主函数，调用所有算法测试生成cost并对比
local_cost_list = []
random_cost_list = []
GA_cost_list = []
ModifiedGA_cost_list = []
# Standard_cost_list = []
for epioside in range(10):
    sum_task = 0
    Task = []
    while sum_task < 140 or sum_task > 160:
        Task = gettask()
        sum_task = sum(Task)
    # print("任务大小：",Task)

    full_local_cost = 0
    full_local_cost = full_local_compute(Task)
    local_cost_list.append(full_local_cost)

    # Standard_cost_list.append(sum_task/2)


    # print("全本地计算花费：",full_local_cost)

    # 随机生成策略花费计算,因为随机性过高，可能导致随机出来的结果比迭代得到的策略还好，所以取1000个可能的策略的平均值
    random_strategy_list = []
    for i in range(1000):
        is_noway=0
        random_strategy = []
        while is_noway!=1:
            random_strategy=make_random_strategy()
            is_noway=judge_strategy(random_strategy)
        random_strategy_list.append(random_strategy)
    average_random_cost = 0
    for i in range(1000):
        average_random_cost = average_random_cost + has_strategy_compute(random_strategy_list[i],Task)
    average_random_cost = average_random_cost/1000
    random_cost_list.append(average_random_cost)

    # 普通版本遗传算法
    GA_least_cost=Genetic_algorithms(Task)
    GA_cost_list.append(GA_least_cost)

    # 改进版本遗传算法
    ModifiedGA_least_cost = ModifiedGA(Task)
    ModifiedGA_cost_list.append(ModifiedGA_least_cost)

print("全部本地计算花费：",local_cost_list)
print("随机卸载花费：",random_cost_list)
print("GA算法花费：",sum(GA_cost_list))
print("改进GA算法花费：",sum(ModifiedGA_cost_list))
# print("标准值对比：",Standard_cost_list)

# 通过画图来对比不同策略的结果
X=np.arange(len(local_cost_list))
bar_width = 0.2
tick_label = ['1','2','3','4','5','6','7','8','9','10']

#绘制柱状图
plt.bar(X, local_cost_list, bar_width, align="center", color="tomato", label="full local", alpha=0.5)
plt.bar(X+bar_width, random_cost_list, bar_width, color="darkorange", align="center",label="random", alpha=0.5)
plt.bar(X+bar_width+bar_width, GA_cost_list, bar_width, color="yellowgreen", align="center",label="GA", alpha=0.5)
plt.bar(X+bar_width+bar_width+bar_width, ModifiedGA_cost_list, bar_width, color="dodgerblue", align="center",label="TSGA", alpha=0.5)
# plt.bar(X, Standard_cost_list, bar_width, align="center", color="purple", label="Standard", alpha=0.5)

plt.xlabel("cycle_times")
plt.ylabel("total_cost")
plt.title("Algorithm comparison")
# X+bar_width
plt.xticks(X+bar_width, tick_label)
#显示图例
plt.legend()
# plt.savefig("Algorithm comparison.jpg")
plt.show()
