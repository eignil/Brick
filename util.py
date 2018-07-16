
def walk_dict(dict_data):
    #https://anjingwd.github.io/AnJingwd.github.io/2017/08/19/%E5%A6%82%E4%BD%95%E4%BC%98%E9%9B%85%E7%9A%84%E7%94%9F%E6%88%90python%E5%B5%8C%E5%A5%97%E5%AD%97%E5%85%B8/
    for _key,_val in dict_data.items():
        if isinstance(_val,dict):
            for tup in walk_dict(_val):
                yield (_key,)+tup
        else:
            yield _key,_val
