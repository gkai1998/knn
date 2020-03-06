import random
import csv
import math
import operator


def Distance(train, test, dim):
    pingfanghe = 0
    for x in range(dim):
        pingfanghe += pow(train[x] - test[x], 2)
    distance = math.sqrt(pingfanghe)
    return distance


def caculate_k_neighbors(trainset, test, k):
    dim = len(test) - 1
    dist = []
    k_neighbors = []
    for x in range(len(trainset)):
        distance = Distance(trainset[x], test, dim)
        dist.append([trainset[x], distance])
    dist.sort(key=operator.itemgetter(1))  # 根据第二维排序
    for x in range(k):
        k_neighbors.append(dist[x][0])
    return k_neighbors


def vote(all_test_neighbors, k):
    pred = []
    for x in range(len(all_test_neighbors)):
        nvote = {}
        for y in range(k):
            key = all_test_neighbors[x][y][-1]
            if key not in nvote.keys():
                nvote[key] = 1
            else:
                nvote[key] += 1
        # print(nvote)
        Max = max(nvote, key=nvote.get)  # 获取最大value对应的key
        pred.append(Max)
    # print(pred)
    return pred


def prediction(testset, predict, way):
    test = []
    sum = 0
    for x in range(len(testset)):
        test.append(testset[x][-1])
    for y in range(len(test)):
        if (test[y] == predict[y]):
            sum += 1
    return way + "'accuracy is :%.4f" % (sum * 1.0 / len(test))


def read_data(way):
    data = []
    with open(way, 'r') as file:
        lines = csv.reader(file)
        for row in lines:
            data.append(row)
    testset = []
    trainset = []
    if (way == 'iris.data'):
        for x in range(len(data) - 1):
            for y in range(4):
                data[x][y] = float(data[x][y])
            if (random.random()) < 0.7:
                trainset.append(data[x])
            else:
                testset.append(data[x])
    elif (way == 'breast-cancer-wisconsin.data'):
        dele = []
        # print(len(data))
        for x in range(len(data) - 1):
            for y in range(10):
                if data[x][y] == '?':
                    dele.append(x)
        # print(dele)
        i = 0
        for x in dele:
            data.pop(x - i)
            i += 1
        for x in range(len(data) - 1):
            data[x] = data[x][1:]
            for y in range(9):
                data[x][y] = float(data[x][y])
            if (random.random()) < 0.7:
                trainset.append(data[x])
            else:
                testset.append(data[x])
    elif (way == 'wine.data'):
        for x in range(len(data) - 1):
            for y in range(1, 14):
                data[x][y] = float(data[x][y])
            data[x][0], data[x][-1] = data[x][-1], data[x][0]
            if (random.random()) < 0.7:
                trainset.append(data[x])
            else:
                testset.append(data[x])
    elif (way == 'abalone.data'):
        for x in range(len(data) - 1):
            for y in range(1, 9):
                data[x][y] = float(data[x][y])
            data[x][0], data[x][-1] = data[x][-1], data[x][0]
            if (random.random()) < 0.7:
                trainset.append(data[x])
            else:
                testset.append(data[x])
    elif (way == 'haberman.data'):
        for x in range(len(data) - 1):
            for y in range(3):
                data[x][y] = float(data[x][y])
            if (random.random()) < 0.7:
                trainset.append(data[x])
            else:
                testset.append(data[x])
    # print(testset)
    return testset, trainset


def main(way):
    k = 5
    testset, trainset = read_data(way=way)
    all_test_neighbors = []
    for x in range(len(testset)):
        all_test_neighbors.append(
            caculate_k_neighbors(trainset,
                                 testset[x], k))  # 三维列表
    # print(all_test_neighbors)
    predict = vote(all_test_neighbors, k)
    # print(predict)
    accu = prediction(testset, predict, way=way)
    print(accu)


if __name__ == '__main__':
    iris = 'iris.data'
    bcw = 'breast-cancer-wisconsin.data'
    wine = 'wine.data'
    abalone = 'abalone.data'
    haberman = 'haberman.data'
    main(iris)
    main(bcw)
    main(wine)
    main(abalone)
    main(haberman)
