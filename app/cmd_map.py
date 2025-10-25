from .handler import Handler

cmd_map = {
    "exit": Handler.handle_exit,
    "echo": Handler.handle_echo, 
    "type": Handler.handle_type
}