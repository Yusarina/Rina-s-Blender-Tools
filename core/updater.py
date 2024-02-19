import bpy
import requests
import zipfile
import shutil
import os

class AddonUpdater(bpy.types.Operator):
    bl_idname = "rinasplugin.addon_updater"
    bl_label = "Addon Updater"
    def __init__(self):
        self.repo = "Yusarina/Rinas-Blender-Tools-Updater-Test"
        self.latest_release = None
        
    def check_for_update(self):
        # Get latest release from GitHub API
        response = requests.get(f"https://api.github.com/repos/{self.repo}/releases/latest")
        latest_release = response.json()
        
        # Compare versions
        if latest_release["tag_name"] > bl_info["version"]:
            self.latest_release = latest_release  
            # Show update popup
            bpy.ops.rinas.update_available('INVOKE_DEFAULT')
            
    def install_update(self):
        # Download latest zip 
        download_url = self.latest_release["zipball_url"]
        zip_path = os.path.join("/tmp", "addon_update.zip")
        response = requests.get(download_url)
        with open(zip_path, "wb") as f:
            f.write(response.content)
            
        # Extract and copy files
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall("/tmp/addon_update")
            
        addon_path = os.path.dirname(os.path.realpath(__file__))
        tmp_path = os.path.join("/tmp/addon_update/", os.listdir("/tmp/addon_update")[0])
        
        # Copy updated files
        for src_dir, dirs, files in os.walk(tmp_path):
            dst_dir = src_dir.replace("/tmp/addon_update", "")
            if not os.path.exists(os.path.join(addon_path, dst_dir)):
                os.mkdir(os.path.join(addon_path, dst_dir))
            for file_ in files:
                src_file = os.path.join(src_dir, file_)
                dst_file = os.path.join(addon_path, dst_dir, file_)
                if os.path.exists(dst_file):
                    os.remove(dst_file)
                shutil.copy(src_file, addon_path)
        
        # Refresh addon
        bpy.ops.wm.addon_refresh()
  