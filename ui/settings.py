import bpy
import os
from core.translations import t
from addon_updater_ops import AddonUpdaterCheckNow, AddonUpdaterInstallManually, updater, AddonUpdaterEndBackground, AddonUpdaterUpdateNow, AddonUpdaterUpdateTarget, AddonUpdaterRestoreBackup

class SettingsSubMenu(bpy.types.Menu):
    bl_idname = 'VIEW3D_MT_RINA_Settings'
    bl_label = "SettingsSubMenu.label"
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        box = layout.box()
        
        col = box.column(align=True)
        col.label(text=t("SettingsSubMenu.LanguageLabel"))

        col.separator()
        col.separator()
        
        split = col.row(align=True)
        split.prop(context.scene, 'plugin_language', text='')

        col.separator()
        
        element = self.layout
        box = element.box()

        col.separator()

        col = box.column(align=True)
        col.label(text=t("SettingsSubMenu.UpdateLabel"))

        col.separator()

		# Updater draw function, could also pass in col as third arg.
        row = box.row()
        col = row.column()
        if updater.error is not None:
            sub_col = col.row(align=True)
            sub_col.scale_y = 1
            split = sub_col.split(align=True)
            split.scale_y = 2
            if "ssl" in updater.error_msg.lower():
                split.enabled = True
                split.operator(AddonUpdaterInstallManually.bl_idname,
                            text=updater.error)
            else:
                split.enabled = False
                split.operator(AddonUpdaterCheckNow.bl_idname,
                            text=updater.error)
            split = sub_col.split(align=True)
            split.scale_y = 2
            split.operator(AddonUpdaterCheckNow.bl_idname,
                        text="", icon="FILE_REFRESH")

        elif updater.update_ready is None and not updater.async_checking:
            col.scale_y = 2
            col.operator(AddonUpdaterCheckNow.bl_idname)
        elif updater.update_ready is None:  # async is running
            sub_col = col.row(align=True)
            sub_col.scale_y = 1
            split = sub_col.split(align=True)
            split.enabled = False
            split.scale_y = 2
            split.operator(AddonUpdaterCheckNow.bl_idname, text=(t("SettingsSubMenu.CheckingUpdate")))
            split = sub_col.split(align=True)
            split.scale_y = 2
            split.operator(AddonUpdaterEndBackground.bl_idname, text="", icon="X")

        elif updater.include_branches and \
                len(updater.tags) == len(updater.include_branch_list) and not \
                updater.manual_only:
            # No releases found, but still show the appropriate branch.
            sub_col = col.row(align=True)
            sub_col.scale_y = 1
            split = sub_col.split(align=True)
            split.scale_y = 2
            update_now_txt = "Update directly to {}".format(
                updater.include_branch_list[0])
            split.operator(AddonUpdaterUpdateNow.bl_idname, text=update_now_txt)
            split = sub_col.split(align=True)
            split.scale_y = 2
            split.operator(AddonUpdaterCheckNow.bl_idname,
                        text="", icon="FILE_REFRESH")

        elif updater.update_ready and not updater.manual_only:
            sub_col = col.row(align=True)
            sub_col.scale_y = 1
            split = sub_col.split(align=True)
            split.scale_y = 2
            split.operator(AddonUpdaterUpdateNow.bl_idname,
                        text=(t("SettingsSubMenu.UpdateNow") + str(updater.update_version)))
            split = sub_col.split(align=True)
            split.scale_y = 2
            split.operator(AddonUpdaterCheckNow.bl_idname,
                        text="", icon="FILE_REFRESH")

        elif updater.update_ready and updater.manual_only:
            col.scale_y = 2
            dl_now_txt = "Download " + str(updater.update_version)
            col.operator("wm.url_open",
                        text=dl_now_txt).url = updater.website
        else:  # i.e. that updater.update_ready == False.
            sub_col = col.row(align=True)
            sub_col.scale_y = 1
            split = sub_col.split(align=True)
            split.enabled = False
            split.scale_y = 2
            split.operator(AddonUpdaterCheckNow.bl_idname,
                        text=(t("SettingsSubMenu.UpToDate")))
            split = sub_col.split(align=True)
            split.scale_y = 2
            split.operator(AddonUpdaterCheckNow.bl_idname,
                        text="", icon="FILE_REFRESH")

        if not updater.manual_only:
            col = row.column(align=True)
            if updater.include_branches and len(updater.include_branch_list) > 0:
                branch = updater.include_branch_list[0]
                col.operator(AddonUpdaterUpdateTarget.bl_idname,
                            text="Install {} / old version".format(branch))
            else:
                col.operator(AddonUpdaterUpdateTarget.bl_idname,
                            text=(t("SettingsSubMenu.ReinstallAddon")))
                        
            last_date = "none found"
            backup_path = os.path.join(updater.stage_path, "backup")
            if "backup_date" in updater.json and os.path.isdir(backup_path):
                if updater.json["backup_date"] == "":
                    last_date = "Date not found"
                else:
                    last_date = updater.json["backup_date"]
            backup_text = (t('SettingsSubMenu.RestoreAddon') + last_date)
            col.operator(AddonUpdaterRestoreBackup.bl_idname, text=backup_text)

        row = box.row()
        row.scale_y = 0.7
        last_check = updater.json["last_check"]
        if updater.error is not None and updater.error_msg is not None:
            row.label(text=updater.error_msg)
        elif last_check:
            last_check = last_check[0: last_check.index(".")]
            row.label(text=t("SettingsSubMenu.UpdateLastChecked") + last_check)
        else:
            row.label(text=t("SettingsSubMenu.UpdateLastCheckedNone"))
      