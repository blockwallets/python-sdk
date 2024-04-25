# Python SDK

## 概述

功能丰富 的 USDT-TRC20(TRON)、TRX(TRON) 收款接口服务;

通过以 Python 的形式完成一个完整的支付流程。

[接入文档](https://blockwallets.io/docs/api)

## 特性

- 特点

  - 钱包是跟用户绑定长期有效的；

  - 具有钱包余额系统自动归集、自动提现等功能；

- 稳定：公开可靠公链信息，可随时在区块浏览器实时查询，数据实时同步；

- 其他：后续将支持多链。

## 支付流程

- 1.创建钱包
  - 因为钱包是跟用户是唯一绑定的，所以可以为每个用户创建一个唯一且长期有效的钱包地址；
  - 一个开发者拥有一个系统主钱包，可以管理多个子钱包，子钱包都是跟每个用户相关联的；
  - 钱包用来进行后续的交易操作；
  - 目前仅支持 Tron（波场）钱包的创建。
- 2.等待用户支付
  - 当用户要进行支付操作时，这个时候需要通过当前支付用户的钱包地址，进行实时查询当前最新的交易记录；
  - 通过轮询的方式间隔一定的时间进行查询(轮询建议 10 秒 一次)；
  - 在这个等待用户支付的过程中，可能需要较长时间，因为每个用户的支付时间都会有所不同，在这里可以自定义一个等待的有效时间或一直等待；
- 3.查询交易结果
  - 以用户发起支付时的时间为查询起始时间，查询在这个时间之后是否有最新的交易收款记录；
  - 当有最新的收款记录，查看对应的交易金额，就是用户支付所对应的金额，这里对用户支付多少金额目前没做要求；
  - 最终就完成了一笔完整的支付。

## 先决条件

在操作支付流程之前，您需要：

- 1.访问并 登录/注册 [用户后台](https://blockwallets.io/auth/signin)

- 2.在用户后台查看 API 接入必需的 [api-key](https://blockwallets.io/account/apiKeys)

  ![index](https://raw.githubusercontent.com/blockwallets/public/main/images/wallet/api-key-page.png)

- 3.安装需要请求 HTTP 的依赖库 requests，可以通过下面命令安装

  ```
  pip install requests
  ```

### 1. 创建钱包

_发送请求_

- 代码演示

```python
# 发送 创建钱包 POST 请求
response = requests.post(
    url="https://api.blockwallets.io/api/v1/block/wallets",  # 请求地址
    headers={"api-key": "需要去用户后台查看"},  # 请求 header 头数据
    json={
        "block_category_id": 1
    },  # 请求数据 block_category_id: 区块链类型 ID（1: Tron ...)
)
```

_响应结果_

![index](https://raw.githubusercontent.com/blockwallets/public/main/images/wallet/python/create_wallet.png)

### 2. 等待用户支付

- 用户需要通过其他方式向此钱包进行支付
- 等待的同时，验证等待用户支付结果，直接进行下面步骤

![index](https://raw.githubusercontent.com/blockwallets/public/main/images/wallet/python/wait_pay.png)

### 3. 查询交易结果

_发送请求_

- 代码演示

```python
# 发送 查询交易结果 GET 请求
response = requests.get(
    url="https://api.blockwallets.io/api/v1/block/trons/transaction/record/gather",  # 请求地址
    headers={
        "accept": "application/json",
        "api-key": api_key,
    },  # 请求 header 头数据
    params={"address": address, "token_type": token_type},  # 请求参数
)
```

_响应结果_

![index](https://raw.githubusercontent.com/blockwallets/public/main/images/wallet/python/query_results.png)

### 结语

要想运行完整代码示例，请下载仓库源码
