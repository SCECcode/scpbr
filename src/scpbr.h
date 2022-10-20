#ifndef SCPBR_H
#define SCPBR_H

/**
 * @file scpbr.h
 * @brief Main header file for SCPBR library.
 * @author - SCEC 
 * @version 1.0
 *
 * Delivers Southern California Plate Boundary Region Velocity Model
 *
 */

// Includes
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <math.h>

#include "ucvm_model_dtypes.h"

/* config string */
#define SCPBR_CONFIG_MAX 1000

// Structures
/** Defines a point (latitude, longitude, and depth) in WGS84 format */
typedef struct scpbr_point_t {
  /** Longitude member of the point */
  double longitude;
  /** Latitude member of the point */
  double latitude;
  /** Depth member of the point */
  double depth;
} scpbr_point_t;

/** Defines the material properties this model will retrieve. */
typedef struct scpbr_properties_t {
  /** P-wave velocity in meters per second */
  double vp;
  /** S-wave velocity in meters per second */
  double vs;
  /** Density in g/m^3 */
  double rho;
        /** NOT USED from basic_property_t */
        double qp;
        /** NOT USED from basic_property_t */
        double qs;
} scpbr_properties_t;

/** The SCPBR configuration structure. */
typedef struct scpbr_configuration_t {
  /** The zone of UTM projection */
  int utm_zone;
  /** The model directory */
  char model_dir[128];
  /** Number of x points */
  int nx;
  /** Number of y points */
  int ny;
  /** Number of z points */
  int nz;
  /** Depth in meters */
  double depth;
  /** Top left corner easting */
  double top_left_corner_lon;
  /** Top left corner northing */
  double top_left_corner_lat;
  /** Top right corner easting */
  double top_right_corner_lon;
  /** Top right corner northing */
  double top_right_corner_lat;
  /** Bottom left corner easting */
  double bottom_left_corner_lon;
  /** Bottom left corner northing */
  double bottom_left_corner_lat;
  /** Bottom right corner easting */
  double bottom_right_corner_lat;
  /** Bottom right corner northing */
  double bottom_right_corner_lon;
  /** Z interval for the data */
  double depth_interval;
        /** Bilinear or Trilinear Interpolation on or off (1 or 0) */
        int interpolation;

} scpbr_configuration_t;

## define data status
typedef enum { SCPBR_DATA_NA = 0,
               SCPBR_DATA_FILE = 1,
               SCPBR_DATA_MEMORY = 2 } scpbr_data_t;
#define SCPBR_DATA_FAIL 1
#define SCPBR_DATA_USABLE 0
#define SCPBR_DATA_SUCCESS 2
/** The model structure which points to available portions of the model. */
typedef struct scpbr_model_t {
  /** A pointer to the Vp data either in memory or disk. Null if does not exist. */
  void *vp;
  /** Vp status: 0 = not found, 1 = found and not in memory, 2 = found and in memory */
  scpbr_data_t vp_status;
  /** A pointer to the Vs data either in memory or disk. Null if does not exist. */
  void *vs;
  /** Vs status: 0 = not found, 1 = found and not in memory, 2 = found and in memory */
  scpbr_data_t vs_status;
} scpbr_model_t;

// Constants
/** The version of the model. */
const char *scpbr_version_string = "SCPBR";

// Variables
/** Set to 1 when the model is ready for query. */
int scpbr_is_initialized = 0;

/** Location of the binary data files. */
char scpbr_data_directory[128];

/** Configuration parameters. */
scpbr_configuration_t *scpbr_configuration;
/** Holds pointers to the velocity model data OR indicates it can be read from file. */
scpbr_model_t *scpbr_velocity_model;

/** The height of this model's region, in meters. */
double scpbr_total_height_m = 0;
/** The width of this model's region, in meters. */
double scpbr_total_width_m = 0;

// UCVM API Required Functions

#ifdef DYNAMIC_LIBRARY

/** Initializes the model */
int model_init(const char *dir, const char *label);
/** Cleans up the model (frees memory, etc.) */
int model_finalize();
/** Returns version information */
int model_version(char *ver, int len);
/** Queries the model */
int model_query(scpbr_point_t *points, scpbr_properties_t *data, int numpts);

#endif

// SCPBR Related Functions

/** Initializes the model */
int scpbr_init(const char *dir, const char *label);
/** Cleans up the model (frees memory, etc.) */
int scpbr_finalize();
/** Returns version information */
int scpbr_version(char *ver, int len);
/** Queries the model */
int scpbr_query(scpbr_point_t *points, scpbr_properties_t *data, int numpts);

// Non-UCVM Helper Functions
/** Reads the configuration file. */
int scpbr_read_configuration(char *file, scpbr_configuration_t *config);
void print_error(char *err);
/** Retrieves the value at a specified grid point in the model. */
void scpbr_read_properties(int x, int y, int z, scpbr_properties_t *data);
/** Attempts to malloc the model size in memory and read it in. */
int scpbr_try_reading_model(scpbr_model_t *model);
/** Calculates density from Vs. */
double scpbr_calculate_density(double vp);
/** Calculates Vs from Vp. */
double scpbr_calculate_vs(double vp);

// Interpolation Functions
/** Linearly interpolates two scpbr_properties_t structures */
void scpbr_linear_interpolation(double percent, scpbr_properties_t *x0, scpbr_properties_t *x1, scpbr_properties_t *ret_properties);
/** Bilinearly interpolates the properties. */
void scpbr_bilinear_interpolation(double x_percent, double y_percent, scpbr_properties_t *four_points, scpbr_properties_t *ret_properties);
/** Trilinearly interpolates the properties. */
void scpbr_trilinear_interpolation(double x_percent, double y_percent, double z_percent, scpbr_properties_t *eight_points,
               scpbr_properties_t *ret_properties);
