from dedupe.fs import PathOp


class TestFs:
    def testHasChildOrIsSame(self):
        p = PathOp("this/that")
        assert p.hasChildOrIsSame("this/that")
        assert p.hasChildOrIsSame("this/that/then")

        assert not p.hasChildOrIsSame("this")
        assert not p.hasChildOrIsSame("this/then")
        assert not p.hasChildOrIsSame("that")
        assert not p.hasChildOrIsSame("then")


    def testDiff(self):
        diff = PathOp("one/two/three/four") - "one/two"
        assert diff == PathOp("three/four"), diff

        diff = PathOp("one/two") - "one/two/three"
        assert diff == None, diff

        diff = PathOp("one/two/three") - "one/two/four"
        assert diff == None, diff