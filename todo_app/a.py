import os
import shutil

cur_dir = os.curdir
src_avatar = os.path.join(cur_dir, 'todo_app/static/default/avatar.jpg')
dest_folder = os.path.join(cur_dir, 'todo_app/static/user')
shutil.copy(src_avatar, dest_folder)
dest_avatar = dest_folder + 'avatar.jpg'
new_avatar = dest_folder + '1111' + '.jpg'
if os.path.isfile(new_avatar):
    os.remove(new_avatar)
os.rename(dest_avatar, new_avatar)