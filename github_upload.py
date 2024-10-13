import requests as rq
import base64
import os

# 刪除 Github 指定文件
def delete_github_file(username, repo, sha, token, path_in_github):
    # API url
    url = f"https://api.github.com/repos/{username}/{repo}/contents/{path_in_github}"

    # 設置 headers
    headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
    }

    # 定義 request 資訊
    put_data = {
        "message": "Deleting file via API",
        "sha": sha,
        "branch": "main"  # 指定要刪除文件的分支
    }

    # 發送 delete request
    del_res = rq.delete(url, json=put_data, headers=headers)

        # 檢查結果
    if del_res.status_code == 200:
        print("文件已成功刪除！")
    else:
        print(f"刪除失敗，狀態碼：{del_res.status_code}")
        print(del_res.json())

    # 上傳文件到 Github

# 上傳 Github 檔案
def upload_file_to_github(username, repo, path_in_github, token, path_of_the_file):

    # 讀取圖片文件並進行 Base64 編碼
    print("嘗試讀取文件...")
    with open(path_of_the_file, "rb") as image_file:
        encoded_content = base64.b64encode(image_file.read()).decode('utf-8')
    print("文件讀取成功！")

    # 設置請求頭
    print("正在設置 request header...")
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    print("正在設置 request json")
    # 構建 API 請求數據
    put_data = {
        "message": "Upload a file via API",
        "content": encoded_content, 
        "branch": "main"    # 指定要上傳的分支
    }

    # 確認檔案是否存在
    get_url = f"https://api.github.com/repos/{username}/{repo}/contents/{path_in_github}"
    get_res = rq.get(get_url, headers=headers)
    get_data = get_res.json()

    # 確認檔案是否存在
    if get_res.status_code // 100 == 2 :    # 如果 get 狀態碼是 200，代表檔案已存在，需刪除
        print("檔案已存在，刪除中...")
        sha = get_data['sha']
        delete_github_file(username = username, repo = repo, sha = sha, path_in_github = path_in_github, token = token)
    else :
        print("確認檔案不存在")

    # 發送 put requests
    try :
        print("發送 put request 上傳檔案中...")
        url = f"https://api.github.com/repos/{username}/{repo}/contents/{path_in_github}"
        put_res = rq.put(url, json = put_data ,headers = headers)
        if put_res.status_code // 100 == 2 :
            print("檔案上傳成功！")
        elif put_res.status_code // 100 == 4 :
            print(f"Woooops...回應碼是 {put_res.status_code}，看一下出了甚麼問題吧！\n{put_res.json()}")

        return put_res.json()
        
    except :
        print(f"檔案 {path_of_the_file} 上傳失敗...")
        return None
    
def main():

    username = 'foxplaysguitar'
    repo = 'foxplaysguitar.github.io'
    token = os.getenv('GITHUB_UPLOAD_KEY')

    current_folder = os.path.dirname(__file__)
    files = os.listdir(current_folder)
    for file in files :
        path_of_the_file = os.path.join(current_folder, file)
        upload_file_to_github(
            username=username,
            repo=repo,
            path_in_github = file,
            token=token,
            path_of_the_file=path_of_the_file
        )

if __name__ == '__main__' :
    main()