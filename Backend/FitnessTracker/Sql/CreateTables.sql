CREATE TABLE User (
    u_userID SERIAL PRIMARY KEY NOT NULL,
    u_firstName TEXT NOT NULL,
    u_lastName TEXT NOT NULL
);

CREATE TABLE Plan (
    p_planID SERIAL PRIMARY KEY NOT NULL,
    p_planName TEXT NOT NULL,
    p_userID INT REFERENCES User ( u_userID )
);

CREATE TABLE Plan_Workout (
    pw_planID INT REFERENCES Plan ( p_planID )
    pw_workoutID INT REFERENCES Workout ( w_workoutID )
);

CREATE TABLE Workout (
    w_workoutID SERIAL PRIMARY KEY NOT NULL,
    w_workoutName TEXT NOT NULL,
    w_mainMuscleGroup TEXT,
    w_equipment TEXT,
    w_description TEXT,
    w_level TEXT,
    w_images TEXT [],
    w_isPrivate BOOLEAN DEFAULT 0 NOT NULL
);

