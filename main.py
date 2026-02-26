import sys
from virtual_memory import *

if __name__ == '__main__':

    init_path = sys.argv[1]
    va_path = sys.argv[2]
    out_path = sys.argv[3]

    demand_arg = sys.argv[4].lower()
    if demand_arg == "true":
        demand_paging = True
    elif demand_arg == "false":
        demand_paging = False

    run(
        init_path=init_path,
        va_path=va_path,
        out_path=out_path,
        demand_paging=demand_paging
    )