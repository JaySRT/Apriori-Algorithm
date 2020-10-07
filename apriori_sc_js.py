import sys
from itertools import permutations
from itertools import combinations
from typing import Dict

#How to run
#python <apriori_sc_js.py>  <dataset_file>  <Minimum Support>  <Minimum Confidence>
#Example python apriori_sc_js.py ds_grocery.txt 20 30

def print_items(freq_items,n):                              #Function with 2 args. arg1 is a set and arg2 is a number
    print("ooooooooooooooooooooooooooooooooooooooo")
    print("Selected itemsets after ",n," iteration")
    print("__Itemset__", "__Support__")
    print("ooooooooooooooooooooooooooooooooooooooo")
    print()
    for i in freq_items:
        print(i,round(freq_items[i]*100/total_txns,2),)    #This is the formula to calculate the support/confidence
    print()


def find_freq_items(nlist, few_items, set_items, n):       #This is a function with 4 args. 1-2-3 args are lists, arg 4 is a number.
    comb = combinations(nlist, n)                          #Getting combinations through arg1 and arg4
    item_support = {}                                      #Dictionery of count defined here
    for i in comb:                                         
        set_i = set(i)                                     #Making a set of unique items
        i=tuple(sorted(i))
        for j in set_items:                                #defined in main program     #'for' loop for arg3
            if set_i.issubset(j):
                if few_items:
                    count = 0
                    for k in few_items:                    #'for' loop for arg2
                        if k.issubset(set_i):
                            count = 1
                            break
                    if not count:                          #item_support_count was defined in this fn itself
                        if i in item_support:
                            item_support[i] += 1
                        else:
                            item_support[i] = 1
                else:
                    if i in item_support:
                        item_support[i] += 1
                    else:
                        item_support[i] = 1
    freq_set_dict = {}                                     #Defining this dict for loops in this fn itself
    few_item_list = []                                     #Defining this list to use it in this fn itself
    #print(item_support)
    if item_support:
        print("oooooooooooooooooooooooooooooo")
        print("Itemsets for ", n, "Iteration")
        print("oooooooooooooooooooooooooooooo")
        print()
        for i in item_support:                            #'for' loop for calculating support
            print(i,round(item_support[i]*100/total_txns,2))
            if (item_support[i]/total_txns)*100 >= min_supp:    #'if' condition for minimum support
                freq_set_dict[i] = item_support[i]
            else:
                few_item_list.append(set(list(i)))               #'else' store it in few list set
        print()
        if freq_set_dict:                                   #Using that dict here again
            print_items(freq_set_dict,n)
            support_all_items.update(item_support)          #Updating the dict with item support value
            association_rules(freq_set_dict)
            return freq_set_dict, few_item_list
    return None,None

def association_rules(freq_items):                         #arg of this fn is a dictionery
    for item_pair in freq_items.keys():
        print("Association Rule for Pair - ",item_pair)
        print("__Rule__","__Confidence__")
        item_size=len(item_pair)
        item_set=set(item_pair)
        while item_size-1>0:
            comb = combinations(item_pair, item_size-1)
            for i in comb:
                left_item=i
                right_item=tuple(item_set-set(i))
                item_confidence=round(support_all_items[item_pair]*100/support_all_items[left_item],2)
                if item_confidence>=min_conf:
                    print(left_item,"=>",right_item,item_confidence,"This Rule is Acceptable")
                else:
                    print(left_item,"=>",right_item,item_confidence,"This Rule is Rejected")

            item_size -=1
        print()

        
### Program Start from here ###
file_name = sys.argv[1]
file_object = open(file_name, "r")
lines = file_object.readlines()
all_txns = []
total_txns=0
support_all_items={}
min_supp = int(sys.argv[2])                        #Minimum support argument
min_conf = int(sys.argv[3])                        #Minimum support argument
c1 = {}  # type: Dict[str, int]
set_items = []                                     #List created for input in 2nd function
print("oooooooooooooooooo")
print("Input Transactions")
print("oooooooooooooooooo")
print()

for txns in lines:
    txns = txns.replace("\n", "")
    print(txns)
    all_txns.append("".join(txns.split(" ")[1].split(",")))
    seen = set()                                   #Declared a set here
    for i in "".join(txns.split(" ")[1:]).split(","):

        if (i,) in c1:
            c1[(i,)] += 1
        else:
            # print((i,),txns)
            c1[(i,)] = 1
        seen.add(i)
    set_items.append(seen)                         #Adding it to the Item set list
    total_txns+=1                                  #Total no. of txns
    # print(seen)
freq_items = {}
# print(c1)
few_set = []
print()
print("oooooooooooooooooooooooooo")
print("Item Sets", 1, "Iteration")
print("oooooooooooooooooooooooooo")
print()
for i in c1:
    print(i,round(c1[i]*100/total_txns))
    if (c1[i]/20)*100 >= min_supp:
        freq_items[i] = c1[i]
    else:
        few_set.append(set(i))
support_all_items.update(c1)
nlist =[item[0] for item in freq_items.keys()]   #This list is created for the loop below (using List Comprehension)

print()
print_items(freq_items,1)
item_count = 1
while len(nlist) > item_count:                   #This while loop will help us generate frequent item pairs
    freq_items1, few_set1 = find_freq_items(nlist, few_set, set_items, item_count + 1)
    if not freq_items1:
        break
    item_list = [items for item_groups in list(freq_items1.keys()) for items in item_groups]
    nlist = list(set(item_list))
    few_set = few_set1
    freq_items=freq_items1
    item_count += 1