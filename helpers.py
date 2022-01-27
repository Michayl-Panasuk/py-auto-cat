def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def safeget(dct, *keys):
    for key in keys:
        try:
            dct = dct[key]
        except (KeyError, TypeError):
            return None
    return dct


def safeDictSet(dct, value, *keys):
    i = 0
    for key in keys:
        try:
            if i == (len(keys) - 1):
              dct[key] = value
            else:  
              test = dct[key]
        except (KeyError, TypeError):
            if i == (len(keys) - 1):
              dct[key] = value
            else:  
              dct[key] = {}
        i += 1
    return value;

def filterNoneInDict(dict):
  return {k: v for k, v in dict.items() if v is not None}


def items_to_names(items):
    newArr = []
    for item in items:
        newArr.append(item.name)
    return newArr


def forEach(items, cb):
    i = 0
    for item in items:
        cb(item, i)
        i += 1


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
