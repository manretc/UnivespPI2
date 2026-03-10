# app/routes.py
# Versão com lógica para reservar e confirmar recolhimento de doações.

import logging

from flask import render_template, flash, redirect, url_for, request, current_app
from app import db
from app.forms import LoginForm, RegistrationForm, DonationForm, EditProfileForm
from app.models import User, Donation
from flask_login import current_user, login_user, logout_user, login_required
import requests

from flask import Blueprint

logger = logging.getLogger(__name__)

bp = Blueprint("main", __name__)


@bp.route("/health")
def health():
    return {"status": "ok"}, 200


@bp.route("/")
@bp.route("/index")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html", title="Início")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Usuário ou senha inválidos")
            return redirect(url_for("main.login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("main.dashboard"))
    return render_template("login.html", title="Entrar", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = RegistrationForm()
    if form.validate_on_submit():
        lat, lon = geocode_address(form.address.data)
        if lat is None:
            flash(
                "Não foi possível encontrar as coordenadas para o endereço fornecido. Tente um endereço mais específico."
            )
            return render_template("register.html", title="Registrar", form=form)
        user = User(
            username=form.username.data,
            email=form.email.data,
            user_type=form.user_type.data,
            address=form.address.data,
            latitude=lat,
            longitude=lon,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            logger.exception("Erro ao registrar usuario")
            flash("Erro ao registrar. Tente novamente.")
            return render_template("register.html", title="Registrar", form=form)
        flash("Parabéns, você foi registrado com sucesso!")
        return redirect(url_for("main.login"))
    return render_template("register.html", title="Registrar", form=form)


@bp.route("/donate", methods=["GET", "POST"])
@login_required
def create_donation():
    if current_user.user_type != "donor":
        flash("Apenas doadores podem registrar alimentos.")
        return redirect(url_for("main.dashboard"))
    form = DonationForm()
    if form.validate_on_submit():
        address = form.address.data or current_user.address
        lat, lon = geocode_address(address)
        if lat is None:
            flash(
                "Não foi possível encontrar as coordenadas para o endereço da doação."
            )
        else:
            donation = Donation(
                description=form.description.data,
                quantity=form.quantity.data,
                donor=current_user,
                address=address,
                latitude=lat,
                longitude=lon,
            )
            db.session.add(donation)
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                logger.exception("Erro ao registrar doacao")
                flash("Erro ao registrar doação. Tente novamente.")
                return render_template("create_donation.html", title="Registrar Doação", form=form)
            flash("Sua doação foi registrada com sucesso!")
            return redirect(url_for("main.dashboard"))
    return render_template("create_donation.html", title="Registrar Doação", form=form)


@bp.route("/dashboard")
@login_required
def dashboard():
    """Rota do painel atualizada para buscar todas as listas de doações."""
    available_donations = Donation.query.filter_by(status="available").all()

    # Doações que o utilizador (instituição) reservou
    claimed_by_me = []
    if current_user.user_type == "charity":
        claimed_by_me = Donation.query.filter_by(
            status="claimed", claimed_by_id=current_user.id
        ).all()

    # Doações do utilizador (doador) que foram reservadas por outros
    my_donations_claimed = []
    if current_user.user_type == "donor":
        my_donations_claimed = Donation.query.filter_by(
            status="claimed", user_id=current_user.id
        ).all()

    collected_donations = Donation.query.filter_by(status="collected").all()

    # Combina as listas de doações reservadas para simplificar o template
    claimed_donations = claimed_by_me + my_donations_claimed

    donations_coords = [
        {"lat": d.latitude, "lon": d.longitude, "desc": d.description}
        for d in available_donations
        if d.latitude is not None and d.longitude is not None
    ]
    return render_template(
        "dashboard.html",
        title="Painel",
        available_donations=available_donations,
        claimed_donations=claimed_donations,
        collected_donations=collected_donations,
        donations_coords=donations_coords,
    )


@bp.route("/perfil/editar", methods=["GET", "POST"])
@login_required
def editar_perfil():
    form = EditProfileForm()
    if request.method == "GET":
        # Preenche o formulário com os dados atuais do usuário
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.address.data = current_user.address

    if form.validate_on_submit():
        # Se o endereço mudou, geocodifica novamente
        address_changed = form.address.data != current_user.address
        if address_changed:
            lat, lon = geocode_address(form.address.data)
            if lat is None:
                flash(
                    "Não foi possível encontrar as coordenadas para o endereço fornecido. Tente um endereço mais específico."
                )
                return render_template(
                    "edit_profile.html", title="Editar Perfil", form=form
                )
            current_user.latitude = lat
            current_user.longitude = lon

        # Atualiza campos básicos
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.address = form.address.data

        # Atualiza senha se fornecida
        if form.password.data:
            current_user.set_password(form.password.data)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            logger.exception("Erro ao atualizar perfil")
            flash("Erro ao atualizar perfil. Tente novamente.")
            return render_template("edit_profile.html", title="Editar Perfil", form=form)
        flash("Seu perfil foi atualizado com sucesso!")
        return redirect(url_for("main.dashboard"))

    return render_template("edit_profile.html", title="Editar Perfil", form=form)


# --- NOVAS ROTAS DE AÇÃO ---


@bp.route("/donation/<int:donation_id>/claim", methods=["POST"])
@login_required
def claim_donation(donation_id):
    """Rota para uma instituição reservar uma doação."""
    if current_user.user_type != "charity":
        flash("Apenas instituições podem reservar doações.")
        return redirect(url_for("main.dashboard"))

    donation = Donation.query.get_or_404(donation_id)
    if donation.status == "available":
        donation.status = "claimed"
        donation.claimed_by_id = current_user.id
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            logger.exception("Erro ao reservar doacao %s", donation_id)
            flash("Erro ao reservar doação. Tente novamente.")
            return redirect(url_for("main.dashboard"))
        flash("Doação reservada com sucesso! Por favor, proceda com o recolhimento.")
    else:
        flash("Esta doação já não está disponível.")
    return redirect(url_for("main.dashboard"))


@bp.route("/donation/<int:donation_id>/confirm", methods=["POST"])
@login_required
def confirm_collection(donation_id):
    """Rota para confirmar que uma doação foi recolhida."""
    donation = Donation.query.get_or_404(donation_id)
    # Permite que tanto o doador como a instituição que reservou confirmem
    if donation.user_id == current_user.id or donation.claimed_by_id == current_user.id:
        if donation.status == "claimed":
            donation.status = "collected"
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                logger.exception("Erro ao confirmar recolhimento da doacao %s", donation_id)
                flash("Erro ao confirmar recolhimento. Tente novamente.")
                return redirect(url_for("main.dashboard"))
            flash("Recolhimento da doação confirmado com sucesso!")
        else:
            flash("Ação inválida para o estado atual da doação.")
    else:
        flash("Você não tem permissão para realizar esta ação.")
    return redirect(url_for("main.dashboard"))


# --- FUNÇÕES AUXILIARES ---
def geocode_address(address):
    """Geocodifica um endereço usando Nominatim (OpenStreetMap) — gratuito."""
    if not address or len(address) > 500:
        return None, None
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "limit": 1}
    headers = {"User-Agent": "RedeDoacoes/1.0"}
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        results = response.json()
        if results:
            return float(results[0]["lat"]), float(results[0]["lon"])
    except (requests.exceptions.RequestException, ValueError, KeyError):
        return None, None
    return None, None
