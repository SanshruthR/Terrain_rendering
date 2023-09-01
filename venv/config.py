from panda3d.core import loadPrcFile, DirectionalLight, AmbientLight,loadPrcFileData
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.ShowBase import ShowBase
import random
loadPrcFile("settings.prc")
loadPrcFileData("", "window-title Random 3d Terrain Rendering [Press WASD for movement]")
class MyGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        
        self.setBackgroundColor(0, 0, 0)
        self.loadModeIs()
        self.setupLights()
        self.generateTerrain()
        self.disable_mouse()
        self.keys = {"w": False, "s": False, "a": False, "d": False}  # To track key states
        self.accept("w", self.set_key, ["w", True])
        self.accept("w-up", self.set_key, ["w", False])
        self.accept("s", self.set_key, ["s", True])
        self.accept("s-up", self.set_key, ["s", False])
        self.accept("a", self.set_key, ["a", True])
        self.accept("a-up", self.set_key, ["a", False])
        self.accept("d", self.set_key, ["d", True])
        self.accept("d-up", self.set_key, ["d", False])
        self.mouse_x = 0
        self.mouse_y = 0
        self.accept("mouse1", self.start_mouse_drag)
        self.accept("mouse1-up", self.stop_mouse_drag)
        self.taskMgr.add(self.moveCamera, "moveCameraTask")  # Add the camera movement task
        self.taskMgr.add(self.update_mouse_drag, "updateMouseDragTask")
        self.position_text = OnscreenText(text="", pos=(-0.95, 0.9), scale=0.05)
        self.taskMgr.add(self.update_position_text, "updatePositionTextTask")
        self.camera.setPos(7.04, 8.47, 2.32)

    def update_position_text(self, task):
        x, y, z = self.camera.getPos()
        self.position_text.setText(f"X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f}")
        return Task.cont

    def set_key(self, key, value):
        self.keys[key] = value

    def start_mouse_drag(self):
        self.enable_mouse()

    def stop_mouse_drag(self):
        self.disable_mouse()

    def update_mouse_drag(self, task):
        if self.mouseWatcherNode.hasMouse():
            # Get the mouse position
            x = self.mouseWatcherNode.getMouseX()
            y = self.mouseWatcherNode.getMouseY()

            # Calculate the change in mouse position
            dx = x - self.mouse_x
            dy = y - self.mouse_y

            # Rotate the camera based on mouse movement
            self.camera.setH(self.camera.getH() - dx * 100)  # Adjust the sensitivity as needed
            self.camera.setP(self.camera.getP() - dy * 100)

            # Clamp the camera's pitch to prevent flipping
            self.camera.setP(max(min(self.camera.getP(), 90), -90))

            # Update the previous mouse position
            self.mouse_x = x
            self.mouse_y = y

        return Task.cont

    def moveCamera(self, task):
        move_speed = 0.1  # Adjust the movement speed as needed
        if self.keys["w"]:
            self.camera.setY(self.camera, move_speed)  # Move forward
        if self.keys["s"]:
            self.camera.setY(self.camera, -move_speed)  # Move backward
        if self.keys["a"]:
            self.camera.setX(self.camera, -move_speed)  # Move left
        if self.keys["d"]:
            self.camera.setX(self.camera, move_speed)  # Move right
        return Task.cont

    def generateTerrain(self):
        # Define a list of available block models
        block_models = [self.purptess, self.tess]

        for z in range(10):
            for y in range(20):
                for x in range(20):
                    newBlockNode = render.attachNewNode('new-block-placeholder')
                    newBlockNode.setPos(
                        x * 2 - 20,
                        y * 2 - 20,
                        -z * 2,
                    )

                    if z / 2 == 1:  # checking if it's the ground layer and rendering the ground block
                        # Randomly select a block model from the list
                        selected_model = random.choice(block_models)
                        selected_model.instanceTo(newBlockNode)
                    else:
                        # Randomly select a block model from the list
                        selected_model = random.choice(block_models)
                        selected_model.instanceTo(newBlockNode)

    def loadModeIs(self):
        # loading the blue tesseract glb
        self.tess = loader.loadModel('tesseract.glb')
        self.tess.setScale(0.01, 0.01, 0.01)

        # loading the purple tesseract glb
        self.purptess = loader.loadModel('purptess.glb')

    def setupLights(self):
        mainLight = DirectionalLight('mainlight')
        mainLightNodePath = render.attachNewNode(mainLight)
        mainLightNodePath.setHpr(30, -60, 0)
        render.setLight(mainLightNodePath)

        ambientLight = AmbientLight('ambient light')
        ambientLight.setColor((0.3, 0.3, 0.3, 1))
        ambientLightNodePath = render.attachNewNode(ambientLight)
        render.setLight(ambientLightNodePath)

game = MyGame()
game.run()
