# coding=utf-8
import xml.dom.minidom
import arcpy_crete_xml
#C:/Users\a\Documents\ArcGIS\Default.gdb
from PIL import Image
import arcpy
import sys
import gdal
import re
from gdalconst import *
import os,string
def Createxml(url,address):

    fn = url
    #im = Image.open(fn)#返回一个Image对象
    ds = gdal.Open(fn,GA_ReadOnly)
    dict={}
    dict["0"] = u"1 bit"
    dict["1"] = u"2 bit"
    dict["2"] = u"4 Bit"
    dict["3"] = u"8 Bit,unsigned integer"
    dict["4"] = u"8 Bit,integer"
    dict["5"] = u"16 Bit,unsigned integer"
    img_valuetype =str(arcpy.GetRasterProperties_management(fn,"VALUETYPE"))
    valuetype=dict[img_valuetype]
    #
    #Columns and Rows
    Columns = ds.RasterXSize
    Rows = ds.RasterYSize
    Columns_and_Rows = Columns,Rows

    #Number of Bands
    Number_of_Bands = arcpy.GetRasterProperties_management(fn,"BANDCOUNT")


    #Cell Size
    img_sizeX = arcpy.GetRasterProperties_management(fn,"CELLSIZEX")
    #Get the elevation standard deviation value from geoprocessing result object
    img_sizeY = arcpy.GetRasterProperties_management(fn,"CELLSIZEY")

    #Uncompressed Size
    imgpath= arcpy.Describe(fn).CatalogPath
    img_size = str(float(os.path.getsize(imgpath))/1024/1024)+('MB')

    #Format
    Format =arcpy.Describe(fn).format


    #Source Type
    Source_Type = arcpy.GetRasterProperties_management(fn,"SOURCETYPE")

    #Pixel Type
    Pixel_Type = valuetype.split(",")[1]

    #Pixel Depth
    Pixel_Depth = valuetype.split(",")[0]

    #NoData Value
    NoData_Value = ds.GetRasterBand(1).GetNoDataValue(),ds.GetRasterBand(2).GetNoDataValue(),ds.GetRasterBand(3).GetNoDataValue()

    #Colormap

    #Pyramids

    #Compression

    #Mensuration Capabilities

    #Status

    #Extent top
    Top = arcpy.GetRasterProperties_management(fn,"TOP")

    #Extent Left
    Left = arcpy.GetRasterProperties_management(fn,"LEFT")

    #Extent Right
    Right = arcpy.GetRasterProperties_management(fn,"RIGHT")

    #Extent Button
    Buttom = arcpy.GetRasterProperties_management(fn,"BOTTOM")

    #Spatial Reference
    Spatial_Reference = arcpy.Describe(fn).spatialReference.name

    Spatial_Reference = arcpy.Describe(fn).spatialReference.MResolution
    ds = gdal.Open(fn,GA_ReadOnly)
    if ds is None:
        print 'cannot open ',fn
        sys.exit(1)
    pattern = re.compile('"(.*)"')  #提取双引号里面的值
    Spatial = ds.GetProjection().split(",")
    #Linear Unit
    Linear_Unit = " ".join(pattern.findall(Spatial[21]))," ".join(Spatial[22])

    #Anjular Unit
    Anjular_Unit = " ".join(pattern.findall(Spatial[8]))," ".join(re.findall(r"\d+\.?\d*",Spatial[9]))

    #false_easting
    False_easting = " ".join(re.findall(r"\d+\.?\d*",Spatial[18]))

    #false_northing
    False_northing = " ".join(re.findall(r"\d+\.?\d*",Spatial[7]))

    #central_meridian
    Central_meridian =" ".join(re.findall(r"\d+\.?\d*",Spatial[14]))

    #scale_factor
    Scale_factor = " ".join(re.findall(r"\d+\.?\d*",Spatial[16]))

    #lantitude_of_origin
    Lantitude_of_origin = " ".join(re.findall(r"\d+\.?\d*",Spatial[12]))
    #Datum
    Datum = " ".join(pattern.findall(Spatial[2]))

    #Build Parameters

    #band_1  MIN
    Min = arcpy.GetRasterProperties_management(fn,"MINIMUM")
    #band_1  Max
    Max = arcpy.GetRasterProperties_management(fn,"MAXIMUM")
    #band_1  mean
    Mean = arcpy.GetRasterProperties_management(fn,"MEAN")
    #band_1 Std dev
    Std_dev = arcpy.GetRasterProperties_management(fn,"STD")
    # Classes

    ##创建xml

    #在内存中创建一个空的文档
    doc = xml.dom.minidom.Document()
    #创建一个根节点Managers对象
    root = doc.createElement('Metadatafile')
    #设置根节点的属性
    #将根节点添加到文档对象中
    doc.appendChild(root)

    managerList = [{'name':'Raster_Information','Columns_and_Rows' :Columns_and_Rows,'Number_of_Bands':Number_of_Bands,  'Cell_Size' : img_size, 'Format' : Format,'Source_Type':Source_Type,'Pixel_Type':Pixel_Type,'Pixel_Depth':Pixel_Depth,'NoData_Value':NoData_Value},
                   {'name' : 'Extent', 'Top' : Top, 'Left' : Left,'Right':Right,'Bottom':Buttom},
                   {'name' : 'Spatial_Reference', 'Spatial_Reference' : Spatial_Reference, 'Linear_Unit' : Linear_Unit,'Anjular_Unit':Anjular_Unit,'false_easting':False_easting,'false_northing':False_northing,'central_meridian':Central_meridian,'scale_factor':Scale_factor,'lantitude_of_origin':Lantitude_of_origin,'Datum':Datum},
                   {'name':'band_1','Min':Min,'Max':Max,'Mean':Mean,'Std_dev':Std_dev}
    ]

    #Raster Information
    nodeManager = doc.createElement(managerList[0]['name'])
    nodeColumnsandRows = doc.createElement('Columns_and_Rows')
    # 给叶子节点name设置一个文本节点，用于显示文本内容
    nodeColumnsandRows.appendChild(doc.createTextNode(str(managerList[0]['Columns_and_Rows'])))

    nodeNumberofBands = doc.createElement("Number_of_Bands")
    nodeNumberofBands.appendChild(doc.createTextNode(str(managerList[0]['Number_of_Bands'])))

    nodeCellSize = doc.createElement("Cell_Size")
    nodeCellSize.appendChild(doc.createTextNode(str(managerList[0]['Cell_Size'])))

    nodeFormat = doc.createElement("Format")
    nodeFormat.appendChild(doc.createTextNode(str(managerList[0]['Format'])))

    nodeSource_Type = doc.createElement("Source_Type")
    nodeSource_Type.appendChild(doc.createTextNode(str(managerList[0]['Source_Type'])))

    nodePixel_Type = doc.createElement("Pixel_Type")
    nodePixel_Type.appendChild(doc.createTextNode(str(managerList[0]['Pixel_Type'])))

    nodePixel_Depth = doc.createElement("Pixel_Depth")
    nodePixel_Depth.appendChild(doc.createTextNode(str(managerList[0]['Pixel_Depth'])))

    nodeNoData_Value = doc.createElement("NoData_Value")
    nodeNoData_Value.appendChild(doc.createTextNode(str(managerList[0]['NoData_Value'])))

    nodeManager.appendChild(nodeColumnsandRows)
    nodeManager.appendChild(nodeNumberofBands)
    nodeManager.appendChild(nodeCellSize)
    nodeManager.appendChild(nodeFormat)
    nodeManager.appendChild(nodeSource_Type)
    nodeManager.appendChild(nodePixel_Type)
    nodeManager.appendChild(nodePixel_Depth)
    nodeManager.appendChild(nodeNoData_Value)
    root.appendChild(nodeManager)

    #Extent
    nodeExtent = doc.createElement(managerList[1]['name'])

    nodeTop = doc.createElement('Top')
    nodeTop.appendChild(doc.createTextNode(str(managerList[1]['Top'])))

    nodeLeft = doc.createElement('Left')
    nodeLeft.appendChild(doc.createTextNode(str(managerList[1]['Left'])))

    nodeRight = doc.createElement('Right')
    nodeRight.appendChild(doc.createTextNode(str(managerList[1]['Right'])))

    nodeBottom = doc.createElement('Bottom')
    nodeBottom.appendChild(doc.createTextNode(str(managerList[1]['Bottom'])))

    nodeExtent.appendChild(nodeTop)
    nodeExtent.appendChild(nodeLeft)
    nodeExtent.appendChild(nodeRight)
    nodeExtent.appendChild(nodeBottom)
    root.appendChild(nodeExtent)

    #Spatial Reference
    nodeSpatial_Reference = doc.createElement(managerList[2]['name'])
    nodeSpatial_Reference_Name = doc.createElement('Spatial_Reference')
    nodeSpatial_Reference_Name.appendChild(doc.createTextNode(str(managerList[2]['Spatial_Reference'])))

    nodeLinear_Unit = doc.createElement('Linear_Unit')
    nodeLinear_Unit.appendChild(doc.createTextNode(str(managerList[2]['Linear_Unit'])))

    nodeAnjular_Unit = doc.createElement('Anjular_Unit')
    nodeAnjular_Unit.appendChild(doc.createTextNode(str(managerList[2]['Anjular_Unit'])))

    nodefalse_easting = doc.createElement('false_easting')
    nodefalse_easting.appendChild(doc.createTextNode(str(managerList[2]['false_easting'])))

    nodefalse_northing = doc.createElement('false_northing')
    nodefalse_northing.appendChild(doc.createTextNode(str(managerList[2]['false_northing'])))

    nodecentral_meridian = doc.createElement('central_meridian')
    nodecentral_meridian.appendChild(doc.createTextNode(str(managerList[2]['central_meridian'])))

    nodescale_factor = doc.createElement('scale_factor')
    nodescale_factor.appendChild(doc.createTextNode(str(managerList[2]['scale_factor'])))

    nodeslantitude_of_origin = doc.createElement('lantitude_of_origin')
    nodeslantitude_of_origin.appendChild(doc.createTextNode(str(managerList[2]['lantitude_of_origin'])))

    nodesDatum = doc.createElement('Datum')
    nodesDatum.appendChild(doc.createTextNode(str(managerList[2]['Datum'])))

    nodeSpatial_Reference.appendChild(nodeSpatial_Reference_Name)
    nodeSpatial_Reference.appendChild(nodeLinear_Unit)
    nodeSpatial_Reference.appendChild(nodeAnjular_Unit)
    nodeSpatial_Reference.appendChild(nodefalse_easting)
    nodeSpatial_Reference.appendChild(nodefalse_northing)
    nodeSpatial_Reference.appendChild(nodecentral_meridian)
    nodeSpatial_Reference.appendChild(nodescale_factor)
    nodeSpatial_Reference.appendChild(nodeslantitude_of_origin)
    nodeSpatial_Reference.appendChild(nodesDatum)
    root.appendChild(nodeSpatial_Reference)

    #band_1

    nodeband_1 = doc.createElement(managerList[3]['name'])
    nodeMin = doc.createElement('Min')
    nodeMin.appendChild(doc.createTextNode(str(managerList[3]['Min'])))

    nodeMax = doc.createElement('Max')
    nodeMax.appendChild(doc.createTextNode(str(managerList[3]['Max'])))

    nodeMean = doc.createElement('Mean')
    nodeMean.appendChild(doc.createTextNode(str(managerList[3]['Mean'])))

    nodeStd_dev = doc.createElement('Std_dev')
    nodeStd_dev.appendChild(doc.createTextNode(str(managerList[3]['Std_dev'])))

    nodeband_1.appendChild(nodeMin)
    nodeband_1.appendChild(nodeMax)
    nodeband_1.appendChild(nodeMean)
    nodeband_1.appendChild(nodeStd_dev)

    root.appendChild(nodeband_1)
    #开始写xml文档
    fp = open(address, 'w')
    doc.writexml(fp, indent='\t', addindent='\t', newl='\n', encoding="utf-8")