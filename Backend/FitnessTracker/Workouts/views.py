# Import HTTP Rest 
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse

# custom apps 
from Workouts.apps import *
from .apps import *
from django.shortcuts import render
from django.db import connection

# Create your views here.

class UserUpdateNameView(APIView):
    """
        update the user
    """
    @staticmethod
    def post(request):
            email = request.POST.get('email')
            new_name = request.POST.get('first_name')
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                        UPDATE Users 
                        SET u_firstName = '{new_name}'
                        WHERE u_email = '{email}'
                        RETURNING *;
                    """
                )

                user = cursor.fetchall()
                cursor.db.commit()
                if len(user) <= 0:
                    return Response(f"{email} User not found " , status=400)
            
            return Response(user, status=200)

class UserUpdateLastNameView(APIView):
    """
        update the user
    """
    @staticmethod
    def post(request):
            email = request.POST.get('email')
            new_name = request.POST.get('last_name')
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                        UPDATE Users 
                        SET u_lastName = '{new_name}'
                        WHERE u_email = '{email}'
                        RETURNING *;
                    """
                )

                user = cursor.fetchall()
                cursor.db.commit()
                if len(user) <= 0:
                    return Response(f"{email} User not found " , status=400)
            
            return Response(user, status=200)

class UserUpdateEmailView(APIView):
    """
        update the user
    """
    @staticmethod
    def post(request):
            old_email = request.POST.get('old_email')
            new_email = request.POST.get('new_email')
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                        UPDATE Users 
                        SET u_email = '{new_email}'
                        WHERE u_email = '{old_email}'
                        RETURNING *;
                    """
                )

                user = cursor.fetchall()
                cursor.db.commit()
                if len(user) <= 0:
                    return Response(f"{old_email} User not found " , status=400)
            
            return Response(user, status=200)
class PlanInsertView(APIView):
    """
        Add a plan
    """
    @staticmethod
    def post(request):
            email = request.POST.get('email')
            plan_name = request.POST.get('plan_name')
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                        INSERT INTO Plans (
                            p_planName,
                            p_userID
                        )
                        VALUES (
                            '{plan_name}',
                            (
                                SELECT u_userID 
                                FROM Users 
                                WHERE u_email = '{email}'
                            )
                        )
                        RETURNING *;
                    """
                )
                cursor.db.commit()
                plan = cursor.fetchall()
                if len(plan) <= 0:
                    return Response(f"{email} User not found " , status=400)
            
            return Response(plan, status=200)

class PlanAddWorkoutView(APIView):
    """
        Add workout to a plan 
    """
    @staticmethod
    def post(request):
            planID = request.POST.get('plan_id')
            workoutID = request.POST.get('workout_id')
            with connection.cursor() as cursor:
                cursor.execute(
                    f"""
                        INSERT INTO Plans_Workouts (
                            pw_planID,
                            pw_workoutID
                        )
                        VALUES (
                            '{planID}',
                            '{workoutID}'
                        )
                        RETURNING *;
                    """
                )
                cursor.db.commit()
                plan_workout = cursor.fetchall()
                if len(plan_workout) <= 0:
                    return Response(f"{planID} or {workoutID} not found " , status=400)
            
            return Response(plan_workout, status=200)

class WorkoutSessionView(APIView):
    """
        Creates a session, a sensorData collection group and relates it back to user
    """
    @staticmethod
    def post(request):
            email = request.POST.get('email')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')
            min_heart_rate = request.POST.get('min_heart_rate')
            max_heart_rate  = request.POST.get('max_heart_rate')
            avg_heart_rate = request.POST.get('avg_hear_rate')
            steps = request.POST.get("steps")

            
            with connection.cursor() as cursor:
                #create a session
                cursor.execute(
                    f"""
                        INSERT INTO Sessions(
                            s_date,
                            s_startTime,
                            s_endTime,
                            s_userID
                        )
                        VALUES (
                            CURRENT_DATE,
                            '{start_time}',
                            '{end_time}',
                            (
                                SELECT u_userID 
                                FROM Users 
                                WHERE u_email = '{email}'
                            )
                        )
                        RETURNING s_sessionID;
                    """
                )

                session_id = cursor.fetchone()

                cursor.execute(
                    f"""
                        INSERT INTO SensorData(
                            sd_minHeartRate ,
                            sd_maxHeartRate ,
                            sd_averageHeartRate ,
                            sd_steps
                        )
                        VALUES (
                            '{min_heart_rate}',
                            '{max_heart_rate}',
                            '{avg_heart_rate}',
                            '{steps}'
                        )
                        RETURNING sd_sensorDataID;
                    """
                )
                
                sensor_data_id = cursor.fetchone()

                cursor.execute(
                    f"""
                        INSERT INTO Sessions_SensorData (
                            ssd_sessionID,
                            ssd_sensorDataID,
                            ssd_userID
                        )
                        VALUES (
                            {session_id[0]},
                            {sensor_data_id[0]},
                            (
                                SELECT u_userID 
                                FROM Users 
                                WHERE u_email = '{email}'
                            )
                        )
                        RETURNING *
                    """
                )
                cursor.db.commit()
                overall_session = cursor.fetchall()

                if len(overall_session) <= 0:
                    return Response(f"{email} not found " , status=400)
            
            return Response(overall_session, status=200)


class WorkingSetAddView(APIView):
    """
        Add a working set to a session
    """
    @staticmethod
    def post(request):
        session_id = request.POST.get('session_id')
        set_count = request.POST.get('set_count')

        with connection.cursor() as cursor:
            # check if session exists
            cursor.execute(
                f"""
                    SELECT * FROM Sessions WHERE s_sessionID = {session_id}
                """
            )
            
            session = cursor.fetchone()

            if len(session) <= 0:
                return Response("Session does not exist", status=400)

            # create the working set
            cursor.execute(
                f"""
                    INSERT INTO WorkingSets (
                        ws_setCount
                    )
                    VALUES (
                        {set_count}
                    )
                    RETURNING *;
                """
            )

            working_set_id = cursor.fetchone()

            # relate working set to the session
            cursor.execute(
                f"""
                    INSERT INTO Sessions_WorkingSets (
                        sws_sessionID,
                        sws_workingSetID
                    ) VALUES (
                        {session_id},
                        {working_set_id[0]}
                    ) RETURNING *
                """
            )
            cursor.db.commit()
            session_working_set = cursor.fetchone()

            return Response(session_working_set, status=200)

class SetAddView(APIView):
    """
        Add an individual set to a working set
    """
    @staticmethod
    def post(request):
        working_set_id = request.POST.get('working_set_id')
        weight = request.POST.get('weight_lbs')
        reps = request.POST.get('reps')
        workout_id = request.POST.get('workout_id')

        with connection.cursor() as cursor:
            # create set
            cursor.execute(
                f"""
                    INSERT INTO Sets (
                        s_weight,
                        s_reps,
                        s_workoutID
                    ) 
                    VALUES (
                        {weight},
                        {reps},
                        {workout_id}
                    ) 
                    RETURNING s_setID;
                """
            )
            
            set_id = cursor.fetchone()

            # update working set with set id
            cursor.execute(
                f"""
                    UPDATE WorkingSets
                    SET ws_setID = {set_id[0]}
                    WHERE ws_workingSetID = {working_set_id}
                    RETURNING *;
                """
            )

           
            working_set = cursor.fetchone()
            cursor.db.commit()
            return Response(working_set, status=200)

