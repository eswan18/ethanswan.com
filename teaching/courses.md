---
layout: page
title: My Courses
css: assets/custom-styles/course-overview-box.css
---
{% for course in site.courses %}

{% if course.hidden %}

  {% comment %} Checking if item.field is NIL isn't supported before Jekyll 4.0... {% endcomment %}

{% else %}

  {% comment %}
    This hacky if clause keeps us from including standalone pages in the courses folder in the course list.
  {% endcomment %}
  {% if course.layout != "page" %}
  {% include course-overview-box.html course=course %}
  {% endif %}

{% endif %}

{% endfor %}
