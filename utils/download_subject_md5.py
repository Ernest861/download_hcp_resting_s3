# encoding = utf-8
"""
@version:0.1
@author: jorian
@time: 2021/9/11  9:29
"""
#from conf import *
import boto3
import os
from pathlib import Path
from loguru import logger
import time
#from util import merge_subject_json

project_path = Path.cwd().parent
log_path = Path(project_path, "log")
out_dir = '../data/.xdlm/'
# out_dir = '/sharing01/sharedata_HCP/'
t = time.strftime("%Y_%m_%d")

access_key = ''
secret_key = ''
s3_bucket_name = 'hcp-openaccess'
s3_prefix = 'HCP_1200'

def download_subject_md5(subjects):
    logger.add(f'{log_path}/download_md5_info_{t}.log', rotation="500MB", encoding="utf-8", enqueue=True,
               compression="zip",
               retention="10 days", level="INFO")
    logger.add(f'{log_path}/download_md5_error_{t}.log', rotation="500MB", encoding="utf-8", enqueue=True,
               compression="zip",
               retention="10 days", level="ERROR")

    resource = boto3.resource('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    bucket = resource.Bucket(s3_bucket_name)

    time_start = time.time()
    files_downloaded = 0
    total_num_files = 55*1120
    actual_num_files = 0

    for subject in subjects:

        s3_keys = bucket.objects.filter(Prefix='HCP_1200/%s/.xdlm/' % subject)
        s3_keylist = [key.key for key in s3_keys]

        actual_num_files += len(s3_keylist)

        if not os.path.exists(out_dir):
            print('Could not find %s, creating now...' % out_dir)
            logger.warning(f'Could not find {out_dir}, creating now...')
            os.makedirs(out_dir)

        for path_idx, s3_path in enumerate(s3_keylist):
            # rel_path = s3_path.replace(s3_prefix, '')
            # rel_path = rel_path.lstrip('/')
            # download_file = os.path.join(out_dir, rel_path)
            download_file = os.path.join(out_dir, str(subject), s3_path.split('/')[-1])
            download_dir = os.path.dirname(download_file)
            # If downloaded file's directory doesn't exist, create it
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
            try:
                if not os.path.exists(download_file) or os.path.getsize(download_file) == 0:
                    # while file is empty
                    if os.path.exists(download_file):
                        if os.path.getsize(download_file) == 0:
                            print("%s is empty" % (s3_path))
                            logger.error("%s is empty" % (s3_path))

                    print('Downloading to: %s' % download_file)
                    bucket.download_file(s3_path, download_file)
                    files_downloaded += 1
                    print("FACTS: path: %s, file: %s" % (s3_path, download_file))
                    print('%.3f%% percent complete' % \
                          (100 * (float(path_idx + 1) / total_num_files)))
                    complete_percent = (100 * (float(path_idx + 1) / total_num_files))
                # elif os.path.getsize(download_file) == 0:
                #     print("%s is empty" % (s3_path))
                #     logger.error("%s is empty" % (s3_path))
                else:
                    print('File %s already exists, skipping...' % download_file)
            except Exception as exc:
                print('There was a problem downloading %s.\n' \
                      'Check and try again.' % s3_path)
                logger.error(f"There was a problem downloading {s3_path}. Check and try again.")
                print(exc)
                logger.error(exc)

        print('%d files have been downloaded.' % (files_downloaded))
        logger.info(f"{files_downloaded} files have been downloaded.")

    print('Done!')
    logger.info("DOne!")

    time_cost = (time.time() - time_start) / 60
    print("Actual total nums of md5 file is :{}".format(actual_num_files))

    print("Time cost of downloading all md5 file is :{} min".format(time_cost))
    logger.info(f"Time cost of downloading all md5 file is :{time_cost} h")

def merge_subject_json(subject, root_dir, out_dir):
    out_file = os.path.join(out_dir,str(subject) '_md5.json')
    paths = os.listdir(root_dir)
    count = 0  # 记录数据总条数

    merged_data = []
    for path in paths:
        file_path = os.path.join(root_dir, path)
        print(file_path)
        sds_name, suffix = os.path.splitext(path)
        if suffix != '.json':
            continue

        fp = open(file_path, 'r', encoding='utf-8')
        data = json.loads(fp.readline())
        data = data['DownloadManifest']['Includes']
        # attention: the dic content can't repeat
        merged_data.extend(data)
        # !!!!!        merged_data  = data
        fp.close()
    fw = open(out_file, 'w', encoding='utf-8')
    subject_md5 = {"subject":subject, "Include":merged_data}
    json.dump(subject_md5, fw, ensure_ascii=False)
    fw.close()

if __name__ == '__main__':
    subject_list = []
    fr = open('./subjects_all.txt', 'r', encoding='utf-8')
    line = fr.readline()
    while line:
        subject_list.append(line.strip())
        line = fr.readline()
    fr.close()
    download_subject_md5(subject_list)
    # download_subject_md5([104012,101107])

    # merge every subject'json file
    for subject in subject_list:
        merge_subject_json(subject, '../data/.xdlm/'+str(subject)+'/','../data/md5/')

    print("Merge finished!")