# 发布到 GitHub

## 上传结构

建议仓库名为 `prd-generator`，也可使用自己的仓库名。将本发布目录里的内容上传到仓库根目录，使 README、LICENSE、skills 和 .github 直接位于根目录，不额外套一层本地发布文件夹。

发布格式依靠 `skills/prd-generator/SKILL.md` 及相对资源引用。这里无需 npm 发布、`package.json` 或助手插件的 marketplace 清单；若另行制作插件，应按对应产品的规则处理。

保留 `.github/workflows/validate.yml`、`.gitignore` 与 `.gitattributes`。如网页上传隐藏文件不便，可使用 Git 客户端。README 中的 `OWNER/REPO` 需要替换成实际仓库地址。

## 发布前检查

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
```

Python 只用于维护检查。上传后查看 GitHub Actions 是否通过，再从真实仓库验证：

```bash
npx skills add OWNER/REPO --list
npx skills add OWNER/REPO --skill prd-generator
```

第一项应只列出本仓库声明的 `prd-generator`；安装后资源目录应完整。执行公开示例时核对关键行为，不能仅凭技能被发现就认定生成质量已验证。

## 版本与许可

首次技能发布版本为0.1.0；确认检查结果后可为对应提交创建`v0.1.0`标签和GitHub Release，说明可参考CHANGELOG。元数据与CHANGELOG一起更新，规则基线和模板基线不等同于技能发布版本。

本发布包按用户选择采用MIT。根目录和可安装技能目录均保留许可正文，保证仅安装子目录时仍带许可。

本次整理不执行创建仓库、推送、发布Release或安装到个人助手目录，也不代表已被任何技能目录收录。

## 与原资料的关系

本技能取自生成规范v1.2、模板v4.1，保留通用写作规则，调整相对路径、独立工作区输出及本仓库维护方式。原规范和模板不被本发布包改写；安装者不需要原作者的本地目录、历史业务材料或其他方法论工件。

后续维护入口为本仓库的`references/prd-guidelines.md`与`assets/prd-template.md`（均位于技能子目录）。实际涉及原规范变更时，由维护者另行同步，不要求使用者访问个人环境。

## 格式依据与核对范围

目录与元数据遵循[Agent Skills](https://agentskills.io/specification)形式，并使用本机当前技能创建工具核对；GitHub安装形式参考[Skills CLI](https://github.com/vercel-labs/skills)。2026-11-27使用本次会话下载的Skills CLI 1.9.1进行本地发现检查，运行要求为Node.js >=22.20。

本次重新读取远程发布说明超时，因此不声称已完成所有上游网页的最新在线核验；真实仓库安装、GitHub Actions和各助手实际生成效果需发布后分别确认。
