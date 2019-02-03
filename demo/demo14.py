import getopt
a = "asdf asdf"
option,args = getopt.getopt(a,"","")
print(option,type(args))
