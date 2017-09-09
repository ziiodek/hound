import os
import shutil

class Uploader:
    dir_path = "/home/level_zero/envs/houndenv/hound/hound_app/static/hound/data"

    def upload_file(file,directory):
        if not os.path.isfile(Uploader.dir_path+directory+file.name):
            os.path.join(Uploader.dir_path+directory,file.name)
	    

    def create_directory(directory):
        if not os.path.isdir(Uploader.dir_path+directory):
            os.makedirs(Uploader.dir_path+directory)

    def move_file(old_path,new_path):
        if not os.path.isfile(Uploader.dir_path+new_path):
            shutil.move(old_path,Uploader.dir_path+new_path)

    def clear_directory(directory_path):
        for root, dirs, files in os.walk(Uploader.dir_path+directory_path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    def clear_tmp_dir(directory_path):
        for root, dirs, files in os.walk(directory_path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    def get_path(file_path):
        return Uploader.dir_path.replace("\hound\data","")+'/'+file_path

