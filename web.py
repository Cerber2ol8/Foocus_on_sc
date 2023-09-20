import requests
from flask import Flask, request, Response, send_file, make_response

app = Flask(__name__)
target_url = "http://127.0.0.1:8080"  # 目标URL
forward = "/aiforward691247814230933505"


@app.route(forward, methods=['GET', 'POST'])
def forward_request():


    # 获取来自客户端的请求
    client_request = request.data

    client_headers = request.headers

    client_method = request.method

    
    
    # 发送请求到目标URL
    response = None
    if client_method == 'GET':
        response = requests.get(target_url, headers=client_headers)
    elif client_method == 'POST':
        response = requests.post(target_url, data=client_request, headers=client_headers)

    # 构建响应
    if response:
        content = response.text
        if content.find("./assets/"):
          content = content.replace("./assets/", "." + forward + "/assets/")
        if content.find("./info/"):
          content = content.replace("./assets/", "." + forward + "/assets/")


          
        #print(response.content)
        forwarded_response = Response(content)
        forwarded_response.status_code = response.status_code
        for key, value in response.headers.items():
            forwarded_response.headers[key] = value

        return forwarded_response
    else:
        return Response("Failed to forward request", status=500)
      
@app.route(forward + '/queue/join', methods=['GET'])
def queue_request(asset_path):	


    # 获取来自客户端的请求
    client_request = request.data

    client_headers = request.headers

    client_method = request.method

    
    response = None

    response = requests.get(target_url, headers=client_headers)

    # 构建响应
    if response:

        forwarded_response = Response(content)
        forwarded_response.status_code = response.status_code
        for key, value in response.headers.items():
            forwarded_response.headers[key] = value

        return forwarded_response
    else:
        return Response("Failed to forward request", status=500)
      
      
      
@app.route(forward + '/<path:asset_path>', methods=['GET'])
def forward_assets(asset_path):	

    # 构建目标URL以获取静态资源
    asset_url = f"{target_url}/{asset_path}"

    # 发送请求到目标URL以获取静态资源
    asset_response = requests.get(asset_url)


    # 构建响应
    if asset_response.status_code == 200:
        #print(asset_response.content)
        # 将静态资源文件作为响应发送给客户端
        
        response = make_response(asset_response.content)
        response.headers = dict(asset_response.headers)
        #return send_file(asset_response.content)
        return response

    return Response("Failed to forward asset request", status=asset_response.status_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
