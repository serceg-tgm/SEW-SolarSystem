class Luminary(object):
    """
    Diese Klasse stellt einen bestimmten Himmelskoerper dar. Dabei werden alle Eigenschaften, die zum Initialisieren
    eines Himmelskoerpers angegeben werden muessen, als Parameter uebergeben.
    """
    def __init__(self, name, texturePath, modelPath, initPosition, scale, children, selfRotate, orbitRotate, textureToggle):
        """
        Hier werden alle Attribute, welche zum Erzeugen eines Himmelskoerpers benoetigt werden, initialisiert.

        :param name: Name des Himmelskoerpers
        :param texturePath: gibt den Pfad an, wo sich die Textur befindet
        :param modelPath: gibt den Pfad zum Objekt an, welche die Form des Himmelskoerpers angibt
        :param initPosition: initiale Position des Himmelskoerpers
        :param scale: gibt die Groesse des Himmelskoerpers an
        :param children: dient zur Definition der Kinder, die der jeweilige Himmelskoerper besitzt
        :param selfRotate: gibt an, wie schnell sich der Himmelskoerper um sich selbst drehen soll
        :param orbitRotate: gibt an, wie schnell sich der Himmelskoerper um die Laufbahn drehen soll
        :param textureToggle: dient zur Definition, welche Texturen von Himmelskoerpern togglen sollen und welche nicht
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
