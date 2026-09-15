EXP = []
LOG = [0]

exp_dict = {}
log_dict = {}

value = 1
for i in range(256):
    exp_dict[i] = value
    value *= 2
    if(value > 255):
        value = value^285

for i in range(256):
    log_dict[exp_dict[i]] = i

for i in range(256):
    EXP.append(exp_dict[i])

for i in range(1,256):
    LOG.append(log_dict[i])

print(EXP)
print("\n")
print(LOG)

print("\n")
print(len(EXP))
print(len(LOG))