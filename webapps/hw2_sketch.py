# Import javascript modules
from js import THREE, window, document, Object, console
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math
# Import NumPy as np
import numpy as np



#-----------------------------------------------------------------------
# USE THIS FUNCTION TO WRITE THE MAIN PROGRAM
def main():
    #-----------------------------------------------------------------------
    # VISUALS
    global renderer, scene, camera, controls, composer
    
    # General Settings - Renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize(window.innerWidth/1.02,window.innerHeight/1.02)
    document.body.appendChild(renderer.domElement)
    
    # General Settings - Scene
    scene = THREE.Scene.new()
    back_color = THREE.Color.new('#152238')
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(75,(window.innerWidth/1.02)/(window.innerHeight/1.02), 0.1, 10000)
    camera.position.z = 3000
    camera.zoom = 1
    scene.add(camera)
    
    # Window Resize
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy)
    
    # Post Processing
    global composer
    post_process() 
    #-----------------------------------------------------------------------
    #DESIGN
    # Geometry
    global geom1_params, my_axiom_system, my_axiom_system1, my_axiom_system2, max_iterations
    max_iterations = ()
    geom1_params = {
            'x':3
    }
    geom1_params = Object.fromEntries(to_js(geom1_params))
    my_axiom_system = []
    my_axiom_system1 = system1(0, 3, "X")
    my_axiom_system2 = system2(0, 3, "Y")
    my_axiom_system.append(my_axiom_system1)
    my_axiom_system.append(my_axiom_system2)
    

    console.log(my_axiom_system1)

    draw_system1(my_axiom_system1, THREE.Vector3.new(0,0,0))
    draw_system2(my_axiom_system2, THREE.Vector3.new(0,0,0))


    #-----------------------------------------------------------------------
    # UI
    # Controls
    controls = THREE.OrbitControls.new(camera, renderer.domElement)
    controls.enableRotate = False
    # Gui
    gui = window.dat.GUI.new()
    param_folder = gui.addFolder('Parameters')
    param_folder.add(geom1_params, 'x', 1,10,1)
    param_folder.open()
    
    #-----------------------------------------------------------------------
    # RENDER / UPDATE
    render()
    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS
# Define RULES in a function which takes one SYMBOL and applies rules generation
def generate1(symbol1):
    if symbol1 == "X":
        return "F[+X]F[+X]+F[-X]+X"
    elif symbol1 == "F":
        return "FF"
    elif symbol1 == "+":
        return "+"
    elif symbol1 == "-":
        return "-"
    elif symbol1 == "[":
        return "["
    elif symbol1 == "]":
        return "]"

def generate2(symbol2):
    if symbol2 == "Y":
        return "G[+Y][-Y]+G*Y"
    elif symbol2 == "G":
        return "GG"
    elif symbol2 == "+":
        return "+"
    elif symbol2 == "*":
        return "*"
    elif symbol2 == "-":
        return "-"
    elif symbol2 == "[":
        return "["
    elif symbol2 == "]":
        return "]"
# A recursive fundtion, which taken an AXIOM as an inout and runs the generate function for each symbol
def system1(current_iteration1, max_iterations, axiom1):
    current_iteration1 += 1
    new_axiom1 = ""
    for symbol1 in axiom1:
        new_axiom1 += generate1(symbol1)
    if current_iteration1 >= max_iterations:
        return new_axiom1
    else:
        return system1(current_iteration1, max_iterations, new_axiom1)
    
def system2(current_iteration2, max_iterations, axiom2):
    
    current_iteration2 += 1
    new_axiom2 = ""
    for symbol2 in axiom2:
        new_axiom2 += generate2(symbol2)
    if current_iteration2 >= max_iterations:
        return new_axiom2
    else:
        return system2(current_iteration2, max_iterations, new_axiom2)
    

                
def draw_system1(axiom1, start_pt1):
    global lines1,line1,vis_line1,crv1,material1
    move_vec1 = THREE.Vector3.new(1,10,0)
    old_states1 = []
    old_move_vecs1 = []
    lines1 = []

    for symbol1 in axiom1:
        if symbol1 == "F" or symbol1 == "X":
            old1 = THREE.Vector3.new(start_pt1.x, start_pt1.y, start_pt1.z)
            new_pt1 = THREE.Vector3.new(start_pt1.x, start_pt1.y, start_pt1.z)
            new_pt1 = new_pt1.add(move_vec1)
            line1 = []
            line1.append(old1)
            line1.append(new_pt1)
            lines1.append(line1)

            start_pt1 = new_pt1

        elif symbol1 == "+": 
            move_vec1.applyAxisAngle(THREE.Vector3.new(0,0,1), math.pi/7)
        
        elif symbol1 == "-":
            move_vec1.applyAxisAngle(THREE.Vector3.new(0,0,1), -math.pi/7)
        
        elif symbol1 == "[":
            old_state1 = THREE.Vector3.new(start_pt1.x, start_pt1.y, start_pt1.z)
            old_move_vec1 = THREE.Vector3.new(move_vec1.x, move_vec1.y, move_vec1.z)
            old_states1.append(old_state1)
            old_move_vecs1.append(old_move_vec1)

        elif symbol1 == "]":
            start_pt1 = THREE.Vector3.new(old_states1[-1].x, old_states1[-1].y, old_states1[-1].z)
            move_vec1 = THREE.Vector3.new(old_move_vecs1[-1].x, old_move_vecs1[-1].y, old_move_vecs1[-1].z)
            old_states1.pop(-1)
            old_move_vecs1.pop(-1)

    for points1 in lines1:
        line_geom1 = THREE.BufferGeometry.new()
        points1 = to_js(points1)
        
        console.log(points1)

        line_geom1.setFromPoints( points1 )

        material1 = THREE.LineBasicMaterial.new( THREE.Color.new('#ff8800'))
        vis_line1 = THREE.Line.new( line_geom1, material1 )

        global scene
        crv1 = []
        crv1.append(vis_line1)
        scene.add(crv1)
        
def draw_system2(axiom2, start_pt2):
    global lines2,line2,vis_line2,crv2,material2
    move_vec2 = THREE.Vector3.new(5,15,5)
    old_states2 = []
    old_move_vecs2 = []
    lines2 = []

    for symbol2 in axiom2:
        if symbol2 == "G" or symbol2 == "Y":
            old2 = THREE.Vector3.new(start_pt2.x, start_pt2.y, start_pt2.z)
            new_pt2 = THREE.Vector3.new(start_pt2.x, start_pt2.y, start_pt2.z)
            new_pt2 = new_pt2.add(move_vec2)
            line2 = []
            line2.append(old2)
            line2.append(new_pt2)
            lines2.append(line2)

            start_pt2 = new_pt2

        elif symbol2 == "+": 
            move_vec2.applyAxisAngle(THREE.Vector3.new(0,0,1), math.pi/7)
        
        elif symbol2 == "-":
            move_vec2.applyAxisAngle(THREE.Vector3.new(0,0,1), -math.pi/7)
        
        elif symbol2 == "[":
            old_state2 = THREE.Vector3.new(start_pt2.x, start_pt2.y, start_pt2.z)
            old_move_vec2 = THREE.Vector3.new(move_vec2.x, move_vec2.y, move_vec2.z)
            old_states2.append(old_state2)
            old_move_vecs2.append(old_move_vec2)

        elif symbol2 == "]":
            start_pt2 = THREE.Vector3.new(old_states2[-1].x, old_states2[-1].y, old_states2[-1].z)
            move_vec2 = THREE.Vector3.new(old_move_vecs2[-1].x, old_move_vecs2[-1].y, old_move_vecs2[-1].z)
            old_states2.pop(-1)
            old_move_vecs2.pop(-1)

    for points2 in lines2:
        line_geom2 = THREE.BufferGeometry.new()
        points2 = to_js(points2)
        
        console.log(points2)

        line_geom2.setFromPoints( points2 )

        material2 = THREE.LineBasicMaterial.new( THREE.Color.new('#ff8800'))
        vis_line2 = THREE.Line.new( line_geom2, material2 )

        global scene
        crv2 = []
        crv2.append(vis_line2)
        scene.add(crv2)


    
        
def update1():
        if (geom1_params.x) != 0:
            if (geom1_params.x) != max_iterations:
                crv1 = []
                vis_line1 = ()
                for vis_line1 in crv1: scene.remove(vis_line1)
                
                for i in range(geom1_params.x):
                    for points1 in lines1:
                        line_geom1 = THREE.BufferGeometry.new()
                        points1 = to_js(points1)
                        
                        console.log(points1)

                        line_geom1.setFromPoints( points1 )

                        material1 = THREE.LineBasicMaterial.new( THREE.Color.new(0x0000ff))
                        vis_line1 = THREE.Line.new( line_geom1, material1 )

                        scene.add(vis_line1)  
            else:
                for i in range(len(my_axiom_system1)): 
                    line_geom1 = vis_line1[i]
                    line_geom1 = THREE.BufferGeometry.new()
                    points1 = to_js(points1)
                        
                    console.log(points1)

                    line_geom1.setFromPoints( points1 )

                    vis_line1 = THREE.Line.new( line_geom1, material1 )
        else:
            pass
                    
def update2():
        if (geom1_params.x) != 0:
            if (geom1_params.x) != max_iterations:
                crv2 = []
                vis_line2 = ()
                for vis_line2 in crv2: scene.remove(vis_line2)
                
                for i in range(geom1_params.x):
                    for points2 in lines2:
                        line_geom2 = THREE.BufferGeometry.new()
                        points2 = to_js(points2)
                        
                        console.log(points2)

                        line_geom2.setFromPoints( points2 )

                        material2 = THREE.LineBasicMaterial.new( THREE.Color.new(0x0000ff))
                        vis_line2 = THREE.Line.new( line_geom2, material2 )

                        scene.add(vis_line2)  
            else:
                for i in range(len(my_axiom_system2)): 
                    line_geom2 = vis_line2[i]
                    line_geom2 = THREE.BufferGeometry.new()
                    points2 = to_js(points2)
                        
                    console.log(points2)

                    line_geom2.setFromPoints( points2 )

                    vis_line2 = THREE.Line.new( line_geom2, material2 )
        else:
            pass

# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    update1()
    update2()
    controls.update()
    renderer.render(scene, camera)
    composer.render()

# Post Processing
def post_process():
    render_pass = THREE.RenderPass.new(scene, camera)
    render_pass.clearColor = THREE.Color.new(0,0,0)
    render_pass.ClearAlpha = 0
    fxaa_pass = THREE.ShaderPass.new(THREE.FXAAShader)

    pixelRatio = window.devicePixelRatio

    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth * pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight * pixelRatio )
   
    global composer
    composer = THREE.EffectComposer.new(renderer)
    composer.addPass(render_pass)
    composer.addPass(fxaa_pass)

# Resize
def on_window_resize(event):

    event.preventDefault()

    global renderer
    global camera
    
    camera.aspect = ((window.innerWidth/1.02)/(window.innerHeight/1.02))
    camera.updateProjectionMatrix()

    renderer.setSize((window.innerWidth/1.02),(window.innerHeight/1.02))

    post_process()
#-----------------------------------------------------------------------
#RUN THE MAIN PROGRAM
if __name__=='__main__':
    main()
