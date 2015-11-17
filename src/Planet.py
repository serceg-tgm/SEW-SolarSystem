__author__ = 'mkritzl'

class Planet(object):
    def __init__(self, name, texturePath, modelPath, initPosition, scale, children, selfRotate, orbitRotate, textureToggle):
        self.orbitRotate = orbitRotate
        self.selfRotate = selfRotate
        self.children = children
        self.name = name
        self.initPosition = initPosition
        self.texturePath = texturePath
        self.textureToggle = textureToggle

        self.model = loader.loadModel(modelPath)
        self.model.setTexture(loader.loadTexture(texturePath), 1)
        self.model.setScale(scale)
        if (initPosition):
            self.model.setPos(initPosition, 0, 0)

    def disableTexture(self):
        self.model.clearTexture()

    def enableTexture(self):
        self.model.setTexture(loader.loadTexture(self.texturePath), 1)
