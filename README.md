JWT Tools

	一套本地化、可扩展的 JWT (JSON Web Token) 安全测试与调试工具合集

功能特性
	•	快速解析：离线解析并展示 JWT 的 Header、Payload、Signature 以及算法信息，并可选将时间戳（iat/exp/nbf）转换为可读时间。
	•	转换格式：一键生成可供 John the Ripper 使用的哈希格式，用于爆破或检测弱密钥。
	•	重新签名：支持对 JWT 进行 Payload 和 Header 的替换或字段更新，再使用自定义密钥、算法重新生成新的 JWT。
	•	弱密钥破解：可通过指定一个常见弱密钥字典，对给定的 JWT 进行爆破测试，检查是否能找到匹配密钥。
	•	模糊测试 (Fuzz)：自动对 Payload 进行随机插值或修改，以检测后端对 JWT 的健壮性，适合挖掘潜在安全隐患或异常处理漏洞。
	•	支持多算法：包含最常用的对称算法（HS256、HS384、HS512）及可选的非对称算法（RS/ES）。可轻松扩展以适配更多算法需求。
	•	命令行模式：提供人性化的 CLI 界面，在本地离线运行，高度可定制，能与其他工具无缝整合。

安装方式
	1.	克隆本仓库：

git clone https://github.com/<你的GitHub用户名>/jwt_tools.git
cd jwt_tools


	2.	安装依赖：

	注：如果你只需要最基础的功能，确保 PyJWT 已安装即可；若有更多高级场景，可根据需求增添依赖。

	3.	授予执行权限（可选）：

chmod +x jwt_tool.py



快速上手

假设你有一个 JWT，如：

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJyb2xlIjoiYWRtaW4ifQ.BQYDtBRaKbLSfbe8Lbx4ew9ncvQ9q38rLEW0WRdCfeQ

下面示例展示如何解析该 JWT、如何改写并重新签名等常见操作。

1. 解析并查看关键信息

python3 jwt_tool.py parse --jwt "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

	•	打印 Header、Payload、Signature 以及所使用的算法。
	•	若添加 --human-time 参数，还能将 iat/exp/nbf 等时间戳转换为人类可读格式。
<img width="567" alt="image" src="https://github.com/user-attachments/assets/9f7f5913-2689-451a-a490-a0561c620eb3" />

2. 转换为 John the Ripper 哈希格式

python3 jwt_tool.py tojohn --jwt "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

	•	输出形如 header.payload#signature_hex 的格式，可用于弱密钥爆破或测试。

3. 重新签名

python3 jwt_tool.py resign \
  --jwt "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  --secret "mysecret" \
  --alg HS256 \
  --payload-update '{"role":"guest","iat":1690000000}'

	•	将原有 JWT 的 role 改为 guest，并更新 iat，然后使用密钥 mysecret 和 HS256 算法生成新的 JWT。

4. 弱密钥爆破

python3 jwt_tool.py bruteforce \
  --jwt "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  --wordlist "/path/to/common_secrets.txt" \
  --alg HS256

	•	对指定 JWT 尝试常见密钥，若成功匹配出签名，脚本将打印出对应的弱密钥。

5. 模糊测试 (Fuzz)

python3 jwt_tool.py fuzz \
  --jwt "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  --secret "mysecret" \
  --alg HS256 \
  --rounds 10

	•	将随机修改 Payload 中的字段内容，并输出模糊后的 JWT。
	•	适合对后端服务进行压力测试或异常处理测试。

应用场景
	•	开发者调试：在开发 JWT 功能时进行本地调试，不必依赖第三方在线服务。
	•	安全测试/渗透测试：配合字典爆破、模糊测试以及对 alg=none 等不安全场景进行检查，全面评估后端接口安全性。
	•	自动化测试：将脚本整合到 CI/CD 管道中，批量验证 Token 正确性或对弱密钥的配置进行扫描。
	•	学习与研究：加深对 JWT 内部结构、签名原理、常见安全漏洞（如 alg none 攻击）的理解。

贡献方式
	1.	提 Issue：如果你在使用过程中发现任何 Bug 或者有改进建议，欢迎在 Issue 区提出。
	2.	提交 Pull Request：若你实现了新的功能（比如新增算法支持、更多自定义 Header/Payload 的操作），欢迎提交 PR，让更多人受益。

