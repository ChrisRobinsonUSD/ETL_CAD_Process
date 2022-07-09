#-------------------------------------------------------------------------------
# Name:         ETL_Workflow.py
# Purpose:      
#
# Author:       Chris Robinson
#
# Created:      3/01/2020
# Updated:      
# Copyright:
# Licence:
#-------------------------------------------------------------------------------

import arcpy
import datetime
import os
import traceback
import sys
import shutil

input_gdb = arcpy.GetParameterAsText(0)
output_shp = arcpy.GetParameterAsText(1)
zipShapes = arcpy.GetParameterAsText(2)
arcpy.env.workspace = input_gdb

arcpy.env.overwriteOutput = True

# Set local variables
out_coordinate_system = arcpy.SpatialReference('NAD 1983 StatePlane Vermont FIPS 4400 (Meters)')

calcRoadCenterlines = arcpy.GetParameterAsText(3)
calcAddressPoints = arcpy.GetParameterAsText(4)
calcEMS = arcpy.GetParameterAsText(5)
calcFire = arcpy.GetParameterAsText(6)
calcLaw = arcpy.GetParameterAsText(7)
calcForestService = arcpy.GetParameterAsText(8)
calcUniComm = arcpy.GetParameterAsText(9)
calcIncMuni = arcpy.GetParameterAsText(10)
calcProvisioning = arcpy.GetParameterAsText(11)
calcPSAP = arcpy.GetParameterAsText(12)
calcRailroadCenterlines = arcpy.GetParameterAsText(13)
calcMileMarkers = arcpy.GetParameterAsText(14)

ems_in = "EMS"
ems_out = "EMS"
ems_table = "EMS_Appendix_Table"
fire_in = "Fire"
fire_out = "Fire"
fire_table = "Fire_Appendix_Table"
forest_service_in = "Forest_Service"
forest_service_out = "Forest_Service"
forest_service_table = "Forest_Service_Appendix_Table"
incorporated_muni_in = "Incorporated_Municipality_Boundary"
incorporated_muni_out = "Incorporated_Municipality_Boundary"
incorporated_muni_table = "Incorporated_Muni_Appendix_Table"
law_in = "Law"
law_out = "Law"
law_table = "Law_Appendix_Table"
mile_marker_in = "Mile_Marker"
mile_marker_out = "Mile_Marker"
mile_marker_table = "Mile_Marker_Appendix_Table"
provisioning_boundary_in = "Provisioning_Boundary"
provisioning_boundary_out = "Provisioning_Boundary"
PSAP_boundary_in = "PSAP_Boundary"
PSAP_boundary_out = "PSAP_Boundary"
provisioning_boundary_table = "Provisioning_Boundary_Appendix_Table"
railroad_centerlines_in = "Railroad_Centerlines"
railroad_centerlines_out = "Railroad_Centerlines"
railroad_centerlines_table = "Railroad_Centerlines_Appendix_Table"
road_centerlines_in = "Road_Centerlines"
road_centerlines_out = "Road_Centerlines"
road_centerlines_table = "Road_Centerlines_Appendix_Table"
site_address_points_in = "Site_Address_Points"
site_address_points_out = "Site_Address_Points"
site_address_points_table = "Site_Address_Points_Appendix_Table"
unincorporated_community_in = "Unincorporated_Community_Boundary"
unincorporated_community_out = "Unincorporated_Community_Boundary"
unincorporated_community_table = "Unincorporated_Community_Boundary_Appendix_Table"
rcl_update = "update"
rcl_roadclass = "roadclass"
rcl_intersect = "Road_Centerlines_Intersect"

#Populate Versaterm Fields for Road Centerlines

if calcRoadCenterlines == 'true':


#Join Road Centerline Feature Class and Appendix Table
	arcpy.JoinField_management(road_centerlines_in , "external_nguid", road_centerlines_table, "external_nguid", ["strname","fmaddr_l", "toaddr_l", "fmaddr_r", "toaddr_r", "lmuni", "rmuni", "stpredir", "stdirsuf", "strtype", "avrrstr", "traveldr", "speed", "planid", "fmnodeid", "tonodeid", "divroad", "update"])
	
	#Versaterm Routing

	#Add Geometry Attributes
	arcpy.AddGeometryAttributes_management(road_centerlines_in, "LINE_START_MID_END", "", "", "")

	#Intersect
	arcpy.Intersect_analysis(road_centerlines_in, rcl_intersect, "ONLY_FID", "", "POINT")

	#Add Field
	arcpy.AddField_management(rcl_intersect, "ID", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

	#Calculate ID Field
	arcpy.CalculateField_management(rcl_intersect, "ID", "[OBJECTID]", "VB", "")

	#Delete Identical
	arcpy.DeleteIdentical_management(rcl_intersect, "SHAPE", "", "0")

	#Add Geometry Attributes
	arcpy.AddGeometryAttributes_management(rcl_intersect, "CENTROID", "", "", "")

	#Add Start X_Y Field
	arcpy.AddField_management(road_centerlines_in, "Start_X_Y", "TEXT", "", "", "100", "", "NULLABLE", "NON_REQUIRED", "")

	#Add End X_Y Field
	arcpy.AddField_management(road_centerlines_in, "End_X_Y", "TEXT", "", "", "100", "", "NULLABLE", "NON_REQUIRED", "")

	#Add X_Y Field
	arcpy.AddField_management(rcl_intersect, "CENTROID_X_Y", "TEXT", "", "", "100", "", "NULLABLE", "NON_REQUIRED", "")

	#Field Calculate Start X_Y
	arcpy.CalculateField_management(road_centerlines_in, "Start_X_Y", "[Start_X] & \"_\" & [Start_Y]", "VB", "")

	#Field Calculate End X_Y
	arcpy.CalculateField_management(road_centerlines_in, "End_X_Y", "[End_X] & \"_\" & [End_Y]", "VB", "")

	#Field Calculate Centroid X_Y
	arcpy.CalculateField_management(rcl_intersect, "CENTROID_X_Y", "[CENTROID_X] & \"_\" & [CENTROID_Y]", "VB", "")
	
	rcl_in_layer = "rcl_in_layer"
	rcl_intersect_layer = "rcl_intersect_layer"

	arcpy.MakeFeatureLayer_management(road_centerlines_in, rcl_in_layer)
	arcpy.MakeFeatureLayer_management(rcl_intersect, rcl_intersect_layer)

	
	arcpy.CalculateField_management(rcl_in_layer, "fmnodeid", "NULL", "VB", "")

	
	arcpy.CalculateField_management(rcl_in_layer, "tonodeid", "NULL", "VB", "")

	
	arcpy.SelectLayerByAttribute_management(rcl_in_layer, "NEW_SELECTION", "planid is null")
	arcpy.CalculateField_management(rcl_in_layer, "planid", "[external_nguid]", "VB", "")
	arcpy.SelectLayerByAttribute_management(rcl_in_layer, "CLEAR_SELECTION")

	
	arcpy.SelectLayerByAttribute_management(rcl_in_layer, "NEW_SELECTION", "rcl_nguid is null")
	arcpy.CalculateField_management(rcl_in_layer, "rcl_nguid", "\"RCL\" & [external_nguid] & \".CA.US\"", "VB", "")
	arcpy.SelectLayerByAttribute_management(rcl_in_layer, "CLEAR_SELECTION")

	joinfield1 = "Start_X_Y"
	joinfield2 = "End_X_Y"
	joinfield3 = "CENTROID_X_Y"
	outfeature = "XY_Join_Output"

	
	Start_X_Y_joined_table = arcpy.AddJoin_management(rcl_in_layer, joinfield1, rcl_intersect_layer, joinfield3, "KEEP_ALL")
	
	arcpy.SelectLayerByAttribute_management(Start_X_Y_joined_table, "NEW_SELECTION", "ID is not null")
	
	arcpy.CalculateField_management(Start_X_Y_joined_table, "fmnodeid", "[Road_Centerlines_Intersect.ID]", "VB", "")
	
	arcpy.SelectLayerByAttribute_management(Start_X_Y_joined_table, "CLEAR_SELECTION")

	arcpy.RemoveJoin_management (Start_X_Y_joined_table)

	End_X_Y_joined_table = arcpy.AddJoin_management(rcl_in_layer, joinfield2, rcl_intersect_layer, joinfield3, "KEEP_ALL")

	arcpy.SelectLayerByAttribute_management(End_X_Y_joined_table, "NEW_SELECTION", "ID is not null")

	arcpy.CalculateField_management(End_X_Y_joined_table, "tonodeid", "[Road_Centerlines_Intersect.ID]", "VB", "")

	arcpy.SelectLayerByAttribute_management(End_X_Y_joined_table, "CLEAR_SELECTION")

	arcpy.RemoveJoin_management (End_X_Y_joined_table)

	#Delete Processing Fields
	arcpy.DeleteField_management(rcl_in_layer, ["START_X", "START_Y", "MID_X", "MID_Y", "END_X", "END_Y", "START_X_Y", "END_X_Y"])
	
	arcpy.SelectLayerByAttribute_management(rcl_in_layer, "NEW_SELECTION", "roadclass = 'FAKE'")
	arcpy.CalculateField_management(rcl_in_layer, "planid", "NULL", "VB", "")
	arcpy.CalculateField_management(rcl_in_layer, "fmnodeid", "NULL", "VB", "")
	arcpy.CalculateField_management(rcl_in_layer, "tonodeid", "NULL", "VB", "")
	arcpy.SelectLayerByAttribute_management(rcl_in_layer, "CLEAR_SELECTION")
	
	arcpy.SelectLayerByAttribute_management(rcl_in_layer, "NEW_SELECTION", "update is null")
	arcpy.CalculateField_management(rcl_in_layer, "strname", "[st_name]", "VB", "")
	arcpy.CalculateField_management(rcl_in_layer, "fmaddr_l", "[fromaddr_l]", "VB", "")
	arcpy.CalculateField_management(rcl_in_layer, "toaddr_l", "[toaddr_l]", "VB", "")
	arcpy.CalculateField_management(rcl_in_layer, "fmaddr_r", "[fromaddr_r]", "VB", "")
	arcpy.CalculateField_management(rcl_in_layer, "toaddr_r", "[toaddr_r]", "VB", "")
	arcpy.CalculateField_management(rcl_in_layer, "lmuni", "[addcode_l]", "VB", "")
	arcpy.CalculateField_management(rcl_in_layer, "rmuni", "[addcode_r]", "VB", "")
	arcpy.CalculateField_management(rcl_in_layer, "stpredir", "[st_predir]", "VB", "")
	arcpy.CalculateField_management(rcl_in_layer, "stdirsuf", "[st_posdir]", "VB", "")
	arcpy.CalculateField_management(rcl_in_layer, "strtype", "[lst_type]", "VB", "")
	arcpy.CalculateField_management(rcl_in_layer, "avrrstr", "[fullrdname]", "VB", "")
	arcpy.CalculateField_management(rcl_in_layer, "traveldr", "left([oneway], 1)", "VB", "")
	arcpy.CalculateField_management(rcl_in_layer, "speed", "[speedlimit]", "VB", "")
	arcpy.SelectLayerByAttribute_management(rcl_in_layer, "CLEAR_SELECTION")

	#Delete Processing Feature Classes
	arcpy.Delete_management(rcl_intersect)
	arcpy.Delete_management(rcl_in_layer)

	arcpy.Project_management(road_centerlines_in, road_centerlines_out, out_coordinate_system)
	
	Road_Centerlines = "Road_Centerlines"
	
	arcpy.MakeFeatureLayer_management(road_centerlines_out, Road_Centerlines, "", "", "OBJECTID OBJECTID HIDDEN NONE;Shape Shape HIDDEN NONE;discrpagid discrpagid HIDDEN NONE;dateupdate dateupdate HIDDEN NONE;effective effective HIDDEN NONE;expire expire HIDDEN NONE;rcl_nguid rcl_nguid HIDDEN NONE;adnumpre_l adnumpre_l HIDDEN NONE;adnumpre_r adnumpre_r HIDDEN NONE;fromaddr_l fromaddr_l HIDDEN NONE;toaddr_l toaddr_l HIDDEN NONE;fromaddr_r fromaddr_r HIDDEN NONE;toaddr_r toaddr_r HIDDEN NONE;parity_l parity_l HIDDEN NONE;parity_r parity_r HIDDEN NONE;st_premod st_premod HIDDEN NONE;st_predir st_predir HIDDEN NONE;st_pretyp st_pretyp HIDDEN NONE;st_presep st_presep HIDDEN NONE;st_name st_name HIDDEN NONE;st_postyp st_postyp HIDDEN NONE;st_posdir st_posdir HIDDEN NONE;st_posmod st_posmod HIDDEN NONE;lst_predir lst_predir HIDDEN NONE;lst_name lst_name HIDDEN NONE;lst_type lst_type HIDDEN NONE;lst_posdir lst_posdir HIDDEN NONE;esn_l esn_l HIDDEN NONE;esn_r esn_r HIDDEN NONE;msagcomm_l msagcomm_l HIDDEN NONE;msagcomm_r msagcomm_r HIDDEN NONE;country_l country_l HIDDEN NONE;country_r country_r HIDDEN NONE;state_l state_l HIDDEN NONE;state_r state_r HIDDEN NONE;county_l county_l HIDDEN NONE;county_r county_r HIDDEN NONE;addcode_l addcode_l HIDDEN NONE;addcode_r addcode_r HIDDEN NONE;incmuni_l incmuni_l HIDDEN NONE;incmuni_r incmuni_r HIDDEN NONE;uninccom_l uninccom_l HIDDEN NONE;uninccom_r uninccom_r HIDDEN NONE;nbrhdcom_l nbrhdcom_l HIDDEN NONE;nbrhdcom_r nbrhdcom_r HIDDEN NONE;postcode_l postcode_l HIDDEN NONE;postcode_r postcode_r HIDDEN NONE;postcomm_l postcomm_l HIDDEN NONE;postcomm_r postcomm_r HIDDEN NONE;roadclass roadclass HIDDEN NONE;oneway oneway HIDDEN NONE;speedlimit speedlimit HIDDEN NONE;valid_l valid_l HIDDEN NONE;valid_r valid_r HIDDEN NONE;psap_idleft psap_idleft HIDDEN NONE;psap_idright psap_idright HIDDEN NONE;external_nguid external_nguid HIDDEN NONE;data_source data_source HIDDEN NONE;created_user created_user HIDDEN NONE;created_date created_date HIDDEN NONE;last_edited_user last_edited_user HIDDEN NONE;last_edited_date last_edited_date HIDDEN NONE;fullrdname fullrdname HIDDEN NONE;Shape_Length Shape_Length HIDDEN NONE;strname strname VISIBLE NONE;fmaddr_l fmaddr_l VISIBLE NONE;toaddr_l toaddr_l VISIBLE NONE;fmaddr_r fmaddr_r VISIBLE NONE;toaddr_r toaddr_r VISIBLE NONE;lmuni lmuni VISIBLE NONE;rmuni rmuni VISIBLE NONE;stpredir stpredir VISIBLE NONE;stdirsuf stdirsuf VISIBLE NONE;strtype strtype VISIBLE NONE;avrrstr avrrstr VISIBLE NONE;traveldr traveldr VISIBLE NONE;speed speed VISIBLE NONE;planid planid VISIBLE NONE;fmnodeid fmnodeid VISIBLE NONE;tonodeid tonodeid VISIBLE NONE;divroad divroad VISIBLE NONE;update update VISIBLE NONE")
	
	arcpy.FeatureClassToShapefile_conversion(Road_Centerlines, output_shp)
	
	arcpy.DeleteField_management("Road_Centerlines", ["strname", "fmaddr_l", "toaddr_l", "fmaddr_r", "toaddr_r", "lmuni", "rmuni", "stpredir", "stdirsuf", "strtype", "avrrstr", "traveldr", "speed", "planid", "fmnodeid", "tonodeid", "divroad", "update"])
	


#Polulate Fields for Site Address Points

if calcAddressPoints == 'true':

	#Join Address Point Feature Class and Appendix Table
	arcpy.JoinField_management("Site_Address_Points", "external_nguid", "Site_Address_Points_Appendix_Table", "external_nguid", ["housenum","strname", "stpredir", "stdirsuf", "strtype", "hnumsuf", "hnumfrac", "addr", "unit", "uni_comm"])


	arcpy.CalculateField_management(site_address_points_in, "housenum", "[add_number]", "VB", "")
	arcpy.CalculateField_management(site_address_points_in, "strname", "[st_name]", "VB", "")
	arcpy.CalculateField_management(site_address_points_in, "stpredir", "[st_predir]", "VB", "")
	arcpy.CalculateField_management(site_address_points_in, "stdirsuf", "[st_posdir]", "VB", "")
	arcpy.CalculateField_management(site_address_points_in, "strtype", "[lst_type]", "VB", "")
	arcpy.CalculateField_management(site_address_points_in, "hnumsuf", "[addnum_suf]", "VB", "")
	arcpy.CalculateField_management(site_address_points_in, "hnumfrac", "[building]", "VB", "")
	arcpy.CalculateField_management(site_address_points_in, "addr", "[add_number] & \" \" & [fullrdname]", "VB", "")
	arcpy.CalculateField_management(site_address_points_in, "unit", "[unit]", "VB", "")
	arcpy.CalculateField_management(site_address_points_in, "uni_comm", "[uninc_comm]", "VB", "")
	
	arcpy.Project_management(site_address_points_in, site_address_points_out, out_coordinate_system)
	
	Site_Address_Points = "Site_Address_Points"
	
	arcpy.MakeFeatureLayer_management(site_address_points_out, Site_Address_Points, "", "", "OBJECTID OBJECTID HIDDEN NONE;Shape Shape HIDDEN NONE;discrpagid discrpagid HIDDEN NONE;dateupdate dateupdate HIDDEN NONE;effective effective HIDDEN NONE;expire expire HIDDEN NONE;site_nguid site_nguid HIDDEN NONE;country country HIDDEN NONE;state state HIDDEN NONE;county county HIDDEN NONE;addcode addcode HIDDEN NONE;inc_muni inc_muni HIDDEN NONE;uninc_comm uninc_comm HIDDEN NONE;nbrhd_comm nbrhd_comm HIDDEN NONE;addnum_pre addnum_pre HIDDEN NONE;add_number add_number HIDDEN NONE;addnum_suf addnum_suf HIDDEN NONE;st_premod st_premod HIDDEN NONE;st_predir st_predir HIDDEN NONE;st_pretyp st_pretyp HIDDEN NONE;st_presep st_presep HIDDEN NONE;st_name st_name HIDDEN NONE;st_postyp st_postyp HIDDEN NONE;st_posdir st_posdir HIDDEN NONE;st_posmod st_posmod HIDDEN NONE;lst_predir lst_predir HIDDEN NONE;lst_name lst_name HIDDEN NONE;lst_type lst_type HIDDEN NONE;lst_posdir lst_posdir HIDDEN NONE;esn esn HIDDEN NONE;msagcomm msagcomm HIDDEN NONE;post_comm post_comm HIDDEN NONE;post_code post_code HIDDEN NONE;post_code4 post_code4 HIDDEN NONE;building building HIDDEN NONE;floor floor HIDDEN NONE;unit_type unit_type HIDDEN NONE;unit unit HIDDEN NONE;room room HIDDEN NONE;seat seat HIDDEN NONE;addtl_loc addtl_loc HIDDEN NONE;landmkname landmkname HIDDEN NONE;mile_post mile_post HIDDEN NONE;place_type place_type HIDDEN NONE;placement placement HIDDEN NONE;long long HIDDEN NONE;lat lat HIDDEN NONE;elev elev HIDDEN NONE;psap_id psap_id HIDDEN NONE;adddatauri adddatauri HIDDEN NONE;external_nguid external_nguid HIDDEN NONE;globalid globalid HIDDEN NONE;data_source data_source HIDDEN NONE;created_user created_user HIDDEN NONE;created_date created_date HIDDEN NONE;last_edited_user last_edited_user HIDDEN NONE;last_edited_date last_edited_date HIDDEN NONE;fullrdname fullrdname HIDDEN NONE;housenum housenum VISIBLE NONE;strname strname VISIBLE NONE;;stpredir stpredir VISIBLE NONE;stdirsuf stdirsuf VISIBLE NONE;strtype strtype VISIBLE NONE;hnumsuf hnumsuf VISIBLE NONE;hnumfrac hnumfrac VISIBLE NONE;addr addr VISIBLE NONE;unit unit VISIBLE NONE;uni_comm uni_comm VISIBLE NONE")
	
	arcpy.FeatureClassToShapefile_conversion(Site_Address_Points, output_shp)
	
	arcpy.DeleteField_management("Site_Address_Points", ["housenum","strname", "stpredir", "stdirsuf", "strtype", "hnumsuf", "hnumfrac", "addr", "unit", "uni_comm"])
	
if calcEMS == 'true':

	#Join EMS Feature Class and Appendix Table
	arcpy.JoinField_management("EMS", "external_nguid", "EMS_Appendix_Table", "external_nguid", ["jurisdic","district", "zone", "grid"])

	arcpy.Project_management(ems_in, ems_out, out_coordinate_system)
	
	EMS = "EMS"
	
	arcpy.MakeFeatureLayer_management(ems_out, EMS, "", "", "OBJECTID OBJECTID HIDDEN NONE;Shape Shape HIDDEN NONE;discrpagid discrpagid HIDDEN NONE;dateupdate dateupdate HIDDEN NONE;effective effective HIDDEN NONE;expire expire HIDDEN NONE;es_nguid es_nguid HIDDEN NONE;state state HIDDEN NONE;agency_id agency_id HIDDEN NONE;serviceuri serviceuri HIDDEN NONE;serviceurn serviceurn HIDDEN NONE;servicenum servicenum HIDDEN NONE;avcard_uri avcard_uri HIDDEN NONE;dsplayname dsplayname HIDDEN NONE;external_nguid external_nguid HIDDEN NONE;globalid globalid HIDDEN NONE;data_source data_source HIDDEN NONE;created_user created_user HIDDEN NONE;created_date created_date HIDDEN NONE;last_edited_user last_edited_user HIDDEN NONE;last_edited_date last_edited_date HIDDEN NONE;Shape_Length Shape_Length HIDDEN NONE;Shape_Area Shape_Area HIDDEN NONE;jurisdic jurisdic VISIBLE NONE;district district VISIBLE NONE;zone zone VISIBLE NONE;grid grid VISIBLE NONE")
	
	arcpy.FeatureClassToShapefile_conversion(EMS, output_shp)

	arcpy.DeleteField_management("EMS", ["jurisdic","district", "zone", "grid"])
	
if calcFire == 'true':

	#Join Fire Feature Class and Appendix Table
	arcpy.JoinField_management("Fire", "external_nguid", "Fire_Appendix_Table", "external_nguid", ["jurisdic","district", "zone", "grid"])

	arcpy.Project_management(fire_in, fire_out, out_coordinate_system)
	
	Fire = "Fire"
	
	arcpy.MakeFeatureLayer_management(fire_out, Fire, "", "", "OBJECTID OBJECTID HIDDEN NONE;Shape Shape HIDDEN NONE;discrpagid discrpagid HIDDEN NONE;dateupdate dateupdate HIDDEN NONE;effective effective HIDDEN NONE;expire expire HIDDEN NONE;es_nguid es_nguid HIDDEN NONE;state state HIDDEN NONE;agency_id agency_id HIDDEN NONE;serviceuri serviceuri HIDDEN NONE;serviceurn serviceurn HIDDEN NONE;servicenum servicenum HIDDEN NONE;avcard_uri avcard_uri HIDDEN NONE;dsplayname dsplayname HIDDEN NONE;external_nguid external_nguid HIDDEN NONE;GlobalID GlobalID HIDDEN NONE;data_source data_source HIDDEN NONE;created_user created_user HIDDEN NONE;created_date created_date HIDDEN NONE;last_edited_user last_edited_user HIDDEN NONE;last_edited_date last_edited_date HIDDEN NONE;Shape_Length Shape_Length HIDDEN NONE;Shape_Area Shape_Area HIDDEN NONE;jurisdic jurisdic VISIBLE NONE;district district VISIBLE NONE;zone zone VISIBLE NONE;grid grid VISIBLE NONE")
	
	arcpy.FeatureClassToShapefile_conversion(Fire, output_shp)
	
	arcpy.DeleteField_management("Fire", ["jurisdic","district", "zone", "grid"])

if calcLaw == 'true':

	#Join Law Feature Class and Appendix Table
	arcpy.JoinField_management("Law", "external_nguid", "Law_Appendix_Table", "external_nguid", ["jurisdic","district", "zone", "grid"])

	arcpy.Project_management(law_in, law_out, out_coordinate_system)
	
	Law = "Law"
	
	arcpy.MakeFeatureLayer_management(law_out, Law, "", "", "OBJECTID OBJECTID HIDDEN NONE;Shape Shape HIDDEN NONE;discrpagid discrpagid HIDDEN NONE;dateupdate dateupdate HIDDEN NONE;effective effective HIDDEN NONE;expire expire HIDDEN NONE;es_nguid es_nguid HIDDEN NONE;state state HIDDEN NONE;agency_id agency_id HIDDEN NONE;serviceuri serviceuri HIDDEN NONE;serviceurn serviceurn HIDDEN NONE;servicenum servicenum HIDDEN NONE;avcard_uri avcard_uri HIDDEN NONE;dsplayname dsplayname HIDDEN NONE;external_nguid external_nguid HIDDEN NONE;GlobalID GlobalID HIDDEN NONE;data_source data_source HIDDEN NONE;created_user created_user HIDDEN NONE;created_date created_date HIDDEN NONE;last_edited_user last_edited_user HIDDEN NONE;last_edited_date last_edited_date HIDDEN NONE;Shape_Length Shape_Length HIDDEN NONE;Shape_Area Shape_Area HIDDEN NONE;jurisdic jurisdic VISIBLE NONE;district district VISIBLE NONE;zone zone VISIBLE NONE;grid grid VISIBLE NONE")
	
	arcpy.FeatureClassToShapefile_conversion(Law, output_shp)
	
	arcpy.DeleteField_management("Law", ["jurisdic","district", "zone", "grid"])

if calcForestService == 'true':

	arcpy.AddField_management(forest_service_in, "jurisdic", "TEXT", "", "", "2", "", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(forest_service_in, "district", "TEXT", "", "", "4", "", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(forest_service_in, "zone", "TEXT", "", "", "6", "", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(forest_service_in, "grid", "TEXT", "", "", "6", "", "NULLABLE", "NON_REQUIRED", "")
	
	arcpy.CalculateField_management(forest_service_in, "jurisdic", "left([discrpagid], 2)", "VB", "")
	arcpy.CalculateField_management(forest_service_in, "district", "NULL", "VB", "")
	arcpy.CalculateField_management(forest_service_in, "zone", "[external_nguid]", "VB", "")

	forest_service_in_layer = "forest_service_in_layer"

	arcpy.MakeFeatureLayer_management(forest_service_in, forest_service_in_layer)

	arcpy.SelectLayerByAttribute_management(forest_service_in_layer, "NEW_SELECTION", "dsplayname LIKE '% SB%' or dsplayname LIKE '%BEACH%'")
	arcpy.CalculateField_management(forest_service_in_layer, "grid", "\"BEACH\"", "VB", "")
	arcpy.SelectLayerByAttribute_management(forest_service_in_layer, "SWITCH_SELECTION")
	arcpy.CalculateField_management(forest_service_in_layer, "grid", "\"PARK\"", "VB", "")
	arcpy.SelectLayerByAttribute_management(forest_service_in_layer, "CLEAR_SELECTION")	

	arcpy.Project_management(forest_service_in, forest_service_out, out_coordinate_system)
	
	Forest_Service = "Forest_Service"
	
	arcpy.MakeFeatureLayer_management(forest_service_out, Forest_Service, "", "", "OBJECTID OBJECTID HIDDEN NONE;Shape Shape HIDDEN NONE;discrpagid discrpagid HIDDEN NONE;dateupdate dateupdate HIDDEN NONE;effective effective HIDDEN NONE;expire expire HIDDEN NONE;es_nguid es_nguid HIDDEN NONE;state state HIDDEN NONE;agency_id agency_id HIDDEN NONE;serviceuri serviceuri HIDDEN NONE;serviceurn serviceurn HIDDEN NONE;servicenum servicenum HIDDEN NONE;avcard_uri avcard_uri HIDDEN NONE;dsplayname dsplayname HIDDEN NONE;external_nguid external_nguid HIDDEN NONE;data_source data_source HIDDEN NONE;created_user created_user HIDDEN NONE;created_date created_date HIDDEN NONE;last_edited_user last_edited_user HIDDEN NONE;last_edited_date last_edited_date HIDDEN NONE;Shape_Length Shape_Length HIDDEN NONE;Shape_Area Shape_Area HIDDEN NONE;jurisdic jurisdic VISIBLE NONE;district district VISIBLE NONE;zone zone VISIBLE NONE;grid grid VISIBLE NONE")

	arcpy.FeatureClassToShapefile_conversion(Forest_Service, output_shp)
	
	arcpy.DeleteField_management("Forest_Service", ["jurisdic","district", "zone", "grid"])

if calcUniComm == 'true':

	arcpy.AddField_management(unincorporated_community_in, "uni_comm", "TEXT", "", "", "6", "", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(unincorporated_community_in, "county", "TEXT", "", "", "2", "", "NULLABLE", "NON_REQUIRED", "")

	arcpy.CalculateField_management(unincorporated_community_in, "uni_comm", "[uninc_comm]", "VB", "")
	arcpy.CalculateField_management(unincorporated_community_in, "county", "left([county], 2)", "VB", "")
	
	arcpy.Project_management(unincorporated_community_in, unincorporated_community_out, out_coordinate_system)
	
	Unincorporated_Community_Boundary = "Unincorporated_Community_Boundary"
	
	arcpy.MakeFeatureLayer_management(unincorporated_community_out, Unincorporated_Community_Boundary, "", "", "OBJECTID OBJECTID HIDDEN NONE;Shape Shape HIDDEN NONE;discrpagid discrpagid HIDDEN NONE;effective effective HIDDEN NONE;expire expire HIDDEN NONE;unincnguid unincnguid HIDDEN NONE;country country HIDDEN NONE;state state HIDDEN NONE;county county HIDDEN NONE;addcode addcode HIDDEN NONE;uninc_comm uninc_comm HIDDEN NONE;dateupdate dateupdate HIDDEN NONE;external_nguid external_nguid HIDDEN NONE;globalid globalid HIDDEN NONE;Shape_Length Shape_Length HIDDEN NONE;Shape_Area Shape_Area HIDDEN NONE;uni_comm uni_comm VISIBLE NONE;county county VISIBLE NONE")

	arcpy.FeatureClassToShapefile_conversion(Unincorporated_Community_Boundary, output_shp)
	
	arcpy.DeleteField_management("Unincorporated_Community_Boundary", ["uni_comm","county"])

if calcIncMuni == 'true':

	arcpy.AddField_management(incorporated_muni_in, "inc_muni", "TEXT", "", "", "6", "", "NULLABLE", "NON_REQUIRED", "")
	arcpy.AddField_management(incorporated_muni_in, "county", "TEXT", "", "", "2", "", "NULLABLE", "NON_REQUIRED", "")

	arcpy.CalculateField_management(incorporated_muni_in, "inc_muni", "[addcode]", "VB", "")
	arcpy.CalculateField_management(incorporated_muni_in, "county", "left([county], 2)", "VB", "")
	
	arcpy.Project_management(incorporated_muni_in, incorporated_muni_out, out_coordinate_system)
	
	Incorporated_Municipality_Boundary = "Incorporated_Municipality_Boundary"
	
	arcpy.MakeFeatureLayer_management(incorporated_muni_out, Incorporated_Municipality_Boundary, "", "", "OBJECTID OBJECTID HIDDEN NONE;Shape Shape HIDDEN NONE;discrpagid discrpagid HIDDEN NONE;effective effective HIDDEN NONE;expire expire HIDDEN NONE;incm_nguid incm_nguid HIDDEN NONE;country country HIDDEN NONE;state state HIDDEN NONE;county county HIDDEN NONE;addcode addcode HIDDEN NONE;inc_muni inc_muni HIDDEN NONE;dateupdate dateupdate HIDDEN NONE;external_nguid external_nguid HIDDEN NONE;globalid globalid HIDDEN NONE;Shape_Length Shape_Length HIDDEN NONE;Shape_Area Shape_Area HIDDEN NONE;inc_muni inc_muni VISIBLE NONE;county county VISIBLE NONE")

	arcpy.FeatureClassToShapefile_conversion(Incorporated_Municipality_Boundary, output_shp)
	
	arcpy.DeleteField_management("Incorporated_Municipality_Boundary", ["inc_muni","county"])

if calcProvisioning == 'true':

	arcpy.Project_management(provisioning_boundary_in, provisioning_boundary_out, out_coordinate_system)

if calcPSAP == 'true':

	arcpy.Project_management(PSAP_boundary_in, PSAP_boundary_out, out_coordinate_system)

if calcRailroadCenterlines == 'true':

	arcpy.Project_management(railroad_centerlines_in, railroad_centerlines_out, out_coordinate_system)

if calcMileMarkers == 'true':

	arcpy.AddField_management(mile_marker_in, "milem", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
	arcpy.CalculateField_management(mile_marker_in, "milem", "[milemvalue] * 10", "VB", "")
	
	arcpy.Project_management(mile_marker_in, mile_marker_out, out_coordinate_system)
	
	mile_marker = "mile_marker"
	
	arcpy.MakeFeatureLayer_management(mile_marker_out, mile_marker, "", "", "OBJECTID OBJECTID HIDDEN NONE;Shape Shape HIDDEN NONE;discrpagid discrpagid HIDDEN NONE;dateupdate dateupdate HIDDEN NONE;milemnguid milemnguid HIDDEN NONE;milem_unit milem_unit HIDDEN NONE;milemvalue milemvalue HIDDEN NONE;milem_rte milem_rte HIDDEN NONE;milem_type milem_type HIDDEN NONE;milem_ind milem_ind HIDDEN NONE;external_nguid external_nguid HIDDEN NONE;globalid globalid HIDDEN NONE;milem milem VISIBLE NONE")

	arcpy.FeatureClassToShapefile_conversion(mile_marker, output_shp)
	
	arcpy.DeleteField_management("Mile_Marker", ["milem"])
	
if zipShapes == 'true':
	
	shutil.make_archive(output_shp, "zip", output_shp)  
