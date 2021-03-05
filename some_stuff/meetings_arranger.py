import time

#SOLUTION 1 | TIME = 0.0002 sec 
def make_num(s):
    s = s.replace(':', '')
    return int(s)

def make_str(n):
    n = str(n)
    if len(n) == 3:
        return n[0] + ':' + n[1:]
    else:
        return n[:2] + ':' + n[2:]


def find_free_time(cal, db):
    free = []
    start = make_num(db[0])
    stop = make_num(db[1])
    if start < make_num(cal[0][0]):
        free.append(range(start, make_num(cal[0][0])+1))
    for i in range(len(cal) - 1):
        if cal[i][1] != cal[i+1][0:]:
            free.append(range(make_num(cal[i][1]), make_num(cal[i+1][0])+1))
    if stop > make_num(cal[-1][1]):
        free.append(range(make_num(cal[-1][1]), stop+1))
    return free



def main():
    #input
    cal1 = [['9:00', '10:30'], ['12:00', '13:00'], ['16:00', '18:00']]
    day_bounds1 = ['9:00', '20:00']
    cal2 = [['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['16:00', '17:00']]
    day_bounds2 = ['10:00', '18:31']

    time0 = time.time()

    start = max(make_num(day_bounds1[0]), make_num(day_bounds2[0]))
    stop = min(make_num(day_bounds1[1]), make_num(day_bounds2[1]))
    day_bounds = range(start, stop)
    free1 = find_free_time(cal1, day_bounds1)
    free2 = find_free_time(cal2, day_bounds2)

    match = []
    for r in free1:
        rs = set(r)
        for r2 in free2:
            m = rs.intersection(r2)
            if len(m) > 1:
                match.append(m.intersection(day_bounds))

    result = []
    for per in match:
        result.append([make_str(min(per)), make_str(max(per))])
    
    print(result)

    time1 = time.time()
    print(f'{round(time1 - time0, 4)} sec')

if __name__ == '__main__':
    main()


