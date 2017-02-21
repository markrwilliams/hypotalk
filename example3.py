from hypothesis import stateful


class ExampleStateMachine(stateful.RuleBasedStateMachine):
    def __init__(self):
        super(ExampleStateMachine, self).__init__()
        self.n = 37

    @stateful.precondition(lambda self: self.n % 2 == 0)
    @stateful.rule()
    def even(self):
        self.n //= 2
        print("even, self.n = {}".format(self.n))

    @stateful.precondition(lambda self: self.n % 2 != 0)
    @stateful.rule()
    def odd(self):
        self.n = 3 * self.n + 1
        print("odd, self.n = {}".format(self.n))


TestCase = ExampleStateMachine.TestCase
