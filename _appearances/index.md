---
layout: page
title: Talks and Appearances
css: assets/custom-styles/appearance-overview-box.css
---

Below you can find conference talks I've given and instances in which I've appeared on podcasts, etc.


{% for appearance in site.appearances %}

{% if appearance.hidden %}

  {% comment %} Checking if item.field is NIL isn't supported before Jekyll 4.0... {% endcomment %}

{% else %}

  {% comment %}
    This hacky if clause keeps us from including standalone pages in the appearances folder in the list.
  {% endcomment %}
  {% if appearance.layout != "page" %}
  {% include appearance-overview-box.html appearance=appearance %}
  {% endif %}

{% endif %}

{% endfor %}
