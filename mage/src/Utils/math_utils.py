def percentage_difference(old_value, new_value):
    try:
        return ((new_value - old_value) / old_value)
    except ZeroDivisionError:
        return "Cannot calculate percentage difference when the average is zero."