# Copy Selected Comments

Copy selected comments from specified file.

## Prerequisite

```bash
pip3 -m venv .venv
pip3 install -r requirements.txt
```

```bash
zypper install xauth
xauth add :0 MIT-MAGIC-COOKIE-1 $(openssl rand -hex 16)
```

```bash
zypper install gnome-screenshot
```

## Build

```bash
python3 -m build
pip3 install -e .
```

## Run

```bash
python3 -m copy_selected_comments.gui
```

## Remarks

This program was created by AI (Copilot) assisted programming.
