# IMPORTS
from js import THREE, window, document, Object
from pyodide.ffi import create_proxy, to_js
import math

#-----------------------------------------------------------------------
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
    camera.position.z = 100
    scene.add(camera)
    
    # Window Resize
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy)
    
    # Post Processing
    global composer
    post_process()
     
    #-----------------------------------------------------------------------
    # DESIGN
    # Materials
    global material, line_material, colorFormats
    colorFormats = {
	        "edges": '#ff8800',
            "mesh": '#eff7fs'
    }
    colorFormats = Object.fromEntries(to_js(colorFormats))
    material = THREE.MeshBasicMaterial.new()
    material.transparent = True
    material.opacity = 0.9
    material.color = THREE.Color.new(colorFormats.mesh)
    
    line_material = THREE.LineBasicMaterial.new()
    line_material.color = THREE.Color.new(colorFormats.edges)    
    
    # Form
    global geom1_params, octa, octa_mult, octa_lines, line, edges, geom1, octa_mesh, a_params, func_change, negative_param
    octa_mult = []
    octa_lines = []
    func_change = {
            "invert": False
    }
    func_change = Object.fromEntries(to_js(func_change))
    a_params = {
            "radius":30
    }
    a_params = Object.fromEntries(to_js(a_params))
    geom1_params = {
            "radius":a_params.radius,
            "x":2,
            "detail":0,
            "rotation_x":0,
            "rotation_z":0,
            "gap":0.3,
            "size_increase":a_params.radius*((((a_params.radius*2)/math.sqrt(2))/a_params.radius)/100)
    }
    geom1_params = Object.fromEntries(to_js(geom1_params))
        
    # Loops
    for i in range(geom1_params.x):
        geom1 = THREE.OctahedronGeometry.new((a_params.radius*0.707)*geom1_params.size_increase*i, (geom1_params.detail+i)-1)
        geom1.translate(((a_params.radius)*geom1_params.gap*i*i), 0,0)
        geom1.rotateX(math.radians(geom1_params.rotation_x*i)/geom1_params.x*-i)
        geom1.rotateY(math.radians(geom1_params.rotation_z)/geom1_params.x*-i)
        
        octa = THREE.Mesh.new(geom1, material)
        octa_mesh = octa.material.color.getHex()
        octa_mult.append(octa)
        scene.add(octa) 
        
        edges = THREE.EdgesGeometry.new(octa.geometry)
        line = THREE.LineSegments.new( edges, line_material)
        octa_lines.append(line)
        scene.add(line)
    
    #-----------------------------------------------------------------------
    # UI
    # Controls
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    # Gui
    gui = window.dat.GUI.new() 
    param_folder = gui.addFolder('Inverse')
    param_folder.add(func_change, 'invert')
    param_folder.open()
        
    param_folder = gui.addFolder('Object Parameters')
    param_folder.add(a_params, 'radius', 0,100,1)
    param_folder.add(geom1_params, 'x', 2,20,1)
    param_folder.add(geom1_params, 'detail', 0,10,1)
    param_folder.add(geom1_params, 'rotation_x', 0,180)
    param_folder.add(geom1_params, 'rotation_z', 0,180)
    param_folder.add(geom1_params, 'gap', 0,2,0.1)
    param_folder.open()
        
    param_folder = gui.addFolder('Material Parameters')
    param_folder.add(octa.material, 'wireframe')
    '''param_folder.addColor(colorFormats, 'edges')
    param_folder.addColor(colorFormats, 'mesh')'''
    param_folder.open()
        
    #-----------------------------------------------------------------------
    # RENDER / UPDATE
    render()
    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS
# Update

# case1

def function1():
    global octa_mult, octa_lines, material, line_material, line, octa_mesh, geom1_params, octa
    for i in range(geom1_params.x):
        geom1 = THREE.OctahedronGeometry.new((a_params.radius*0.707)*geom1_params.size_increase*i, (geom1_params.detail+i)-1)
        geom1.translate(((a_params.radius)*geom1_params.gap*i*i), 0,0)
        geom1.rotateX(math.radians(geom1_params.rotation_x*i)/geom1_params.x*-i)
        geom1.rotateY(math.radians(geom1_params.rotation_z)/geom1_params.x*-i)
        
        octa = THREE.Mesh.new(geom1, material)
        octa_mesh = octa.material.color.getHex()
        octa_mult.append(octa)
        scene.add(octa) 
        
        edges = THREE.EdgesGeometry.new(octa.geometry)
        line = THREE.LineSegments.new( edges, line_material)
        octa_lines.append(line)
        scene.add(line)
def update_octa_mult1():    
    global octa_mult, octa_lines, material, line_material, line
    if len(octa_mult) != 0:
        if len(octa_mult) != geom1_params.x:
            for octa in octa_mult: scene.remove(octa)
            for line in octa_lines: scene.remove(line)
            octa_mult = []
            octa_lines = []
            for i in range(geom1_params.x):
                geom1 = THREE.OctahedronGeometry.new((a_params.radius*0.707)*geom1_params.size_increase*i, (geom1_params.detail+i)-1)   
                geom1.translate(((a_params.radius)*geom1_params.gap*i*i), 0,0)
                geom1.rotateX(math.radians(geom1_params.rotation_x*i)/geom1_params.x*-i)
                geom1.rotateY(math.radians(geom1_params.rotation_z)/geom1_params.x*-i)
                    
                octa = THREE.Mesh.new(geom1, material)
                    
                octa_mult.append(octa)
                scene.add(octa)

                edges = THREE.EdgesGeometry.new( octa.geometry )
                line = THREE.LineSegments.new( edges, line_material)
                octa_lines.append(line)
                scene.add(line)
        else:
            for i in range(len(octa_mult)): 
                octa = octa_mult[i]
                line = octa_lines[i]
                geom1 = THREE.OctahedronGeometry.new((a_params.radius*0.707)*geom1_params.size_increase*i, (geom1_params.detail+i)-1)   
                geom1.translate(((a_params.radius)*geom1_params.gap*i*i), 0,0)
                geom1.rotateX(math.radians(geom1_params.rotation_x*i)/geom1_params.x*-i)
                geom1.rotateY(math.radians(geom1_params.rotation_z)/geom1_params.x*-i)    

                octa.geometry = geom1

                edges = THREE.EdgesGeometry.new( octa.geometry )
                line.geometry = edges
                



# case2                

def function2():
    global octa_mult, octa_lines, material, line_material, line, octa_mesh, geom1_params, octa
    for i in range(geom1_params.x):
        geom1 = THREE.OctahedronGeometry.new((a_params.radius*0.707)*geom1_params.size_increase*i, (geom1_params.x-i)-1)  
        geom1.translate(((a_params.radius)*geom1_params.gap*i*i), 0,0)
        geom1.rotateX(math.radians(geom1_params.rotation_x*i)/geom1_params.x*-i)
        geom1.rotateY(math.radians(geom1_params.rotation_z)/geom1_params.x*-i)
            
        octa = THREE.Mesh.new(geom1, material)
        octa_mesh = octa.material.color.getHex()
        octa_mult.append(octa)
        scene.add(octa) 
            
        edges = THREE.EdgesGeometry.new(octa.geometry)
        line = THREE.LineSegments.new( edges, line_material)
        octa_lines.append(line)
        scene.add(line) 
def update_octa_mult2():              
    global octa_mult, octa_lines, material, line_material, line
    if len(octa_mult) != 0:
        if len(octa_mult) != geom1_params.x:
            for octa in octa_mult: scene.remove(octa)
            for line in octa_lines: scene.remove(line)
            octa_mult = []
            octa_lines = []
            for i in range(geom1_params.x):
                geom1 = THREE.OctahedronGeometry.new((a_params.radius*0.707)*geom1_params.size_increase*i, (geom1_params.x-i)-1)  
                geom1.translate(((a_params.radius)*geom1_params.gap*i*i), 0,0)
                geom1.rotateX(math.radians(geom1_params.rotation_x*i)/geom1_params.x*-i)
                geom1.rotateY(math.radians(geom1_params.rotation_z)/geom1_params.x*-i)
                    
                octa = THREE.Mesh.new(geom1, material)
                    
                octa_mult.append(octa)
                scene.add(octa)

                edges = THREE.EdgesGeometry.new( octa.geometry )
                line = THREE.LineSegments.new( edges, line_material)
                octa_lines.append(line)
                scene.add(line)
        else:
            for i in range(len(octa_mult)): 
                octa = octa_mult[i]
                line = octa_lines[i]
                geom1 = THREE.OctahedronGeometry.new((a_params.radius*0.707)*geom1_params.size_increase*i, (geom1_params.x-i)-1)   
                geom1.translate(((a_params.radius)*geom1_params.gap*i*i), 0,0)
                geom1.rotateX(math.radians(geom1_params.rotation_x*i)/geom1_params.x*-i)
                geom1.rotateY(math.radians(geom1_params.rotation_z)/geom1_params.x*-i)    

                octa.geometry = geom1

                edges = THREE.EdgesGeometry.new( octa.geometry )
                line.geometry = edges   


                         
# Render
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    if func_change.invert == True:
        function1()
    else:
        function2()
    if func_change.invert == True:
        update_octa_mult1()
    else:
        update_octa_mult2()
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
# RUN MAIN
if __name__=='__main__':
    main()