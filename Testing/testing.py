from datetime import datetime
from datetime import timedelta
from core_service import Parser
from Model.Transaction import Transaction
import cPickle as p
print str((datetime.now() + timedelta(days=2)).date())
#
# trans = Transaction("*", "CN", "P2P", "!ICBC", "LOCAL", "CN", "CNY")
#
# parser = Parser(trans)
#
# dic = parser.dumpRequiredFields()
#
#
# for k , v in dic.items():
#   print k.toString() + '\n' + str(v)


lst = "AU,CZ,SG".split(",")
empty = "".split(",")


print(lst)
print("\n")
print(empty)


t1 = Transaction()
t2 = Transaction()

s1 = p.dumps(t1)
s2 = p.dumps(t2)
print s1 == s2


print p.loads(s1).beneficiaryCountry


