from django.apps import AppConfig
from django.db import connection

class WorkoutsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Workouts'
    
    def ready(self) -> None:
        """
            Setup the database for the app. This configuration occurs once on server launch.
        """
        
        print("created tables")
        return super().ready()

    
class ConfigureDB(AppConfig):
    """
    
    """

    # Drop All Tables - comment the portion below to persist data
    with connection.cursor() as cursor:
        cursor.execute(
            """
                DROP TABLE IF EXISTS Plans_Workouts;
                DROP TABLE IF EXISTS Sessions_SensorData;
                DROP TABLE IF EXISTS ReportItems;
                DROP TABLE IF EXISTS Reports;
                DROP TABLE IF EXISTS SensorData;
                DROP TABLE IF EXISTS Sessions CASCADE;
                DROP TABLE IF EXISTS WorkingSets CASCADE;
                DROP TABLE IF EXISTS Sets;
                DROP TABLE IF EXISTS Workouts;
                DROP TABLE IF EXISTS Plans;
                DROP TABLE IF EXISTS Users;
            """
        )
        cursor.db.commit()


    # Create All Tables
    with connection.cursor() as cursor:
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS Users (
                    u_userID SERIAL PRIMARY KEY NOT NULL,
                    u_image TEXT,
                    u_firstName TEXT NOT NULL,
                    u_lastName TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS Plans (
                    p_planID SERIAL PRIMARY KEY NOT NULL,
                    p_planName TEXT NOT NULL,
                    p_userID INT REFERENCES Users ( u_userID )
                );

                CREATE TABLE IF NOT EXISTS Workouts (
                    w_workoutID SERIAL PRIMARY KEY NOT NULL,
                    w_workoutName TEXT NOT NULL,
                    w_mainMuscleGroup TEXT,
                    w_equipment TEXT,
                    w_description TEXT,
                    w_level TEXT,
                    w_images TEXT [],
                    w_isPrivate BOOLEAN DEFAULT False NOT NULL
                );

                CREATE TABLE IF NOT EXISTS Sets (
                    s_setID SERIAL PRIMARY KEY NOT NULL,
                    s_weight FLOAT DEFAULT 0.0 NOT NULL,
                    s_reps INT DEFAULT 0 NOT NULL,
                    s_workoutID INT REFERENCES Workouts ( w_workoutID )
                );

                CREATE TABLE IF NOT EXISTS WorkingSets (
                    ws_workingSetID SERIAL PRIMARY KEY NOT NULL,
                    ws_setCount INT DEFAULT 0 NOT NULL,
                    ws_setID INT REFERENCES Sets ( s_setID )
                );


                CREATE TABLE IF NOT EXISTS Sessions (
                    s_sessionID SERIAL PRIMARY KEY NOT NULL,
                    s_date DATE NOT NULL,
                    s_startTime TIME NOT NULL,
                    s_endTime TIME NOT NULL
                );

                CREATE TABLE IF NOT EXISTS SensorData(
                    sd_sensorDataID SERIAL PRIMARY KEY NOT NULL,
                    sd_minHeartRate FLOAT DEFAULT 0.0,
                    sd_maxHeartRate FLOAT DEFAULT 0.0,
                    sd_averageHeartRate FLOAT DEFAULT 0.0,
                    sd_steps INT DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS Reports(
                    r_reportID SERIAL PRIMARY KEY NOT NULL,
                    r_generatedDate DATE DEFAULT NOW() NOT NULL,
                    r_startDate DATE NOT NULL,
                    r_endDate DATE NOT NULL,
                    r_userID INT REFERENCES Users (u_userID)
                );
                
                CREATE TABLE IF NOT EXISTS ReportItems(
                    ri_reportItemID SERIAL PRIMARY KEY NOT NULL,
                    ri_maxSet INT REFERENCES Sets ( s_setID ),
                    ri_minSet INT REFERENCES Sets ( s_setID ),
                    ri_averageSet INT REFERENCES Sets ( s_setID ),
                    ri_workoutID INT REFERENCES Workouts ( w_workoutID )
                );

                CREATE TABLE IF NOT EXISTS Plans_Workouts (
                    pw_planID INT REFERENCES Plans ( p_planID ),
                    pw_workoutID INT REFERENCES Workouts ( w_workoutID )
                );

                CREATE TABLE IF NOT EXISTS Sessions_SensorData (
                    ssd_sessionID INT REFERENCES Sessions ( s_sessionID ),
                    ssd_sensorDataID INT REFERENCES SensorData ( sd_sensorDataID )
                );

                CREATE TABLE IF NOT EXISTS Sessions_WorkingSets (
                    sws_sessionID INT REFERENCES Sessions ( s_sessionID ),
                    sws_workingSetID INT REFERENCES WorkingSets ( ws_workingSetID )
                );
                """
            )
            cursor.db.commit()
        
