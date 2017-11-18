import time
import datetime


class Context(object):
    def __enter__(self):
        self.start_time = datetime.datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Время выполнения кода в контекст менеджере - {}'.format(datetime.datetime.now() - self.start_time))

    @staticmethod
    def get_execution_time(_function):
        def get_arguments(*args, **kwargs):
            start = datetime.datetime.now()

            _function(*args, **kwargs)

            print('Время выполнения функции - {}'.format(datetime.datetime.now() - start))

        return get_arguments


context = Context()

with context as test:
    time.sleep(1)


@context.get_execution_time
def run_time_function(seconds):
    time.sleep(seconds)


run_time_function(3)
