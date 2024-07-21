# MiHoyo Auto Login

Scriptlet for doing daily logins for Mihoyo games.

## Installation

```shell
pip install .
```

## Usage

Create the credentials file

```yaml
---
users:
  - uid: 123123
    token: my_token123
  - uid: 456456
    token: another_token456
```

Running

[//]: <> (TODO update with console script)

```shell
python -m mihoyo_auto_login.main example.yml genshin
```
