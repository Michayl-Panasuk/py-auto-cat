def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default

def items_to_names(items):
    newArr = []
    for item in items:
        newArr.append(item.name)
    return newArr


def filterArr(items, predicate):
    newArr = []
    i = 0
    for item in items:
        if predicate(item):
            newArr.append(item.name)
        i += 1
    return newArr


# def mapArray(items, mapper):
#     newArr = []
#     i = 0
#     for item in items:
#         newArr.append(mapper(item))
#         i += 1
#     return newArr


def findInArray(items, predicate):
    i = 0
    for item in items:
        if predicate(item):
            return item
        i += 1
    return