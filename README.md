# JWT Tools

> 一套本地化、可扩展的 **JWT (JSON Web Token)** 安全测试与调试工具合集

## 功能特性

- **快速解析**：离线解析并展示 JWT 的 Header、Payload、Signature 以及算法信息，并可选将时间戳（`iat`/`exp`/`nbf`）转换为可读时间  
- **转换格式**：一键生成可供 **John the Ripper** 使用的哈希格式，用于爆破或检测弱密钥  
- **重新签名**：支持对 JWT 进行 **Payload 和 Header** 的替换或字段更新，再使用自定义密钥、算法重新生成新的 JWT  
- **弱密钥破解**：可通过指定一个常见弱密钥字典，对给定的 JWT 进行爆破测试，检查是否能找到匹配密钥  
- **模糊测试 (Fuzz)**：自动对 Payload 进行随机插值或修改，以检测后端对 JWT 的健壮性，适合挖掘潜在安全隐患或异常处理漏洞  
- **支持多算法**：包含最常用的对称算法（HS256、HS384、HS512）及可扩展的非对称算法（RS/ES）  
- **命令行模式**：本地离线、高度可定制，能与其他工具和脚本无缝整合

## 安装方式

1. **克隆本仓库**

    ```bash
    git clone https://github.com/wwwziziyu/JWT_Tools.git
    cd JWT_Tools
    ```

2. **安装依赖**

    ```bash
    pip install -r requirements.txt
    ```
    > 如果你只需要基础功能，确保安装 `PyJWT` 即可；需要更多高级场景可自行扩充依赖。

3. **授予执行权限（可选）**

    ```bash
    chmod +x jwt_tool.py
    ```

## 快速上手

假设你有一个 JWT：

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJyb2xlIjoiYWRtaW4ifQ.BQYDtBRaKbLSfbe8Lbx4ew9ncvQ9q38rLEW0WRdCfeQ

下面演示如何解析、改写、重新签名以及如何对其进行弱密钥爆破等操作。

### 1. 解析并查看关键信息

```bash
python3 jwt_tool.py parse --jwt "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```
	•	打印 Header、Payload、Signature 以及所使用的算法
	•	若加上 --human-time 参数，还能将 iat/exp/nbf 等时间戳转成人类可读格式
<img width="566" alt="image" src="https://github.com/user-attachments/assets/6249401a-5ac4-4ceb-a7cb-ca5a955707e4" />

2. 转换为 John the Ripper 哈希格式
```bash
python3 jwt_tool.py tojohn --jwt "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```
	•	输出形如 header.payload#signature_hex 的格式，方便与字典破解工具结合使用

3. 重新签名
```bash
python3 jwt_tool.py resign \
    --jwt "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
    --secret "mysecret" \
    --alg HS256 \
    --payload-update '{"role":"guest","iat":1690000000}'
```
	•	将原有 JWT 中的 role 改为 guest，并更新 iat，然后使用 mysecret 作为密钥以 HS256 算法生成新的 JWT

4. 弱密钥爆破
```bash
python3 jwt_tool.py bruteforce \
    --jwt "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
    --wordlist "/path/to/common_secrets.txt" \
    --alg HS256
```
	•	利用常见弱密钥字典爆破 JWT，若签名匹配则会显示对应密钥

5. 模糊测试 (Fuzz)
```bash
python3 jwt_tool.py fuzz \
    --jwt "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
    --secret "mysecret" \
    --alg HS256 \
    --rounds 10
```
	•	随机插值或修改 Payload 中字段，输出模糊后的 JWT 用于测试后端的健壮性

应用场景
	•	开发者调试：离线、本地化，不依赖任何第三方在线服务
	•	安全测试/渗透测试：配合暴力破解、模糊测试以及算法劫持等多种手段，可对后端 Token 验证逻辑进行深入评估
	•	自动化测试：命令行模式易于与 CI/CD、脚本或其他工具整合，大规模批量验证 Token
	•	学习与研究：学习和演练 JWT 的结构、签名原理以及安全漏洞（如 alg=none）

贡献方式
	1.	提交 Issue：发现任何 Bug 或改进建议均可在 Issues 区提问
	2.	Pull Request：实现新功能（例如支持更多算法、增加自定义 Header/Payload）后欢迎提交合并请求，共同完善项目


如你觉得本项目有帮助，欢迎点下 Star 让更多人发现并加入进来，与我们一同完善这款 JWT 安全测试工具！

