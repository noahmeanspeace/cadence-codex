# Cadence SSH Skill

通过 SSH，让 Codex 辅助检查 Linux 或 VMware 中的 Cadence 工程、分析仿真日志，并在明确授权下编写 SKILL/OCEAN 脚本和运行有限仿真。

## 发布文件

- `cadence-ssh.skill`：技能分发包，内部为 ZIP 格式。
- `README.md`：本使用说明。

该 Skill 不包含个人 IP、用户名、私人路径、密钥、设计文件、PDK 或许可证。它不是 Cadence 插件，也不会安装 Cadence。

## 前提

- 已有支持本地 Skill 的 Codex 环境。
- 本机 SSH 客户端可连接远程 Linux。
- 远程主机已合法安装并授权使用 Cadence 和所需 PDK。
- 使用者知道自己的 SSH 目标和工程目录。

## 安装

1. 将 `cadence-ssh.skill` 复制一份，将副本扩展名改为 `.zip`，用 ZIP 工具解压。
2. 得到以下文件夹：

   ```text
   cadence-ssh/
   ├── SKILL.md
   ├── README.md
   └── references/
       └── connection.md
   ```

3. 将整个 `cadence-ssh` 文件夹放进 Codex 个人技能目录，通常为 `~/.codex/skills/`。如果使用了自定义 `CODEX_HOME`，放到它的 `skills/` 子目录。
4. 确认最终位置为 `skills/cadence-ssh/SKILL.md`，不要多套一层文件夹，也不要仅将 `.skill` 文件放进技能目录。
5. 开启新会话；如果没有发现技能，重新启动 Codex CLI。

本包不依赖平台支持直接导入 `.skill`。其他技能宿主请按其安装规则使用，直接导入兼容性尚未验证。

## 快速开始

先在普通终端中建立并核实自己的 SSH 连接。SSH 别名不必叫 `cadence`，以下仅为示例。

在 Codex 中输入，并替换 SSH 目标和工程目录：

```text
使用 $cadence-ssh。
SSH 目标是 cadence，工程目录是 /path/to/project。
先只读检查连接、Virtuoso 命令和 cds.lib。
不要修改文件、权限或配置，不启动 GUI 或仿真。
```

### 查找学习电路

```text
使用 $cadence-ssh，只读检查指定工程的用户库，列出 Library / Cell / View。
寻找基础电路候选；未核实电路内部连接时，请明确说明功能只是候选。
```

### 分析 Spectre 报错

```text
使用 $cadence-ssh，通过指定 SSH 目标读取 /path/to/spectre.out。
解释具体报错原因，不修改工程、不实施修复。
```

### 编写自动化脚本

```text
使用 $cadence-ssh，为指定测试电路编写 OCEAN 脚本。
只允许写入 /path/to/new-workspace，不修改 PDK 和原始库，暂不运行仿真。
先核实实际工具版本、目标 Library / Cell / View 和支持的参数。
```

## 安全边界

- 默认只读，修改配置、权限、PDK、历史库或运行仿真必须在用户授权范围内。
- 不禁用 SSH 主机指纹检查，不全局启用旧算法，不关闭 StrictModes 或 SELinux。
- 旧版 RHEL/OpenSSH 的兼容排查说明位于解包后的 `references/connection.md`；现代主机不要默认启用旧版 RSA 算法。
- 不上传私钥、密码、完整许可证信息、内部配置或受限制的 PDK/设计数据。
- 默认只读是代理行为指令，不是操作系统级隔离，使用者仍应审查命令和授权范围。

## 验证与限制

本发布包已经通过：

- ZIP 解包与文件完整性检查。
- 解包后 SKILL.md 格式校验。
- 必需文件、内部引用与源文件一致性检查。
- 已知个人信息与私钥标记扫描。

上述验证说明分发包结构有效，可按解压方式安装；不等于已验证所有平台的直接导入、所有 Cadence 版本或他人机器的连接与仿真。

SSH 成功、Virtuoso GUI 可用、许可证可用和 Spectre 仿真成功是不同验证层次。本 Skill 不直接操作 Virtuoso 鼠标界面，OA 目录结构检查也不等于原理图内容解码。

## 贡献与开源许可

反馈问题时提供脱敏后的环境信息、错误信息、复现步骤和期望行为。

本发布包尚未指定许可证。正式开源发布前，维护者需要选择许可证并添加 `LICENSE`；公开文件本身不等于授予开源许可。

本项目与 Cadence、VMware 或 OpenAI 无官方关联，各产品名称属于各自权利人。
