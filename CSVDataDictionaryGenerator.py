from wb import * 
import grt
from mforms import Utilities, FileChooser
import mforms
import csv
 
ModuleInfo = DefineModule(name="GenerateCSVDataDictionary", author="Jan Lynnel Balitaan", version="1.0", description="Database dictionary in CSV format")
 
@ModuleInfo.plugin("jlb.data.dictionary.generator", caption="Data dictionary in CSV format", description="Data dictionary in CSV format", input=[wbinputs.currentCatalog()], pluginMenu="Catalog")
@ModuleInfo.export(grt.INT, grt.classes.db_Catalog)
 
def generateCSVDataDictionary(catalog):
    #choose a file name for the data dictionary
    fileName = ""
    fileChooser = FileChooser(mforms.SaveFile)
    fileChooser.set_extensions("CSV File (*.csv)|*.csv", "csv");
    if fileChooser.run_modal():
       fileName = fileChooser.get_path()
    
    #static headers
    headers = ['Schema', 'Table', 'Name', 'Data Type', 'Nullable', 'PK', 'FK', 'Default', 'Description', 'Sample Data']
    
    #create and open the csv file
    with open(fileName, 'wb') as csvfile:
        #create a csv writer
        csvWriter = csv.writer(csvfile)
    
        #write the headers into the csv file
        csvWriter.writerow(headers)
        
        #start of schema iteration
        for schema in catalog.schemata:
        
            #start of tables iteration
            for table in schema.tables:
            
                #start of columns iteration
                for column in table.columns:
                
                    isPrimaryKey = ('No', 'Yes')[bool(table.isPrimaryKeyColumn(column))]
                    isForeignKey = ('No', 'Yes')[bool(table.isForeignKeyColumn(column))]
                    isNotNullable = ('No', 'Yes')[bool(column.isNotNull)]
                    
                    #write the values in a row in the csv file
                    csvWriter.writerow([schema.name, table.name, column.name, column.formattedType, isNotNullable, isPrimaryKey, isForeignKey, column.defaultValue])
               
               #end of columns iteration
            
            #end of tables iteration
        
        #end of schema iteration        
    
    #show message for a successful generation of data dictionary
    Utilities.show_message("Data dictionary generated", "CSV format data dictionary generated", "OK","","")
    
    return 0
