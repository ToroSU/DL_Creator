list_1 = ["A", "B", "C", "D", "E", "F", "G", "H"]
list_2 = ["1", "2", "3", "4", "5", "6", "7", "8"]
list_3 = ["x", "y", "z", "w", "n"]
list_4 = ["A", "B", "C", "C", "C", "C", "G", "H"]

# record the index of the element with the key
index_of_path_with_the_keyword = []
for i in range(0, len(list_4)):
    if "c" in list_4[i].lower(): 
        index_of_path_with_the_keyword.append(i)

# print(index_of_path_with_the_keyword)
insert_i = index_of_path_with_the_keyword[0] # 首個被紀錄的指標
del_i = index_of_path_with_the_keyword
del_i.reverse()


for i in del_i:
    del list_4[i]


# print(index_of_path_with_the_keyword)
# print(insert_i)
list_4[insert_i:insert_i] = list_3


print(list_4)