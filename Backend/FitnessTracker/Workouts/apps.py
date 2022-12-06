from django.apps import AppConfig
from django.db import connection
import random
from .Scraper import Scraper
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

    # start getting all workout data
    #scraper = Scraper()
    #scraper.getData()

    # Drop All Tables - comment the portion below to persist data
   # with connection.cursor() as cursor:
        
    #    cursor.execute(
    #        """
    #            DROP TABLE IF EXISTS Plans_Workouts;
    #            DROP TABLE IF EXISTS Sessions_SensorData;
    #            DROP TABLE IF EXISTS ReportItems;
    #            DROP TABLE IF EXISTS Reports;
    #            DROP TABLE IF EXISTS SensorData;
    #            DROP TABLE IF EXISTS Sessions CASCADE;
    #            DROP TABLE IF EXISTS WorkingSets CASCADE;
    #            DROP TABLE IF EXISTS Sets;
    #           DROP TABLE IF EXISTS Workouts;
    #           DROP TABLE IF EXISTS Plans;
    #           DROP TABLE IF EXISTS Users;
    #        """
    #    )
    #    cursor.db.commit()


    # Create All Tables
    with connection.cursor() as cursor:
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS Users (
                    u_userID SERIAL PRIMARY KEY NOT NULL,
                    u_image TEXT,
                    u_email TEXT NOT NULL,
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
                    w_minorMuscleGroup TEXT,
                    w_equipment TEXT,
                    w_description TEXT,
                    w_level TEXT DEFAULT 'Basic',
                    w_images TEXT,
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
                    s_endTime TIME NOT NULL,
                    s_userID INT REFERENCES Users ( u_userID )
                );

                CREATE TABLE IF NOT EXISTS SensorData(
                    sd_sensorDataID SERIAL PRIMARY KEY NOT NULL,
                    sd_minHeartRate FLOAT DEFAULT 0.0,
                    sd_maxHeartRate FLOAT DEFAULT 0.0,
                    sd_averageHeartRate FLOAT DEFAULT 0.0,
                    sd_steps INT DEFAULT 0,
                    s_userID INT REFERENCES Users ( u_userID )
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
                    ssd_sensorDataID INT REFERENCES SensorData ( sd_sensorDataID ),
                    ssd_userID INT REFERENCES Users ( u_userID )
                );

                CREATE TABLE IF NOT EXISTS Sessions_WorkingSets (
                    sws_sessionID INT REFERENCES Sessions ( s_sessionID ),
                    sws_workingSetID INT REFERENCES WorkingSets ( ws_workingSetID )
                );
                """
            )
            cursor.db.commit()


    # we have now created database and now we can fill in some data
    with connection.cursor() as connection:
        #write insert statements here

        #example lets insert 20 users
        print("filling tables...")
        userCount = 0
        for i in range (0, 1000):
            connection.execute (
                f"""
                    INSERT INTO Users (u_image, u_email, u_firstName, u_lastName)
                    VALUES (
                        'fdsdfsd',
                        'user@{userCount}.com',
                        'user{userCount}',
                        'lastname{userCount}'
                    );
                    
                """
            )
            userCount += 1
            # insert data into workouts
            userCount += 1

        # a user can have a plan for each user in DB giver them a plan
        
        
        # # each user has logged into app and recorded 1 gym session
        # connection.execute(
        #     f"""
        #         SELECT u_userID FROM Users;
        #     """
        # )

        # all_users = connection.fetchall()
        # # make a plan for each user

        # # make report for each user
        # index = 0 
        # for id in (all_users):
        #     connection.execute(
        #         f"""
        #                 INSERT INTO Plans (
        #                     p_planName, 
        #                     p_userID
        #                 )
        #                 VALUES (
        #                     'chest_day',
        #                     {all_users[index][0]}
        #                 );
        #             """
        #         )
        #     connection.execute(
        #         f"""
        #         INSERT INTO Reports (
        #             r_startDate,
        #             r_endDate,
        #             r_userID
        #             )
        #             VALUES (
        #                 '2022-10-10',
        #                 '2022-11-10',
        #                 {all_users[index][0]}
        #             );
        #         """
        #     )
        #     index+= 1
        # # create a session for each user
        # index = 0
        # for id in (all_users):
        #     connection.execute(
        #         f"""
        #             INSERT INTO Sessions (
        #                 s_date,
        #                 s_startTime ,
        #                 s_endTime ,
        #                 s_userID 
        #             )
        #             VALUES (
        #                 CURRENT_DATE,
        #                 '02:03:04',
        #                 '03:03:04',
        #                 {all_users[index][0]}
        #             )
        #             RETURNING s_sessionID;
        #         """
        #     )

        #     session_id = connection.fetchone()

        #     connection.execute(
        #         f"""
        #             INSERT INTO SensorData(
        #             sd_minHeartRate,
        #             sd_maxHeartRate,
        #             sd_averageHeartRate,
        #             sd_steps
        #             )
        #             VALUES (
        #                 {random.randrange(75,100)},
        #                 {random.randrange(115,200)},
        #                 {random.randrange(100,115)},
        #                 {random.randrange(200, 1000)}
        #             )
        #             RETURNING sd_sensorDataID
        #         """
        #     )
            
        #     sensor_data_id = connection.fetchone()
        #     connection.execute(
        #             f"""
        #                 INSERT INTO Sessions_SensorData (
        #                     ssd_sessionID,
        #                     ssd_sensorDataID,
        #                     ssd_userID
        #                 )
        #                 VALUES (
        #                     {session_id[0]},
        #                     {sensor_data_id[0]},
        #                     {all_users[index][0]}
        #                 )
        #             """
        #         )
        #     index += 1

        # # for each session give it  a random workign set

        # connection.execute(
        #     """
        #         SELECT s_sessionID FROM SESSIONS;
        #     """
        # )

        # all_session = connection.fetchall()

        # index = 0 
        # for session in all_session:
        #     # assign a random number od working set 
        #     connection.execute(
        #         f"""
        #             INSERT INTO Sets (
        #                 s_weight,
        #                 s_reps,
        #                 s_workoutID
        #             ) 
        #             VALUES (
        #                 {random.randrange(2,200)},
        #                 {random.randrange(1, 30)},
        #                 1
        #             ) 
        #             RETURNING s_setID;
        #         """
        #     )

        #     set_id = connection.fetchone()
        #     connection.execute(
        #         f"""
        #             INSERT INTO WorkingSets (
        #                 ws_setCount,
        #                 ws_setID
        #             )
        #             VALUES (
        #                 {random.randrange(1,4)},
        #                 {set_id[0]}
        #             )
        #             RETURNING *;
        #         """
        #     )

        #     working_set_id = connection.fetchone()

        #     connection.execute(
        #         f"""
        #             INSERT INTO Sessions_WorkingSets (
        #                 sws_sessionID,
        #                 sws_workingSetID
        #             ) VALUES (
        #                 {all_session[index][0]},
        #                 {working_set_id[0]}
        #             ) RETURNING *
        #         """
        #     )
            
    
       #load in workouts from csv
        with open('workouts.csv', 'r') as f:
            connection.copy_from(f, 'workouts', sep='|', columns=[
                "w_workoutname",
                "w_mainmusclegroup",
                "w_minormusclegroup",
                "w_equipment",
                "w_description",
                "w_level",
                "w_images",
                "w_isprivate"
            ])
        connection.db.commit()
        
