"""Spatial analysis helpers for GeoPandas datasets."""

from .add_nearest_distance import add_nearest_distance
from .assign_lines_by_max_overlap import assign_lines_by_max_overlap
from .assign_polygons_by_max_overlap import assign_polygons_by_max_overlap
from .attach_nearest_features import attach_nearest_features
from .buffer_features import buffer_features
from .calculate_facility_coverage import calculate_facility_coverage
from .calculate_area import calculate_area
from .calculate_length import calculate_length
from .check_crs import check_crs
from .clip_to_boundary import clip_to_boundary
from .drop_empty_geometries import drop_empty_geometries
from .find_nearest_feature import find_nearest_feature
from .prepare_spatial_data import prepare_spatial_data
from .quick_plot import quick_plot
from .reproject_gdf import reproject_gdf
from .save_gdf import save_gdf
from .spatial_join import spatial_join
from .summarize_lines_within_distance import summarize_lines_within_distance
from .summarize_lines_by_polygon import summarize_lines_by_polygon
from .summarize_gdf import summarize_gdf
from .summarize_points_by_polygon import summarize_points_by_polygon
from .summarize_points_within_distance import summarize_points_within_distance
from .summarize_polygons_by_polygon import summarize_polygons_by_polygon
from .summarize_polygons_within_distance import summarize_polygons_within_distance
from .summarize_street_connectivity import summarize_street_connectivity

__all__ = [
    "add_nearest_distance",
    "assign_lines_by_max_overlap",
    "assign_polygons_by_max_overlap",
    "attach_nearest_features",
    "buffer_features",
    "calculate_facility_coverage",
    "calculate_area",
    "calculate_length",
    "check_crs",
    "clip_to_boundary",
    "drop_empty_geometries",
    "find_nearest_feature",
    "prepare_spatial_data",
    "quick_plot",
    "reproject_gdf",
    "save_gdf",
    "spatial_join",
    "summarize_lines_within_distance",
    "summarize_lines_by_polygon",
    "summarize_gdf",
    "summarize_points_by_polygon",
    "summarize_points_within_distance",
    "summarize_polygons_by_polygon",
    "summarize_polygons_within_distance",
    "summarize_street_connectivity",
]
