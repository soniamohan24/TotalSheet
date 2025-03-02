from django import template

register = template.Library()


@register.filter(name="get_icon")
def get_icon(value):
    icon_mapping = {
        "fb": '<i class="ph ph-facebook-logo"></i>',
        "insta": '<i class="ph ph-instagram-logo"></i>',
        "x": '<i class="ph ph-x-logo"></i>',
        "snapchat": '<i class="ph ph-snapchat-logo"></i>',
        "tiktok": '<i class="ph ph-tiktok-logo"></i>',
        "linkedin": '<i class="ph ph-linkedin-logo"></i>',
        "youtube": '<i class="ph ph-youtube-logo"></i>',
        "whatsapp": '<i class="ph ph-whatsapp-logo"></i>',
        "telegram": '<i class="ph ph-telegram-logo"></i>',
        "other": '<i class="ph ph-network"></i>',
    }
    return icon_mapping.get(value)


@register.filter
def exclude_formulas(formulas):
    # Define unwanted patterns
    exclude_patterns = ["Sum = A+B+C", "SUM=A+C", "SUM=B+C", "SUM=D+C"]

    # Filter out formulas that match any of the unwanted patterns
    return [formula for formula in formulas if formula.name not in exclude_patterns]
