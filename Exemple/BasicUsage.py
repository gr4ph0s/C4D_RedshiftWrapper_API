import c4d
from RedshiftWrapper.Redshift import Redshift

def main():
    rs = Redshift()
    if rs is False:
        return

    #Assign Material
    rs.SetMat(doc.GetFirstMaterial())

    #Create Constant Node
    ConstNode = rs.CreateShader(c4d.ID_OPERATOR_CONST, x=100, y=500)

    #Create Fresnel shader and expose parameter
    FresnelNode = rs.CreateShader("Fresnel", x=200, y=500)
    FresnelNode.ExposeParameter(c4d.REDSHIFT_SHADER_FRESNEL_USER_CURVE, c4d.GV_PORT_INPUT)

    #Connect Constant and fresnel
    rs.CreateConnection(ConstNode, FresnelNode, 0, 0)

    #Get default material node and output node
    listNode = rs.GetAllNodes()
    MatNode = None
    OutPutNode = None
    for node in listNode:
        if node.GetType() == "Output":
            OutPutNode = node
        elif node.GetType() == "Material":
            MatNode = node

    if not MatNode or not OutPutNode:
        return

    #Expose a paramter of the material
    MatNode.ExposeParameter(c4d.REDSHIFT_SHADER_MATERIAL_DIFFUSE_WEIGHT, c4d.GV_PORT_INPUT)

    #Connect Fresnel shader to the material
    rs.CreateConnection(FresnelNode, MatNode, 0, 0)

    #Connect material shader to the output
    rs.CreateConnection(MatNode, OutPutNode, 0, 0)

    c4d.EventAdd()
if __name__=='__main__':
    main()