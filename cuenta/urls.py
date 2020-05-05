"""
    Definición de las URI's para la aplicación globales
"""
# Django Libraries
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path, reverse_lazy

# Local Folders Libraries
from .views import activar, avatar, cambio_clave, perfil, registro

app_name = "cuenta"

urlpatterns = [
    path("cuenta/registro/", registro, name="registro"),
    path("cuenta/activar/<uidb64>/<token>", activar, name="activar"),
    path(
        "cuenta/login/",
        LoginView.as_view(
            template_name="perfil_login.html", redirect_field_name="next",
        ),
        name="login",
    ),
    path("cuenta/salir/", LogoutView.as_view(next_page="cuenta:login"), name="logout"),
    path("cuenta/perfil/", login_required(perfil), name="perfil"),
    path("", login_required(perfil), name="perfil2"),
    path("cuenta/cambiar-clave/", login_required(cambio_clave), name="cambiar-clave"),
    path(
        "cuenta/reiniciar-clave-enviado/",
        PasswordResetDoneView.as_view(template_name="reinicio_enviado.html"),
        name="reiniciar-enviado",
    ),
    path(
        "cuenta/reiniciar-clave/",
        PasswordResetView.as_view(
            template_name="reinicio_clave.html",
            email_template_name="reinicio_correo.html",
            success_url=reverse_lazy("cuenta:reiniciar-enviado"),
        ),
        name="reiniciar-clave",
    ),
    path(
        "cuenta/nueva-clave/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="reinicio_nueva_clave.html",
            success_url=reverse_lazy("cuenta:perfil"),
            post_reset_login=True,
        ),
        name="nueva-clave",
    ),
    path("cuenta/avatar/", login_required(avatar), name="avatar"),
]
