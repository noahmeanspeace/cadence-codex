# Cadence SSH Agent Skill

通过 SSH 为 AI 编程助手提供 Cadence 工程检查与排错流程。

## 项目缘起与目标

本项目来自作者已经跑通的 Windows Codex CLI → SSH → VMware/Linux → Cadence 工作流程。目标是把安装、连接、排错和工程检查的经验整理成可复用能力包，帮助其他使用者完成同样的流程。

README 面向首次使用者，从安装 Codex CLI 开始；`SKILL.md` 面向 Agent，指导它接手后续 SSH 配置、故障诊断和 Cadence 工程检查。读者不需要预先安装 Codex CLI，但需要自行准备合法可用的 Linux/Cadence 环境。

这是一个 **Agent Skill 能力包**：`SKILL.md` 定义触发条件、工作流程和操作边界，Python 脚本执行固定的连接检查，参考资料提供故障处理方法。适合把 Windows 上的 AI 助手与 VMware/Linux 中已有的 Cadence 环境配合使用。

## 功能

- 检查 SSH 身份和当前远程环境中的 Virtuoso、Spectre、OCEAN 命令路径。
- 指导 Agent 检查 `cds.lib` 和 Library / Cell / View 结构。
- 指导 Agent 分析仿真日志、区分连接、环境、许可证和仿真问题。
- 在用户要求的范围内辅助编写 SKILL/OCEAN 脚本。

连接检查已经提供可执行脚本；库解析、日志分析和仿真辅助由 Agent 按说明调用工具完成，尚未封装为独立程序。它不包含 Cadence、PDK、许可证或设计数据。

## 仓库结构

```text
cadence-ssh-agent-skill/
├── README.md
├── LICENSE
├── .gitignore
├── skills/cadence-ssh/
│   ├── SKILL.md
│   ├── scripts/check_connection.py
│   └── references/connection.md
└── tests/test_connection.py
```

## 从零开始：先安装 Codex CLI

本教程默认使用者尚未安装 Codex CLI，主要面向 Windows + VMware/Linux。下面的安装命令来自 [Codex CLI 官方文档](https://learn.chatgpt.com/docs/codex/cli)，核对日期为 2026-09-16。安装与登录由使用者在自己的电脑上完成，Skill 在 Codex 启动后加载。

### 1. 安装 CLI

在 Windows 打开 PowerShell，运行：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"
```

这条命令会从官方地址下载并运行安装器。装好后关闭当前 PowerShell，重新打开，再检查：

```powershell
codex --version
```

看到版本号再继续；若提示找不到命令，先重开终端刷新 PATH，再按官方文档排查，不要反复重装。安装器问 `y/N` 时输入选项，不要把下一条终端命令填进选项提示。

macOS/Linux 可采用同一官方文档中的安装方式：

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

### 2. 启动并登录

运行：

```text
codex
```

首次启动按照提示选择 ChatGPT 登录或其他可用认证方式，由使用者在浏览器完成。账号需具备相应使用权限；本仓库不提供账号或 API 密钥。确认进入交互界面后退出，继续安装本 Skill。

### 3. 安装 Skill

将仓库中的整个 `skills/cadence-ssh` 文件夹复制到项目的 `.agents/skills/` 下：

```text
你的项目/.agents/skills/cadence-ssh/SKILL.md
```

个人使用也可按当前 Codex 的技能发现规则安装。开启新会话，在技能列表中确认 `cadence-ssh`，再通过 `$cadence-ssh` 调用。参见 [官方 Skill 文档](https://learn.chatgpt.com/docs/build-skills)。

Windows 用户可下载本仓库 ZIP 并解压，进入解压后的仓库根目录，运行以下 PowerShell 命令，将 Skill 安装到这个项目：

```powershell
New-Item -ItemType Directory -Force '.agents/skills' | Out-Null
if (Test-Path '.agents/skills/cadence-ssh') {
    throw '已存在同名 Skill，请先检查现有内容再决定如何更新。'
}
Copy-Item -LiteralPath 'skills/cadence-ssh' -Destination '.agents/skills/cadence-ssh' -Recurse
codex
```

在该项目目录启动 Codex，输入 `/skills` 确认能找到 `cadence-ssh`。

仓库以源码目录和 ZIP 发布，无需 `.skill` 扩展名。其他 Agent 可复用这些文件，但安装位置与调用方式须遵循对应产品说明；本项目未验证所有宿主。

## 使用前准备

### 4. 配置 SSH，再连接 Cadence

开启 VMware 中的 Linux 虚拟机，在 Linux 桌面终端用 `ip addr` 确认地址，并确认自己的 Linux 用户名。Windows PowerShell 中运行 `ssh -V` 检查客户端；若不存在，在 Windows 的“可选功能”中安装 OpenSSH 客户端后重新打开终端。

用自己的实际值替换下方大写占位符：

```text
ssh YOUR_LINUX_USER@YOUR_VM_IP
```

首次连接先核实主机指纹，再输入 Linux 用户密码。能登录后输入 `exit` 返回本机。在当前用户的 `.ssh/config` 中添加以下主机段，保留其他已有配置：

```text
Host cadence
    HostName YOUR_VM_IP
    User YOUR_LINUX_USER
```

然后测试 `ssh cadence`。此时可让已经加载 Skill 的 Codex 引导配置公钥认证：

```text
使用 $cadence-ssh。Codex CLI 已安装并登录，ssh cadence 可以用密码登录。
请先检查现有 SSH 配置和密钥，帮我配置该主机的公钥认证，保留现有密钥和其他主机配置。
交互密码和主机指纹由我自行确认。配置好后做非交互只读验证，再检查 Cadence 环境。
```

公钥配置、旧版 RSA 兼容和权限问题按 [连接排查](skills/cadence-ssh/references/connection.md) 处理。虚拟机必须已经提供 SSH 服务；连接被拒绝时先查服务状态，超时时先查地址与网络，不通过关闭防火墙来替代诊断。

### 5. 开始工程检查

本机需要 Python 3.9+、OpenSSH 客户端；Python 脚本仅使用标准库。远程主机需要支持 POSIX `sh`。先在终端手动验证 SSH 目标及主机指纹，并配置可用于非交互连接的认证。

SSH 别名、用户和工程目录由使用者提供，包内没有预设私人环境。

## 快速开始

在 Codex 中输入，替换自己的工程目录：

```text
使用 $cadence-ssh。
我的 SSH 别名是 cadence，工程目录是 /path/to/project。
先检查连接和 Cadence 命令，再只读检查 cds.lib。
```

独立运行连接检查（从仓库根目录执行）：

```bash
python skills/cadence-ssh/scripts/check_connection.py --target cadence --dry-run
python skills/cadence-ssh/scripts/check_connection.py --target cadence
```

第一条只显示计划，第二条真实连接用户指定的 SSH 目标。脚本返回 JSON；成功返回码为 0，连接或响应错误为 2。`connected` 表示固定查询完成，工具字段为 `null` 表示当前 SSH 环境未找到对应命令。

查询不会启动 Cadence 或仿真；正常 SSH 会话可能产生服务器审计记录。脚本会复用本机 SSH 配置（包括已配置的跳板机等行为），应使用可信配置。

其他任务示例：

```text
使用 $cadence-ssh，分析指定工程的 spectre.out 报错，仅解释原因。
```

```text
使用 $cadence-ssh，检查指定用户库中的 cell/view，推荐基础电路候选。
无法读取原理图内部连接时，请标明依据仅为名称和目录结构。
```

```text
使用 $cadence-ssh，为指定测试电路编写 OCEAN 脚本。
输出到我指定的新工作目录，暂不运行仿真。
```

## 操作边界

检查和诊断默认只读，修改与仿真遵循用户明确给定的范围。Skill 会要求 Agent 保留 PDK、历史库和未授权修改的配置，不读取私钥内容，不关闭 SSH 主机检查。旧系统兼容方法见 [连接排查](skills/cadence-ssh/references/connection.md)。

这些规则是 Agent 工作指令，不是操作系统沙箱。SSH 连通、找到命令、GUI 可用、许可证可用、仿真完成需要分别验证。目录检查不能替代 OA 原理图解析，也不包含自动鼠标操作。

## 测试与已验证范围

```bash
python -m unittest discover -s tests -v
```

离线测试覆盖成功响应、缺少工具、认证失败、截断响应、超时、缺少 SSH 客户端及目标参数校验，不需要真实账户。

本发布版本已通过上述离线测试、Skill 格式检查和分发文件检查。`--dry-run` 已实际运行。未进行真实远程连接、许可证、GUI 或仿真测试，也未验证其他 Agent 的加载行为；不将离线测试描述为 Cadence 集成测试。

作者原始环境中的连接与工程检查流程已跑通（由作者确认）。新增加的通用 Python 检查脚本仅完成上述离线验证；原始环境成功不等于该脚本已在所有目标主机验证。

## 贡献

提交问题时附上脱敏后的操作系统、SSH/Cadence 版本、命令与错误信息。不要上传密钥、账号密码、许可证文件、内部主机配置或受限制的设计/工艺资料。

## 许可证

本仓库原创说明与脚本采用 [MIT License](LICENSE)。Cadence、PDK 和其他第三方软件仍受各自许可证约束。本项目与 Cadence、VMware、OpenAI 无官方关联。
