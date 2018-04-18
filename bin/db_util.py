
import pandas as pd
from utility import *

# relational DB list from wikipedia
# list of db software to search for

''' stuff removed from list
%Microsoft SQL Server Express Edition%
'''

RELATIONAL_DB_LIST_STR = """%4th Dimension%
%Adabas D%
%Alpha Five%
%Apache Derby%
%Derby%
Aster Data%
%Amazon Aurora %
%Aurora %
%Altibase%
%CA Datacom%
%CA IDMS%
%Clarion%
%ClickHouse%
%Clustrix%
%CSQL%
%CUBRID%
%DataEase%
%Database Management Library%
%Dataphor%
%dBase %
%Java%DB%
%Empress Embedded Database%
%EXASolution%
%EnterpriseDB%
%eXtremeDB%
FileMaker Pro%
%Firebird SQL Server%
%FrontBase%
%Google Fusion Tables%
%Fusion Tables%
%Greenplum%
%GroveSite%
H2 %
%Helix database%
%HSQLDB%
IBM DB2% Enterprise% Server%
IBM DB2 OEM Limited Use
DB2 %
%IBM Lotus Approach%
%IBM DB2 Express-C%
%DB2 Express-C%
%Infobright%
%Informix%
%Ingres%
%InterBase%
%InterSystems Caché%
%LibreOffice Base%
%Linter%
%MariaDB%
%MaxDB%
%MemSQL%
Microsoft Access%
%Microsoft Jet Database Engine%
Microsoft SQL Server%
%SQL Azure%
%Cloud SQL Server%
%Microsoft Visual FoxPro%
%Microsoft FoxPro%
%Mimer SQL%
%MonetDB%
%mSQL%
MySQL Server%
Microsoft MySQL%
Sun Microsystems MySQL Server%
%Netezza%
%NexusDB%
%NonStop SQL%
%NuoDB%
%Omnis Studio%
%Openbase%
%OpenLink Virtuoso%
%OpenLink Virtuoso Universal Server%
%OpenOffice.org Base%
Oracle Database %
%Oracle Rdb%
%Panorama%
%Pervasive PSQL%
%Polyhedra%
%PostgreSQL%
%Postgres Plus Advanced Server%
%Progress Software%
%RDM Embedded%
%RDM Server%
%R:Base%
%SAND CDBMS%
%SAP HANA%
%SAP Adaptive Server Enterprise%
%SAP IQ%
%Sybase IQ%
SAP SQL Anywhere%
Sybase SQL Anywhere%
SQL Anywhere%
%Sybase Adaptive Server Anywhere%
%Watcom SQL%
%solidDB%
%SQLBase%
%SQLite%
%SQream DB%
%SAP Advantage Database Server%
%Sybase Advantage Database Server%
%Teradata%
%Tibero%
%TimesTen%
%Trafodion%
%txtSQL%
%Unisys RDMS 2200%
%UniData%
%UniVerse%
%Vectorwise%
%Vertica%
%VoltDB%"""

RELATIONAL_DB_LIST = RELATIONAL_DB_LIST_STR.split('\n')

# list of terms we DONT want to have in the name/path
# list of terms we DONT want to have in the name/path
DB_CONSTRAINT_TERMS_Caseless = ['install', 'uninstall', 'ODBC', 'JDBC', 'update', 'document', 'client', 'driver', 'adapter', 'tools', 'toolkit', 'upgrade', 'utility', 'utilities', 'browser']
DB_CONSTRAINT_TERMS = ['TOAD', 'Console', '.app ', 'Setup']

DB_SPECIFIC_CONSTRAINT_TERMS = { 
   'Microsoft SQL Server%' : ['Analysis Service', 'Common Files', 'Engine Service', 'Integration Service', 'Notification Service', 'Reporting Service', 'Replication% Agent', 'Best Practices Analyzer', 'Management Studio', 'Master Data Service', 'Migration', 'PowerPivot', 'BI Development Studio', 'Registry Rebuild', 'Service Manager', 'VSS Writer', 'Management Objects', 'Language Service', 'Policies', 'Analysis Management', 'Dashboard', 'App Framework', 'Application Framework', 'Backward compatibility', 'OData', 'Publishing Wizard', 'ScriptDom', 'Addin for SharePoint', 'Add-in for SharePoint', 'Compiler Service', 'System CLR Types', 'Report Builder', 'Prerequisites', 'SQLXML4', 'ADOMD.NET', 'Data-Tier App', 'Design', 'Agent', 'Books', 'Remote BLOB Store', 'BPA' ], 
   'Microsoft Access%' : ['Control Panel', 'Database Packer'], 
   'SQL Anywhere%' : ['Studio', 'Sybase', 'SAP'], 
   '%dBase%' : ['QuickReport', 'mold', 'Audbase' ], 
   '%Microsoft Visual FoxPro%' : ['Sedna'], 
   '%Panorama%' : ['32', 'Maker' ], 
   '%mSQL%' : ['Embarcadero TeamSQL', ], 
   '%UniVerse%' : ['Nice Universe', 'Sandbox', 'Omicron'], 
   'FileMaker Pro%' : ['fmxdbc_listener', ], 
   '%PostgreSQL%' : ['Apache', 'Security Manager', 'PostGIS', 'Convert' ], 
   '%SQLite%' : ['ADO.NET', 'Studio', 'System.Data.SQLite'],
   '%Aurora %' : ['Ground Processing', 'Blu-ray', 'HDR', 'Z88'],  
} 


def db_filter_constraint (db_software):

    db_no_percent_name = db_software.replace('%','')
    db_constraint = f"""where (software_name ilike '{db_software}' or install_location ilike '%{db_no_percent_name}%')"""

    '''
    for term in DB_CONSTRAINT_TERMS_Caseless:
        db_constraint += f""" and software_name not ilike '%{term}%'"""
        # db_constraint += f""" and install_location not ilike '%{term}%'"""

    for term in DB_CONSTRAINT_TERMS:
        # db_constraint += f""" and install_location not like '%{term}%'"""
        db_constraint += f""" and software_name not like '%{term}%'"""
    '''

    if db_software in DB_SPECIFIC_CONSTRAINT_TERMS:
        for term in DB_SPECIFIC_CONSTRAINT_TERMS[db_software]:
            db_constraint += f""" and software_name not like '%{term}%'"""
            # db_constraint += f""" and install_location not like '%{term}%'"""

    return db_constraint


# Define a software search method or 2 for us
def db_software (software, conn):
    ''' Simple program to automate software searches '''
    
    return Query (conn, 'rdbs_data', db_filter_constraint(software)).result
        
def db_software_histo (software, conn):
    '''Program to provide breakdown of types of software '''

    return HistoQuery(conn, 'rdbs_data', 'software_name', db_filter_constraint(software)).result 
        
def db_software_count (conn, software, table='rdbs_data', distinct=None):
    '''Determine count of matching software'''
    
    return CountQuery (conn, table, db_filter_constraint(software), distinct).result

def count_rdbs_types(conn):
    '''Count out all of the db software we can find'''
    
    data = []
    for db_software in RELATIONAL_DB_LIST:
        data.append(pd.DataFrame.from_dict({'software_name': db_software.replace('%',''), 'num_types' : db_software_count(conn, db_software, distinct='software_name')['num']}))
    
    return pd.concat(data).sort_values(['num_types'], ascending=False)
    
def count_rdbs_installs(conn):
    
    data = []
    for db_software in RELATIONAL_DB_LIST:
        data.append(pd.DataFrame.from_dict({'software_name': db_software.replace('%',''), 'num_installs' : db_software_count(conn, db_software, table='device_rdbs_basic')['num']}))
        
    return pd.concat(data).sort_values(['num_installs'], ascending=False)
