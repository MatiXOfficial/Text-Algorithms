from bisect import bisect

def lcs(x, y):
    ranges = []
    ranges.append(len(y))
    y_letters = list(y)
    for i in range(len(x)):
        positions = [j for j, l in enumerate(y_letters) if l == x[i]]
        positions.reverse()
        for p in positions:
            k = bisect(ranges, p)
            if k == bisect(ranges, p - 1):
                if k < len(ranges) - 1:
                    ranges[k] = p
                else:
                    ranges.insert(k, p)
    return len(ranges) - 1