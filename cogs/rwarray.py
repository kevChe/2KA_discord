def write_array(file, array):
    with open(file, 'w') as f:
        for item in array:
            f.write(f'{item}\n')

def read_array(file):
    array = []
    with open(file, 'r') as f:
        for line in f:
            array.append(line[:-1])
    return array

#messages = [1036671342361190410, 1037033275899781230, 1037397736686882846, 1037758428984123452, 1038120439253303307,  1038482827353800755, 1038845215294881862]
