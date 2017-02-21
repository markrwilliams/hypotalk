from hypothesis import stateful


class ExampleStateMachine(stateful.RuleBasedStateMachine):
    pass  # interesting stuff will go here!


TestCase = ExampleStateMachine.TestCase
