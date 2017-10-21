import c4d
from RedshiftWrapper.Redshift import Redshift
 
def main():
    rs = Redshift()
   
    #Assign Material
    rs.SetMat(doc.GetFirstMaterial())
   
    #Get all node and assign color
    listNode = rs.GetAllNodes()
    for node in listNode:
        node.SetColor()
   
    c4d.EventAdd()
if __name__=='__main__':
    main()