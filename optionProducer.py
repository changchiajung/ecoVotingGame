'''
Used to Produce choices for game.

Division Profiles:
(1): 1,2,3,6,8
(2): 2,3,4,5,6
(3): 10,20,30,60,80
(4): 20,30,40,50,60

Rank Turnovers:
Small: A, B, C, D, E => B, C, A, E, D
Large: A, B, C, D, E => D, E, B, A, C
'''


def turnover(division, turnover):
    new_division = []
    for index in turnover:
        new_division.append(division[index])
    return new_division


def produce(division_list, turnover_sequence):
    result = []
    for origin in division_list:
        for alt in division_list:
            if origin != alt:
                for sequence in turnover_sequence:
                    pair = [origin, turnover(alt, sequence)]
                    result.append(pair)
    return result


def write_file(result, file_name):
    f = open(file_name, "w")
    for r in result:
        f.write(str(r)[1:-1]+"\n")

if __name__ == '__main__':
    division_list = [[1, 2, 3, 6, 8],
                     [2, 3, 4, 5, 6],
                     [10, 20, 30, 60, 80],
                     [20, 30, 40, 50, 60]]
    turnover_sequence = [[1, 2, 0, 4, 3], [3, 4, 1, 0, 2]]
    result = produce(division_list, turnover_sequence)
    write_file(result, "divisions.txt")