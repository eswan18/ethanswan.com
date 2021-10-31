---
layout: page
title: Talks
---

{% assign date_format = site.date_format | default: "%d %b %Y" %}
{% for page in site.talks %}

{% if talk.hidden %}

  {% comment %} Checking if item.field is NIL isn't supported before Jekyll 4.0... {% endcomment %}

{% else %}

  <table class="talks"><tr>
  <td class="talk-title" id="{{ page.title | slugify }}">
    <span class="talk-title"><a href="{{ site.baseurl }}{{ page.url }}">{{ page.title }}</a></span>
    <br>
    {% include talk-meta.html %}
    <br>
  </td>
  </tr></table>
  <br>

{% endif %}

{% endfor %}
