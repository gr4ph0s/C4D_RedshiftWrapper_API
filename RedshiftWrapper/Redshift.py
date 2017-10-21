# ==============================================
#                   Import
# ==============================================
import c4d
import redshift

from Node import Node
from MetaName import MetaName

# ==============================================
#                   Import
# ==============================================

__author__ = 'Adam Maxime - Graphos <gr4ph0s(at)hotmail.fr>'
__project__ = "https://github.com/gr4ph0s/RedshiftWrapper"
__version__ = '1.0'


class Redshift(MetaName):
    """
    The main wrapper arround Redshift API.
    :member: doUndo: 
        Bool => True if the wrapper have to call GvMaster.AddUndo() before any change otherwise False
    :member: _mat:
        c4d.BaseMaterial => The redshift material we act on
    :member: _gvMaster:
        c4d.modules.graphview.GvNodeMaste => The Node master of self._mat
    """
    doUndo = True
    _mat = None
    _gvMaster = None

    def SetMat(self, mat):
        """
        Set the mat to act on
        :param mat: 
            c4d.BaseMaterial => Accept only a Redshift Material
        """
        global redshift
        if not isinstance(mat, c4d.BaseMaterial):
            raise TypeError('material is not a c4d.BaseMaterial')
        if not mat.IsInstanceOf(redshift.Mrsmaterial):
            raise TypeError('material is not a redshift material')

        self._mat = mat
        self._gvMaster = redshift.GetRSMaterialNodeMaster(mat)
        if not self._gvMaster:
            raise TypeError('can\'t get GvMaster from mat')

    def _CheckMatIsValid(self):
        """
        Check if _self.mat is currently set and valid
        """
        global redshift
        if self._mat is None:
            raise TypeError('Mat is not define')
        if not isinstance(self._mat, c4d.BaseMaterial):
            raise TypeError('material is not a c4d.BaseMaterial')
        if not self._mat.IsInstanceOf(redshift.Mrsmaterial):
            raise TypeError('material is not a redshift material')

    def GetAllNodes(self, removeMasterGroup=True, gvNode=None, nodeList=None):
        """
        Get all nodes inside the material
        Use redshift.GatAllNodes(), only removeMasterGroup is needed other parameters are for internal use
        :param removeMasterGroup: 
            Bool => True to remove the Shader Group that hold all other Node otherwise false
        :return: 
            List of ::class:: Node => All Nodes inside the material
        """
        self._CheckMatIsValid()

        if nodeList is None:
            nodeList = list()
            gvNode = self._gvMaster.GetRoot()

        while gvNode:
            nodeList.append(Node(gvNode, self.doUndo))
            self.GetAllNodes(False, gvNode.GetDown(), nodeList)
            gvNode = gvNode.GetNext()

        if len(nodeList) > 1 and removeMasterGroup:
            nodeList = nodeList[1:]
        return nodeList

    def CreateShader(self, shaderType, x=-1, y=-1, NodeBefore=None):
        """
        Create a shader inside the material
        :param shaderType: 
            Int => a Cinema 4D Node look at https://developers.maxon.net/docs/Cinema4DPythonSDK/html/types/gvnodes.html
            Str => a Redshift Node look at ::class:: MetaclassName
        :param x: 
            int => X position in the Xpresso windows
        :param y: 
            int => Y position in the Xpresso windows
        :param NodeBefore: 
            Node => The node to insert before (Change execution order !!)
            c4d.modules.graphview.GvNode => The node to insert before (Change execution order !!)
        :return: 
            List of ::class:: Node => All Nodes inside the material
        """
        self._CheckMatIsValid()

        if not isinstance(shaderType, str) and not isinstance(shaderType, int):
            raise TypeError('shaderType is not valid type')

        if not isinstance(x, int):
            raise TypeError('x is not valid type')

        if not isinstance(y, int):
            raise TypeError('y is not valid type')

        if not isinstance(NodeBefore, Node) and not isinstance(NodeBefore, c4d.modules.graphview.GvNode) and NodeBefore is not None:
            raise TypeError('NodeBefore is not valid type')

        # Create redshift node
        if isinstance(shaderType, str):
            if self.doUndo:
                self._gvMaster.AddUndo()

            # Check if we accept this meta class
            if not self._TestProperty(shaderType):
                raise TypeError('shaderType is not a valid metaclassname')

            # Get a GvNode
            if isinstance(NodeBefore, Node) and NodeBefore is not None:
                NodeBefore = NodeBefore.GetNode()

            # Check if it' a C4D Baked
            if shaderType == self.UtBaker:
                node = Node(self._gvMaster.CreateNode(self._gvMaster.GetRoot(), 1036762, NodeBefore, x, y), self.doUndo)

            # Check Output
            elif shaderType == self.Output:
                # Check if there is already an output node
                nodeList = self.GetAllNodes()
                for node in nodeList:
                    if node.GetType() == self.Output:
                        return None

                node = Node(self._gvMaster.CreateNode(self._gvMaster.GetRoot(), 1036746, NodeBefore, x, y), self.doUndo)

            # Other
            else:
                node = self._gvMaster.CreateNode(self._gvMaster.GetRoot(), 1036227, NodeBefore, x, y)
                node[c4d.GV_REDSHIFT_SHADER_META_CLASSNAME] = shaderType
                node = Node(node, self.doUndo)

            if node:
                node.SetColor()
            return node

        # Create c4d node
        else:
            if self.doUndo:
                self._gvMaster.AddUndo()
            
            return Node(self._gvMaster.CreateNode(self._gvMaster.GetRoot(), shaderType, NodeBefore, x, y), self.doUndo)

        return None

    def RemoveShader(self, node):
        """
        Remove a shader inside the material
        :param node: 
            Node => THe node object to remove
        :return: 
            Bool : True if delete overthiwe False
        """
        self._CheckMatIsValid()

        # Check Type
        if not isinstance(node, Node):
            raise TypeError('node is not valid Node Object')

        if self.doUndo:
            self._gvMaster.AddUndo()
        return node.GetNode().Delete()

    def CreateConnection(self, SrcNode, DestNode, SrcParameter=None, DestParameter=None):
        """
        Connect two Nodes together
        :param SrcNode: 
            Node => The source Node (The one with an output)
            c4d.modules.graphview.GvPort => The GvPort of the source Node returned by Node.ExposeParameter or Node.SearchPort
        :param DestNode: 
            Node => The destination Node (The one with an input)
            c4d.modules.graphview.GvPort => The GvPort of the destination Node returned by Node.ExposeParameter or Node.SearchPort
        :param SrcParameter: PARAMETER WILL BE IGNORED IF GvPORT IS USED IN SrcNode !!!
            int => Id of the source GvPort (not the ID of the parameter)
            str => Name of the source GvPort
        :param DestParameter: PARAMETER WILL BE IGNORED IF GvPORT IS USED IN DestNode !!!
            int => Id of the destination GvPort (not the ID of the parameter)
            str => Name of the destination GvPort
        :return: 
            Bool : True if connection is created overthiwe False
        """
        self._CheckMatIsValid()

        # Check Type
        if not isinstance(SrcNode, Node) and not isinstance(SrcNode, c4d.modules.graphview.GvPort):
            raise TypeError('SrcNode is not valid Node Object or gvPort')

        if not isinstance(DestNode, Node) and not isinstance(DestNode, c4d.modules.graphview.GvPort):
            raise TypeError('DestNode is not valid Node Object or gvPort')

        if not isinstance(SrcNode, c4d.modules.graphview.GvPort):
            if not isinstance(SrcParameter, int) and not isinstance(SrcParameter, str):
                raise TypeError('SrcParameter is not parameter or not name of a parameter')

        if not isinstance(DestNode, c4d.modules.graphview.GvPort):
            if not isinstance(DestParameter, int) and not isinstance(DestParameter, str):
                raise TypeError('DestParameter is not parameter or not name of a parameter')

        # Get GvNode
        gvNodeSrc = SrcNode.GetNode()
        gvNodeDest = DestNode.GetNode()
        if not gvNodeSrc or not gvNodeDest:
            return False

        # Get Src GvPort
        if isinstance(SrcNode, c4d.modules.graphview.GvPort):
            gvPortSrc = SrcNode
        else:
            gvPortSrc = SrcNode.SearchPort(SrcParameter, c4d.GV_PORT_OUTPUT)

        # Get Dest GvPort
        if isinstance(DestNode, c4d.modules.graphview.GvPort):
            gvPortDest = DestNode
        else:
            gvPortDest = DestNode.SearchPort(DestParameter, c4d.GV_PORT_INPUT)

        # Check if they can be linked
        if not gvPortSrc or not gvPortDest: return False
        if gvNodeSrc.GetNodeMaster() != gvNodeDest.GetNodeMaster(): return False
        if gvPortDest.IsIncomingConnected(): return False

        if self.doUndo:
            self._gvMaster.AddUndo()
        return gvPortSrc.Connect(gvPortDest)
        
    def CreateMaterial(self, MatType=1000):
        """
        Create a new redshift material
        :param MatType: 
            int => The type of the Redshift shader ()
                1000 => Material
                1001 => Architectural
                1002 => CarPaint
                1003 => C4D Hair
                1004 => Hair
                1005 => Incandescent
                1006 => Skin
                1007 => Sprite
                1008 => SSS
                1009 => Particle
                1010 => Volume
        :return: 
            c4d.Material : Created material or None if it's fail
        """
        if not isinstance(MatType, int):
            raise TypeError('MatType is not an integer')

        if MatType < 1000 or MatType > 1010:
            raise ValueError('Invalid value for matType, must be from 1000 to 1010')

        c4d.CallCommand(1036759, MatType) 
        mat = doc.GetFirstMaterial()
        if not mat:
            return None

        SetMat(mat)
        return mat
        
    def RemoveConnection(self, port, node=None, portType=None):
        """
        Disconnect all connection from a given port of Nodes
        :param port: 
            int => Id of the GvPort (not the ID of the parameter)
            str => Name of the GvPort
            c4d.modules.graphview.GvPort => The GvPort of the Node returned by Node.ExposeParameter or Node.SearchPort
        :param node: PARAMETER WILL BE IGNORED IF GvPORT IS USED IN port !!!
            Node => The Node that host the GvPort who want to remove connection
        :param portType: PARAMETER WILL BE IGNORED IF GvPORT IS USED IN port !!!
            int => GV_PORT_INPUT or GV_PORT_OUTPUT
        :return: 
            Bool : True if connection is created overthiwe False
        """
        self._CheckMatIsValid()

        # Check Type
        if not isinstance(port, c4d.modules.graphview.GvPort):
            if not isinstance(node, Node):
                raise TypeError('node is not valid Node Object')

        if not isinstance(port, int) and not isinstance(port, str) and not isinstance(port, c4d.modules.graphview.GvPort):
            raise TypeError('port is not parameter or not name of a parameter')

        # Get the GvPort
        gvPort = None
        if  isinstance(port, c4d.modules.graphview.GvPort):
            gvPort = port
        else :
            gvPort = node.SearchPort(port, portType)

        #Undo if needed
        if self.doUndo:
            self._gvMaster.AddUndo()

        #Remove connection
        return gvPort.Remove()