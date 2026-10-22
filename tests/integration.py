import os
from pathlib import Path
import shutil
import subprocess
import tempfile

SOURCE = Path(__file__).resolve().parents[1]
BLOCK = '<!-- lerd:begin -->\nlerd original\n<!-- lerd:end -->\n'

def run(args, env, ok=True):
    result = subprocess.run([str(a) for a in args], env=env, text=True, capture_output=True)
    if ok and result.returncode:
        raise AssertionError(f'{args}: {result.stdout}\n{result.stderr}')
    if not ok:
        assert result.returncode, args
    return result

with tempfile.TemporaryDirectory(prefix='dotagents-tests-') as temp:
    root = Path(temp)
    env = {k: v for k, v in os.environ.items() if not k.startswith(('DOTAGENTS_', 'XDG_', 'GIT_')) and k != 'CODEX_HOME'}
    home = root / 'home'
    home.mkdir()
    env.update(HOME=str(home), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null',
               GIT_AUTHOR_NAME='Test', GIT_AUTHOR_EMAIL='test@example.invalid',
               GIT_COMMITTER_NAME='Test', GIT_COMMITTER_EMAIL='test@example.invalid')
    repo = root / 'repo with spaces'
    shutil.copytree(SOURCE, repo, ignore=shutil.ignore_patterns('.git'))
    agents = [home / p for p in ['.codex/AGENTS.md', '.claude/CLAUDE.md', '.config/opencode/AGENTS.md', '.gemini/GEMINI.md']]
    for target in agents:
        target.parent.mkdir(parents=True)
        target.write_text(BLOCK)
    # Installation discovers conventional profiles, including names with spaces.
    profiles = [home / '.codex_work', home / '.codex-personal account']
    for profile, marker in zip(profiles, ['config.toml', 'auth.json']):
        profile.mkdir()
        (profile / marker).write_text('')
        (profile / 'AGENTS.md').write_text('previous rules\n')
    unrelated = home / '.codex_unrelated'
    unrelated.mkdir()
    run([repo / 'install.sh'], env)
    command = home / '.local/bin/dotagents-sync'
    state = home / '.local/state/dotagents'
    memory = home / '.local/share/dotagents/memory'
    for profile in profiles:
        assert (profile / 'AGENTS.md').is_symlink()
        assert (profile / 'AGENTS.md').resolve() == state / 'AGENTS.md'
        assert any(p.read_text() == 'previous rules\n' for p in profile.glob('AGENTS.md.bak-*'))
    assert not (unrelated / 'AGENTS.md').exists()
    assert (memory / '.git').is_dir()
    assert 'lerd original' in (state / 'AGENTS.md').read_text()
    assert 'lerd original' not in (state / 'CLAUDE.md').read_text()
    assert str(memory) in (state / 'AGENTS.md').read_text()
    for generated in ['AGENTS.md', 'CLAUDE.md']:
        rules = (state / generated).read_text()
        assert f'Edite {repo}/global.md' in rules
        assert 'inputmode="numeric"' in rules
        assert '3950' in rules
        assert 'Instruções do repositório dotagents' not in rules
    # Only global.md supplies shared rules; repository instructions stay local.
    with (repo / 'AGENTS.md').open('a') as instructions:
        instructions.write('\nREPOSITORY_ONLY_SENTINEL\n')
    with (repo / 'global.md').open('a') as shared:
        shared.write('\nSHARED_RULE_SENTINEL\n')
    run([command], env)
    for generated in ['AGENTS.md', 'CLAUDE.md']:
        rules = (state / generated).read_text()
        assert 'SHARED_RULE_SENTINEL' in rules
        assert 'REPOSITORY_ONLY_SENTINEL' not in rules
    for name, tags in [('plain', ''), ('tagged', 'applies_to: [php]\n')]:
        (memory / f'{name}.md').write_text(f'---\ndescription: {name}\n{tags}---\nBody\n')
    run([command], env)
    output = (state / 'AGENTS.md').read_bytes()
    assert f'[php] tagged ({memory}/tagged.md)' in output.decode()
    head = run(['git', '-C', memory, 'rev-parse', 'HEAD'], env).stdout
    backups = list(home.rglob('*.bak-*'))
    run([command], env)
    assert output == (state / 'AGENTS.md').read_bytes()
    assert head == run(['git', '-C', memory, 'rev-parse', 'HEAD'], env).stdout
    assert backups == list(home.rglob('*.bak-*'))
    # Sync also discovers profiles created after installation, without duplicates.
    later = home / '.codex_later'
    later.mkdir()
    (later / 'config.toml').write_text('')
    run([command], dict(env, CODEX_HOME=str(later) + '/'))
    assert (later / 'AGENTS.md').resolve() == state / 'AGENTS.md'
    assert not list(later.glob('AGENTS.md.bak-*'))
    # Custom Codex profiles receive instructions and preserve existing files.
    profile = home / 'custom codex'
    profile.mkdir()
    (profile / 'AGENTS.md').write_text('existing profile rules\n')
    profile_env = dict(env, CODEX_HOME=str(profile))
    run([command], profile_env)
    assert (profile / 'AGENTS.md').is_symlink()
    assert (profile / 'AGENTS.md').resolve() == state / 'AGENTS.md'
    assert any(p.read_text() == 'existing profile rules\n' for p in profile.glob('AGENTS.md.bak-*'))
    profile_backups = list(profile.glob('AGENTS.md.bak-*'))
    run([command], profile_env)
    assert profile_backups == list(profile.glob('AGENTS.md.bak-*'))
    run([command], dict(env, CODEX_HOME='relative'), ok=False)
    # Freeze timestamps to prove backup uniqueness in the same second.
    tools = root / 'tools'
    tools.mkdir()
    date = tools / 'date'
    date.write_text('#!/bin/sh\necho 20261020120000\n')
    date.chmod(0o755)
    frozen = dict(env, PATH=f'{tools}:{env["PATH"]}')
    for text in ['first', 'second']:
        agents[0].unlink()
        agents[0].write_text(BLOCK.replace('original', text))
        run([command], frozen)
    unique = list(agents[0].parent.glob('AGENTS.md.bak-20261020120000-*'))
    assert len(unique) == 2
    assert 'lerd second' in (state / 'AGENTS.md').read_text()
    assert 'lerd second' not in (state / 'CLAUDE.md').read_text()
    # Overrides, empty and relative XDG settings, unrelated cwd.
    custom = dict(env, DOTAGENTS_DATA=str(root / 'custom data'), DOTAGENTS_CONFIG=str(root / 'custom config'),
                  DOTAGENTS_STATE=str(root / 'custom state'), XDG_CONFIG_HOME=str(root / 'xdg config'))
    (root / 'custom config').mkdir()
    (root / 'custom config/local.md').write_text('PERSONAL RULE\n')
    run([repo / 'install.sh'], custom)
    assert 'PERSONAL RULE' in (root / 'custom state/AGENTS.md').read_text()
    run([command], dict(env, DOTAGENTS_DATA='relative'), ok=False)
    run([command], dict(env, XDG_DATA_HOME='relative', XDG_STATE_HOME='', XDG_CONFIG_HOME=''), ok=True)
    assert (state / 'AGENTS.md').exists()
    xdg = dict(env, XDG_DATA_HOME=str(root / 'xdg data'), XDG_STATE_HOME=str(root / 'xdg state'),
               XDG_CONFIG_HOME=str(root / 'xdg config'))
    run([repo / 'install.sh'], xdg)
    assert (root / 'xdg data/dotagents/memory/.git').is_dir()
    assert (root / 'xdg state/dotagents/AGENTS.md').is_file()
    assert not (root / 'xdg config/opencode').exists()
    capped = run([command], dict(env, INDEX_CAP='1'))
    assert 'teto' in capped.stderr
    assert 'plain' in (state / 'AGENTS.md').read_text()
    assert 'tagged' in (state / 'AGENTS.md').read_text()
    # Legacy migration with tracked clone, git memory history, external-only block and skills.
    legacy_home = root / 'legacy home'
    legacy = legacy_home / '.agents'
    shutil.copytree(repo, legacy)
    old_env = dict(env, HOME=str(legacy_home))
    run(['git', '-C', legacy, 'init', '-q', '-b', 'main'], old_env)
    run(['git', '-C', legacy, 'add', '.'], old_env)
    run(['git', '-C', legacy, 'commit', '-qm', 'test: fixture'], old_env)
    run(['git', '-C', legacy, 'remote', 'add', 'origin', 'https://example.invalid/repo'], old_env)
    (legacy / 'skills').mkdir()
    skill = legacy / 'skills/untouched'
    skill.write_text('untouched')
    inode = skill.stat().st_ino
    (legacy / 'memory').mkdir()
    run(['git', '-C', legacy / 'memory', 'init', '-q', '-b', 'main'], old_env)
    (legacy / 'memory/a.md').write_text('---\ndescription: preserved\n---\n')
    run(['git', '-C', legacy / 'memory', 'add', '.'], old_env)
    run(['git', '-C', legacy / 'memory', 'commit', '-qm', 'test: memory'], old_env)
    old_head = run(['git', '-C', legacy / 'memory', 'rev-parse', 'HEAD'], old_env).stdout
    (legacy / 'local.md').write_text('PRIVATE\n')
    (legacy / 'build/external').mkdir(parents=True)
    (legacy / 'build/external/lerd.md').write_text(BLOCK)
    (legacy / 'build/AGENTS.md').write_text(BLOCK)
    (legacy_home / '.codex').mkdir()
    (legacy_home / '.codex/AGENTS.md').symlink_to(legacy / 'build/AGENTS.md')
    dest = legacy_home / 'dev/dotagents'
    run([legacy / 'bin/migrate', legacy_home], old_env, ok=False)
    run([legacy / 'bin/migrate', dest], old_env)
    assert sorted(p.name for p in legacy.iterdir()) == ['skills']
    assert skill.stat().st_ino == inode
    assert run(['git', '-C', dest, 'remote', 'get-url', 'origin'], old_env).stdout.strip() == 'https://example.invalid/repo'
    migrated_memory = legacy_home / '.local/share/dotagents/memory'
    assert run(['git', '-C', migrated_memory, 'rev-parse', 'HEAD'], old_env).stdout == old_head
    migrated_state = legacy_home / '.local/state/dotagents'
    assert BLOCK in (migrated_state / 'AGENTS.md').read_text()
    assert 'PRIVATE' in (migrated_state / 'AGENTS.md').read_text()
    assert BLOCK not in (migrated_state / 'CLAUDE.md').read_text()
    assert (legacy_home / '.codex/AGENTS.md').resolve() == migrated_state / 'AGENTS.md'
    run([legacy_home / '.local/bin/dotagents-sync'], old_env)
    print('OK: installation, symlink command, memories, idempotence, backups, overrides and legacy migration')
