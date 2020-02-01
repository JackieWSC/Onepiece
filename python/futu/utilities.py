from inspect import currentframe


def get_line_number():
    cf = currentframe()
    return cf.f_back.f_lineno


class Logger:
    log_level_type_list = ['Info', 'L1', 'L2', 'L3', 'Warning']
    log_level_on = 'Info Warning'

    @classmethod
    def log_trace(cls,  log_level, function_name, line_number, log):
        for log_level_type in cls.log_level_type_list:
            if (log_level in log_level_type) and (log_level_type in cls.log_level_on):
                print("Log Trace - {0}: {1} (Line Number:{2})\n{3}\n".format(
                    log_level,
                    function_name,
                    line_number,
                    log))
