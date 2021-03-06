from ..framework.application import Application
from ..framework.service import ServiceUser, LazySingletonServiceProvider
from ..framework.proc import Forker, Callback


class Greeter(ServiceUser):
    """
    A class, who's instances may greet a specific noun.
    """

    def __init__(self, name):
        assert isinstance(name, str)
        self.name = name.capitalize()

    def greet(self):
        print('Greetings and salutations, {name}!'.format(name=self.name))


class HelloApplication(Application):
    """
    Say hello!
    """
    name = None
    count = None

    def __init__(self):
        """
        Use this to perform any application initialization, such as registering custom services.
        """
        self.services.register(LazySingletonServiceProvider('greeter', Greeter, self.name))

    @staticmethod
    def help(parser):
        """
        Say "Hello, <name>!" as required.
        """
        parser.add_argument('name', help='To whom to say hello.')
        parser.add_argument('-c', '--count', type=int, help='The number of processes to fork.', default=1)

    def run(self):
        print(self.services.random.bytes(100))
        cb = Callback(self.services.greeter.greet)
        f = Forker(*(cb*self.count))
        f.fork()
