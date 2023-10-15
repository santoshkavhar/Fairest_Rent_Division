def validate_values(values):

    sums = []

    # Iterate over row
    for row in values:

        row_sum = 0

        # Iterate over elements in the row
        for element in row:

            if int(element) < 0:
                print("Error: Negative element found!")
                return False
            row_sum += int(element)

        sums.append(row_sum)

    return all(x == sums[0] for x in sums)
