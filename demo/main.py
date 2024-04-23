import time
import json
import requests

"""
创建钱包 API

首先需要安装 requests 库
安装命令：pip install requests
"""


def create_wallet(api_key: str):
    """创建钱包方法

    具体 API 说明 请参考： https://blockwallets.io/docs/api/wallet-create

    :param api_key:     用户后台查看的 api_key
    :return:            新创建钱包相关信息
    """

    # 发送请求
    response = requests.post(
        url="https://api.blockwallets.io/api/v1/block/wallets",  # 请求地址
        headers={"api-key": api_key},  # 请求 header 头数据
        json={"block_category_id": 1},  # 请求数据
    )
    # 检查响应 HTTP 状态码及结果内容
    if response.status_code != 200:
        print(f"请求创建钱包失败！({response.json().get('error', {}).get('message')})")

        return None
    else:
        response = response.json()
        # 格式化输出到控制台
        print(
            f"请求创建钱包响应数据: {json.dumps(response, indent=4, ensure_ascii=False)}"
        )

        data = response.get("data")  # 请求成功返回的数据

        return data


def transaction_query(api_key: str, address: str, token_type: str = "TRC20"):
    """查询钱包最新交易列表信息

    具体 API 说明 请参考： https://blockwallets.io/docs/api/transaction-query

    :param api_key:         用户后台查看的 api_key
    :param address:         钱包地址
    :param token_type:      代币类型（TRX、TRC20）[默认：TRC20 对应的是 USDT]
    :return:                交易列表信息
    """

    # 发送 GET 请求
    response = requests.get(
        url="https://api.blockwallets.io/api/v1/block/trons/transaction/record/gather",  # 请求地址
        headers={
            "accept": "application/json",
            "api-key": api_key,
        },  # 请求 header 头数据
        params={"address": address, "token_type": token_type},  # 请求参数
    )
    # 检查响应 HTTP 状态码及结果内容
    if response.status_code != 200:
        print("查询钱包最新交易列表信息失败！")

        return None
    else:
        response = response.json()
        print(
            f"请求查询钱包最新交易列表信息响应数据：{json.dumps(response, indent=4, ensure_ascii=False)}"
        )

        data = response.get("data")  # 请求成功返回的数据

        return data


def main(api_key: str):
    # 1. 创建钱包
    # 调用创建钱包方法
    create_wallet_result_data = create_wallet(api_key)
    if not create_wallet_result_data:
        # 当创建钱包失败时，则直接返回
        return False
    else:
        result = create_wallet_result_data.get("result")
        address = result.get("address")  # 新创建的钱包地址

    # 2. 等待用户支付
    print(f"新创建的钱包地址为：{address}")
    transaction_type = "TRX"  # 代币类型（TRX、TRC20）可指定对应的代币类型
    print(
        f"请往地址为 {address} 的钱包里，支付一定的 {transaction_type} 金额(最低：0.000001 {transaction_type})"
    )

    # 3. 轮询的方式查询最新交易记录
    print(f"正在查询钱包 {address} 最新交易记录，请稍候...")
    if transaction_type == "TRX":
        token_type = "TRX"
    elif transaction_type == "USDT":
        token_type = "TRC20"

    while True:
        transaction_query_result = transaction_query(
            api_key=api_key, address=address, token_type=token_type
        )
        if transaction_query_result:
            results = transaction_query_result.get("results")
            if len(results) > 0:
                transaction = results[0]
                print(
                    f"本次最新交易金额为 {transaction.get('amount'):.6f} {transaction.get('transaction_type')}"
                )

                return True

        # 延迟
        time.sleep(20)


if __name__ == "__main__":

    api_key = "替换成用户后台查看的 Api Key"

    main(api_key)
