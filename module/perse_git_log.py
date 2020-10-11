# git log を整形する.
# --pretty=format:"%H,%an,%ae,%ad,%s,%f" ではファイル名称が取得できなかったので
# 一度ログを出力した上で整形を行う.
#
# 想定するログの取得コマンド.
"""
git --no-pager log --name-status --no-merges --all \
--date-order --date=format:'%Y/%m/%d %H:%M:%S' > git.log
"""
import re
import csv
import os
import configparser

ini_file = configparser.ConfigParser()
ini_file.read('./config/settings.ini', 'UTF-8')

# 環境ファイルの読み込み設定.
env = 'DEFAULT'
# env = 'JP'

COMMIT_ID = ini_file.get(env, 'COMMIT_ID')
STATUS_ADD = ini_file.get(env, 'STATUS_ADD')
STATUS_MOD = ini_file.get(env, 'STATUS_MOD')
STATUS_DEL = ini_file.get(env, 'STATUS_DEL')
GIT_AUTHOR = ini_file.get(env, 'GIT_AUTHOR')
GIT_DATE = ini_file.get(env, 'GIT_DATE')

# 処理対象のログファイルのパス.
if env == 'DEFAULT':
    path = './input/git.log'
else:
    path = './input/git_log_jp.log'

# gitのlogファイルを読み込む.
array_commit_info = []
with open(path) as git_log_file:
    data = git_log_file.readlines()

for item in data:
    # 末尾の改行コードを削除.
    item = item.replace('\n', '')

    if COMMIT_ID in item:
        # コミットのハッシュIDを取得.
        # commit_id = item.replace(COMMIT_ID, '')
        commit_id = re.sub('.*: ', '', item)

    elif GIT_AUTHOR in item:
        # コミットしたユーザー情報を取得.
        author_tmp = item.replace(GIT_AUTHOR, '')
        # メールアドレス部分を削除.
        author = re.sub(' +<.*>', '', author_tmp)

    elif GIT_DATE in item:
        # コミット日時を取得.
        # date = item.replace(GIT_DATE, '')
        date = re.sub('.*: ', '', item)

    else:
        # ファイルの変更履歴を取得.
        if STATUS_ADD in item or STATUS_MOD in item or STATUS_DEL in item:
            # Gitのステータスを除いたファイル名の取得.
            file_name = re.sub('.*: ', '', item)
            # 出力用の配列に情報を保持.
            array_commit_info.append([commit_id, author, date, file_name])

print(array_commit_info)

# 出力先が存在しない場合は作成する.
file_path = './output/'
if not os.path.exists(file_path):
    os.mkdir(file_path)

# CSV形式で出力.
output_filename = file_path + 'git_output.csv'
with open(output_filename, 'w') as f:
    writer = csv.writer(f)

    # ヘッダ情報を出力.
    writer.writerow(['COMMIT_ID', 'AUTHOR', 'DATE', 'COMMIT_FILE_NAME'])
    for line_data in array_commit_info:
        # コミット情報を出力.
        writer.writerow(line_data)

