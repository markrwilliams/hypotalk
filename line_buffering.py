import pytest
from hypothesis import stateful, strategies


class NoLine(Exception):
    pass


class BuffersLines(object):
    def __init__(self):
        self._buffer = []

    def feed(self, data):
        self._buffer.append(data)

    def readline(self):
        for i, chunk in enumerate(self._buffer, 1):
            if b"\n" in chunk:
                break
        else:
            raise NoLine
        line_chunks, self._buffer = self._buffer[:i], self._buffer[i:]
        line, nl, chunk = b"".join(line_chunks).partition(b"\n")
        return line + nl


def partial_byte_lines():
    return strategies.binary().map(lambda bs: bs.replace(b'\n', ''))


class BuffersLineStateMachine(stateful.RuleBasedStateMachine):

    def __init__(self):
        super(BuffersLineStateMachine, self).__init__()
        self.line_buffer = BuffersLines()
        self.partials = []
        self.completes = []

    @stateful.rule(partial=partial_byte_lines())
    def feed_partial(self, partial):
        self.partials.append(partial)
        self.line_buffer.feed(partial)

    @stateful.rule(complete=partial_byte_lines().map(lambda bs: bs + b'\n'))
    def feed_complete(self, complete):
        self.partials.append(complete)
        self.completes.append(''.join(self.partials))
        self.partials = []
        self.line_buffer.feed(complete)

    @stateful.precondition(lambda self: self.completes)
    @stateful.rule()
    def readline_has_complete(self):
        assert self.line_buffer.readline() == self.completes.pop(0)

    @stateful.precondition(lambda self: not self.completes)
    @stateful.rule()
    def readline_has_partial(self):
        with pytest.raises(NoLine):
            self.line_buffer.readline()


TestBuffersLines = BuffersLineStateMachine.TestCase
