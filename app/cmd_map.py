from .handler import Handler

cmd_map = {
    "exit": Handler.handle_exit,
    "echo": Handler.handle_echo, 
    "type": Handler.handle_type,
    "pwd": Handler.handle_pwd,
    "cd": Handler.handle_cd,
    "history": Handler.handle_history, 
    }