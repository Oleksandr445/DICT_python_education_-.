import sys
import os
import hashlib
import shutil

VCS_DIR = "vcs"
CONFIG_FILE = os.path.join(VCS_DIR, "config.txt")
INDEX_FILE = os.path.join(VCS_DIR, "index.txt")
LOG_FILE = os.path.join(VCS_DIR, "log.txt")
COMMITS_DIR = os.path.join(VCS_DIR, "commits")


def ensure_vcs():
    os.makedirs(VCS_DIR, exist_ok=True)
    os.makedirs(COMMITS_DIR, exist_ok=True)

    for file in [CONFIG_FILE, INDEX_FILE, LOG_FILE]:
        if not os.path.exists(file):
            open(file, "w").close()


def read_file(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


def write_file(path, data):
    with open(path, "w") as f:
        f.write(data)


def show_help():
    print("""These are VCS commands:
config Get and set a username.
add Add a file to the index.
log Show commit logs.
commit Save changes.
checkout Switch between commits and restore a previous file state.""")


def config(args):
    ensure_vcs()

    if len(args) == 0:
        username = read_file(CONFIG_FILE)
        if username:
            print(f"The username is {username}.")
        else:
            print("Please, tell me who you are.")
    else:
        write_file(CONFIG_FILE, args[0])
        print(f"The username is {args[0]}.")


def add(args):
    ensure_vcs()

    if len(args) == 0:
        files = read_file(INDEX_FILE)
        if files:
            print("Tracked files:")
            print(files)
        else:
            print("Add a file to the index.")
        return

    filename = args[0]

    if not os.path.exists(filename):
        print(f"Can't find '{filename}'.")
        return

    files = read_file(INDEX_FILE).splitlines()

    if filename not in files:
        with open(INDEX_FILE, "a") as f:
            f.write(filename + "\n")

    print(f"The file '{filename}' is tracked.")


def get_hash():
    files = read_file(INDEX_FILE).splitlines()
    hash_obj = hashlib.sha1()

    for file in files:
        if os.path.exists(file):
            with open(file, "rb") as f:
                hash_obj.update(f.read())

    return hash_obj.hexdigest()


def commit(args):
    ensure_vcs()

    if len(args) == 0:
        print("Message was not passed.")
        return

    message = args[0]
    files = read_file(INDEX_FILE).splitlines()

    if not files:
        print("Nothing to commit.")
        return

    new_hash = get_hash()
    log_content = read_file(LOG_FILE)

    if new_hash in log_content:
        print("Nothing to commit.")
        return

    commit_path = os.path.join(COMMITS_DIR, new_hash)
    os.makedirs(commit_path, exist_ok=True)

    for file in files:
        if os.path.exists(file):
            shutil.copy(file, commit_path)

    username = read_file(CONFIG_FILE)

    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"commit {new_hash}\n")
        log_file.write(f"Author: {username}\n")
        log_file.write(f"{message}\n\n")

    print("Changes are committed.")


def show_log():
    ensure_vcs()

    content = read_file(LOG_FILE)

    if not content:
        print("No commits yet.")
        return

    print(content)


def checkout(args):
    ensure_vcs()

    if len(args) == 0:
        print("Commit id was not passed.")
        return

    commit_id = args[0]
    commit_path = os.path.join(COMMITS_DIR, commit_id)

    if not os.path.exists(commit_path):
        print("Commit does not exist.")
        return

    for file in os.listdir(commit_path):
        shutil.copy(os.path.join(commit_path, file), file)

    print(f"Switched to commit {commit_id}.")


def main():
    args = sys.argv[1:]

    if not args or args[0] == "--help":
        show_help()
        return

    command = args[0]
    params = args[1:]

    commands = {
        "config": config,
        "add": add,
        "commit": commit,
        "log": show_log,
        "checkout": checkout
    }

    if command in commands:
        commands[command](params)
    else:
        print(f"'{command}' is not a VCS command.")


if __name__ == "__main__":
    main()