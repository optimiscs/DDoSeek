from django.urls import path

from core import views

urlpatterns = [
    path('', views.index),
    path('firewall_log/', views.firewallLog),
    path('ids_log/', views.idsLog),
    path('admin_log/', views.adminLog),
    path('firewall_rule/', views.firewallRule),
    path('ids_rule/', views.idsRule),
    path('traffic_statistic/', views.trafficStatistic),
    path('node_state/', views.nodeState),
    path('system_test/', views.systemTest),

    path('submit/firewall_rule/', views.submitFirewallRule),
    path('submit/ids_rule/', views.submitIDSRule),

    path('test/<int:test_id>/', views.test),
    path('reset/', views.reset),
    path('topo/', views.topo),

    path('v1.0/topology/switches', views.get_sw_topo),
    path('v1.0/topology/links', views.get_l_topo),

    path('topo/router.svg', views.get_svg),

    path('stats/flow/<str:flow_id>', views.get_flow),
    path('monitor/', views.get_monitor),
    path('delay', views.delay),
    
]