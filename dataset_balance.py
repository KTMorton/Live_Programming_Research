import random
right_counter = 0
dataset = []


for i in range(30000):
    point1 = [0, 0, 0]
    dist = [0.5, 0.64, 0.18]
    for i in range(3):
        p1 = random.uniform(0, 1)
        if p1 < dist[i]:
            point1[i] = 1

    dataset.append(point1)


arr_sum = dataset[0]

new_data = []


toggle = True
counter = 0
while toggle:
    print(arr_sum)
    min_index = arr_sum.index(min(arr_sum))
    for i, element in enumerate(dataset):
        if i != 0:
            if element[min_index] == 1:
                new_data.append(element)
                arr_sum = [x + y for x, y in zip(arr_sum, element)]
                dataset.pop(i)
                break
            elif i == len(dataset)-1 and element[min_index] != 1:
                toggle = False
print(arr_sum)
print(len(new_data))



