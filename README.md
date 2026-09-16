# Cadence SSH Skill

一个供 Codex 使用的中文 Skill：通过 SSH 辅助 Linux/VMware 中的 Cadence 工程检查、连接排查、日志分析和 SKILL/OCEAN 自动化。

```text
Codex CLI → 本机 SSH → Linux / VMware → Cadence 工程与工具
```

## 能做什么

- 检查 SSH 连接及远程 Cadence 环境
- 分析 `cds.lib` 与 library/cell/view 结构
- 排查 Spectre 日志和环境加载问题
- 在明确授权下辅助编写脚本、有限参数扫描和仿真
- 指导用户从正确工程目录启动 Virtuoso

默认只读；不会自动修改 PDK、系统配置、权限或运行仿真。它是提示与操作规程，不是 Cadence 插件，也不是“一键安装 EDA”工具。

## 文件结构

```text
cadence-ssh/
├── SKILL.md
├── README.md
└── references/
    └── connection.md
```

`SKILL.md` 是必要入口，`references/connection.md` 是故障排查说明；安装时一起复制。README 供使用者阅读。

## 前提

1. 可用的 Codex CLI 或支持本地 Skill 的 Codex 环境。
2. 本机有 SSH 客户端，可以访问远程 Linux。
3. 远程主机有合法安装、授权使用的 Cadence 环境及所需 PDK。
4. 用户知道 SSH 目标和工程目录，或授权进行有限的只读发现。

不附带 Cadence 软件、PDK、模型、许可证、密钥或设计数据。不要把这些内容提交到公开仓库。

## 安装

`cadence-ssh.skill` 是 ZIP 格式的分发包，不是可执行程序。本包不依赖宿主支持直接导入 `.skill`：可以复制一份并将扩展名改为 `.zip`，解压得到 `cadence-ssh` 文件夹，再按下面的方法安装。不要仅把 `.skill` 文件放进 skills 目录。

把整个 `cadence-ssh` 文件夹放到 Codex 的个人技能目录：通常为 `~/.codex/skills/`；如果设置了 `CODEX_HOME`，放到其 `skills/` 子目录。最终路径应是 `skills/cadence-ssh/SKILL.md`，避免多套一层目录。

Windows 示例位置：

```text
C:\Users\YOUR_WINDOWS_USER\.codex\skills\cadence-ssh\SKILL.md
```

安装后开启新会话；若未发现技能，重新启动 CLI。其他技能宿主的发现规则可能不同，应按其说明放置。

## 首次使用

先在普通终端中自行建立并核实 SSH 连接。SSH 别名可以叫 `cadence`，也可以使用别的名称。现代主机不需要默认开启旧版 RSA 算法，旧系统兼容见 [连接排查](references/connection.md)。

在 Codex 中输入（替换工程路径）：

```text
使用 $cadence-ssh。
SSH 目标是 cadence，工程目录是 /path/to/project。
先只读检查连接、Virtuoso 命令和 cds.lib，不修改文件、不启动 GUI 或仿真。
```

分析日志：

```text
使用 $cadence-ssh，通过 cadence 查看 /path/to/spectre.out，解释报错原因，不实施修复。
```

查找学习电路：

```text
使用 $cadence-ssh，只读检查 /path/to/project 中的用户库。
列出 cell/view，并推荐基础电路候选；没有验证内部连接时不要把名称当成功能证据。
```

脚本实现：

```text
使用 $cadence-ssh，为指定测试电路编写 OCEAN 脚本。
只允许写入 /path/to/new-workspace，不修改 PDK 和原始库；暂不执行仿真。
先核实当前版本支持的命令与目标 library/cell/view。
```

## 限制与验证状态

- SSH 成功不代表 GUI、许可证、Spectre 或模型已可用。
- 目录结构检查不等于读取或验证 OA 原理图内容。
- 不直接操作 Virtuoso 鼠标界面，不保证跨版本脚本兼容。
- 默认只读是给代理的指令，不是操作系统级强制隔离；仍应审查执行命令与授权范围。
- 发布包已做 ZIP 解包、解包后 Skill 格式、内部引用、源文件一致性和隐私检查。验证的是安装文件结构，不是所有宿主的直接导入功能；未对其他用户主机或所有 Cadence 版本做实际连接/仿真测试。

## 贡献与发布

欢迎提交脱敏后的错误信息、复现步骤和改进建议。不要上传私钥、密码、完整许可证信息、内部主机配置或受限制的 PDK/设计文件。

本包尚未指定开源许可证。公开源码不等于授予开源许可；正式开源发布前，请维护者选择合适的许可证并添加 `LICENSE` 文件。Cadence、VMware、Codex 等产品名称属于各自权利人，本项目与其无官方关联。
