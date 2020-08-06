# coding=utf-8
import pathlib
import json
import time
from pydub import AudioSegment
import oss2
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

ACK_ID = 'LTAI4G471e1gcHBrwCr1FoVQ'
ACK_SEC = 'sALPXWRhZjV8hH7kTPDodRFd51ouNI'
APP_KEY = 'yGAYN6QoObQzjJL1'

client = AcsClient(ACK_ID, ACK_SEC, 'cn-shanghai')


def video_to_mono(video_path, audio_path):
    '''
    视频转音频，16K采样率，单声道，wav格式

    :param video_path: 视频地址
    :param audio_path: 音频地址
    :return audio_path: 音频地址
    '''
    audio = AudioSegment.from_file(video_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(audio_path, format='wav', codec='pcm_s16le')
    return audio_path


def upload_file(file_path):
    '''
    文件上传到OSS

    :param file_path: 文件路径
    :return file_url: 文件公网访问路径
    '''
    auth = oss2.Auth(ACK_ID, ACK_SEC)
    bucket = oss2.Bucket(
        auth, 'https://oss-cn-hangzhou.aliyuncs.com', 'python1024')
    obj_name = f'demo/{file_path.name}'
    bucket.put_object_from_file(obj_name, file_path)
    file_url = f'https://python1024.oss-cn-hangzhou.aliyuncs.com/{obj_name}'
    return file_url


def video_to_txt(video_path, audio_path, txt_path):
    '''
    提取视频中的语音，识别出文字后保存到文本文件。
    思路：
    1. 提取视频中的音频
    2. 把音频转为云服务需要的格式：16K采样率

    :param video_path: 视频文件地址
    :param audio_path: 提取的音频文件地址
    :param txt_path: 文本保存路径
    '''
    audio_path = video_to_mono(video_path, audio_path)
    file_url = upload_file(audio_path)
    print(file_url)

    # 构造请求，并设置参数
    post_req = CommonRequest()
    post_req.set_domain('filetrans.cn-shanghai.aliyuncs.com')
    post_req.set_version('2018-08-17')
    post_req.set_product('nls-filetrans')
    post_req.set_action_name('SubmitTask')
    post_req.set_method('POST')
    task = {'appkey': APP_KEY, 'file_link': file_url,
            'version': '4.0', 'enable_words': False}
    post_req.add_body_params('Task', json.dumps(task))
    task_id = ''
    try:
        post_res = client.do_action_with_exception(post_req)
        post_res = json.loads(post_res)
        status_txt = post_res['StatusText']
        if status_txt == 'SUCCESS':
            task_id = post_res['TaskId']
            print(f'录音文件识别请求成功响应，task_id: {task_id}')
        else:
            print(f'录音文件识别请求失败: {status_txt}')
            return
    except Exception as e:
        print(e)
        return

    get_req = CommonRequest()
    get_req.set_domain('filetrans.cn-shanghai.aliyuncs.com')
    get_req.set_version('2018-08-17')
    get_req.set_product('nls-filetrans')
    get_req.set_action_name('GetTaskResult')
    get_req.set_method('GET')
    get_req.add_query_param('TaskId', task_id)

    status_txt = ''
    while True:
        try:
            get_res = client.do_action_with_exception(get_req)
            get_res = json.loads(get_res)
            status_txt = get_res['StatusText']
            if status_txt in ['RUNNING', 'QUEUEING']:
                time.sleep(10)
            else:
                break
        except Exception as e:
            print(e)
            return

    # print(get_res)
    if status_txt == 'SUCCESS':
        result = get_res["Result"]
        sentences = result["Sentences"]
        txt_list = [s['Text'] for s in sentences]
        with open(txt_path, 'a') as f:
            f.writelines('\n'.join(txt_list))
    else:
        print(f'录音文件识别失败, {status_txt}')
        return


if __name__ == '__main__':
    path = pathlib.Path(
        '~/dev/python/python1024/data/automate/007audio/007audio_case'
    ).expanduser()
    video_path = path.joinpath('case.mp4')
    audio_path = path.joinpath('case.wav')
    txt_path = path.joinpath('case.txt')
    video_to_txt(video_path, audio_path, txt_path)
