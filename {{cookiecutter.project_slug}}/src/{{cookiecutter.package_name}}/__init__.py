"""{{ cookiecutter.project_description }}"""
{% if cookiecutter.use_cli == "yes" %}
from {{ cookiecutter.package_name }}.cli import main
{% endif %}
from {{ cookiecutter.package_name }}._version import __version__

__all__ = ["__version__"{% if cookiecutter.use_cli == "yes" %}, "main"{% endif %}]
