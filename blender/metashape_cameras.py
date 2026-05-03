import bpy
import os

# ------------------------------------------------------------------------
#    Operator 
# ------------------------------------------------------------------------
class OBJECT_OT_assign_camera_images(bpy.types.Operator):
    """Assign images from a folder to matching cameras"""
    bl_idname = "object.assign_camera_images"
    bl_label = "Apply to All Cameras"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        folder_path = bpy.path.abspath(scene.ms_image_dir)
        scale_val = scene.ms_image_scale
        
        if not os.path.exists(folder_path):
            self.report({'ERROR'}, "Selected folder does not exist.")
            return {'CANCELLED'}

        available_images = {}
        for f in os.listdir(folder_path):
            full_path = os.path.join(folder_path, f)
            if os.path.isfile(full_path):
                name, ext = os.path.splitext(f)
                available_images[name] = full_path

        cams_updated = 0

        for obj in scene.objects:
            if obj.type == 'CAMERA':
                cam_name = obj.data.name 
                
                if cam_name in available_images:
                    img_path = available_images[cam_name]
                    img = bpy.data.images.load(filepath=img_path, check_existing=True)
                    
                    obj.data.show_background_images = True
                    obj.data.background_images.clear()
                    
                    bg = obj.data.background_images.new()
                    bg.image = img
                    
                    # Hardcoded to CROP based on workflow
                    bg.frame_method = 'CROP'
                    bg.scale = scale_val
                    
                    cams_updated += 1
                else:
                    print(f"Warning: No matching image found for '{cam_name}'")

        self.report({'INFO'}, f"Success! Assigned to {cams_updated} cameras at {scale_val} scale.")
        return {'FINISHED'}


# ------------------------------------------------------------------------
#    Panel 
# ------------------------------------------------------------------------
class VIEW3D_PT_metashape_cameras(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Metashape' 
    bl_label = "Camera Backgrounds"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="1. Select Undistorted Images:")
        layout.prop(scene, "ms_image_dir", text="") 
        
        layout.separator()
        
        layout.label(text="2. Master Scale:")
        layout.prop(scene, "ms_image_scale", text="Scale")
        
        layout.separator()
        
        layout.operator("object.assign_camera_images", icon='FILE_IMAGE')


# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------
classes = (
    OBJECT_OT_assign_camera_images,
    VIEW3D_PT_metashape_cameras,
)

def register():
    for cls in classes:
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass
            
    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.Scene.ms_image_dir = bpy.props.StringProperty(
        name="Image Directory", subtype='DIR_PATH'
    )
    
    # Precision increased to 5 to handle exact matches like 1.01600
    bpy.types.Scene.ms_image_scale = bpy.props.FloatProperty(
        name="Scale", default=1.00000, precision=5
    )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.ms_image_dir
    del bpy.types.Scene.ms_image_scale

if __name__ == "__main__":
    register()
