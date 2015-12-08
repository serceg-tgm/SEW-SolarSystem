class Luminary(object):
    """
    Diese Klasse stellt einen bestimmten Himmelskoerper dar. Dabei werden alle Eigenschaften, die zum Initialisieren
    eines Himmelskoerpers angegeben werden muessen, als Parameter uebergeben.
    """
    def __init__(self, name, texturePath, modelPath, initPosition, scale, children, selfRotate, orbitRotate, textureToggle):
        """
        Hier werden alle Attribute, welche zum Initialisieren eines Himmelskoerpers benoetigt werden, initialisiert.
        Als Parameter
        """
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
        """
        Mittels dieser Methode wird die Textur ausgeschaltet. Die Funktion wird in der Methode "toggleTexture"
        aufgerufen, um die Textur bei jedem Himmelskoerper auszuschalten.
        """
        self.model.clearTexture()

    def enableTexture(self):
        """
        Mittels dieser Methode wird die Textur eingeschaltet. Die Funktion wird in der Methode "toggleTexture"
        aufgerufen, um die Textur bei jedem Himmelskoerper einzuschalten.
        """
        self.model.setTexture(loader.loadTexture(self.texturePath), 1)
