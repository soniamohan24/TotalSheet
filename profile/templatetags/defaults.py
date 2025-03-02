from django import template
from profile.models import *
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="get_profession")
def get_profession(value):
    profession = Profession.objects.all()
    return profession


@register.filter(name="get_skill")
def get_skill(value):
    skill = Skill.objects.all()
    return skill


@register.filter(name="get_physical_fitness")
def get_physical_fitness(value):
    physical_fitness = PhysicalFitness.objects.all()
    return physical_fitness


@register.filter(name="get_work_challenge")
def get_work_challenge(value):
    work_challenge = WorkChallenge.objects.all()
    return work_challenge


@register.filter(name="get_vision")
def get_vision(value):
    vision = Vision.objects.all()
    return vision


@register.filter(name="get_workplace")
def get_workplace(value):
    workplace = WorkPlace.objects.all()
    return workplace


@register.filter(name="get_icon")
def get_icon(value):
    icon_mapping = {
        "fb": '<i class="ph fs-4 ph-facebook-logo"></i>',
        "insta": '<i class="ph fs-4 ph-instagram-logo"></i>',
        "x": '<i class="ph fs-4 ph-x-logo"></i>',
        "snapchat": '<i class="ph fs-4 ph-snapchat-logo"></i>',
        "tiktok": '<i class="ph fs-4 ph-tiktok-logo"></i>',
        "linkedin": '<i class="ph fs-4 ph-linkedin-logo"></i>',
        "youtube": '<i class="ph fs-4 ph-youtube-logo"></i>',
        "whatsapp": '<i class="ph fs-4 ph-whatsapp-logo"></i>',
        "telegram": '<i class="ph fs-4 ph-telegram-logo"></i>',
        "other": '<i class="ph fs-4 ph-network"></i>',
    }
    return mark_safe(icon_mapping.get(value))
