import c4d
import redshift
from MetaName import MetaName


class Node(MetaName):
    """
    Represent a Node that already exist in a Material.
    :member: _GvNode: c4d.modules.graphview.GvNode => The GvNode linked to this Node. READ-ONLY => DO NOT EDIT !!! 
    :member: _NodeType:
        Int => a Cinema 4D Node look at https://developers.maxon.net/docs/Cinema4DPythonSDK/html/types/gvnodes.html 
        Str => a Redshift Node look at ::class:: MetaclassName
    :member: __DoUndo: DEFINE BY ::class:: REDSHIFT
        Bool => True if the wrapper have to call GvMaster.AddUndo() before any change otherwise False
    """

    _GvNode = None
    _NodeType = None  # string if redshift int if xpresso
    __DoUndo = True

    def __init__(self, gvNode, undo=True):
        """
        Initialization of the node
        :param gvNode: 
            c4d.modules.graphview.GvNode => The GvNode linked to this Node.
        """
        if not isinstance(gvNode, c4d.modules.graphview.GvNode):
            raise TypeError('gvNode is not a c4d.modules.graphview.GvNode')

        self.__DoUndo = undo
        self._GvNode = gvNode
        self._SetNodeType()

    def __getitem__(self, key):
        return self.GvNode[key]

    def __setitem__(self, key, value):
        self._GvNode[key] = value

    def __repr__(self):
        return self.GetName()

    def _SetNodeType(self):
        """
        Set self._NodeType according the GvNode
            Int => a Cinema 4D Node look at https://developers.maxon.net/docs/Cinema4DPythonSDK/html/types/gvnodes.html 
            Str => a Redshift Node look at ::class:: MetaclassName 
        """
        global redshift
        if self._GvNode.IsInstanceOf(redshift.GVrsshader):
            self._NodeType = self._GvNode[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME]
        elif self._GvNode.GetOperatorID() == 1036746:
            self._NodeType = self.Output
        elif self._GvNode.GetOperatorID() == 1036762:
            self._NodeType = self.UtBaker
        else:
            self._NodeType = self._GvNode.GetOperatorID()

    def GetNode(self):
        """
        Get the GvNode linked
        :return: c4d.modules.graphview.GvNode => The GvNode linked to this Node.
        """
        return self._GvNode

    def GetType(self):
        """
        Get the GvNode Type
        :return:    Int: A Cinema 4D Node look at https://developers.maxon.net/docs/Cinema4DPythonSDK/html/types/gvnodes.html 
                    Str: A Redshift Node look at ::class:: MetaclassName 
        """
        return self._NodeType

    def GetColor(self):
        """
        Get the color of a GvNode Type
        :return:    c4d.Vector: color of the GvNode lined to this Node
        """
        return self[c4d.ID_GVBASE_COLOR]
        
    def SetColor(self, color=None):
        """
        Set the color of the GvNode
        :param color: 
            c4d.Vector => New color of the node
            None => Default color according the type of the node
        """
        if not isinstance(color, c4d.Vector) and color is not None:
            raise TypeError('color is not a valid color')
            
        if color is None:
            color = self.GetDefaultColorNode(self.GetType())
        
        if self.__DoUndo:
            self._GvNode.GetNodeMaster().AddUndo()
        self[c4d.ID_GVBASE_COLOR] = color
        
    def SetName(self, newName):
        """
        Set the name of the GvNode
        :param newName: 
            str => New name of the GvNode
        """
        if self.__DoUndo:
            self._GvNode.GetNodeMaster().AddUndo()
        self._GvNode.SetName(newName)

    def GetName(self):
        """
        Get the name of the GvNode
        :return: 
            str => Name of the GvNode
        """
        return self._GvNode.GetName()

    def SearchPort(self, portToSearch, searchType=None):
        """
        Search a GvPort in the Node, parameter should be exposed.
        :param portToSearch: 
            str => The name of the parameter
            int => The port ID of the Node
        :param searchType: 
            int => GV_PORT_INPUT or GV_PORT_OUTPUT or None For both (None is only working for str portToSearch)
        :return: c4d.modules.graphview.GvPort => None or GvPort that match the search
        """
        if not isinstance(portToSearch, int) and not isinstance(portToSearch, str):
            raise TypeError('portToSearch is not parameter or not name of a parameter')

        # Search by Name
        if isinstance(portToSearch, str):
            # Set the list of gvPort to check
            gvPortList = list()
            if searchType is None:
                gvPortList += self._GvNode.GetOutPorts()
                gvPortList += self._GvNode.GetInPorts()
            elif searchType == c4d.GV_PORT_OUTPUT:
                gvPortList += self._GvNode.GetOutPorts()
            elif searchType == c4d.GV_PORT_INPUT:
                gvPortList += self._GvNode.GetInPorts()
            else:
                raise TypeError('SearchType Unknow')

            for gvPort in gvPortList:
                if gvPort.GetName(self._GvNode) == portToSearch:
                    return gvPort

        # Get port ID
        if isinstance(portToSearch, int):
            if searchType is None:
                raise TypeError('Cant search int without SearchType')
            elif searchType == c4d.GV_PORT_OUTPUT:
                return self._GvNode.GetOutPort(portToSearch)
            elif searchType == c4d.GV_PORT_INPUT:
                return self._GvNode.GetInPort(portToSearch)

        return None

    def ExposeParameter(self, parameterID, portType):
        """
        Expose a parameter in a GvNode
        :param parameterID: 
            int => The ID of the parameter
            c4d.DescID => The full DescID
        :param portType: 
            int => GV_PORT_INPUT or GV_PORT_OUTPUT
        :return: Bool => True if success otherwise false
        """
        if not isinstance(parameterID, int) and not isinstance(parameterID, c4d.DescID):
            raise TypeError('parameterID is not valid')

        if isinstance(parameterID, int):
            if self._GvNode.AddPortIsOK(portType, parameterID):
                if self.__DoUndo:
                    self._GvNode.GetNodeMaster().AddUndo()
                return self._GvNode.AddPort(portType, c4d.DescID(c4d.DescLevel(parameterID)), message=True)
        else:
            if self.__DoUndo:
                self._GvNode.GetNodeMaster().AddUndo()
            return self._GvNode.AddPort(portType, parameterID, message=True)

        return False