def vote(votes):
    d = {}
    for v in votes:
        d.setdefault(v, 0)
        d[v] += 1
    sorted_by_count = sorted(d.items(), key=lambda a: a[1], reverse=True)
    return sorted_by_count[0][0]


if __name__ == '__main__':
    print(vote([1, 1, 1, 2, 3]))
    print(vote([1, 2, 3, 2, 2]))
