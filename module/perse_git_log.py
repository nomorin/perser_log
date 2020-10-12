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

COMMIT_ID = 'commit '
STATUS_ADD = 'A	'
STATUS_MOD = 'M	'
STATUS_DEL = 'D	'
GIT_AUTHOR = 'Author: '
GIT_DATE = 'Date:   '

path = './input/test.log'

# gitのlogファイルを読み込む.
array_commit_info = []
with open(path, encoding='CP932') as git_log_file:
    data = git_log_file.readlines()

comment = ''
for item in data:
    # 末尾の改行コードを削除.
    item = item.replace('\n', '')

    # ファイルの変更履歴を取得.
    file_status = item[0:2]

    if COMMIT_ID in item:
        # コミットのハッシュIDを取得.
        commit_id = item.replace(COMMIT_ID, '')

    elif GIT_AUTHOR in item:
        # コミットしたユーザー情報を取得.
        author_tmp = item.replace(GIT_AUTHOR, '')
        # メールアドレス部分を削除.
        author = re.sub(' +<.*>', '', author_tmp)

    elif GIT_DATE in item:
        # コミット日時を取得.
        date = item.replace(GIT_DATE, '')
        comment_area = True

    elif file_status == STATUS_ADD or file_status == STATUS_MOD or file_status == STATUS_DEL:
        # Gitのステータスを除いたファイル名の取得.
        file_name = item[2:]
        # 出力用の配列に情報を保持.
        array_commit_info.append([commit_id, author, date, file_name, comment])

        # コメント情報をクリア.
        comment_area = False
        comment = ''

    elif comment_area:
        # コメントを取得.
        comment += re.sub(' *', '', item)


# フォルダが存在しない場合は作成する.
file_path = './output/'
if not os.path.exists(file_path):
    os.mkdir(file_path)

# CSV形式で出力.
output_filename = file_path + 'git_output.csv'
with open(output_filename, 'w') as f:
    writer = csv.writer(f)

    # ヘッダ情報を出力.
    writer.writerow(['COMMIT_ID', 'AUTHOR', 'DATE', 'COMMIT_FILE_NAME', 'Comment'])

    # コミット情報を出力.
    for line_data in array_commit_info:
        writer.writerow(line_data)

