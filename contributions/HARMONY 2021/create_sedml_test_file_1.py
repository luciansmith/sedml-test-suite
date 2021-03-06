# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 14:58:01 2021

@author: Lucian
"""

import tellurium as te
import phrasedml
import libsedml
import sys

r = te.loada("""
   model case_01
       species S1=10, S2=5
       S1 -> S2; S1*k
       k = 0.3
   end
   """)

SBML = r.getSBML()

p_str = """
    model0 = model "case_01.xml"
    sim0 = simulate uniform(0, 10, 30)
    task0 = run sim0 on model0
    plot "UniformTimecourse" time vs S1, S2
    report task0.time vs task0.S1
"""
te.saveToFile("case_01.xml", SBML)

# phrasedml.setReferencedSBML("case_01.xml", SBML)
sed = phrasedml.convertString(p_str)
if sed is None:
    print(phrasedml.getLastError())
    sys.exit()

sedml = libsedml.readSedMLFromString(sed)
sedml.setVersion(4)

plot = sedml.getOutput(0)
curve = plot.getCurve(0)
curve.setType(libsedml.SEDML_CURVETYPE_POINTS)
curve.setStyle("blue_line_green_markers")
curve = plot.getCurve(1)
curve.setType(libsedml.SEDML_CURVETYPE_POINTS)
curve.setStyle("red_line_yellow_markers")

style = sedml.createStyle()
style.setId("blue_line_green_markers")
line = style.createLineStyle()
line.setColor("#0000FF")
line.setStyle(libsedml.SEDML_LINETYPE_DASHDOT)
line.setThickness(10)
marker = style.createMarkerStyle()
marker.setFill("#00FF00")
marker.setLineColor("#0000FF")

style = sedml.createStyle()
style.setId("red_line_yellow_markers")
line = style.createLineStyle()
line.setColor("#FF0000")
line.setStyle(libsedml.SEDML_LINETYPE_SOLID)
marker = style.createMarkerStyle()
marker.setFill("#FFFF00")
marker.setLineColor("#FF0000")
marker.setSize(2)
marker.setLineThickness(1)
marker.setStyle(libsedml.SEDML_MARKERTYPE_DIAMOND)


sedstr = libsedml.writeSedMLToString(sedml)
print(sedstr)

te.saveToFile("case_01", SBML)
te.executeSEDML(sedstr)

import os
sedfile = os.path.basename(__file__)
sedfile = sedfile.replace(".py", ".sedml")
sedfile = sedfile.replace("create_sedml_", "")

te.saveToFile(sedfile, sedstr)
