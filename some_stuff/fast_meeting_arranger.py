import time

#SOLUTION 2 | TIME = 0.0001 sec 
def num(s):
    ns = s.replace(':', '')
    return int(ns)

def make_str(n):
    n = str(n)
    if len(n) == 3:
        return n[0] + ':' + n[1:]
    else:
        return n[:2] + ':' + n[2:]


def find_free_time(cal, db):
    free = []
    start = num(db[0])
    stop = num(db[1])
    if start < num(cal[0][0]):
        free.append([db[0], cal[0][0]])
    for i in range(len(cal) - 1):
        if cal[i][1] != cal[i+1][0]:
            free.append([cal[i][1], cal[i+1][0]])
    if stop > num(cal[-1][1]):
        free.append([cal[-1][1], db[1]])
    return free


def merge(cal1, cal2):
    s1 = len(cal1)
    s2 = len(cal2)
    i, j = 0, 0
    res = []

    def compare(per):
        begin = num(per[0])
        end = num(per[1])
        if res:
            last = num(res[-1][1])
            if begin <= last and end > last:
                res[-1][1] = per[1]
            if begin > last:
                res.append(per)
        else:
            res.append(per)

    while i < s1 or j < s2:
        begin1 = num(cal1[i][0])
        end1 = num(cal1[i][1])
        begin2 = num(cal2[j][0])
        end2 = num(cal2[j][1])

        if begin1 < begin2:
            compare(cal1[i])
            i += 1
        elif begin1 == begin2:
            if end1 > end2:
                compare(cal1[i])
            else:
                compare(cal2[j])
            i += 1
            j += 1
        else:
            compare(cal2[j])
            j += 1
          
        if i == s1:
            while j < s2:
                compare(cal2[j])
                j += 1
            break
        if j == s2:
            while i < s1:
                compare(cal1[i])
                i += 1
            break 


    return res


def main():
    #input
    cal1 = [['9:00', '10:30'], ['12:00', '13:00'], ['16:00', '18:00']]
    day_bounds1 = ['9:00', '20:00']
    cal2 = [['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['16:00', '17:00']]
    day_bounds2 = ['10:00', '18:30']

    time0 = time.time()
    #find common day bounds
    if num(day_bounds1[0]) >= num(day_bounds2[0]):
        start = day_bounds1[0]
    else:
        start = day_bounds2[0]

    if num(day_bounds1[1]) <= num(day_bounds2[1]):
        stop = day_bounds1[1]
    else:
        stop = day_bounds2[1]
    day_bounds = [start, stop]

    #periods when any is bussy
    busy = merge(cal1, cal2)
    print('\n'.join(map(str, find_free_time(busy, day_bounds))))
    
    #time measuring
    time1 = time.time()
    print(f'{round(time1 - time0, 4)} sec')

if __name__ == '__main__':
    main()

