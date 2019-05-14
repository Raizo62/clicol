from __future__ import print_function
from __future__ import unicode_literals
from builtins import input
import re

class HumanNumbers:
    loadonstart = True
    active = False

    def __init__(self, setup):
        self.regex = re.compile(r"(?<!MTU )(\d{1,3}(?=(?:\d{3})+(?!\d) (?:.*m)?(?:bytes|packets|pkts|bits|broadcasts|multicasts?|overrun|CRC|unknown protocol|(?:in|out)put errors)))", re.M)

    def postprocess(self, input = "", effects = []):
        if "cisco_interface" in effects or "test" in effects:
            return self.regex.sub(r"\1,", input)
        else:
            return input

    def test(self):
        return ("plugin.humannumbers", "\n postprocess:\n%s" % self.postprocess("     853297735 packets input, 545445115336 bytes, 0 no buffer","test"))
