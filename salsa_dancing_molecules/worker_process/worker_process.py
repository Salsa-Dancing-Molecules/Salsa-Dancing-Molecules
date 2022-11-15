import os


def start(path):
    while len(os.listdir(path+"/input")) != 0:
        list_of_files = os.listdir(path+"/input")
        current_file = list_of_files[0]
        try:
            os.rename(path+"/input/"+current_file, path+"/started/"+current_file)
        except FileNotFoundError as e:
            print(e)
        except FileExistsError as e:
            print(e)
        else:
            try:
                # handle infile(s)
                # run simulation
                pass
            except Exception as e:
                filename = os.path.splitext(current_file)[0]+"_error.txt"
                f = open(filename, 'w')
                f.write(e)
                f.close()
            else:
                os.rename(path+"/started/"+current_file, path+"/done/"+current_file)