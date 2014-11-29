# coding: utf-8
import sys
from niconico_ctrl import NicoCtrl
import json

def main(argvs, argc):
    if len(argvs) != 4:
        print ('python nicolive.py email pass lv142315925')
        return 1
    nicovideo_id = argvs[1]
    nicovideo_pw = argvs[2]
    move_id = argvs[3]

    t = NicoCtrl(nicovideo_id, nicovideo_pw)
    chats = t.get_live_comment(move_id)
    f = open(move_id + '.json', 'w')
    f.write(json.dumps(chats))
    f.close()
    return 0

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))
