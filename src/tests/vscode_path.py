import psutil
import json


vscode_cwds = set()
env = {}

for proc in psutil.process_iter(['pid', 'name']):
    if "Code.exe" in proc.name():
        proc_env = proc.environ()


        for key, value in proc_env.items():
            if key in env:
                if type(env[key]) == set:
                    env[key].add(value)

                else:
                    if env[key] != value:
                        env[key] = set([env[key], value])


            else:
                env[key] = value

        # print(json.dumps(proc.environ(), indent=4, ensure_ascii=False))

        # if "VSCODE_CWD" in proc.environ():
        #     print(proc.environ()['VSCODE_CWD'])
            # vscode_cwds.add(proc.environ()['VSCODE_CWD'])



# for cwd in vscode_cwds:
#     print(cwd)


for key, value in env.items():
    if type(env[key]) == set:
        env[key] = list(env[key])

print(json.dumps(env, indent=4, ensure_ascii=False))