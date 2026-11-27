#!/usr/bin/env python3
"""Check this skill's packaging, local resources and fictional example structure."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'prd-generator'
IGNORED = {'.git', '.idea', '__pycache__', '.venv', 'venv', 'node_modules'}
TEXT_SUFFIXES = {'.md', '.yaml', '.yml', '.py', '.txt', '.json'}
CHAPTERS = [('1', '背景'), ('2', '方案设计'), ('3', '防控手段'), ('4', '验收标准'), ('5', '沟通过程与决策记录')]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def without_code(text):
    return re.sub(r'^```[^\n]*\n[\s\S]*?^```\s*$', '', text, flags=re.M)


def frontmatter():
    text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---(?:\n|$)', text, re.S)
    require(match is not None, 'Missing YAML frontmatter')
    meta = yaml.safe_load(match.group(1))
    require(isinstance(meta, dict), 'Frontmatter must be a mapping')
    require(set(meta) <= {'name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools'}, 'Unsupported frontmatter field')
    name = meta.get('name', '')
    require(isinstance(name, str) and re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) and len(name) <= 64, 'Invalid skill name')
    require(name == SKILL.name, 'Name and folder differ')
    description = meta.get('description', '')
    require(isinstance(description, str) and 1 <= len(description) <= 1024, 'Invalid description')
    require('<' not in description and '>' not in description, 'Description must not contain angle brackets')
    metadata = meta.get('metadata', {})
    require(isinstance(metadata, dict) and all(isinstance(k, str) and isinstance(v, str) for k, v in metadata.items()), 'metadata must map strings to strings')
    version = metadata.get('version', '')
    require(re.fullmatch(r'\d+\.\d+\.\d+', version), 'Invalid version')
    require(version in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8'), 'Version missing from changelog')
    require(meta.get('license') == 'MIT', 'Expected selected MIT license')
    require((ROOT / 'LICENSE').read_bytes() == (SKILL / 'LICENSE.txt').read_bytes(), 'Installed skill must carry the same license')
    ui = yaml.safe_load((SKILL / 'agents/openai.yaml').read_text(encoding='utf-8'))['interface']
    require(all(isinstance(ui.get(k), str) and ui[k] for k in ['display_name', 'short_description', 'default_prompt']), 'Missing interface strings')
    require(25 <= len(ui['short_description']) <= 64, 'UI description must be 25-64 characters')
    require('$' + name in ui['default_prompt'], 'UI prompt must invoke the skill')
    require(len(text.splitlines()) < 500, 'Keep the entrypoint concise')


def files_and_links():
    count = 0
    for path in ROOT.rglob('*'):
        if not path.is_file() or any(part in IGNORED for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix not in TEXT_SUFFIXES and path.name not in {'LICENSE', '.gitignore', '.gitattributes'}:
            continue
        text = path.read_text(encoding='utf-8')
        require('\ufffd' not in text and not text.startswith('\ufeff'), f'Encoding problem: {path.relative_to(ROOT)}')
        if path.suffix != '.md':
            continue
        for target in re.findall(r'!?\[[^\]\n]*\]\(([^)\n]+)\)', without_code(text)):
            uri = urlsplit(target.strip().strip('<>'))
            if uri.scheme or target.startswith('#'):
                continue
            resolved = (path.parent / unquote(uri.path)).resolve()
            require(resolved.is_relative_to(ROOT.resolve()), f'Link escapes repository: {target}')
            require(resolved.exists(), f'Broken link in {path.name}: {target}')
            if path.is_relative_to(SKILL):
                require(resolved.is_relative_to(SKILL.resolve()), f'Installed skill depends on repository-only file: {target}')
            count += 1
    return count


def chapters_and_examples():
    for path in [SKILL / 'assets/prd-template.md', ROOT / 'examples/example-prd.md']:
        text = path.read_text(encoding='utf-8')
        require(re.findall(r'^# ([1-5])\. (.+)$', without_code(text), re.M) == CHAPTERS, f'Expected five main chapters: {path.name}')
    example = (ROOT / 'examples/example-prd.md').read_text(encoding='utf-8')
    require('【待填写】' not in example and 'xxxxxx' not in example, 'Example has template placeholders')
    acceptance = example.split('# 4. 验收标准', 1)[1].split('# 5.', 1)[0]
    rows = re.findall(r'^\| (T\d{2}) \|.*$', acceptance, re.M)
    require(rows == [f'T{i:02d}' for i in range(1, 13)], 'Example acceptance cases must be T01-T12')
    require(len(re.findall(r'\| 未执行 \|$', acceptance, re.M)) == len(rows), 'Example must not claim execution passed')
    require('【待填写】' not in (SKILL / 'SKILL.md').read_text(encoding='utf-8'), 'Unfinished skill entrypoint')
    return len(rows)


def main():
    try:
        frontmatter()
        links = files_and_links()
        cases = chapters_and_examples()
        workflow = yaml.safe_load((ROOT / '.github/workflows/validate.yml').read_text(encoding='utf-8'))
        require(isinstance(workflow, dict) and 'jobs' in workflow, 'Invalid workflow YAML')
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as error:
        print(f'FAIL: {error}', file=sys.stderr)
        return 1
    print(f'PASS: skill metadata, UI, MIT license, resource closure, {links} local links, five chapters, {cases} pending example cases and workflow YAML')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
