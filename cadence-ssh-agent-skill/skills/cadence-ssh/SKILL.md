---
name: cadence-ssh
description: 通过 SSH 连接 Linux 主机或 VMware 虚拟机中的 Cadence，检查工程与 PDK、分析仿真日志，并在用户授权范围内辅助 SKILL/OCEAN 自动化。适用于远程 Cadence 工程任务，不用于直接操控 Virtuoso 图形界面。
---

# Cadence SSH 工程助手

## 配置与范围

首次使用不要假定 Codex CLI 或 SSH 已配置。如果用户要求从零部署，先检查 `codex --version` 与 SSH 客户端；CLI 缺失时按当前官方安装说明协助安装，随后由用户完成登录。CLI 已运行时无需重装。登录凭证和交互密码由用户自行输入。再确认本 Skill 被发现，之后配置 SSH 并检查 Cadence；不要跳过未完成的前置环节。

从用户提供的上下文确认 SSH 别名或地址、Linux 用户、工程目录及任务类型。优先复用现有 SSH 配置；不要猜用户名、IP、工程路径或 PDK。缺少连接目标时询问用户；缺少工程目录但已允许检查时，可在用户家目录等有限范围中只读发现候选目录。

支持连接诊断、只读工程检查、日志分析、GUI 启动指导，以及明确授权的脚本实现和仿真。仅要求诊断或检查时默认只读，不自动修复配置、权限或安装软件。

## 工作流程

连接检查优先使用本 Skill 附带的标准库脚本：

```text
python scripts/check_connection.py --target SSH_TARGET
```

路径相对于本 Skill 目录。本机需 Python 3.9+ 和 OpenSSH；不需要远程 Python。脚本只运行固定的远程身份及命令路径查询，输出 JSON。`--dry-run` 可预览 SSH 参数而不连接。先读取 JSON 的 `status`，连接失败时依据 `stderr` 排查；`tools.virtuoso` 缺失仅说明当前 SSH 环境没有找到该命令。脚本不检查许可证或运行仿真。没有 Python 时可采用下面的等价只读命令。

1. 用用户确认的 SSH 目标替换下面的 `SSH_TARGET`，执行非交互只读测试：

   ```text
   ssh -o BatchMode=yes -o ConnectTimeout=10 SSH_TARGET "whoami; hostname; pwd"
   ssh -o BatchMode=yes -o ConnectTimeout=10 SSH_TARGET "which virtuoso"
   ```

   目标和命令按当前本地 shell 正确引用，避免把未经校验的用户文本拼接为可执行 shell 内容。`BatchMode=yes` 防止等待密码；首次指纹由用户核实，不禁用主机密钥检查。
2. 失败时记录实际错误，再读 [连接排查](references/connection.md)。不反复重试相同失败命令，不绕过权限隔离。
3. 检查用户确认的工程根目录中的 `cds.lib`，解析包含文件、相对路径和重复映射；不能仅按库名猜实际位置。有限扫描 library/cell/view，结构存在不等于电路功能或仿真正确。
4. `which virtuoso` 无输出时，检查当前 shell 和已有环境启动文件。按已知安装线索搜索有限目录，不全盘递归扫描；区分非交互 SSH 与 Linux 图形终端的环境。不自动修改 PATH 或 shell 配置。
5. GUI 通常由用户在远程 Linux 图形桌面终端中执行 `cd` 到工程根目录后运行 `virtuoso &`。启动会产生文件并加载初始化脚本，不属于只读检查。SSH 成功不代表 DISPLAY、GUI、许可证或 Spectre 已验证；不猜 DISPLAY，不自动开启 X11 转发。
6. 脚本或仿真任务确认 library/cell/view、允许写入的副本或新库、输出目录和实际工具版本/参数。清楚的现有授权无需重复确认。先做有限试运行，失败时报告证据，不扩大修改或参数扫描范围。

## 安全与证据

- PDK、历史用户库、`cds.lib`、系统配置及权限默认不变。用户明确要求修复时，先定位具体目标与影响，只做最小修改；不关闭安全检查。
- 不读取或输出私钥内容、密码和完整许可证信息；SSH config 只展示当前目标所需的非敏感字段。
- 将连接成功、工程结构检查、工具调用、仿真完成、结果解析分别报告。生成脚本、已有网表或历史 PSF 文件不能作为本次仿真成功的证据。
- 不承诺 SSH 可直接操作 Virtuoso 鼠标界面，不把 OA 目录扫描当成原理图解码。没有兼容 OA 工具时明确说明无法验证电路内部连接。

## 交付

报告当前已验证事项、失败所在层次和下一步。推荐学习电路时提供实际 `Library / Cell / View`，功能未核实则标注。日志诊断给出具体错误和路径，不用“环境完整可用”概括尚未验证的 GUI、许可证与仿真。
