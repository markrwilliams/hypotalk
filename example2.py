from hypothesis import stateful


class ExampleStateMachine(stateful.RuleBasedStateMachine):

    def __init__(self):
        super(ExampleStateMachine, self).__init__()
        self.calls = 0

    @stateful.rule()
    def rule1(self):
        self.calls += 1
        print("rule1, self.calls = {}".format(self.calls))

    @stateful.rule()
    def rule2(self):
        self.calls += 2
        print("rule2, self.calls = {}".format(self.calls))


TestCase = ExampleStateMachine.TestCase
