# -*- coding: utf-8 -*-

# @Date    : 2018-10-24
# @Author  : Peng Shiyu


import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/check")
def check_robot():
    ret = request.args.get("ret")
    rand_str = request.args.get("randstr")
    ticket = request.args.get("ticket")
    ip = request.remote_addr

    check_ret = check_ticket(ticket, rand_str, ip)

    check_ret.update(
        {
            "ret": ret,
            "ticket": ticket,
            "randstr": rand_str,
            "ip": ip,
        })

    return jsonify(check_ret)


# 校验验证码的票据
def check_ticket(ticket, rand_str, user_ip):
    url = "https://ssl.captcha.qq.com/ticket/verify"
    """
    aid (必填)	2032405422
    AppSecretKey (必填)	04urfsEZJDbinsshD1hDlPw**
    Ticket (必填)	验证码客户端验证回调的票据
    Randstr (必填)	验证码客户端验证回调的随机串
    UserIP (必填)	提交验证的用户的IP地址（eg: 10.127.10.2）
    """
    params = {
        "aid": "2032405422",
        "AppSecretKey": "04urfsEZJDbinsshD1hDlPw**",
        "Ticket": ticket,
        "Randstr": rand_str,
        "UserIP": user_ip
    }

    response = requests.get(url, params=params, verify=False)

    # {response:1, evil_level:70, err_msg:""}

    return response.json()


if __name__ == '__main__':
    app.run()
