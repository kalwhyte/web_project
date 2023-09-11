from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name='panel-home'),
    path('about/',views.about_page, name='panel-about'),
    path('welcome/', views.welcome ,name='panel-welcome'),
    path('contact/',views.contact, name='panel-contact'),
    path('login/',views.login_view, name='panel-loginpage'),
    path('myadmin/',views.admin, name='panel-adminpage'),
    path('teach/',views.teacher, name='panel-teachpage'),
    path('student/',views.student, name='panel-studentpage'),
    path('StdReg/',views.StdReg, name='panel-StdRegpage'),
    path('admReg/',views.admReg, name='panel-admRegpage'),
    path('tchReg/',views.tchReg, name='panel-tchRegpage'),
    path('clsReg/',views.clsReg, name='panel-clsRegpage'),
    path('subReg/',views.subReg, name='panel-subRegpage'),
    path('std_all',views.all_student, name='panel-allstd'),
    path('adm_all',views.all_admin, name='panel-alladm'),
    path('tch_all',views.all_teachers, name='panel-alltch'),
    path('cls_all',views.all_class, name='panel-allcls'),
    path('sub_all',views.all_subject, name='panel-allsub'),
    path('std_up/<str:id>/',views.std_update, name='panel-stdup'),
    path('std_del/<str:pk>/',views.std_delete, name='panel-stddel'),
    path('adm_del/<str:pk>/',views.adm_delete, name='panel-admdel'),
    path('tch_del/<str:pk>/',views.tch_delete, name='panel-tchdel'),
    path('update_teacher/<str:id>/',views.tch_update,name='panel-uptch'),
    path('adm_up/<str:id>/',views.adm_update, name='panel-admup'),
    path('cls_del/<str:pk>/',views.cls_delete, name='panel-clsdel'),
    path('cls_up/<str:id>/',views.cls_update, name='panel-clsup'),
    path('sub_del/<str:pk>/',views.sub_delete, name='panel-subdel'),
    path('sub_update/<str:id>',views.sub_update,name='panel-subup'),
    path('privacy/',views.privacy, name='panel-privacy'),
    path('session/',views.sectionReg, name='panel-session'),
    path('sec_all',views.all_section,name='panel-allsec'),
    path('sec_del/<str:pk>/',views.sec_delete,name='panel-secdel'),
    path('sec_up/<str:id>/',views.sec_update,name='panel-secup'),
    path('logout/',views.Logout_view, name='panel-logout'),
    path('view_teacher/<int:id>/',views.view_teacher, name='panel-view-teacher'),
    path('view_student/<int:id>/',views.view_student, name='panel-view-student'),
    path('cls_all/Score/', views.allScore,name='panel-allScore'),
    path('cls_all/Score/<str:cls>/<str:sub>', views.Score,name='panel-Score')
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)