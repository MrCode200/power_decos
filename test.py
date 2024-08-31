import power_decos as pd

pd.log_decorator.init_logger(log_in_terminal=True, log_in_file=True, log_file_in_json=True, use_rotating_file_handler=True)

@pd.log_decorator.log_func()
def func_log():
    return "hello"

func_log()
pd.log_info("testing log_info")


