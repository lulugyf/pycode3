#coding=utf8




def post(post_data, url="http://localhost:1088/call"):
    import requests
    response = requests.post(url, data=post_data, stream=False)
    print(response.status_code, response.reason)
    if response.status_code == 200:
        print( response.content )
    else:
        print("post failed ", response.status_code)
    return None


def main():
    post({"data":"6.4,2.7,5.3,2.1"}, "http://172.18.231.75:1088/call")

if __name__ == '__main__':
    main()