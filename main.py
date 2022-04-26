#importing modules
from ursina import*
from ursina.prefabs.file_browser import *
from ursina.shaders import *
from ursina.prefabs.first_person_controller import FirstPersonController as fpc
from ursina.prefabs.dropdown_menu import *
import json





#Define window
app=Ursina()

#inp=input("What is the name of your game")
def buildthis():
    gameName=""
    global inp
    g=inp.split(' ')
    for i in range(len(g)):
        gameName+=g[i]
    print(gameName)
    os.system('cmd /k "color a & python -m ursina.build"')
    os.rename("build", gameName)


#Define entities
#c=Draggable(parent=scene, model='cube',
#                shader=lit_with_shadows_shader,
#                plane_direction=(1,1,1), color=color.gray,
#                highlight_color=color.gray, enabled=False)


c=Entity(parent=scene, model='cube',
                shader=lit_with_shadows_shader,
                plane_direction=(1,1,1), color=color.gray,
                highlight_color=color.gray, collider='mesh',
                enabled=False)

#Starting stuff
os.system("bat\\test.bat")
os.system("bat\\write.bat")
#Window settings
window.show_ursina_splash=True
window.borderless=False
window.title='Ursina game engine'
window.exit_button.visible = False
window.fps_counter.visible = False
window.icon='folder'
window.development_mode=False
window.fullscreen=False
build_nmbr=Text(text='build 8', position=(-.88,-.47,0), color=color.light_text, parent=camera.ui)

#Variable/list definitions
codepath='build_files/main.py'
code=[]
num=1
num2=1
cubepos=''
fpc_camera=False
a=False

#define dropdown_menu
blue_btn=DropdownMenuButton('blue', enabled=False)
c_menu=DropdownMenu('Cube', enabled=False, Buttons=(
    DropdownMenu('Change color', enabled=False, Buttons=(
        blue_btn
        ))
    ))

#Lighting
pivot=Entity(position=(0,10,0))
light=AmbientLight(pivot=pivot, shadows=True)

#Skybox
skybox = Sky()

#Define ui panels
fb=FileBrowser(file_types=('.obj', '.blend', '.gltf', '.glb'), enabled=False)
ui_left=Panel(parent=camera.ui,position=(-.7,0,0), scale_x=.5)
ui_right=Panel(position=(.7,0,0), scale_x=.5)
#Define button commands
def new_cube():
    global num, cubepos
    c.enable()
    
    num+=1
    #c.enable()
#    with open(codepath, 'a') as f:
#        f.write(f'cube_1 = Entity(model="cube", color=color.gray, shader=lit_with_shadows_shader) \n')
#        num+=1
#        f.close()
#    c_pbtn.enable()
    #entitys.append(c)
    #print(entitys)
#def custom_entity():
#    global num2
#    fb.enable()
#    build_btn.disable()
#    def on_submit(paths):
#        build_btn.enable()
#        print('--------', paths)
#        for p in paths:
#            print('---', p)
#            d=str(p).split('\\')
#            print(d)
#            print()
#            model2=d[len(d)-1]
#            print(model2)
#            ce=Draggable(model=model2, parent=scene, color=color.gray, highlight_color=color.gray, plane_direction=(1,1,1))
#            with open(codepath, 'a') as f:
#                f.write(f'entity = Entity(model="{model2}"')
#                f.close()
#    fb.on_submit = on_submit

g = InputField(name='gameName', enabled = False)
def openBuildMenu():
    
    wp = WindowPanel(
        title='Build settings',
        content=(
            Text('Name of your game'),
            g,
            Button(text='Submit', color=color.azure, on_click = build),
            Slider(),
            Slider(),
            ),
        popup=True,
        enabled=True
        )
    g.enable()
g.text = 'Standard Application'
def build():
    gameName = g
    global cubepos
    #cubepos=c.position
    with open(codepath, 'a') as f:
        print('Building program')
        for x in range(len(code)):
            f.write(code[x]+" \n")
        if fpc_camera == False:
            f.write(f'EditorCamera(origin={camera_pos.position}) \n')
        elif fpc_camera == True:
            f.write(f"fpc=FPC(origin={camera_pos.position}) \n")
        f.write('app.run() \n')
        f.close()
    os.system('cmd /k "cd build_files & python -m ursina.build"')
    os.rename('build_files', gameName.text)

    


#Define setting stuff
def fullscreen():
    if window.fullscreen==True:
        window.fullscreen==False
    elif window.fullscreen==False:
        window.fullscreen==True
settings = WindowPanel(
    title='Settings',
    content=(
        Button(text='Toggle fullscreen', color=color.azure, on_click=fullscreen),
        ),
        popup=False,
        enabled=False
    )
b1=Button(text='First person camera', color=color.black33)
b2=Button(text='Standard camera', color=color.azure, highlight_color=color.black10)
def settings1():
    print(settings.enabled)
    if settings.enabled==True:
        #print('settings.enabled = True')
        settings.close()
    elif settings.enabled==False:
        settings.enabled = True
def FPC_camera():
    global fpc_camera
    fpc_camera=True
    b1.color=color.azure
    b2.color=color.black33
def normal_camera():
    global fpc_camera
    fpc_camera=False
    b2.color=color.azure
    b1.color=color.black33
b1.on_click=FPC_camera
b2.on_click=normal_camera
camera_settings=WindowPanel(title='Camera', content=(
    b1,
    b2))
def save():
    print('saved code')
    with open(f'{g.text}.json', 'w') as f:
        for i in range(len(code)):
            r = code[i]
            r2 = []
            r2 = r.split('=')
            r2.pop(0)
            cont = {
                'model':r2[1].split(',')[0],
                'collider':r2[3].split(',')[0],
                'color':r2[4].split(',')[0],
                'position':r2[5].split('(')[1].split(')')[0],
            }
            #print(cont)
            #print(r2)
            f.write(json.dumps(cont)+'\n')
        f.close()
#Define buttons
new_cube_btn=Button(parent=ui_left, text='Add new cube', scale_y=.1, scale_x=1)
custom_btn=Button(parent=ui_left, y=-.1, text='Import custom model', scale_y=.1, scale_x=1)
build_btn=Button(y=.45, text='Build', scale_y=.1, scale_x=1)
#settings_btn=Button(icon='cog', scale=.1, position=window.top_right-.05, color=color.gray)
#Add button commads to button
unfinished_content_tooltip=Tooltip(text='Not working yet')
custom_btn.tooltip=unfinished_content_tooltip
cube_tooltip=Tooltip(text='Add a draggable cube to build your game')
new_cube_btn.tooltip=cube_tooltip
new_cube_btn.on_click=new_cube
#custom_btn.on_click=custom_entity
build_btn.on_click=openBuildMenu
#settings_btn.on_click=settings1

#camera settings
ec=EditorCamera()

#Playtest
ct=Tooltip(text='camera.pivot')
camera_pos=Draggable(parent=scene, model='quad', color=color.red, plane_direction=(1,1,1), scale=.2)
camera_pos.tooltip=ct
def playtest():
    global a
    global fpc_camera
    global fp
    if a==False:
        print(fpc_camera)
        if fpc_camera==False:
            ec.position=camera_pos.position
            ec.enable()
            #camera.billboard=True
            #print(camera.world_rotation)
        elif fpc_camera==True:
            ec.disable()
            fp=fpc()
            fp.position=camera_pos.position
        camera_settings.disable()
        camera_pos.disable()
        ptbtn.disable()
        ui_right.disable()
        ui_left.disable()
        a=True
    elif a==True:
        try:
            fp.enabled=False
            ec.enable()
        except:
            fpc_camera=False
        camera_settings.enable()
        camera_pos.enable()
        ptbtn.enable()
        ec.position=(0,0,0)
        ui_left.enable()
        ui_right.enable()
        a=False

ptbtnt=Tooltip(text='Press enter to start/stop playtest')
ptbtn=Button(icon='arrow_right', on_click=playtest, scale=.1, y=.45)
ptbtn.tootlip=ptbtnt


#Filewrite handling
if not os.path.exists(codepath):
    os.mkdir('build_files')
try:
    with open("build_files\\main.py", 'x') as f:
        pass
except:
    pass
with open(codepath, 'w') as f:
    f.write('')
    f.close()
with open('build_files/main.py', 'a') as f:
    f.write('from ursina import * \n')
    f.write('from ursina.shaders import * \n')
    f.write('from ursina.prefabs.first_person_controller import FirstPersonController as FPC \n')
    f.write('app=Ursina() \n')
    f.write('Sky()')
    f.close()

#Update Loop
def update():
    c.x=mouse.x*10
    if o==False:
        c.y=mouse.y*10
    elif o==True:
        c.z=mouse.x*10
#input loop
o=False
def input(key):
    global o, num
    if key == 'enter':
        playtest()
    if key == 'g':
        if o == False:
            o = True
        elif o == True:
            o = False
    if key == 's':
        save()
    if key == 'left mouse down':
        if c.enabled == True:
            code.append(f"c{num}=Entity(model='cube', shader=lit_with_shadows_shader, collider='mesh', color=color.gray, position = {c.position})")
            
            c2=Entity(parent=scene, model='cube',
                    shader=lit_with_shadows_shader,
                    plane_direction=(1,1,1), color=color.gray,
                    highlight_color=color.gray, collider='mesh',
                    position=c.position)
            c.disable()


app.run()

