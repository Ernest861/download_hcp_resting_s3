# download_hcp_resting_s3
Downloaded from amazon S3 hcp bucket against Resting and T1W folders by subject number. 
Win 10, anaconda, based on python 3.9.7.  

## module need
0. conda
1. boto3
2. threading
3. awscli
4. shutil

## 1. acess the aws S3
1. conda install -c conda-forge 
2. aws --version
3.  get key from hcp https://wiki.humanconnectome.org/display/PublicData/How+To+Connect+to+Connectome+Data+via+AWS
4. aws config --profile hcp
```
AWS_ACCESS_KEY_ID=XXXXXXXXX
AWS_SECRET_ACCES_KEY=XXXXXXXXXX
```

## 2. downlad all the MD5 josn, use the /utils python code by @jorian 2021
1. add the S3 key ans secret_key in download_subject_md5.py
2. python download_subject_md5.py

download all the md5 (~2GB) need near 24 hour in my internet speed

## 3. use Z_S3_TEST.ipynb
1. change subject list to your list: subject_want.txt
2. add the S3 key and secret_key from step 1.3 to Z_S3_TEST.ipynb
3. change SERIES_MAP dir in Z_S3_TEST.ipynb
```
SERIES_MAP = {
#'MEG_unprocessed':'unprocessed/MEG/',
'3T_unprocessed_rfMRI1_LR':'unprocessed/3T/rfMRI_REST1_LR/',
'3T_unprocessed_rfMRI1_RL':'unprocessed/3T/rfMRI_REST1_RL/',
'3T_unprocessed_rfMRI2_LR':'unprocessed/3T/rfMRI_REST2_LR/',
'3T_unprocessed_rfMRI2_RL':'unprocessed/3T/rfMRI_REST2_RL/',
'3T_unprocessed_T1':'unprocessed/3T/T1w_MPR1/',
#'7T_unprocessed':'7T',
#'Diffusion':'Diffusion',
#'T1w':'T1w',
#'MNINonLinear':'MNINonLinear',
'release-notes':'release-notes',
#'MEG':'MEG'
#'.xdlm':'.xdlm',
}
```
4. run Z_S3_TEST.ipynb

download all the resting and T1W (~900GB) for 190 subjects need near 12 hour in my internet speed
