
#Nested dict 

def walk_dict_leaf(dict_data):
    '''
    The yield content is (_keys,_val).
    https://anjingwd.github.io/AnJingwd.github.io/2017/08/19/%E5%A6%82%E4%BD%95%E4%BC%98%E9%9B%85%E7%9A%84%E7%94%9F%E6%88%90python%E5%B5%8C%E5%A5%97%E5%AD%97%E5%85%B8/
    '''
    for _key,_val in dict_data.items():
        if isinstance(_val,dict):
            for tup in walk_dict_leaf(_val):
                yield (_key,)+tup
        else:
            yield _key,_val

def get_dict_val(dict_data,node_path):
    '''
    dict_data: The dictionary data. The dict's sub node is a dict too.
    node_path: The array to give the path to the node. eg. ["conf","system","nodename"]
    '''
    if len(node_path)>1:
        return get_dict_val(dict_data[node_path[0]],node_path[1:])
    else:
        return dict_data[node_path[0]]

def set_dict_val(dict_data,node_path,val):
    '''
    dict_data: The dictionary data. The dict's sub node is a dict too.
    node_path: The array to give the path to the node. eg. ["conf","system","nodename"]
    val:       The val will be set to the node.
    '''
    if len(node_path)>1:
        return set_dict_val(dict_data[node_path[0]],node_path[1:],val)
    else:
        dict_data[node_path[0]] = val
        return


def is_dict_in(dict_little,dict_big):
    '''
    Check all dict_little elements in dict_b.
    '''
    for _leaf in walk_dict_leaf(dict_little):
        try:
            _keys = _leaf[0:-1]
            _val  = _leaf[-1]
            val = get_dict_val(dict_big,_keys)
            if val == _val:
                continue
            else:
                print("Not match leaf node:",_leaf,dict_big)
                return False
        except Exception as e:
            print(e)
            return False
    return True
        
def is_dict_equal(dict_a, dict_b):
    return is_dict_in(dict_a, dict_b) and is_dict_in(dict_b,dict_a)