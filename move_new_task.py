import shutil, datetime, os
src = 'D:/Dev/AI-TCP/cli_instruction/new_task.json'
dest_dir = 'D:/Dev/AI-TCP/cli_archives'
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
dest_name = f'new_task_{timestamp}.json'
shutil.move(src, os.path.join(dest_dir, dest_name))