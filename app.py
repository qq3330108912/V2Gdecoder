from flask import Flask, request, render_template, jsonify
import subprocess
import shlex

app = Flask(__name__)

def execute_jar(encoded_data):
    jar_path = "V2Gdecoder.jar"  # 确保这里是你的 JAR 文件的正确路径
    command = f"java -jar {jar_path} -e -s {encoded_data}"
    try:
        output = subprocess.check_output(shlex.split(command), stderr=subprocess.STDOUT, universal_newlines=True)
        return output, None  # 成功时返回输出和 None 作为错误
    except subprocess.CalledProcessError as e:
        return None, e.output  # 出错时返回 None 和错误输出



@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    decoded_data = None

    if request.method == 'POST':
        encoded_data = request.form.get('encoded_data')
        if encoded_data:  # 确保输入数据存在
            decoded_data, error = execute_jar(encoded_data)

    print(decoded_data)
    return render_template('index.html', decoded_data=decoded_data, error=error)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')
