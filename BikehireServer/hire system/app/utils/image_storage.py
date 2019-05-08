from qiniu import Auth, put_data, etag, urlsafe_base64_encode
import qiniu.config

# set Access Key and Secret Key
access_key = 'Qysmqk5xyp4Jwbe7bXPWx-vqIV9AS5slRq-FJ0Of'
secret_key = 'VzQBPaA0ToSUS9r3tibOum6iW6JrKQuaBsLWS3u_'


def storage(file_data):
    """
    update to qiniu
    :param file_data: data will be updated
    :return:
    """

    q = Auth(access_key, secret_key)

    # updated space
    bucket_name = 'mystorage-bikehire'

    # create token , set time
    token = q.upload_token(bucket_name, None, 3600)
    ret, info = put_data(token, None, file_data)

    if info.status_code == 200:
        # update success and return file name
        return ret.get("key")
    else:
        # update failed
        raise Exception("update failed")

    # print(info)
    # print("*"*10)
    # print(ret)

if __name__ == '__main__':
    with open("./2.png", "rb") as f:
        file_data = f.read()
        storage(file_data)
