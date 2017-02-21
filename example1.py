from hypothesis import stateful


class ExampleStateMachine(stateful.RuleBasedStateMachine):

    @stateful.rule()
    def rule1(self):
        print("rule1")

    @stateful.rule()
    def rule2(self):
        print("rule2")


TestCase = ExampleStateMachine.TestCase
