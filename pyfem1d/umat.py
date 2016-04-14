from collections import OrderedDict
import inspect

class Umat:
    parameter_values = []
    parameter_names = []

    def __init__(self):
        pass

    def initial_cond(self, n_elem):
        pass

    def update(self):
        pass

    def stress_tangent(self, dt, n, eps):
        raise Exception("Stress-tangent function of umat not defined")

    def set_parameter_values(self, values):
        pass

def deploy_umats(path):
    local_ret = globals()
    # local_ret = {}
    global_ret = globals()
    with open(path) as f:
        code = compile(f.read(), path, 'exec')
        exec(code, global_ret, local_ret)

    # globals().update(global_ret)

    # globals().update(local_ret)

    result = {}
    try:
        for key, i in local_ret.items():
            # print(key, i.__class__)
            if inspect.isclass(i):
                if issubclass(i, Umat) and key != "Umat":
                    # print(key, i)
                    result[key] = i
    except Exception as e:
        raise Exception("There was an error in the config %s:\n%s"%(path, str(e)))

    # Sort the result dict according to the keys alphabetically
    result = OrderedDict(sorted(result.items(), key=lambda t: t[0]))
    return result
