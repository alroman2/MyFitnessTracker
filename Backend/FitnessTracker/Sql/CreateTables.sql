CREATE TABLE Users (
    u_userID SERIAL PRIMARY KEY NOT NULL,
    u_firstName TEXT NOT NULL,
    u_lastName TEXT NOT NULL
);

CREATE TABLE Plans (
    p_planID SERIAL PRIMARY KEY NOT NULL,
    p_planName TEXT NOT NULL,
    p_userID INT REFERENCES Users ( u_userID )
);

CREATE TABLE Plans_Workout (
    pw_planID INT REFERENCES Plans ( p_planID )
    pw_workoutID INT REFERENCES Workout ( w_workoutID )
);

CREATE TABLE Workouts (
    w_workoutID SERIAL PRIMARY KEY NOT NULL,
    w_workoutName TEXT NOT NULL,
    w_mainMuscleGroup TEXT,
    w_equipment TEXT,
    w_description TEXT,
    w_level TEXT,
    w_images TEXT [],
    w_isPrivate BOOLEAN DEFAULT 0 NOT NULL
);

