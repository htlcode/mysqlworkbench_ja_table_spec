#!/usr/bin/env python
# -*- coding: utf-8 -*-
# MySQL Workbench Python script
# Script to Generate an HTML Schema Report from Mysql Model
# Author: Tito Sanchez forked by CAISSON Frederic
# Written in MySQL Workbench 8.0.29

from wb import *
import grt
from mforms import Utilities, FileChooser
import mforms
import time
import json

today = time.strftime("%Y/%m/%d %H:%M:%S")

ModuleInfo = DefineModule(name="DBReport", author="CAISSON Frederic", version="4", description="Create a schema of the database in HTML format")

@ModuleInfo.plugin("CaissonPlugin.htmlReportSchema", caption="Generate tables definition HTML", description="Create a schema of the database in HTML format", input=[wbinputs.currentCatalog()], pluginMenu="Catalog")
@ModuleInfo.export(grt.INT, grt.classes.db_Catalog)

def htmlDataDictionary(catalog):
    # Put plugin contents here
    htmlOut = ""
    filechooser = FileChooser(mforms.SaveFile)
    filechooser.set_extensions("HTML File (*.html)|*.html","html");
    if filechooser.run_modal():
      htmlOut = filechooser.get_path()
    print("HTML File: %s" % (htmlOut))
    if len(htmlOut) <= 1:
      return 1
    # iterate through columns from schema
    schema = catalog.schemata[0]
    # sort table map
    mapTemp = dict()
    for table in schema.tables:
      mapTemp[table.name] = table
    mapTables = dict(sorted(mapTemp.items(), key=lambda item: item[0]))
    tableDatas = []
    for table in mapTables.values():
      tableObj = dict({'tableName': table.name,'columns': []})
      for column in table.columns:
        pk = (0, 1)[bool(table.isPrimaryKeyColumn(column))]
        fk = (0, 1)[bool(table.isForeignKeyColumn(column))]
        nn = (0, 1)[bool(column.isNotNull)]
        ai = (0, 1)[bool(column.autoIncrement)]
        isUnique = 0
        for index in table.indices:
          if index.indexType == "UNIQUE":
            for c in index.columns:
              if c.referencedColumn.name == column.name:
                isUnique = 1
                break
        columnObj = dict({'tableName': table.name, 'columnName': column.name, 'type': column.formattedType, 'notNull': nn, 'primary': pk, 'auto': ai, 'unique': isUnique, 'foreign': fk, 'default': column.defaultValue })
        tableObj['columns'].append(columnObj)
      tableDatas.append(tableObj)
    jsonStr = json.dumps(tableDatas, indent=2)
    htmlFile = open(htmlOut, "w", encoding="utf-8")
    htmlFile.write( "<!DOCTYPE html><html><head><meta charset='UTF-8'>")
    htmlFile.write( "<title>\u30c6\u30fc\u30d6\u30eb\u5b9a\u7fa9\u66f8: %s</title> \n" % (schema.name))
    htmlFile.write( """<style>
        td,th {
        text-align:left;
        vertical-align:middle;
        }
        table {
        border-collapse: collapse;
        border: 1px solid;
        }
        caption, th, td {
        padding: .2em .8em;
        border: 1px solid #000000;
        }
        caption {
        background: #D3D3D3;
        font-weight: bold;
        font-size: 1.1em;
        }
        th {
        font-weight: bold;
        background: #000000;
        color: white;
        }
        td {
        background: #FFFFFF;
        }
        td.td-head {
        background: #D3D3D3;        
        }
        td.field {
        color: navy;        
        }
        hr {
        margin-bottom:24px;
        }
        </style>
        <script>
        toggleJson = function(){
          var item = document.getElementById('json');
          if (item.style.display == "block")
          {
            item.style.display = 'none';
          }
          else
          {
            item.style.display = 'block';
          }
        }
        </script>
      </head>
     <body>""")
    htmlFile.write("\n"  )
    htmlFile.write("<button onclick='toggleJson()'>Json Data</button> \n" ) 
    htmlFile.write("<textarea style='display:none' id='json'>\n")
    htmlFile.write("%s \n" % (jsonStr) )
    htmlFile.write("</textarea>\n")
    htmlFile.write( "<h1>\u30c6\u30fc\u30d6\u30eb\u5b9a\u7fa9\u66f8</h1> \n" )
    htmlFile.write( "<p>\u66f4\u65b0\u65e5: %s<p> \n" % (today) )
    htmlFile.write( "<table style=\"width:100%%\"><caption><a id=\"home\">\u30c6\u30fc\u30d6\u30eb\u4e00\u89a7 </a></caption> \n " )
    i = 0
    for table in mapTables.values():
      i = i + 1
      comment1 = table.comment.split('\n')[0]
      htmlFile.write( "<tr><td>%s</td><td><a href=\"#%s\">%s</a></td><td>%s</td></tr> \n" % (i,table.name,table.name,comment1) )
    htmlFile.write( "</table><hr> \n" )
    for table in mapTables.values():
      comment1 = table.comment.split('\n')[0]
      commentr = '\n'.join(table.comment.split('\n')[1:])
      htmlFile.write( "<a id=\"%s\"></a><table style=\"width:100%%\"><caption>\u7269\u7406\u30c6\u30fc\u30d6\u30eb\u540d: %s </caption> \n" % (table.name,table.name) )
      htmlFile.write( "<tr><td class='td-head'>\u8ad6\u7406\u30c6\u30fc\u30d6\u30eb\u540d</td><td colspan=\"9\"><strong>%s<strong></td></tr> \n" % (comment1) )
      commentrs = str.strip(commentr)
      if (len(commentrs)):
        htmlFile.write( "<tr><td class='td-head'>\u30c6\u30fc\u30d6\u30eb\u30b3\u30e1\u30f3\u30c8</td><td colspan=\"9\">%s</td></tr> \n" % (nl2br(commentr)) )
      htmlFile.write( """<tr>
        <th>\u30d5\u30a3\u30fc\u30eb\u30c9\u540d</th>
        <th>\u8ad6\u7406\u30d5\u30a3\u30fc\u30eb\u30c9\u540d</th>
        <th>\u30c7\u30fc\u30bf\u578b (\u6841\u6570)</th>
        <th>\u5fc5\u9808</th>
        <th>\u4e3b\u30ad\u30fc</th>
        <th>\u81ea\u52d5\u30ad\u30fc</th>
        <th>\u30e6\u30cb\u30fc\u30af</th>
        <th>\u5916\u90e8\u30ad\u30fc</th>
        <th>\u30c7\u30d5\u30a9\u30eb\u30c8\u5024</th>
        <th>\u30d5\u30a3\u30fc\u30eb\u30c9\u30b3\u30e1\u30f3\u30c8</th>
        </tr>""")
      htmlFile.write("\n ")
      for column in table.columns:
        pk = ('', 'PK')[bool(table.isPrimaryKeyColumn(column))]
        fk = ('', 'FK')[bool(table.isForeignKeyColumn(column))]
        nn = ('\u00d7', '\u25cf')[bool(column.isNotNull)]
        ai = ('', 'AI')[bool(column.autoIncrement)]
        comment1 = column.comment.split('\n')[0]
        commentr = '\n'.join(column.comment.split('\n')[1:])
        isUnique = 0
        for index in table.indices:
          if index.indexType == "UNIQUE":
            for c in index.columns:
              if c.referencedColumn.name == column.name:
                isUnique = 1
                break
        uq = ('', 'U')[bool(isUnique)]
        htmlFile.write( "<tr><td class='field'>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr> \n" % (column.name,comment1,column.formattedType,nn,pk,ai,uq,fk,column.defaultValue,commentr) )
      htmlFile.write("</table> \n")
      if (len(table.indices)):
        htmlFile.write( "<br><table style=\"width:100%%\"><caption>\u30a4\u30f3\u30c7\u30c3\u30af\u30b9\u5b9a\u7fa9</caption> \n " )
        htmlFile.write( """<tr>
        <th>\u30a4\u30f3\u30c7\u30c3\u30af\u30b9\u540d</th>
        <th>\u30bf\u30a4\u30d7</th>
        <th>\u5bfe\u8c61\u30d5\u30a3\u30fc\u30eb\u30c9</th>
        </tr>""")
        for index in table.indices:
          fields = ", ".join(map(lambda x: x.referencedColumn.name, index.columns))
          htmlFile.write( "<tr><td>%s</td><td>%s</td><td class='field'>%s</td></tr> \n" % (index.name, index.indexType, fields) )
        htmlFile.write("</table> \n")
      if (len(table.foreignKeys)):
        htmlFile.write( "<br><table style=\"width:100%%\"><caption>\u5916\u90e8\u30ad\u30fc\u5b9a\u7fa9</caption> \n " )
        htmlFile.write( """<tr>
        <th>\u5916\u90e8\u30ad\u30fc\u540d</th>
        <th>\u30c6\u30fc\u30d6\u30eb</th>
        <th>\u30d5\u30a3\u30fc\u30eb\u30c9</th>
        <th>\u53c2\u7167\u5148\u30c6\u30fc\u30d6\u30eb</th>
        <th>\u53c2\u7167\u5148\u30d5\u30a3\u30fc\u30eb\u30c9</th>
        </tr>""")
        for fk in table.foreignKeys:
          for column in table.columns:
            if fk.columns[0].name == column.name:
              htmlFile.write( "<tr><td>%s</td><td>%s</td><td class='field'>%s</td><td>%s</td><td class='field'>%s</td></tr> \n" % (fk.name, table.name, column.name, fk.referencedColumns[0].owner.name, fk.referencedColumns[0].name) )
        htmlFile.write("</table> \n")
      htmlFile.write("<p><a href=\"#home\">\u30c6\u30fc\u30d6\u30eb\u4e00\u89a7 </a></p><hr> \n" )
    htmlFile.write("</body></html> \n")
    htmlFile.close()
    Utilities.show_message("Report generated", "HTML Report format from current model generated in %s" % htmlOut, "OK","","")
    return 0

def nl2br(text):
    return "<br />".join(map(lambda x: x.strip(), text.split("\n")))