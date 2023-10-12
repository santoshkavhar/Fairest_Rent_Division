
def validate_values(values):
    sums = []
    for i in values:
        row_sum = 0
        for j in values[i]:
            element = values[i][j]
            # print(element)
            if int(element) < 0:
                print("Error: Negative element found!")
                return False
            row_sum += int(element)
        sums.append(row_sum)
    return all(x==sums[0] for x in sums)