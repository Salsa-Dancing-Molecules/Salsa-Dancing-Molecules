from config_module import read_configuration, generate_JSON

M = read_configuration('config.cfg')

print(M)
for i in M.keys():
    M[i] = list(M[i])
