# C4D_RedshiftWrapper_API
Wrapper class for the current API of Redshift for c4d<br />
More detailled documentation [Here](https://gr4ph0s.github.io/C4D_RedshiftWrapper_API/)<br />
Download a minified version here https://gist.github.com/gr4ph0s/cdbcf67a05ee6ad8d365220435ae1f93#file-a-minified-version-of-my-module-c4d_redshiftwrapper_api
Example for use minified version https://pastebin.com/BRggfGdA

## Class Presentation

### Redshift
**Redshift class is the main wrapper. Use it for any interaction of the GraphView.
- set_mat, **Make sure to call it before any others one.** Set on which material change are done.
- IsRedshiftMaterial, check if material is a redshift material.
- CreateMaterial, create a redshift material.
- GetAllNodes, return list of all Node in the material.
- CreateShader, create a shader inside the material.
- RemoveShader, remove a shader inside the material.
- CreateConnection, create a connection beetween 2 node and 2 port_id.
- RemoveConnection, discconnect all connections from a node and a given port.

### Node
**Node class represent a c4d.modules.graphview.GvNode inside a redshift shader network.**
- [], set / get parameter of GvNode attached to the Node object.
- GetNode, return the c4d.modules.graphview.GvNode attached to the Node object.
- GetType, return the type of the node str for Redshift, int for xpresso node.
- GetColor, return the color of the GvNode.
- SetColor, set the color of the GvNode.
- GetName, return the name of the GvNode.
- SetName, set the name of the GvNode.
- SearchPort, search a GvPort and return it.
- ExposeParameter, Add a GvPort for a given parameter.

### MetaName
**Represent all metaname possible for create redshift shader.**
- GetDefaultColorNode, return the default color node from a given type.


## Examples
Basic exemple to get the redshift material, add a fresnel shader and constant node, and link all nodes. (Constant => Fresnel => Material => Output)
```python
import c4d
from RedshiftWrapper.Redshift import Redshift
 
def main():
    rs = RedshiftWrapper()
   
    #Assign Material
    rs.SetMat(doc.GetFirstMaterial())
   
    #Create Constant Node
    ConstNode = rs.CreateShader(c4d.ID_OPERATOR_CONST, x=100, y=500)
   
    #Create Fresnel shader and expose parameter
    FresnelNode = rs.CreateShader("Fresnel", x=200, y=500)
    FresnelNode.ExposeParameter(c4d.REDSHIFT_SHADER_FRESNEL_USER_CURVE, c4d.GV_PORT_INPUT)
   
    #Connect Constant and fresnel
    rs.CreateConnection(ConstNode, 0, FresnelNode, 0)
   
    #Get default material node and output node
    listNode = rs.GetAllNodes()
    MatNode = None
    OutPutNode = None
    for node in listNode:
        if node.GetNodeType() == "Output":
            OutPutNode = node
        elif node.GetNodeType() == "Material":
            MatNode = node
           
    if not MatNode or not OutPutNode:
        return
   
    #Expose a paramter of the material
    MatNode.ExposeParameter(c4d.REDSHIFT_SHADER_MATERIAL_DIFFUSE_WEIGHT, c4d.GV_PORT_INPUT)
   
    #Connect Fresnel shader to the material
    rs.CreateConnection(FresnelNode, 0, MatNode, 0)
   
    #Connect material shader to the output
    rs.CreateConnection(MatNode, 0, OutPutNode, 0)
   
    c4d.EventAdd()
if __name__=='__main__':
    main()
```


### Installation

To use it as a library simply copy RedshiftWrapper folder into

Before R23
- Windows
```
%AppData%\MAXON\CINEMA 4D RXX\library\python\packages\win64
```
- Mac
```
/Users/"YOURUSERNAME"/Library/Preferences/MAXON/CINEMA 4D RXX/library/python/packages/win64
```

R23 and more
- Windows
```
%AppData%\MAXON\CINEMA 4D RXX\python37\libs
```
- Mac
```
/Users/"YOURUSERNAME"/Library/Preferences/MAXON/CINEMA 4D RXX/python37/libs
```

Even if I suggest to use it as a library you are free to only include it into your project. For doing it in proper way I suggest you to read [Best Practice For Imports from official support forum](http://www.plugincafe.com/forum/forum_posts.asp?TID=10727)
and then use [py-localimport](https://gist.github.com/NiklasRosenstein/f5690d8f36bbdc8e5556) from [Niklas Rosenstein](https://github.com/NiklasRosenstein)

### Compatibility
Tested and build on Redshift 2.5.32 and R17/R18/R19/23

