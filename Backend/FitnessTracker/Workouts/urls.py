from django.urls import path
from .views import *

urlpatterns = [
    path('api/v1/user/name',
         UserUpdateNameView.as_view(), name='userupdatename'),
    path('api/v1/user/last-name',
         UserUpdateLastNameView.as_view(), name='UserUpdateLastName'),
    path('api/v1/user/email',
         UserUpdateEmailView.as_view(), name='UserUpdateEmail'),
    path('api/v1/save/plan',
         SavePlanView.as_view(), name='SavePlan'),
    path('api/v1/plan-workout',
         PlanAddWorkoutView.as_view(), name='planaddworkout'),
    path('api/v1/session',
         WorkoutSessionView.as_view(), name='WorkoutSession'),  
    path('api/v1/working-set',
         WorkingSetAddView.as_view(), name='WorkingSetAdd'), 
    path('api/v1/set',
         SetAddView.as_view(), name='SetAdd'), 
    path('api/v1/login',
     UserLoginView.as_view(), name='UserLogin'),
    path('api/v1/signup',
    UserSignupView.as_view(), name='UserSignup'),
     path('api/v1/workouts',
    GetWorkoutsView.as_view(), name='GetWorkouts'),
    path('api/v1/user/plans',
    GetPlansByUserView.as_view(), name='GetPlansByUser'),
    
]
