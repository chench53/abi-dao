# Abi Dao

[Abi Dao 白皮书](ABI_DAO白皮书v01.pdf)

Abi Dao 源代码，包含智能合约。基于以太坊网络/solidity 构建。

## 开发

### 相关技术

- ERC721/ERC20 协议
- brownie 框架
- ganache 本地环境
- openzeppelin 合约库

### 环境配置

创建 .env 文件，设置环境变量：

- PRIVATE_KEY, 开发用ether地址密钥，切勿泄漏
- WEB3_INFURA_PROJECT_ID, Infura 项目id

### 安装

参考 [brownie](https://eth-brownie.readthedocs.io/en/stable/install.html) 文档

### 编译合约

```sh
brownie compile
```

### 运行脚本

```sh
brownie run ./scripts/deploy.py
```

### 测试

```sh
brownie test tests/test_abi_token.py -s
```

## 部署

