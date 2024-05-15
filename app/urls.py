from django.urls import path
from app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name='index'),
    path('product/',views.products,name='product'),
    path('login_page/',views.login_page,name='login_page'),
    path('signup/',views.signup,name='signup'),
    path('logout_page/',views.logout_page,name='logout_page'),
    path('update_cart/<int:id>', views.update_cart, name='update_cart'),
    path('cart/', views.cart, name='cart'),
    path('category/<str:category>/', views.category_products, name='category_products'),
    path('checkout/', views.checkout, name='checkout'),
    path('farmerrequest/', views.farmerrequest, name='farmerrequest'),
    path('adminreq/', views.adminreq, name='adminreq'),
    path('send_email/', views.send_email, name='send_email'),
     
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='password_reset.html'),name="password_reset"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),name="password_reset_done"),
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),name="password_reset_complete"),
    
  
    

]