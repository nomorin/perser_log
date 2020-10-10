# git log を整形する

import re
import csv

START_POSITION = 'commit '
STATUS_ADD = 'A	'
STATUS_MOD = 'M	'
STATUS_DEL = 'D	'
GIT_AUTHOR = 'Author: '
GIT_DATE = 'Date:   '

path = './git.log'

# gitのlogファイルを読み込む.
with open(path) as git_log_file:
    data = git_log_file.readlines()
    print(data)

for item in data:
    # 末尾の改行コードを削除.
    item = item.replace('\n', '')

    if START_POSITION in item:
        # コミットのハッシュIDを取得.
        array_commit_info = []
        commit_id = item.replace(START_POSITION, '')

    elif GIT_AUTHOR in item:
        author = item.replace(GIT_AUTHOR, '')

    elif GIT_DATE in item:
        date = item.replace(GIT_DATE, '')

    else:
        # ファイルの変更履歴を取得する.
        s = item[0:2]
        if s == STATUS_ADD or s == STATUS_MOD or s == STATUS_DEL:
            # Gitのステータスを除いたファイル名の取得.
            file_name = item[2:]
            commit_info = [commit_id, author, date, file_name]
            print(commit_info)
