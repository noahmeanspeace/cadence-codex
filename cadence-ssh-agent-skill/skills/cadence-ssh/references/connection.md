# SSH 连接排查

用于连接诊断和用户明确要求的连接配置。本文示例均为占位符，须替换后使用，不构成修改授权。

## 别名与执行环境

无法解析 SSH 别名时，确认当前用户、SSH 可执行文件和配置文件路径。Windows 通常为当前用户的 `.ssh/config`，检查是否误存为 `config.txt`；Linux/macOS 通常为 `~/.ssh/config`。只检查目标主机段，不公开其他主机配置。

桌面应用与 CLI 的权限/执行环境可能不同；访问被拒绝时报告边界，可让用户在有权限的本地终端自行测试，不绕过隔离。

基础配置示例：

```text
Host cadence
    HostName YOUR_VM_IP_OR_HOSTNAME
    User YOUR_LINUX_USER
    IdentityFile ~/.ssh/YOUR_KEY_FILE
    IdentitiesOnly yes
```

仅添加或修改用户授权的主机段，不覆盖整个 config。地址变化时从虚拟机控制台的 `ip addr` 或 `ifconfig` 核实。主机指纹变化先确认原因，不直接删除 known_hosts 或禁用检查。

## 旧版 OpenSSH 兼容

如果实际错误为 `no matching host key type`，且服务端只提供 `ssh-rsa`，核实目标后可在该主机段加入：

```text
    HostKeyAlgorithms +ssh-rsa
```

若进一步确认旧服务端的公钥认证需要 RSA/SHA-1，可加入：

```text
    PubkeyAcceptedAlgorithms +ssh-rsa
```

这是旧系统的兼容措施，不是现代主机的默认配置。仅对目标主机使用，不全局启用旧算法；不要顺手放宽其他算法。长期可由系统管理员评估升级。

## 密钥与权限

配置免密前检查已有密钥，不覆盖私钥。新密钥类型根据双方实际支持选择；老服务端可能需要 RSA 4096。建议使用密钥口令和 ssh-agent；口令留空需要告知保护能力下降。

只将公钥添加到已核实账户的 `authorized_keys`，避免重复添加，保留其他公钥。期望 `.ssh` 为 700、`authorized_keys` 为 600，属主正确。家目录不应允许其他用户写入；755 或 700 需按共享需求选择，不机械套用。

StrictModes 拒绝认证时先只读检查目标家目录、`.ssh` 和公钥文件权限。用户授权后仅修正具体目标，不递归修改家目录、不关闭 StrictModes。怀疑 SELinux 时先诊断标签；恢复标签属于修改操作，需要授权，不关闭 SELinux。

验证免密使用 `BatchMode=yes` 的只读命令，交互密码登录成功不等于免密成功。

## CLI 与 Cadence 环境

只有用户请求时才处理 Codex CLI 安装或升级；采用当时的官方安装说明，不固定历史版本。刚安装后找不到命令，可先重新打开终端刷新 PATH。

SSH 不认识 `virtuoso` 时只读检查实际 shell 与环境脚本，不把 Bash 命令强加给 csh/tcsh。采用用户确认或实际发现的加载方式，不自动改启动文件。许可证、GUI 和仿真需各自验证。
