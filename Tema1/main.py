# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    my_list = [7, 8, 9, 2, 3, 1, 4, 10, 5, 6]
    my_ascend_list = my_list.copy()
    my_ascend_list.sort()
    print("Elementele listei in ordine crescatoare: ", my_ascend_list)
    my_descend_list = my_ascend_list.copy()
    my_descend_list.reverse()
    print("Elementele listei in ordine descrescatoare: ", my_descend_list)

    list_par = my_ascend_list[1::2]
    print("Elementele pare din lista: ", list_par)

    list_impar = my_ascend_list[::2]
    print("Elementele impare din list: ", list_impar)

    list_3 = my_ascend_list[2::3]
    print("Multiplii lui 3: ", list_3)




