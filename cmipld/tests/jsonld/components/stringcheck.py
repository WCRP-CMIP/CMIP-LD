
def hyphenate(cls,value):
    assert '_' not in value
    return value


def maxlen(max):
    def maximum_length(cls,value):
        assert len(value) <= max
        return value
    return maximum_length