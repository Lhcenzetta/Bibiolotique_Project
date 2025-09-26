from data import utilisateurs,aime_livres
list = []
i = 0
while i < len(utilisateurs):
    list.append(utilisateurs[i][3])
    i += 1
# print(list)
def check_age(x):
    if x > 18:
        return True
    else :
        return False

valid_list = filter(check_age ,list)
# print(tuple(valid_list))

def ressemble_names(first_name, second_name):
    return first_name + " " + second_name

def send_data():
    i = 0
    name_list = []
    check_name = []
    while i < len(utilisateurs):
        check_name = ressemble_names(utilisateurs[i][1],utilisateurs[i][2])
        name_list.append(check_name)
        i += 1
        # print(check_name)
    return name_list

# print(tuple(name_list))
def separe_livers(name_list,Livre):
    i = 0
    dict = {}
    while i < len(aime_livres):
        dict[name_list[i]] = Livre[i][1]
        i += 1
    return dict
name_list = send_data()
dict = separe_livers(name_list,aime_livres)
print(dict)